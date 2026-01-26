# Getting Started

This guide will help you set up DittoMation and run your first automation.

## Prerequisites

- **Python 3.8+**
- **ADB (Android Debug Bridge)** installed and in PATH
- **Android device** with USB debugging enabled

### Installing ADB

=== "Windows"

    ```bash
    # Download Android Platform Tools
    # https://developer.android.com/studio/releases/platform-tools
    # Add to PATH
    ```

=== "macOS"

    ```bash
    brew install android-platform-tools
    ```

=== "Linux"

    ```bash
    sudo apt install adb
    ```

### Enable USB Debugging

1. Go to **Settings > About Phone**
2. Tap **Build Number** 7 times
3. Go back to **Settings > Developer Options**
4. Enable **USB Debugging**
5. Connect your device via USB
6. Accept the debugging prompt on your device

---

## Installation

```bash
pip install dittomation
```

Verify installation:

```bash
ditto --version
```

Verify device connection:

```bash
adb devices
```

You should see your device listed.

---

## Your First Automation

### Option 1: Natural Language

The easiest way to start:

```bash
ditto nl "open Settings"
```

More examples:

```bash
ditto nl "open Chrome, tap search bar, type hello world"
ditto nl "swipe up, scroll down, tap first item"
ditto nl "go back, go home"
```

### Option 2: Record & Replay

Record your interactions:

```bash
ditto record --output my_workflow.json
```

Follow the prompts to record taps, swipes, and other gestures. Press `Ctrl+C` to stop.

Replay the workflow:

```bash
ditto run my_workflow.json
```

### Option 3: Python API

```python
from core import Android

# Connect to device
android = Android()

# Open an app
android.open_app("Settings")

# Wait for element
android.wait_for("Wi-Fi", timeout=10)

# Tap by text
android.tap("Wi-Fi")

# Scroll down
android.scroll("down")

# Go back
android.press_back()
```

---

## Next Steps

- [Smart Locator](features/smart-locator.md) - Learn how element detection works
- [Natural Language](features/natural-language.md) - Full command reference
- [Variables & Control Flow](variables-and-control-flow.md) - Variables, loops, and conditions
- [API Reference](api.md) - Complete API documentation
