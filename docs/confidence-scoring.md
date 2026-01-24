# Confidence Scoring System

DittoMation uses a confidence scoring system for element matching, enabling fuzzy matching and more robust automation that works even when UI text has minor variations.

## Overview

Instead of binary matching (found/not found), DittoMation calculates a confidence score (0.0 to 1.0) for each potential match. This allows:

- **Fuzzy matching**: Find "Settings" even if you search for "Setings" (typo)
- **Partial matching**: Find elements containing your search term
- **Ranked results**: Get multiple matches sorted by relevance
- **Configurable thresholds**: Control how strict matching should be

## Confidence Levels

| Score | Level | Description |
|-------|-------|-------------|
| 90-100% | Excellent | Exact or near-exact match |
| 70-89% | Good | Strong match with minor differences |
| 50-69% | Fair | Partial match or contains search term |
| 30-49% | Low | Weak match, may need verification |
| 0-29% | Very Low | Poor match, likely incorrect |

## Scoring Factors

### Text Matching

| Match Type | Score |
|------------|-------|
| Exact match (case-sensitive) | 100% |
| Exact match (case-insensitive) | 95% |
| Search text is substring | 70-90% (based on length ratio) |
| Element text is substring | 60-80% |
| Fuzzy/similar text | 40-70% (based on similarity) |

### Resource ID Matching

| Match Type | Score |
|------------|-------|
| Exact full ID match | 100% |
| Exact ID part match (after `/`) | 95% |
| ID contains search term | 80% |
| Partial/suffix match | 70% |
| Fuzzy match | 50-60% |

### Content Description Matching

| Match Type | Score |
|------------|-------|
| Exact match | 100% |
| Case-insensitive exact | 95% |
| Contains search term | 70-80% |
| Partial match | 60-70% |
| Fuzzy match | 40-70% |

### Bonus Factors

- **Clickable element**: +5% bonus
- **Enabled element**: +5% bonus

## Python API Usage

### Basic Usage with Confidence

```python
from core import Android

android = Android()

# Find with default threshold (30%)
element = android.find("Login")

# Find with custom threshold (require 70% confidence)
element = android.find("Login", min_confidence=0.7)

# Get detailed confidence information
result = android.find_with_confidence("Login")
if result:
    print(f"Element: {result.element['text']}")
    print(f"Confidence: {result.confidence:.0%}")
    print(f"Match details: {result.match_details}")
```

### Setting Global Threshold

```python
# Set threshold at initialization
android = Android(min_confidence=0.5)

# Or change it later
android.min_confidence = 0.7
```

### Finding All Matches with Scores

```python
# Get all matches above threshold
results = android.find_all_with_confidence("Item", min_confidence=0.3)

for r in results:
    print(f"{r.element['text']}: {r.confidence:.0%}")

# Example output:
# Item 1: 95%
# Item 2: 95%
# My Items: 72%
# Itemized: 65%
```

### Checking Confidence Score

```python
# Get confidence without minimum threshold
score = android.get_confidence("Setings")  # typo
print(f"Confidence: {score:.0%}")
# Output: Confidence: 78%

# Use for conditional logic
if android.get_confidence("Login") > 0.8:
    android.tap("Login")
else:
    print("Login button not clearly visible")
```

### Waiting with Confidence

```python
# Wait for element with high confidence
result = android.wait_for_with_confidence(
    "Welcome",
    timeout=10,
    min_confidence=0.8
)

if result:
    print(f"Found with {result.confidence:.0%} confidence")
```

## CLI Usage

### Finding Elements

```bash
# Find with default threshold
ditto find -t "Login"

# Find with custom threshold
ditto find -t "Login" -c 0.7

# Show confidence score
ditto find -t "Login" --show-confidence

# Find all matches
ditto find -t "Item" --all --show-confidence
```

### Tapping with Confidence

```bash
# Tap with default threshold
ditto tap -t "Submit"

# Tap with higher confidence requirement
ditto tap -t "Submit" -c 0.8

# Output shows confidence
# Tapped element: Submit (95% confidence)
```

### Checking Confidence

```bash
# Check confidence score for a search
ditto confidence -t "Setings"
# Output: Confidence for 'Setings': 78% (good)

ditto confidence -t "Login"
# Output: Confidence for 'Login': 100% (excellent)
```

### Waiting with Confidence

```bash
# Wait with confidence threshold
ditto wait -t "Welcome" -c 0.7 --timeout 15
```

## Use Cases

### Handling Typos in Test Scripts

```python
# Will match "Settings" even with typo
android.tap("Setings", min_confidence=0.6)
```

### Finding Similar Elements

```python
# Find all items that might match
results = android.find_all_with_confidence("Save", min_confidence=0.4)
for r in results:
    print(f"{r.element.get('text', r.element.get('resource_id'))}: {r.confidence:.0%}")

# Output might show:
# Save: 100%
# Save Changes: 85%
# Save Draft: 82%
# Saved Items: 65%
```

### Adaptive Automation

```python
# Try high confidence first, fall back to lower
result = android.find_with_confidence("Submit", min_confidence=0.9)
if not result:
    result = android.find_with_confidence("Submit", min_confidence=0.5)
    if result:
        print(f"Warning: Low confidence match ({result.confidence:.0%})")

if result:
    android.tap(result.element['text'])
```

### Debugging Element Finding

```python
# See why an element wasn't found
result = android.find_with_confidence("Login", min_confidence=0.0)
if result:
    print(f"Best match: {result.element.get('text')}")
    print(f"Confidence: {result.confidence:.0%}")
    print(f"Details: {result.match_details}")
else:
    print("No elements matched at all")
```

## Best Practices

1. **Start with default threshold (30%)** for most cases
2. **Use higher thresholds (70-90%)** for critical actions
3. **Use lower thresholds (20-40%)** for exploratory searches
4. **Check confidence** before critical actions like purchases
5. **Log confidence scores** for debugging flaky tests

## Configuration

### Default Threshold

The default minimum confidence is 30% (0.3). This can be configured:

```python
# Per-instance
android = Android(min_confidence=0.5)

# Per-call
android.find("Login", min_confidence=0.8)
```

### Scoring Weights

The scoring weights are defined in `recorder/element_matcher.py`:

```python
SCORE_WEIGHTS = {
    "text_exact": 1.0,
    "text_contains": 0.7,
    "text_fuzzy": 0.5,
    "id_exact": 1.0,
    "id_contains": 0.8,
    "id_suffix": 0.7,
    "desc_exact": 1.0,
    "desc_contains": 0.7,
    "desc_fuzzy": 0.5,
    "class_match": 0.3,
    "clickable_bonus": 0.1,
    "enabled_bonus": 0.05,
}
```
