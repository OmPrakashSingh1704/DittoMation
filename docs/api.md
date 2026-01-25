# DittoMation Python API Reference

Complete reference for the `Android` class and all available methods.

## Installation

```python
from core import Android
```

## Android Class

The main interface for controlling Android devices. Uses **confidence scoring** for robust element matching.

### Constructor

```python
Android(device: str = None, min_confidence: float = 0.3)
```

**Parameters:**
- `device` (str, optional): Device serial number. If not provided, auto-detects the first connected device.
- `min_confidence` (float, optional): Minimum confidence threshold for element matching (0.0-1.0). Default is 0.3 (30%).

**Raises:**
- `DeviceNotFoundError`: If no device is connected.

**Example:**
```python
# Auto-detect device with default 30% confidence threshold
android = Android()

# Connect to specific device with stricter matching
android = Android(device="emulator-5554", min_confidence=0.7)

# Adjust confidence threshold later
android.min_confidence = 0.5
```

> **See also:** [Confidence Scoring Guide](confidence-scoring.md) for details on how matching works.

---

## Gesture Methods

### tap()

Tap at coordinates or on an element.

```python
tap(
    x_or_text: int | str = None,
    y: int = None,
    *,
    id: str = None,
    desc: str = None,
    timeout: float = 5.0
) -> bool
```

**Parameters:**
- `x_or_text`: X coordinate (int) or element text to find (str)
- `y`: Y coordinate (required when x_or_text is int)
- `id`: Find element by resource-id
- `desc`: Find element by content-description
- `timeout`: Timeout for element search in seconds

**Returns:** `True` if successful, `False` otherwise.

**Examples:**
```python
# Tap at coordinates
android.tap(500, 500)

# Tap element by text
android.tap("Login")

# Tap element by resource-id
android.tap(id="com.app:id/btn_submit")

# Tap element by content-description
android.tap(desc="Submit button")

# With custom timeout
android.tap("Submit", timeout=10)
```

---

### long_press()

Long press at coordinates or on an element.

```python
long_press(
    x_or_text: int | str = None,
    y: int = None,
    *,
    id: str = None,
    desc: str = None,
    duration_ms: int = 1000,
    timeout: float = 5.0
) -> bool
```

**Parameters:**
- `x_or_text`: X coordinate (int) or element text (str)
- `y`: Y coordinate
- `id`: Find element by resource-id
- `desc`: Find element by content-description
- `duration_ms`: Press duration in milliseconds (default: 1000)
- `timeout`: Timeout for element search

**Returns:** `True` if successful.

**Examples:**
```python
# Long press at coordinates
android.long_press(500, 500)

# Long press for 2 seconds
android.long_press(500, 500, duration_ms=2000)

# Long press element
android.long_press("Item to select")
```

---

### swipe()

Swipe by direction or coordinates.

```python
swipe(
    x1_or_direction: int | str,
    y1: int = None,
    x2: int = None,
    y2: int = None,
    duration_ms: int = 300
) -> bool
```

**Parameters:**
- `x1_or_direction`: Start X coordinate (int) or direction string ("up", "down", "left", "right")
- `y1`: Start Y coordinate
- `x2`: End X coordinate
- `y2`: End Y coordinate
- `duration_ms`: Swipe duration in milliseconds

**Returns:** `True` if successful.

**Examples:**
```python
# Swipe by direction (from screen center)
android.swipe("up")
android.swipe("down")
android.swipe("left")
android.swipe("right")

# Swipe by coordinates
android.swipe(500, 1500, 500, 500)  # Swipe up

# Slow swipe
android.swipe("up", duration_ms=1000)
```

---

### scroll()

Scroll in a direction.

```python
scroll(
    direction: str = "down",
    distance: float = 0.5,
    duration_ms: int = 500
) -> bool
```

**Parameters:**
- `direction`: "up", "down", "left", or "right"
- `distance`: Scroll distance as fraction of screen (0.0-1.0)
- `duration_ms`: Scroll duration in milliseconds

**Returns:** `True` if successful.

**Examples:**
```python
# Scroll down (default)
android.scroll("down")

# Scroll up with longer distance
android.scroll("up", distance=0.8)

# Slow scroll
android.scroll("down", duration_ms=1000)
```

---

### pinch()

Pinch gesture for zooming in/out.

```python
pinch(
    scale: float = 0.5,
    center_x: int = None,
    center_y: int = None,
    duration_ms: int = 500
) -> bool
```

**Parameters:**
- `scale`: Scale factor (>1 zoom in, <1 zoom out)
- `center_x`: Center X of pinch (default: screen center)
- `center_y`: Center Y of pinch (default: screen center)
- `duration_ms`: Gesture duration

