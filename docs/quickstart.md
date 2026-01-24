# DittoMation Quick Start Guide

Get started with DittoMation in minutes. This guide covers installation, basic usage, and common workflows.

## Prerequisites

- Python 3.8 or higher
- Android device with USB debugging enabled
- ADB (Android Debug Bridge) installed

### Enable USB Debugging on Android

1. Go to **Settings > About phone**
2. Tap **Build number** 7 times to enable Developer options
3. Go to **Settings > Developer options**
4. Enable **USB debugging**
5. Connect your device via USB and authorize the computer when prompted

## Installation

### Option 1: Install from source (recommended)

```bash
# Clone the repository
git clone https://github.com/OmPrakashSingh1704/DittoMations.git
cd DittoMations

# Install in development mode
pip install -e .
```

### Option 2: Install dependencies only

```bash
pip install click
```

## Verify Installation

Check that your device is connected:

```bash
# Using the CLI
ditto devices

# Or using ADB directly
adb devices
```

You should see your device listed with status "device".

## Quick Start: Python API

```python
from core import Android

# Connect to device (auto-detects first connected device)
android = Android()

# Get device info
print(android.info())

# Take a screenshot
android.screenshot("screen.png")

# Tap at coordinates
android.tap(500, 500)

# Tap an element by text
android.tap("Settings")

# Type text
android.type("Hello World")

# Press buttons
android.press_home()
android.press_back()

# Swipe gestures
android.swipe("up")
android.swipe("down")

# Open an app
android.open_app("Chrome")
```

## Quick Start: CLI

```bash
# Get device info
ditto info

# Take a screenshot
ditto screenshot

# Tap at coordinates
ditto tap 500 500

# Tap an element by text
ditto tap --text "Settings"

# Type text
ditto type "Hello World"

# Press buttons
ditto press home
ditto press back

# Swipe gestures
ditto swipe up
ditto swipe down

# Open an app
ditto open Chrome
```

## Common Workflows

### Navigate to Settings and Toggle Wi-Fi

**Python:**
```python
from core import Android

android = Android()

# Open Settings
android.open_app("Settings")
android.wait_for("Network", timeout=10)

# Tap on Network & internet
android.tap("Network")

# Wait for and tap Wi-Fi
android.wait_for("Wi-Fi", timeout=5)
android.tap("Wi-Fi")
```

**CLI:**
```bash
ditto open Settings
ditto wait --text "Network" --timeout 10
ditto tap --text "Network"
ditto wait --text "Wi-Fi" --timeout 5
ditto tap --text "Wi-Fi"
```

### Search in an App

**Python:**
```python
from core import Android

android = Android()

# Open Chrome
android.open_app("Chrome")

# Wait for the search bar and tap it
android.wait_for(id="search_box", timeout=10)
android.tap(id="search_box")

# Type a search query
android.type("DittoMation automation")
android.press_enter()
```

**CLI:**
```bash
ditto open Chrome
ditto wait --id search_box --timeout 10
ditto tap --id search_box
ditto type "DittoMation automation"
ditto press enter
```

### Scroll and Find Element

**Python:**
```python
from core import Android

android = Android()

# Scroll down to find an element
for _ in range(5):
    if android.exists("Target Item"):
        android.tap("Target Item")
        break
    android.scroll("down")
else:
    print("Element not found after scrolling")
```

### Take Multiple Screenshots

**Python:**
```python
from core import Android
import time

android = Android()

# Take screenshots at intervals
for i in range(5):
    android.screenshot(f"screenshot_{i}.png")
    time.sleep(2)
```

## Element Finding

DittoMation supports multiple strategies for finding elements:

| Strategy | Python | CLI |
|----------|--------|-----|
| By text | `android.tap("Login")` | `ditto tap --text "Login"` |
| By resource-id | `android.tap(id="btn_login")` | `ditto tap --id btn_login` |
| By content-desc | `android.tap(desc="Submit button")` | `ditto tap --desc "Submit button"` |
| By coordinates | `android.tap(100, 200)` | `ditto tap 100 200` |

### Finding vs Waiting

- **find()** - Single attempt to find an element
- **wait_for()** - Polls repeatedly until element appears or timeout

```python
# Single attempt (returns None if not found)
element = android.find("Login")

# Wait up to 10 seconds for element
element = android.wait_for("Login", timeout=10)
```

## Error Handling

```python
from core import Android
from core.exceptions import DeviceNotFoundError, ElementNotFoundError

try:
    android = Android()
except DeviceNotFoundError:
    print("No device connected. Please connect a device and enable USB debugging.")

# Safe element interaction
element = android.find("Login")
if element:
    android.tap("Login")
else:
    print("Login button not found")
```

## Confidence Scoring

DittoMation uses confidence scoring for fuzzy element matching. This means:

- Elements are scored 0-100% based on how well they match
- Default threshold is 30% - matches above this are returned
- You can adjust the threshold for stricter or looser matching

```python
# Fuzzy matching - will find "Settings" even with typo
android.tap("Setings", min_confidence=0.5)

# Check confidence score
score = android.get_confidence("Login")
print(f"Match confidence: {score:.0%}")

# Get detailed match information
result = android.find_with_confidence("Submit")
if result:
    print(f"Found with {result.confidence:.0%} confidence")
```

```bash
# CLI with confidence
ditto tap -t "Setings" -c 0.5
ditto find -t "Login" --show-confidence
ditto confidence -t "Lgoin"  # Check confidence for typo
```

See [Confidence Scoring Guide](confidence-scoring.md) for full details.

## Next Steps

- Read the [Python API Reference](api.md) for complete method documentation
- Read the [CLI Reference](cli.md) for all available commands
- Read the [Confidence Scoring Guide](confidence-scoring.md) for fuzzy matching details
- Check [approach.md](approach.md) for technical architecture details
