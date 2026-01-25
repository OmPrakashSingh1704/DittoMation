# DittoMation CLI Reference

Complete reference for the `ditto` command-line interface.

## Installation

```bash
# Install from source
pip install -e .

# Or install click directly
pip install click
```

## Usage

```bash
ditto [OPTIONS] COMMAND [ARGS]...
```

### Global Options

| Option | Description |
|--------|-------------|
| `--version` | Show version and exit |
| `--help` | Show help message and exit |

### Getting Help

```bash
# General help
ditto --help

# Command-specific help
ditto tap --help
ditto swipe --help
```

## Confidence Scoring

DittoMation uses **confidence scoring** for element matching. Instead of exact matching, elements are scored based on how well they match your search criteria.

- Default minimum confidence: **30%**
- Use `-c` or `--min-confidence` to adjust threshold
- Use `--show-confidence` to see scores

See [Confidence Scoring Guide](confidence-scoring.md) for details.

---

## Gesture Commands

### tap

Tap at coordinates or on an element with confidence scoring.

```bash
ditto tap [X] [Y] [OPTIONS]
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `X` | X coordinate (optional if using element options) |
| `Y` | Y coordinate (optional if using element options) |

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--text` | `-t` | Tap element by visible text |
| `--id` | `-i` | Tap element by resource-id |
| `--desc` | `-d` | Tap element by content-description |
| `--timeout` | | Element search timeout in seconds (default: 5) |
| `--min-confidence` | `-c` | Minimum confidence threshold 0.0-1.0 (default: 0.3) |

**Examples:**
```bash
# Tap at coordinates
ditto tap 500 500

# Tap element by text
ditto tap --text "Login"
ditto tap -t "Login"

# Tap element by resource-id
ditto tap --id btn_submit
ditto tap -i com.app:id/btn_submit

# Tap element by content-description
ditto tap --desc "Submit button"

# With custom timeout
ditto tap -t "Loading..." --timeout 15

# Fuzzy matching with lower confidence (will match "Settings" even with typo)
ditto tap -t "Setings" -c 0.5

# Strict matching (require 90% confidence)
ditto tap -t "Submit" -c 0.9
```

**Output with Confidence:**
```
Tapped element: Login (95% confidence)
```

---

### long-press

Long press at coordinates or on an element.

```bash
ditto long-press [X] [Y] [OPTIONS]
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `X` | X coordinate |
| `Y` | Y coordinate |

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--text` | `-t` | Element text |
| `--id` | `-i` | Element resource-id |
| `--desc` | `-d` | Element content-description |
| `--duration` | | Press duration in ms (default: 1000) |
| `--timeout` | | Element search timeout (default: 5) |

**Examples:**
```bash
# Long press at coordinates
ditto long-press 500 500

# Long press for 2 seconds
ditto long-press 500 500 --duration 2000

# Long press element
ditto long-press -t "Item to select"
```

---

### swipe

Swipe by direction or coordinates.

```bash
ditto swipe DIRECTION_OR_X1 [Y1] [X2] [Y2] [OPTIONS]
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `DIRECTION_OR_X1` | Direction (up/down/left/right) or start X |
| `Y1` | Start Y coordinate (for coordinate swipe) |
| `X2` | End X coordinate (for coordinate swipe) |
| `Y2` | End Y coordinate (for coordinate swipe) |

**Options:**
| Option | Description |
|--------|-------------|
| `--duration` | Swipe duration in ms (default: 300) |

**Examples:**
```bash
# Swipe by direction
ditto swipe up
ditto swipe down
ditto swipe left
ditto swipe right

# Swipe by coordinates
ditto swipe 500 1500 500 500

# Slow swipe
ditto swipe up --duration 1000
```

---

### scroll

Scroll in a direction.

```bash
ditto scroll DIRECTION [OPTIONS]
```

**Arguments:**
| Argument | Values | Description |
|----------|--------|-------------|
| `DIRECTION` | up, down, left, right | Scroll direction |

**Options:**
| Option | Description |
|--------|-------------|
| `--distance` | Scroll distance 0.0-1.0 (default: 0.5) |
| `--duration` | Scroll duration in ms (default: 500) |

**Examples:**
```bash
# Basic scroll
ditto scroll down
ditto scroll up

# Long scroll
ditto scroll down --distance 0.8

