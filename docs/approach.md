# DittoMation Technical Approach

This document describes the technical architecture and approach used in DittoMation for Android UI automation.

## Overview

DittoMation uses a **record-replay** paradigm combined with **semantic understanding** to create robust, maintainable Android automation. Unlike coordinate-based automation that breaks with UI changes, DittoMation captures the *meaning* of interactions and can adapt to UI variations.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Recording  │  │   Replay    │  │  Natural Language CLI   │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
└─────────┼────────────────┼──────────────────────┼───────────────┘
          │                │                      │
          ▼                ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Core Components                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Gesture   │  │   Element   │  │    Workflow Engine      │  │
│  │ Classifier  │  │   Matcher   │  │  (parse → execute)      │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
└─────────┼────────────────┼──────────────────────┼───────────────┘
          │                │                      │
          ▼                ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ADB Layer                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  getevent   │  │ uiautomator │  │     input commands      │  │
│  │  (capture)  │  │   (dump)    │  │   (tap/swipe/text)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          │                │                      │
          ▼                ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Android Device                              │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. ADB Wrapper (`recorder/adb_wrapper.py`)

Provides a Python interface to Android Debug Bridge (ADB) commands:

- **Device Detection**: Auto-discovers ADB path and connected devices
- **Screen Info**: Gets screen dimensions for coordinate mapping
- **UI Dump**: Captures UI hierarchy via `uiautomator dump`
- **Shell Streaming**: Streams `getevent` output for touch capture

```python
# Example: Capture UI hierarchy
root = dump_ui()  # Returns XML ElementTree

# Example: Execute ADB command
output = run_adb(['shell', 'input', 'tap', '540', '1200'])
```

### 2. Touch Event Capture (`recorder/event_listener.py`)

Captures raw touch events from the Linux kernel input subsystem:

```
/dev/input/eventX → getevent → TouchEventListener → Gesture Events
```

**Event Types Captured:**
- `EV_ABS` (0x03): Absolute position events
  - `ABS_MT_POSITION_X` (0x35): X coordinate
  - `ABS_MT_POSITION_Y` (0x36): Y coordinate
  - `ABS_MT_TRACKING_ID` (0x39): Finger tracking
- `EV_SYN` (0x00): Synchronization events

**Coordinate Mapping:**
Raw input coordinates are scaled to screen coordinates:
```python
screen_x = (raw_x / max_x) * screen_width
screen_y = (raw_y / max_y) * screen_height
```

### 3. UI Hierarchy Parsing (`recorder/ui_dumper.py`)

Captures and parses the Android view hierarchy:

```xml
<!-- uiautomator dump output -->
<node class="android.widget.Button"
      resource-id="com.app:id/login"
      content-desc="Login button"
      text="Login"
      bounds="[100,200][300,250]"
      clickable="true" />
```

**Parsed Element Structure:**
```python
{
    "class": "android.widget.Button",
    "resource_id": "com.app:id/login",
    "content_desc": "Login button",
    "text": "Login",
    "bounds": (100, 200, 300, 250),
    "clickable": True,
    "xpath": "//android.widget.Button[@text='Login']"
}
```

### 4. Element Matching (`recorder/element_matcher.py`)

Maps touch coordinates to UI elements using spatial containment:

```
Touch at (150, 225) → Find elements containing point → Select best match
```

**Selection Criteria:**
1. Element must contain the touch point
2. Prefer smaller elements (more specific)
3. Prefer clickable elements
4. Break ties using element depth in hierarchy

### 5. Gesture Classification (`recorder/gesture_classifier.py`)

Classifies touch sequences into semantic gestures:

| Gesture | Duration | Movement | Criteria |
|---------|----------|----------|----------|
| Tap | < 500ms | < 50px | Short, stationary |
| Long Press | ≥ 500ms | < 50px | Long, stationary |
| Swipe | Any | ≥ 50px | Directional movement |
| Scroll | Any | ≥ 50px | Within scrollable container |
| Pinch | Any | Multi-touch | Distance change between fingers |

### 6. Smart Locator (`replayer/locator.py`)

Finds elements during replay using a fallback chain:

```
1. resource-id  (most stable)
       ↓ not found
2. content-desc (accessibility label)
       ↓ not found
3. text         (visible text)
       ↓ not found
4. xpath        (structural path)
       ↓ not found
5. coordinates  (last resort)
```

