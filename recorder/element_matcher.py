"""
Element Matcher - Matches tap coordinates to UI elements.

Finds UI elements at given coordinates and builds locator chains
with fallback strategies for robust element identification.
"""

from typing import List, Dict, Any, Optional, Tuple


def find_elements_at_point(
    elements: List[Dict[str, Any]],
    x: int,
    y: int
) -> List[Dict[str, Any]]:
    """
    Find all elements containing the given point.

    Args:
        elements: List of element dicts from UI tree
        x: X coordinate
        y: Y coordinate

    Returns:
        List of elements whose bounds contain the point
    """
    matching = []

    for elem in elements:
        x1, y1, x2, y2 = elem['bounds']

        # Check if point is within bounds
        if x1 <= x <= x2 and y1 <= y <= y2:
            matching.append(elem)

    return matching


def calculate_element_area(element: Dict[str, Any]) -> int:
    """
    Calculate area of element bounds.

    Args:
        element: Element dict

    Returns:
        Area in pixels squared
    """
    x1, y1, x2, y2 = element['bounds']
    return (x2 - x1) * (y2 - y1)


def select_best_match(candidates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Pick the best element from candidates.

    Strategy:
    1. Prefer clickable/long-clickable elements
    2. Among those, prefer smaller elements (more specific)
    3. If no clickable, pick smallest element overall

    Args:
        candidates: List of candidate elements

    Returns:
        Best matching element or None
    """
    if not candidates:
        return None

    # Separate clickable and non-clickable
    clickable = [e for e in candidates if e.get('clickable') or e.get('long_clickable')]
    non_clickable = [e for e in candidates if e not in clickable]

    # Sort by area (ascending - smaller first)
    clickable.sort(key=calculate_element_area)
    non_clickable.sort(key=calculate_element_area)

    # Prefer clickable elements
    if clickable:
        return clickable[0]

    # Fall back to smallest non-clickable
    if non_clickable:
        return non_clickable[0]

    return None


def build_xpath(element: Dict[str, Any]) -> str:
    """
    Build a robust XPath selector for an element.

    Uses multiple attributes for better matching.

    Args:
        element: Element dict

    Returns:
        XPath expression string
    """
    class_name = element['class']
    parts = [f"//{class_name}"]

    conditions = []

    # Add resource-id condition
    if element['resource_id']:
        conditions.append(f"@resource-id='{element['resource_id']}'")

    # Add text condition
    if element['text']:
        # Escape quotes in text
        text = element['text'].replace("'", "\\'")
        conditions.append(f"@text='{text}'")

    # Add content-desc condition
    if element['content_desc']:
        desc = element['content_desc'].replace("'", "\\'")
        conditions.append(f"@content-desc='{desc}'")

    if conditions:
        return f"{parts[0]}[{' and '.join(conditions)}]"

    # Fall back to class + index
    return f"({parts[0]})[{element.get('index', 0) + 1}]"


def build_locator(element: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate locator with fallback chain.

    Creates a primary locator and a list of fallbacks ordered by reliability.

    Strategy order:
    1. resource-id (most reliable)
    2. content-desc (accessibility)
    3. text (visible label)
    4. xpath (structural)
    5. bounds (last resort)

    Args:
        element: Element dict

    Returns:
        Locator dict with primary strategy and fallbacks
    """
    locators = []

    # Strategy 1: Resource ID
    if element['resource_id']:
        locators.append({
            "strategy": "id",
            "value": element['resource_id']
        })

    # Strategy 2: Content Description
    if element['content_desc']:
        locators.append({
            "strategy": "content_desc",
            "value": element['content_desc']
        })

    # Strategy 3: Text
    if element['text']:
        locators.append({
            "strategy": "text",
            "value": element['text']
        })

    # Strategy 4: XPath
    xpath = build_xpath(element)
    locators.append({
        "strategy": "xpath",
        "value": xpath
    })

    # Strategy 5: Bounds (always included as final fallback)
    locators.append({
        "strategy": "bounds",
        "value": element['bounds']
    })

    # First locator is primary, rest are fallbacks
    if len(locators) > 1:
        return {
            "primary": locators[0],
            "fallbacks": locators[1:],
            "bounds": element['bounds']
        }
    else:
        return {
            "primary": locators[0],
            "fallbacks": [],
            "bounds": element['bounds']
        }


def match_element_at_point(
    elements: List[Dict[str, Any]],
    x: int,
    y: int
) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
    """
    Find and match element at given coordinates.

    Convenience function combining find and select.

    Args:
        elements: List of element dicts
        x: X coordinate
        y: Y coordinate

    Returns:
        Tuple of (element_dict, locator_dict)
        If no element found, returns (None, bounds_only_locator)
    """
    candidates = find_elements_at_point(elements, x, y)
    element = select_best_match(candidates)

    if element:
        locator = build_locator(element)
        return element, locator
    else:
        # No element found - use coordinates as locator
        return None, {
            "primary": {
                "strategy": "bounds",
                "value": (x, y, x, y)
            },
            "fallbacks": [],
            "bounds": (x, y, x, y)
        }


def describe_match(
    element: Optional[Dict[str, Any]],
    locator: Dict[str, Any]
) -> str:
    """
    Generate human-readable description of match.

    Args:
        element: Matched element (or None)
        locator: Generated locator

    Returns:
        Description string
    """
    if not element:
        coords = locator['bounds']
        return f"No element found at ({coords[0]}, {coords[1]})"

    parts = []

    # Element class (simplified)
    class_name = element['class'].split('.')[-1]
    parts.append(class_name)

    # Primary identifier
    primary = locator['primary']
    if primary['strategy'] == 'id':
        rid = primary['value'].split('/')[-1]
        parts.append(f'#{rid}')
    elif primary['strategy'] == 'text':
        parts.append(f'"{primary["value"]}"')
    elif primary['strategy'] == 'content_desc':
        parts.append(f'[{primary["value"]}]')

    # Bounds
    x1, y1, x2, y2 = element['bounds']
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    parts.append(f'@({center_x}, {center_y})')

    return ' '.join(parts)


def find_similar_elements(
    elements: List[Dict[str, Any]],
    target: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Find elements similar to target (same class, similar attributes).

    Useful for finding element in changed UI.

    Args:
        elements: All elements
        target: Target element to match

    Returns:
        List of similar elements, scored by similarity
    """
    similar = []

    for elem in elements:
        score = 0

        # Same class
        if elem['class'] == target['class']:
            score += 10

        # Same resource ID
        if elem['resource_id'] and elem['resource_id'] == target['resource_id']:
            score += 50

        # Same text
        if elem['text'] and elem['text'] == target['text']:
            score += 30

        # Same content description
        if elem['content_desc'] and elem['content_desc'] == target['content_desc']:
            score += 40

        # Similar size (within 20%)
        target_area = calculate_element_area(target)
        elem_area = calculate_element_area(elem)
        if target_area > 0:
            size_diff = abs(elem_area - target_area) / target_area
            if size_diff < 0.2:
                score += 5

        if score > 0:
            similar.append((score, elem))

    # Sort by score descending
    similar.sort(key=lambda x: x[0], reverse=True)

    return [elem for score, elem in similar]
