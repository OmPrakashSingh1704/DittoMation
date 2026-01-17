"""
Element Locator - Smart element location with fallback chain.

Finds elements in the current UI using various strategies,
falling back through the chain until a match is found.
"""

import os
import re
import sys
from typing import Dict, Any, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recorder.ui_dumper import get_center


class LocatorResult:
    """Result of element location attempt."""

    def __init__(
        self,
        found: bool,
        element: Optional[Dict[str, Any]] = None,
        strategy_used: Optional[str] = None,
        coordinates: Optional[Tuple[int, int]] = None,
        fallback_level: int = 0
    ):
        """
        Initialize locator result.

        Args:
            found: Whether element was found
            element: Matched element dict (if found)
            strategy_used: Which strategy succeeded
            coordinates: Target coordinates for gesture
            fallback_level: How many fallbacks were tried (0 = primary worked)
        """
        self.found = found
        self.element = element
        self.strategy_used = strategy_used
        self.coordinates = coordinates
        self.fallback_level = fallback_level

    def __str__(self) -> str:
        if self.found:
            return f"Found via {self.strategy_used} at {self.coordinates} (fallback level: {self.fallback_level})"
        return "Element not found"


class ElementLocator:
    """
    Smart element location with fallback chain.

    Tries multiple strategies in order until a match is found.
    """

    def __init__(self):
        """Initialize element locator."""
        # Strategy handlers
        self._strategies = {
            "id": self._find_by_id,
            "content_desc": self._find_by_content_desc,
            "text": self._find_by_text,
            "xpath": self._find_by_xpath,
            "bounds": self._find_by_bounds,
        }

    def find_element(
        self,
        locator: Dict[str, Any],
        elements: List[Dict[str, Any]]
    ) -> LocatorResult:
        """
        Find element using locator with fallback chain.

        Args:
            locator: Locator dict with primary and fallbacks
            elements: Current UI elements list

        Returns:
            LocatorResult with match info
        """
        # Build strategy list: primary first, then fallbacks
        strategies_to_try = []

        primary = locator.get("primary", {})
        if primary:
            strategies_to_try.append(primary)

        fallbacks = locator.get("fallbacks", [])
        strategies_to_try.extend(fallbacks)

        # Try each strategy in order
        for level, strategy in enumerate(strategies_to_try):
            strategy_name = strategy.get("strategy")
            strategy_value = strategy.get("value")

            if strategy_name not in self._strategies:
                continue

            handler = self._strategies[strategy_name]
            element = handler(strategy_value, elements)

            if element:
                # Calculate center coordinates
                bounds = element.get("bounds", (0, 0, 0, 0))
                center = get_center(bounds)

                return LocatorResult(
                    found=True,
                    element=element,
                    strategy_used=strategy_name,
                    coordinates=center,
                    fallback_level=level
                )

        # All strategies failed - use recorded bounds as last resort
        recorded_bounds = locator.get("bounds")
        if recorded_bounds:
            if len(recorded_bounds) == 4:
                center = get_center(tuple(recorded_bounds))
            else:
                # Treat as point
                center = (recorded_bounds[0], recorded_bounds[1])

            return LocatorResult(
                found=False,
                element=None,
                strategy_used="coordinates",
                coordinates=center,
                fallback_level=len(strategies_to_try)
            )

        # Complete failure
        return LocatorResult(found=False)

    def _find_by_id(
        self,
        resource_id: str,
        elements: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Find element by resource-id.

        Args:
            resource_id: Full resource ID (e.g., "com.app:id/button")
            elements: UI elements

        Returns:
            Matched element or None
        """
        for elem in elements:
            if elem.get("resource_id") == resource_id:
                return elem
        return None

    def _find_by_content_desc(
        self,
        content_desc: str,
        elements: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Find element by content-description.

        Args:
            content_desc: Accessibility description
            elements: UI elements

        Returns:
            Matched element or None
        """
        for elem in elements:
            if elem.get("content_desc") == content_desc:
                return elem
        return None

    def _find_by_text(
        self,
        text: str,
        elements: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Find element by visible text.

        Args:
            text: Visible text
            elements: UI elements

        Returns:
            Matched element or None
        """
        # Exact match first
        for elem in elements:
            if elem.get("text") == text:
                return elem

        # Case-insensitive match as fallback
        text_lower = text.lower()
        for elem in elements:
            if elem.get("text", "").lower() == text_lower:
                return elem

        return None

    def _find_by_xpath(
        self,
        xpath: str,
        elements: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Find element by XPath expression.

        Supports simplified XPath matching:
        - //ClassName[@attr='value']
        - //ClassName[@attr1='v1' and @attr2='v2']

        Args:
            xpath: XPath expression
            elements: UI elements

        Returns:
            Matched element or None
        """
        # Parse simple XPath: //ClassName[@attr='value' and @attr2='value2']
        match = re.match(r'//([^\[]+)(?:\[(.*)\])?', xpath)
        if not match:
            return None

        class_name = match.group(1)
        conditions_str = match.group(2)

        # Parse conditions
        conditions = {}
        if conditions_str:
            # Match @attr='value' patterns
            for cond_match in re.finditer(r"@([\w-]+)='([^']*)'", conditions_str):
                attr = cond_match.group(1)
                value = cond_match.group(2)
                conditions[attr] = value

        # Find matching elements
        for elem in elements:
            # Check class name
            if elem.get("class") != class_name:
                continue

            # Check conditions
            all_match = True
            for attr, value in conditions.items():
                attr_key = attr.replace("-", "_")  # resource-id -> resource_id
                if elem.get(attr_key) != value:
                    all_match = False
                    break

            if all_match:
                return elem

        return None

    def _find_by_bounds(
        self,
        bounds: Any,
        elements: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Find element by bounds (exact match).

        Args:
            bounds: Bounds tuple or list (x1, y1, x2, y2)
            elements: UI elements

        Returns:
            Matched element or None
        """
        if not bounds:
            return None

        target_bounds = tuple(bounds) if isinstance(bounds, list) else bounds

        for elem in elements:
            if elem.get("bounds") == target_bounds:
                return elem

        return None


def describe_location_result(result: LocatorResult, step_id: int) -> str:
    """
    Generate human-readable description of location result.

    Args:
        result: LocatorResult
        step_id: Step number for context

    Returns:
        Description string
    """
    if result.found:
        elem = result.element
        class_name = elem.get("class", "").split(".")[-1]

        parts = [f"Step {step_id}: Found"]
        parts.append(f"{class_name}")

        if elem.get("resource_id"):
            rid = elem["resource_id"].split("/")[-1]
            parts.append(f"#{rid}")
        elif elem.get("text"):
            parts.append(f'"{elem["text"]}"')

        parts.append(f"via {result.strategy_used}")

        if result.fallback_level > 0:
            parts.append(f"(fallback #{result.fallback_level})")

        return " ".join(parts)
    else:
        if result.coordinates:
            return f"Step {step_id}: Element not found, using coordinates {result.coordinates}"
        return f"Step {step_id}: Element not found, no fallback available"