**Why This Order?**
- `resource-id`: Developer-assigned, stable across sessions
- `content-desc`: Accessibility label, often stable
- `text`: User-visible, may change with language/state
- `xpath`: Structural, breaks with layout changes
- `coordinates`: Absolute, breaks with any UI change

### 7. Gesture Executor (`replayer/executor.py`)

Executes gestures via ADB input commands:

```bash
# Tap
adb shell input tap X Y

# Long press (swipe with same start/end)
adb shell input swipe X Y X Y DURATION_MS

# Swipe
adb shell input swipe X1 Y1 X2 Y2 DURATION_MS

# Text input (chunked for reliability)
adb shell input text "chunk1"
adb shell input text "chunk2"
```

### 8. Natural Language Parser (`replayer/nl_runner.py`)

Converts natural language to executable actions:

```
"Open YouTube and search for cats"
        ↓
    Tokenize & Split
        ↓
["open youtube", "search for cats"]
        ↓
    Pattern Matching
        ↓
[(_action_tap, "youtube"), (_action_search, "cats")]
        ↓
    Execute Actions
```

**Pattern Examples:**
```python
patterns = [
    (r'\bopen\s+(.+)', _action_tap),
    (r'\bsearch\s+for\s+"?(.+)"?', _action_search),
    (r'\bswipe\s+(up|down|left|right)', _action_swipe),
    (r'\bwait\s+(\d+)', _action_wait),
]
```

## Workflow Format

Recorded workflows are stored as JSON:

```json
{
    "metadata": {
        "app_package": "com.example.app",
        "device": "emulator-5554",
        "screen_size": [1080, 2340],
        "recorded_at": "2026-01-18T10:30:00Z"
    },
    "steps": [
        {
            "step_id": 1,
            "action": "tap",
            "locator": {
                "primary": {"strategy": "id", "value": "com.app:id/login"},
                "fallbacks": [
                    {"strategy": "text", "value": "Login"},
                    {"strategy": "xpath", "value": "//Button[@text='Login']"}
                ]
            },
            "gesture": {
                "type": "tap",
                "start": [540, 1200],
                "duration_ms": 120
            }
        }
    ]
}
```

## Intent-Based App Launching

For reliable app launching, DittoMation uses Android intents:

```python
app_intents = {
    'clock': 'android.intent.action.SHOW_ALARMS',
    'settings': 'android.settings.SETTINGS',
    'camera': 'android.media.action.IMAGE_CAPTURE',
    'phone': 'android.intent.action.DIAL',
    # ...
}

# Launch via ADB
adb shell am start -a android.intent.action.SHOW_ALARMS
```

**Benefits:**
- Works regardless of home screen layout
- No need to find app icon
- Faster and more reliable

## Clipboard/State Management

The natural language runner maintains state across commands:

```python
# Copy operation stores value
"copy last number I called"  →  self.clipboard = "1234567890"

# Later command references it
"search for that number you copied"  →  search(self.clipboard)
```

**Supported References:**
- `that number you copied`
- `the copied text`
- `what you copied`
- `the clipboard`
- `it` (in search context)

## Error Handling & Retry Logic

### UI Dump Retries
```python
for attempt in range(max_retries):
    try:
        dump_ui()
    except TimeoutError:
        kill_uiautomator()  # Kill stuck process
        time.sleep(retry_delay)
        continue
```

### Text Input Chunking
Long text is typed in chunks to prevent dropped characters:
```python
for chunk in split_into_chunks(text, size=10):
    adb_input_text(chunk)
    time.sleep(0.15)  # Delay between chunks
```

## Limitations

1. **Emulator Touch Capture**: Emulator touch events bypass `getevent`. Use interactive recording instead.

2. **Dynamic Content**: Elements that change frequently (timers, animations) may be hard to locate.

3. **Complex Gestures**: Multi-finger gestures beyond pinch are not fully supported.

4. **Root Access**: Some advanced features may require rooted devices.

## Future Improvements

- [ ] Image-based element matching (OpenCV/ML)
- [ ] Record and replay multi-app workflows
- [ ] Cloud device farm integration
- [ ] Visual workflow editor
- [ ] Test assertion framework
