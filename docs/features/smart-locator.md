# Smart Locator

DittoMation's smart locator finds UI elements using multiple strategies with automatic fallback.

## How It Works

When you target an element, DittoMation tries to find it using this fallback chain:

```
resource-id → content-desc → text → xpath → coordinates (last resort)
```

Each strategy has a **confidence score** (0-100%). The locator returns the best match above the threshold.

## Fallback Chain

### 1. Resource ID (Highest Priority)

```python
android.tap(id="login_btn")
```

- Most stable identifier
- Survives text/layout changes
- Confidence: 95-100%

### 2. Content Description

```python
android.tap(desc="Login button")
```

- Accessibility labels
- Good for buttons/icons without text
- Confidence: 90-100%

### 3. Text

```python
android.tap("Login")
```

- Visible text on screen
- Supports fuzzy matching
- Confidence: 70-100%

### 4. XPath

```python
# In workflow JSON
{"strategy": "xpath", "value": "//Button[@text='Login']"}
```

- Structural matching
- Last resort before coordinates
- Confidence: 30-90%

### 5. Coordinates (Fallback)

Used only when all other strategies fail.

- Least reliable
- Breaks on different screen sizes
- Confidence: 0%

---

## Confidence Scoring

Every match has a confidence score:

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100% | Excellent | Exact match |
| 70-89% | Good | High confidence |
| 50-69% | Fair | Acceptable |
| 30-49% | Low | May be wrong |
| 0-29% | Very Low | Likely wrong |

### Setting Minimum Confidence

```python
android = Android(min_confidence=0.5)  # 50% minimum

# Or per-call
android.tap("Login", min_confidence=0.8)  # 80% for this tap only
```

### Getting Confidence Score

```python
result = android.find_with_confidence("Login")
if result:
    print(f"Found with {result.confidence:.0%} confidence")
    print(f"Strategy: {result.strategy_used}")
```

---

## Fuzzy Matching

DittoMation supports fuzzy matching for text and content descriptions:

```python
# These all find "Login Button"
android.tap("Login")         # Partial match
android.tap("login button")  # Case insensitive
android.tap("Logn")          # Typo tolerance (similarity > 0.4)
```

---

## Example: Surviving UI Changes

Original app (v1.0):
```xml
<Button resource-id="login_btn" text="Login"/>
```

Updated app (v2.0):
```xml
<Button resource-id="btn_sign_in" text="Sign In"/>
```

**Coordinate-based automation:** FAILS

**DittoMation with fallbacks:**

```json
{
  "locator": {
    "primary": {"strategy": "id", "value": "login_btn"},
    "fallbacks": [
      {"strategy": "id", "value": "btn_sign_in"},
      {"strategy": "text", "value": "Login"},
      {"strategy": "text", "value": "Sign In"}
    ]
  }
}
```

Result: Finds via `btn_sign_in` with 95% confidence.

---

## Ad Filtering

DittoMation automatically filters out ad elements:

```python
# Ads are skipped by default
android.tap("Download")  # Won't tap ad download buttons

# Disable if needed
locator = ElementLocator(filter_ads=False)
```