**Returns:** `True` if successful.

**Note:** This is an approximation using sequential swipes.

**Examples:**
```python
# Zoom in
android.pinch(scale=2.0)

# Zoom out
android.pinch(scale=0.5)

# Pinch at specific location
android.pinch(scale=1.5, center_x=300, center_y=400)
```

---

## Input Methods

### type()

Type text into the focused field.

```python
type(text: str, clear_first: bool = False) -> bool
```

**Parameters:**
- `text`: Text to type
- `clear_first`: Clear existing text before typing

**Returns:** `True` if successful.

**Examples:**
```python
# Type text
android.type("Hello World")

# Clear field and type
android.type("new text", clear_first=True)
```

---

### press_home()

Press the home button.

```python
press_home() -> bool
```

**Returns:** `True` if successful.

---

### press_back()

Press the back button.

```python
press_back() -> bool
```

**Returns:** `True` if successful.

---

### press_enter()

Press the enter key.

```python
press_enter() -> bool
```

**Returns:** `True` if successful.

---

### press_key()

Press any key by keycode.

```python
press_key(keycode: str) -> bool
```

**Parameters:**
- `keycode`: Android keycode string

**Returns:** `True` if successful.

**Common Keycodes:**
| Keycode | Description |
|---------|-------------|
| `KEYCODE_HOME` | Home button |
| `KEYCODE_BACK` | Back button |
| `KEYCODE_MENU` | Menu button |
| `KEYCODE_ENTER` | Enter key |
| `KEYCODE_DEL` | Backspace |
| `KEYCODE_VOLUME_UP` | Volume up |
| `KEYCODE_VOLUME_DOWN` | Volume down |
| `KEYCODE_POWER` | Power button |
| `KEYCODE_CAMERA` | Camera button |
| `KEYCODE_SEARCH` | Search |

**Examples:**
```python
android.press_key("KEYCODE_VOLUME_UP")
android.press_key("KEYCODE_MENU")
```

---

## App Methods

### open_app()

Open an app by name or package.

```python
open_app(app: str) -> bool
```

**Parameters:**
- `app`: App name (e.g., "Chrome") or package name (e.g., "com.android.chrome")

**Returns:** `True` if app launch was initiated.

**Examples:**
```python
# Open by name
android.open_app("Chrome")
android.open_app("Settings")
android.open_app("Camera")

# Open by package
android.open_app("com.android.chrome")
android.open_app("com.google.android.youtube")
```

**Supported App Names:**
The following common app names are recognized:
- Chrome, Settings, Camera, Phone, Messages
- Gmail, YouTube, Maps, Play Store
- Calculator, Clock, Calendar, Contacts, Files

---

### current_app()

Get information about the current foreground app.

```python
current_app() -> dict
```

**Returns:** Dictionary with keys:
- `package`: Package name (e.g., "com.android.chrome")
- `activity`: Current activity name

**Example:**
```python
info = android.current_app()
print(f"Package: {info['package']}")
print(f"Activity: {info['activity']}")
```

---

## Screen Methods

### screenshot()

Take a screenshot.

```python
screenshot(filename: str = None) -> str
```

**Parameters:**
- `filename`: Output filename (default: auto-generated with timestamp)

**Returns:** Absolute path to saved screenshot.

**Examples:**
```python
# Auto-named screenshot
path = android.screenshot()

# Named screenshot
path = android.screenshot("login_screen.png")
```

---

### screen_size()

Get the screen dimensions.

```python
screen_size() -> tuple[int, int]
```

**Returns:** Tuple of (width, height) in pixels.

**Example:**
```python
width, height = android.screen_size()
print(f"Screen: {width}x{height}")
```

---

## Element Methods

### find()

Find an element on screen using confidence scoring.

```python
find(
    text: str = None,
    *,
    id: str = None,
    desc: str = None,
    timeout: float = 0,
    min_confidence: float = None
) -> dict | None
```

**Parameters:**
- `text`: Find by visible text (fuzzy matching supported)
- `id`: Find by resource-id (partial match supported)
- `desc`: Find by content-description (fuzzy matching supported)
- `timeout`: Timeout in seconds (0 = single attempt)
- `min_confidence`: Minimum confidence threshold (0.0-1.0), overrides instance default

**Returns:** Element dictionary or `None` if no match above confidence threshold.

**Element Dictionary:**
```python
{
    "class": "android.widget.Button",
    "resource_id": "com.app:id/btn_login",
    "text": "Login",
    "content_desc": "",
    "bounds": (100, 200, 300, 250),
    "clickable": True,
    "enabled": True,
    # ... more properties
}
```