# Slow scroll
ditto scroll down --duration 1000
```

---

### pinch

Pinch gesture for zooming.

```bash
ditto pinch [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--scale` | Scale factor: >1 zoom in, <1 zoom out (default: 0.5) |
| `--x` | Center X coordinate (default: screen center) |
| `--y` | Center Y coordinate (default: screen center) |
| `--duration` | Gesture duration in ms (default: 500) |

**Examples:**
```bash
# Zoom in
ditto pinch --scale 2.0

# Zoom out
ditto pinch --scale 0.5

# Pinch at specific location
ditto pinch --scale 1.5 --x 300 --y 400
```

---

## Input Commands

### type

Type text into the focused field.

```bash
ditto type TEXT [OPTIONS]
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `TEXT` | Text to type |

**Options:**
| Option | Description |
|--------|-------------|
| `--clear` | Clear field before typing |

**Examples:**
```bash
# Type text
ditto type "Hello World"

# Clear and type
ditto type "new text" --clear
```

---

### press

Press a device button.

```bash
ditto press BUTTON
```

**Arguments:**
| Argument | Values |
|----------|--------|
| `BUTTON` | home, back, enter, menu, recent, search, volume-up, volume-down |

**Examples:**
```bash
ditto press home
ditto press back
ditto press enter
ditto press menu
ditto press volume-up
```

---

### key

Press any key by keycode.

```bash
ditto key KEYCODE
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `KEYCODE` | Android keycode (e.g., KEYCODE_VOLUME_UP) |

**Common Keycodes:**
- `KEYCODE_HOME` - Home button
- `KEYCODE_BACK` - Back button
- `KEYCODE_MENU` - Menu button
- `KEYCODE_ENTER` - Enter key
- `KEYCODE_DEL` - Backspace
- `KEYCODE_POWER` - Power button
- `KEYCODE_VOLUME_UP` - Volume up
- `KEYCODE_VOLUME_DOWN` - Volume down
- `KEYCODE_CAMERA` - Camera button

**Examples:**
```bash
ditto key KEYCODE_VOLUME_UP
ditto key KEYCODE_POWER
ditto key KEYCODE_CAMERA
```

---

## App Commands

### open

Open an app by name or package.

```bash
ditto open APP_NAME
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `APP_NAME` | App name or package name |

**Supported App Names:**
- Chrome, Settings, Camera, Phone, Messages
- Gmail, YouTube, Maps, Play Store
- Calculator, Clock, Calendar, Contacts, Files

**Examples:**
```bash
# Open by name
ditto open Chrome
ditto open Settings
ditto open "Play Store"

# Open by package
ditto open com.android.chrome
ditto open com.google.android.youtube
```

---

### app

Show current foreground app information.

```bash
ditto app
```

**Output:**
```
Package:  com.android.chrome
Activity: org.chromium.chrome.browser.ChromeTabbedActivity
```

---

## Screen Commands

### screenshot

Take a screenshot.

```bash
ditto screenshot [FILENAME]
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `FILENAME` | Output filename (optional, auto-generated if omitted) |

**Examples:**
```bash
# Auto-named screenshot
ditto screenshot

# Named screenshot
ditto screenshot login.png
ditto screenshot screens/home.png
```

---

### screen-size

Show screen dimensions.

```bash
ditto screen-size
```

**Output:**
```
1080 x 2340
```

---

## Element Commands

### find

Find elements on screen with confidence scoring.

```bash
ditto find [OPTIONS]
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--text` | `-t` | Find by visible text |
| `--id` | `-i` | Find by resource-id |
| `--desc` | `-d` | Find by content-description |
| `--class` | | Find by class name |
| `--all` | | Find all matching elements |
| `--json` | | Output as JSON |
| `--min-confidence` | `-c` | Minimum confidence threshold 0.0-1.0 (default: 0.3) |
| `--show-confidence` | | Show confidence scores in output |

**Examples:**
```bash
# Find single element by text
ditto find -t "Login"

# Find by resource-id
ditto find --id btn_submit

# Find all matching elements
ditto find -t "Item" --all

# Find with confidence display
ditto find -t "Login" --show-confidence

# Fuzzy matching (find "Settings" with typo)
ditto find -t "Setings" -c 0.5

# Find all with scores
ditto find -t "Save" --all --show-confidence

# Output as JSON (includes confidence)
ditto find -t "Login" --json
```

**Sample Output:**
```
  Button id=btn_login text="Login" @(540,1200) [95% excellent]
```

**JSON Output:**
```json
{
  "element": {
    "class": "android.widget.Button",
    "text": "Login",
    ...
  },
  "confidence": 0.95,
  "match_details": {
    "text_exact_ci": 0.95,
    "clickable_bonus": 0.05
  }
}
```

---

### confidence

Get confidence score for an element match.

```bash
ditto confidence [OPTIONS]
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--text` | `-t` | Check element by text |
| `--id` | `-i` | Check element by resource-id |
| `--desc` | `-d` | Check element by content-description |

**Examples:**
```bash
# Check confidence for exact text
ditto confidence -t "Login"
# Output: Confidence for 'Login': 100% (excellent)

# Check confidence for typo
ditto confidence -t "Logn"
# Output: Confidence for 'Logn': 72% (good)

# Check ID confidence
ditto confidence -i btn_submit
```

This is useful for:
- Debugging why elements aren't found
- Testing if fuzzy matching will work
- Verifying element presence before critical actions

---

### wait

Wait for an element to appear.

```bash
ditto wait [OPTIONS]
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--text` | `-t` | Wait for element by text |
| `--id` | `-i` | Wait for element by resource-id |
| `--desc` | `-d` | Wait for element by content-description |
| `--timeout` | | Timeout in seconds (default: 10) |

**Examples:**
```bash
# Wait for text
ditto wait -t "Welcome"

# Wait with timeout
ditto wait -t "Loading complete" --timeout 30

# Wait for element by ID
ditto wait --id main_content --timeout 15
```

---

## Device Commands

### devices

List connected devices.

```bash
ditto devices
```

**Output:**
```
Connected devices (2):
  + emulator-5554 (device)
  + 192.168.1.100:5555 (device)
```

---

### info

Show device information.

```bash
ditto info
```

**Output:**
```
Device Information:
  Serial:          emulator-5554
  Model:           Pixel 4
  Manufacturer:    Google
  Android Version: 12
  SDK Version:     31
  Screen Size:     1080 x 2340
```

---

## Exit Codes

| Code | Description |
|------|-------------|
| `0` | Success |
| `1` | Error (element not found, command failed, etc.) |

---

## Scripting Examples

### Shell Script

```bash
#!/bin/bash
# Open app and navigate

ditto open Settings
sleep 2

ditto tap -t "Network"
sleep 1

ditto tap -t "Wi-Fi"
sleep 1

ditto screenshot wifi_settings.png

ditto press back
ditto press back
ditto press home
```

### Loop Until Element Found

```bash
#!/bin/bash
# Scroll until element is found

for i in {1..10}; do
    if ditto find -t "Target Item" 2>/dev/null; then
        ditto tap -t "Target Item"
        exit 0
    fi
    ditto scroll down
    sleep 0.5
done

echo "Element not found"
exit 1
```

### Batch Screenshots

```bash
#!/bin/bash
# Take multiple screenshots

for i in {1..5}; do
    ditto screenshot "screen_$i.png"
    ditto swipe left
    sleep 1
done
```

### Error Handling

```bash
#!/bin/bash
# With error handling

if ! ditto devices | grep -q "device"; then
    echo "No device connected"
    exit 1
fi

if ditto tap -t "Login" --timeout 5; then
    echo "Tapped Login button"
else
    echo "Login button not found"
    exit 1
fi
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANDROID_HOME` | Path to Android SDK (for ADB detection) |
| `ANDROID_SDK_ROOT` | Alternative to ANDROID_HOME |

---

## Troubleshooting

### Device Not Found

```bash
# Check ADB sees the device
adb devices

# Restart ADB server
adb kill-server
adb start-server
```

### Element Not Found

```bash
# Increase timeout
ditto tap -t "Login" --timeout 15

# Check element exists
ditto find -t "Login"

# List all elements (for debugging)
ditto find --class "" --all --json > elements.json
```

### Permission Denied

Ensure USB debugging is enabled and the computer is authorized on the device.

---

## Automation Commands

### run

Run an automation script from a JSON file with support for variables, conditions, and loops.

```bash
ditto run SCRIPT_FILE [OPTIONS]
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `SCRIPT_FILE` | Path to JSON script file |

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--retries` | `-r` | Default retry count per step (default: 2) |
| `--timeout` | `-t` | Default timeout in seconds (default: 5.0) |
| `--delay` | `-d` | Delay between steps in seconds (default: 0.3) |
| `--stop-on-failure` | | Stop on first failure (default) |
| `--continue-on-failure` | | Continue on failure |
| `--screenshot-on-failure` | | Take screenshot when a step fails |
| `--output` | `-o` | Save result to JSON file |
| `--verbose` | `-v` | Show detailed step output |
| `--var` | `-V` | Set variable: `--var name=value` (can be used multiple times) |
| `--vars-file` | | Load variables from JSON or YAML file |

**Examples:**
```bash
# Basic script execution
ditto run my_script.json

# With retries and verbose output
ditto run my_script.json --retries 3 --verbose

# With variables from command line
ditto run login.json --var username=testuser --var password=secret

# With variables from file
ditto run script.json --vars-file config.json

# Combine CLI vars and file (CLI overrides file)
ditto run script.json --vars-file defaults.json --var username=override

# Save results
ditto run my_script.json -o result.json --verbose
```

**Script Format with Variables:**
```json
{
  "name": "login_test",
  "variables": {
    "username": "default_user",
    "timeout": 10
  },
  "steps": [
    {"action": "open", "app": "MyApp"},
    {"action": "tap", "text": "Login"},
    {"action": "type", "value": "{{username}}"},
    {"action": "tap", "text": "Submit"}
  ]
}
```

**See:** [Variables and Control Flow Guide](variables-and-control-flow.md) for complete documentation.

---

### create-script

Create a new automation script from a template.

```bash
ditto create-script NAME [OPTIONS]
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `NAME` | Script filename (`.json` added if not present) |

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--template` | `-t` | Template to use: `empty`, `alarm`, `app` (default: empty) |

**Examples:**
```bash
# Create empty script
ditto create-script my_automation

# Create from alarm template
ditto create-script set_alarm --template alarm

# Create from app template
ditto create-script app_test -t app
```

---

### validate

Validate an automation script without running it.

```bash
ditto validate SCRIPT_FILE
```

**Examples:**
```bash
ditto validate my_script.json
```

**Output:**
```
Script is valid: 7 steps
```

Or if there are errors:
```
Validation failed with 2 error(s):
  - Step 1: Invalid action 'tapp'
  - Step 3: on_failure must be 'stop', 'continue', or 'retry'
```
