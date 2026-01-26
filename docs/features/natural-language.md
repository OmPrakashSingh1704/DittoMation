# Natural Language Commands

Control Android devices using plain English commands.

## Basic Usage

```bash
ditto nl "open Settings, tap Wi-Fi, toggle first switch"
```

Or in Python:

```python
from replayer.nl_runner import execute_nl_command

execute_nl_command("open YouTube, search for cats, play first video")
```

---

## Command Reference

### App Control

| Command | Example |
|---------|---------|
| Open app | `open YouTube`, `open Settings`, `launch Chrome` |
| Close app | `close app`, `force stop` |

### Touch Gestures

| Command | Example |
|---------|---------|
| Tap | `tap Login`, `tap the search button`, `click Submit` |
| Long press | `long press icon`, `hold Settings` |
| Double tap | `double tap image` |

### Swipe & Scroll

| Command | Example |
|---------|---------|
| Swipe | `swipe up`, `swipe left`, `swipe down slowly` |
| Scroll | `scroll down`, `scroll to bottom`, `scroll up` |

### Text Input

| Command | Example |
|---------|---------|
| Type | `type hello world`, `enter password123`, `input test@email.com` |
| Clear | `clear text`, `clear field` |

### Navigation

| Command | Example |
|---------|---------|
| Back | `go back`, `press back`, `back` |
| Home | `go home`, `press home`, `home` |
| Recent apps | `recent apps`, `open recents` |

### Wait

| Command | Example |
|---------|---------|
| Wait | `wait 5 seconds`, `wait 2s`, `pause 3 seconds` |
| Wait for element | `wait for Login button` |

### Phone Functions

| Command | Example |
|---------|---------|
| Call | `call 1234567890`, `dial +1-555-123-4567` |
| SMS | `send SMS to 1234567890` |

---

## Chaining Commands

Use commas to chain multiple commands:

```bash
ditto nl "open Chrome, tap search, type github, tap first result"
```

Each command executes sequentially with automatic delays.

---

## Examples

### Login Flow

```bash
ditto nl "open MyApp, tap Login, type testuser, tap password field, type secret123, tap Submit"
```

### Social Media

```bash
ditto nl "open Instagram, tap search, type cats, tap first post, double tap to like"
```

### Settings

```bash
ditto nl "open Settings, scroll down, tap About Phone, tap Build Number 7 times"
```

### Navigation

```bash
ditto nl "open Maps, type coffee shops, tap first result, tap Directions"
```

---

## Tips

1. **Be specific** - "tap Login button" is better than "tap button"
2. **Use delays** - Add "wait 2 seconds" between commands if needed
3. **Check elements** - Use `ditto ui` to see current screen elements
