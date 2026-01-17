# DittoMation

Android automation framework that records touch interactions, maps them to UI elements, and replays them using smart element location. Supports natural language commands for intuitive automation.

## Features

- **Record** touch gestures (tap, swipe, long press, scroll, pinch) from Android device
- **Replay** recorded workflows with smart element location
- **Natural Language** command execution - describe actions in plain English
- **Smart Locators** - fallback chain (resource-id → content-desc → text → xpath → coordinates)
- **Intent-based App Launching** - reliable app opening via Android intents

## Requirements

- Python 3.8+
- Android SDK with ADB (Android Debug Bridge)
- Android device/emulator with USB debugging enabled

## Installation

1. Clone the repository:
```bash
git clone https://github.com/OmPrakashSingh1704/DittoMation.git
cd DittoMation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure ADB is accessible:
```bash
adb devices  # Should show your connected device
```

## Project Structure

```
DittoMation/
├── recorder/
│   ├── adb_wrapper.py       # ADB command utilities
│   ├── event_listener.py    # Touch event capture via getevent
│   ├── ui_dumper.py         # UI hierarchy capture & parsing
│   ├── element_matcher.py   # Coordinate to element mapping
│   ├── gesture_classifier.py # Gesture recognition (tap/swipe/etc)
│   ├── workflow.py          # Workflow storage & management
│   ├── main.py              # Recording CLI
│   └── interactive_recorder.py # Manual step-by-step recording
├── replayer/
│   ├── locator.py           # Smart element location
│   ├── executor.py          # Gesture execution via ADB
│   ├── main.py              # Replay CLI
│   ├── text_runner.py       # Plain text command execution
│   └── nl_runner.py         # Natural language execution
├── docs/
│   └── approach.md          # Technical approach documentation
├── output/                  # Generated workflow files
└── README.md
```

## Usage

### Natural Language Runner (Recommended)

Execute Android actions using natural language:

```bash
# Single command
python replayer/nl_runner.py "Open YouTube, search for 'Mr. Beast', play latest video"

# Interactive mode
python replayer/nl_runner.py --interactive

# From file
python replayer/nl_runner.py --file instructions.txt
```

**Supported Commands:**
- `open [app]` - Open an app (Clock, YouTube, Settings, etc.)
- `tap [element]` - Tap on element by text/description
- `long press [element]` - Long press on element
- `swipe up/down/left/right` - Swipe gestures
- `scroll up/down` - Scroll gestures
- `type "text"` - Input text
- `search for "query"` - Search within current app
- `back` / `home` - Navigation
- `wait [seconds]` - Pause execution
- `call [number]` - Make a phone call
- `set alarm for 8:00` - Set an alarm
- `go to [url]` - Open URL in browser
- `play first/latest video` - Play video results
- `copy last number I called` - Copy to clipboard
- `search for that number you copied` - Use clipboard

### Recording Workflows

```bash
# Interactive recording (recommended for emulators)
python recorder/interactive_recorder.py --output my_workflow.json

# Automated recording via getevent (physical devices)
python recorder/main.py --output my_workflow.json
```

### Replaying Workflows

```bash
# Replay a recorded workflow
python replayer/main.py --workflow my_workflow.json

# With custom delay between steps
python replayer/main.py --workflow my_workflow.json --delay 1000
```

### Text-based Commands

```bash
# Simple text commands
python replayer/text_runner.py "tap Phone; tap Contacts; swipe down"

# From file
python replayer/text_runner.py commands.txt
```

## Examples

### Open YouTube and Play a Video
```bash
python replayer/nl_runner.py "Open YouTube, search for 'cooking tutorial', play first video"
```

### Make a Phone Call
```bash
python replayer/nl_runner.py "Call 1234567890, wait 30, end call"
```

### Set an Alarm
```bash
python replayer/nl_runner.py "Open clock, set alarm for 7:30 am"
```

### Copy and Search
```bash
python replayer/nl_runner.py "Open phone, copy last number I called, go home, open youtube, search for that number you copied"
```

## How It Works

See [docs/approach.md](docs/approach.md) for detailed technical documentation.

## Troubleshooting

### ADB not found
Set the `ANDROID_HOME` environment variable or add ADB to your PATH.

### UI dump timeout
The device may be busy. The tool will retry automatically. You can also:
```bash
adb shell pkill -f uiautomator
```

### Text input drops characters
This can happen on slow devices. The tool types in chunks with delays to mitigate this.

### App not found
Use the exact app name as it appears on the device, or use one of the supported intent-based apps (clock, settings, youtube, etc.).

## License

MIT License
