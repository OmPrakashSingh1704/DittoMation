# Record & Replay

Capture your interactions and replay them with smart element matching.

## Recording

### Interactive Recording

```bash
ditto record --output workflow.json
```

Follow the prompts:

1. Choose gesture type (tap, swipe, scroll, etc.)
2. Perform the gesture on your device
3. DittoMation captures the element and coordinates
4. Repeat until done
5. Press `Ctrl+C` to save

### Automated Recording

```bash
ditto record --auto --output workflow.json
```

This captures touch events automatically using `getevent`.

---

## Workflow Format

Recorded workflows are saved as JSON:

```json
{
  "name": "Login Flow",
  "steps": [
    {
      "id": 1,
      "gesture": {
        "type": "tap",
        "start": [540, 350]
      },
      "locator": {
        "primary": {"strategy": "id", "value": "username_input"},
        "fallbacks": [
          {"strategy": "content_desc", "value": "Enter username"},
          {"strategy": "text", "value": "Username"}
        ],
        "bounds": [100, 300, 980, 400]
      },
      "element": {
        "class": "android.widget.EditText",
        "resource_id": "com.example:id/username_input",
        "text": "",
        "content_desc": "Enter username"
      }
    },
    {
      "id": 2,
      "gesture": {
        "type": "tap",
        "start": [540, 650]
      },
      "locator": {
        "primary": {"strategy": "id", "value": "login_btn"},
        "fallbacks": [
          {"strategy": "text", "value": "Login"},
          {"strategy": "text", "value": "Sign In"}
        ]
      }
    }
  ]
}
```

---

## Replaying

### Basic Replay

```bash
ditto run workflow.json
```

### With Variables

```bash
ditto run workflow.json --var username=testuser --var password=secret
```

### With Delay

```bash
ditto run workflow.json --delay 1000  # 1 second between steps
```

---

## Gestures Supported

| Gesture | Description |
|---------|-------------|
| `tap` | Single tap |
| `long_press` | Press and hold |
| `swipe` | Directional swipe |
| `scroll` | Scroll gesture |
| `pinch` | Zoom in/out |

---

## Smart Replay

When replaying, DittoMation:

1. **Finds the element** using the locator chain
2. **Falls back** if primary locator fails
3. **Calculates new coordinates** based on found element
4. **Executes the gesture** at the correct position

This means your workflow works even if:

- Element moved to a different position
- Screen size changed
- Resource ID was renamed (if fallbacks exist)

---

## Editing Workflows

You can manually edit the JSON to:

- Add more fallback strategies
- Change gesture parameters
- Add variables with `{{variable}}` syntax
- Add control flow (loops, conditions)

Example with variables:

```json
{
  "id": 1,
  "action": "type",
  "text": "{{username}}"
}
```