**Examples:**
```python
# Find by text (uses default 30% threshold)
element = android.find("Login")

# Find by ID
element = android.find(id="btn_submit")

# Fuzzy matching with typo (will match "Settings")
element = android.find("Setings", min_confidence=0.6)

# Strict matching (require 90% confidence)
element = android.find("Submit", min_confidence=0.9)
```

---

### find_with_confidence()

Find an element with detailed confidence information.

```python
find_with_confidence(
    text: str = None,
    *,
    id: str = None,
    desc: str = None,
    timeout: float = 0,
    min_confidence: float = None
) -> MatchResult | None
```

**Parameters:** Same as `find()`

**Returns:** `MatchResult` object with:
- `element`: The matched element dictionary
- `confidence`: Confidence score (0.0-1.0)
- `match_details`: Dictionary showing score breakdown

**Examples:**
```python
result = android.find_with_confidence("Login")
if result:
    print(f"Found: {result.element['text']}")
    print(f"Confidence: {result.confidence:.0%}")
    print(f"Details: {result.match_details}")
    # Output:
    # Found: Login
    # Confidence: 100%
    # Details: {'text_exact': 1.0, 'clickable_bonus': 0.05}
```

---

### get_confidence()

Get the confidence score for an element match without a minimum threshold.

```python
get_confidence(
    text: str = None,
    *,
    id: str = None,
    desc: str = None
) -> float
```

**Returns:** Confidence score (0.0-1.0), or 0.0 if no match found.

**Examples:**
```python
# Check how well a search matches
score = android.get_confidence("Setings")  # typo
print(f"Confidence: {score:.0%}")  # Output: Confidence: 78%

# Use for conditional logic
if android.get_confidence("Purchase") > 0.9:
    android.tap("Purchase")
else:
    print("Purchase button not clearly visible - skipping")
```

---

### find_all()

Find all matching elements on screen.

```python
find_all(
    text: str = None,
    *,
    id: str = None,
    desc: str = None,
    class_name: str = None
) -> list[dict]
```

**Parameters:**
- `text`: Find by visible text (substring match)
- `id`: Find by resource-id (substring match)
- `desc`: Find by content-description (substring match)
- `class_name`: Find by class name (substring match)

**Returns:** List of matching element dictionaries.

**Examples:**
```python
# Find all buttons
buttons = android.find_all(class_name="Button")

# Find all items containing "Item"
items = android.find_all(text="Item")

for item in items:
    print(item['text'])
```

---

### wait_for()

Wait for an element to appear.

```python
wait_for(
    text: str = None,
    *,
    id: str = None,
    desc: str = None,
    timeout: float = 10.0,
    poll_interval: float = 0.5
) -> dict | None
```

**Parameters:**
- `text`: Find by visible text
- `id`: Find by resource-id
- `desc`: Find by content-description
- `timeout`: Maximum wait time in seconds
- `poll_interval`: Time between checks in seconds

**Returns:** Element dictionary if found, `None` if timeout.

**Examples:**
```python
# Wait for element
element = android.wait_for("Welcome", timeout=15)

# Wait for loading to complete
android.wait_for(id="main_content", timeout=30)
```

---

### exists()

Check if an element exists on screen.

```python
exists(
    text: str = None,
    *,
    id: str = None,
    desc: str = None
) -> bool
```

**Parameters:**
- `text`: Find by visible text
- `id`: Find by resource-id
- `desc`: Find by content-description

**Returns:** `True` if element exists.

**Example:**
```python
if android.exists("Error"):
    print("Error message is displayed")
```

---

## Device Methods

### devices()

List all connected devices.

```python
devices() -> list[dict]
```

**Returns:** List of dictionaries with keys:
- `serial`: Device serial number
- `status`: Device status ("device", "offline", "unauthorized")

**Example:**
```python
for device in android.devices():
    print(f"{device['serial']}: {device['status']}")
```

---

### info()

Get device information.

```python
info() -> dict
```

**Returns:** Dictionary with device properties:
- `serial`: Device serial number
- `model`: Device model name
- `manufacturer`: Device manufacturer
- `android_version`: Android version
- `sdk_version`: SDK API level
- `screen_size`: Tuple of (width, height)

**Example:**
```python
info = android.info()
print(f"Model: {info['model']}")
print(f"Android: {info['android_version']}")
print(f"Screen: {info['screen_size'][0]}x{info['screen_size'][1]}")
```

---

## Automation Class

The `Automation` class provides a high-level interface for running multi-step automation scripts with variables, conditions, and loops.

### Constructor

```python
Automation(
    device: str = None,
    min_confidence: float = 0.3,
    default_timeout: float = 5.0,
    default_retries: int = 2,
    step_delay: float = 0.3,
    stop_on_failure: bool = True,
    screenshot_on_failure: bool = False,
    initial_vars: Dict[str, Any] = None
)
```

**Parameters:**
- `device`: Device serial (auto-detect if None)
- `min_confidence`: Default confidence for element matching
- `default_timeout`: Default timeout for element search
- `default_retries`: Default retry count per step
- `step_delay`: Delay between steps in seconds
- `stop_on_failure`: Stop on first failure
- `screenshot_on_failure`: Capture screenshot on failure
- `initial_vars`: Initial variables for the context

### run()

Execute a list of automation steps.

```python
run(steps: List[Step], initial_vars: Dict[str, Any] = None) -> AutomationResult
```

**Example:**
```python
from core.automation import Automation, Step

auto = Automation(initial_vars={"username": "test"})

steps = [
    Step(action="open", app="MyApp"),
    Step(action="tap", text="Login"),
    Step(action="type", value="{{username}}"),
]

result = auto.run(steps)
print(result.summary())
```

### run_from_file()

Load and run automation from a JSON file.

```python
run_from_file(filepath: str, extra_vars: Dict[str, Any] = None) -> AutomationResult
```

**Example:**
```python
auto = Automation()
result = auto.run_from_file("script.json", extra_vars={"password": "secret"})
```

### Variable Methods

```python
# Set a variable
auto.set_variable("count", 5)

# Get a variable
value = auto.get_variable("count", default=0)

# Access context directly
ctx = auto.context
```

### Supported Step Types

| Action | Description |
|--------|-------------|
| `tap` | Tap element or coordinates |
| `long_press` | Long press element |
| `swipe` | Swipe gesture |
| `scroll` | Scroll gesture |
| `type` | Type text |
| `press` | Press device button |
| `open` | Open app |
| `wait` | Wait for duration |
| `wait_for` | Wait for element |
| `assert_exists` | Assert element exists |
| `assert_not_exists` | Assert element doesn't exist |
| `screenshot` | Take screenshot |
| `set_variable` | Set variable value |
| `extract` | Extract data from element |
| `if` | Conditional branching |
| `for` | For loop |
| `while` | While loop |
| `until` | Until loop |
| `break` | Break from loop |
| `continue` | Continue to next iteration |
| `log` | Log message |
| `assert` | Assert condition |

> **See also:** [Variables and Control Flow Guide](variables-and-control-flow.md) for detailed documentation.

---

## Exception Classes

Import exceptions for error handling:

```python
from core.exceptions import (
    DittoMationError,         # Base exception
    DeviceNotFoundError,      # No device connected
    DeviceOfflineError,       # Device is offline
    ElementNotFoundError,     # Element not found
    ADBCommandError,          # ADB command failed
    ADBTimeoutError,          # ADB command timed out
    # Variables & Expressions
    ExpressionError,          # Expression evaluation failed
    UnsafeExpressionError,    # Unsafe expression blocked
    VariableNotFoundError,    # Variable not defined
    # Control Flow
    LoopLimitError,           # Loop exceeded max iterations
    ControlFlowError,         # Control flow error
    InvalidControlFlowError,  # break/continue outside loop
    AssertionFailedError,     # Assert condition failed
)
```

**Example:**
```python
from core import Android
from core.exceptions import DeviceNotFoundError, VariableNotFoundError

try:
    android = Android()
except DeviceNotFoundError as e:
    print(f"Error: {e.message}")
    print(f"Hint: {e.hint}")
```

---

## Complete Example

```python
from core import Android
from core.exceptions import DeviceNotFoundError
import time

def automate_settings():
    """Example: Navigate Settings and take screenshots."""

    try:
        android = Android()
    except DeviceNotFoundError:
        print("Please connect a device")
        return

    # Print device info
    info = android.info()
    print(f"Connected to: {info['model']} (Android {info['android_version']})")

    # Open Settings
    android.open_app("Settings")
    time.sleep(2)

    # Take initial screenshot
    android.screenshot("settings_home.png")

    # Look for Network settings
    if android.wait_for("Network", timeout=5):
        android.tap("Network")
        time.sleep(1)
        android.screenshot("settings_network.png")

    # Go back
    android.press_back()

    # Scroll and find Display
    for _ in range(3):
        if android.exists("Display"):
            android.tap("Display")
            break
        android.scroll("down")

    # Return home
    android.press_home()
    print("Automation complete!")

if __name__ == "__main__":
    automate_settings()
```
