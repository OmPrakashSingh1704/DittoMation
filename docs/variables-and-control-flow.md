# Variables and Control Flow Guide

DittoMation supports variables, expressions, and control flow constructs for building dynamic automation scripts.

## Table of Contents

- [Variables](#variables)
- [Variable Resolution](#variable-resolution)
- [Expressions](#expressions)
- [Control Flow](#control-flow)
- [Actions Reference](#actions-reference)
- [Examples](#examples)

---

## Variables

Variables allow you to store and reuse values throughout your automation scripts.

### Defining Variables

Variables can be defined in multiple ways:

**1. In the script file:**
```json
{
  "variables": {
    "username": "testuser",
    "password": "secret123",
    "max_retries": 3,
    "items": ["Item A", "Item B", "Item C"]
  },
  "steps": [...]
}
```

**2. Via command line:**
```bash
ditto run script.json --var username=myuser --var count=5
```

**3. From a variables file:**
```bash
ditto run script.json --vars-file config.json
```

**4. Using set_variable action:**
```json
{"action": "set_variable", "variable": "counter", "value": "0"}
{"action": "set_variable", "variable": "greeting", "expr": "'Hello, ' + username"}
```

### Variable Priority

When the same variable is defined in multiple places, the priority is:
1. CLI `--var` options (highest)
2. `--vars-file` file
3. Script `variables` section (lowest)

---

## Variable Resolution

Use `{{variable}}` syntax to reference variables in step fields.

### Supported Fields

Variables can be used in these step fields:
- `text`, `id`, `desc` - Element locators
- `value` - For type action
- `app` - App name for open action
- `message` - For log action
- `direction` - For swipe/scroll

### Basic Usage

```json
{
  "variables": {"username": "john"},
  "steps": [
    {"action": "type", "value": "{{username}}"},
    {"action": "log", "message": "Logged in as {{username}}"}
  ]
}
```

### Nested Access

Access nested object properties with dot notation:

```json
{
  "variables": {
    "user": {"name": "Alice", "email": "alice@example.com"}
  },
  "steps": [
    {"action": "type", "value": "{{user.name}}"},
    {"action": "type", "value": "{{user.email}}"}
  ]
}
```

### Array Access

Access array elements with bracket notation:

```json
{
  "variables": {
    "items": ["first", "second", "third"]
  },
  "steps": [
    {"action": "tap", "text": "{{items[0]}}"},
    {"action": "tap", "text": "{{items[1]}}"}
  ]
}
```

### Default Values

Provide default values with the pipe syntax:

```json
{"action": "type", "value": "{{username|guest}}"}
```

If `username` is not defined, "guest" will be used.

---

## Expressions

The expression engine allows evaluating conditions and computing values safely.

### Supported Operations

**Comparisons:**
- `==`, `!=`, `<`, `>`, `<=`, `>=`
- `in`, `not in`

**Boolean:**
- `and`, `or`, `not`

**Arithmetic:**
- `+`, `-`, `*`, `/`, `//`, `%`, `**`

**String Methods:**
- `.upper()`, `.lower()`, `.strip()`
- `.startswith()`, `.endswith()`
- `.replace()`, `.split()`

**Built-in Functions:**
- `len()`, `str()`, `int()`, `float()`, `bool()`
- `min()`, `max()`, `sum()`, `abs()`, `round()`
- `any()`, `all()`, `sorted()`, `range()`

### Element Functions

These functions interact with the device UI:

| Function | Description |
|----------|-------------|
| `element_exists(text=, id=, desc=)` | Check if element exists |
| `element_text(text=, id=, desc=)` | Get element's text content |
| `element_count(text=, id=, desc=)` | Count matching elements |
| `element_visible(text=, id=, desc=)` | Check if element is visible |

**Examples:**
```json
{"action": "if", "expr": "element_exists(text='Login')"}
{"action": "if", "expr": "element_count(text='Item') > 5"}
{"action": "while", "expr": "not element_exists(text='Complete')"}
```

### Safety

The expression engine is sandboxed:
- No imports allowed
- No file system access
- No arbitrary code execution
- Only whitelisted functions

---

## Control Flow

### if / elif / else

Conditional execution based on expressions:

```json
{
  "action": "if",
  "expr": "element_exists(text='Welcome')",
  "then_steps": [
    {"action": "log", "message": "Already logged in"}
  ],
  "else_steps": [
    {"action": "tap", "text": "Login"},
    {"action": "type", "value": "{{username}}"},
    {"action": "tap", "text": "Submit"}
  ]
}
```

**With elif:**
```json
{
  "action": "if",
  "expr": "count > 100",
  "then_steps": [
    {"action": "log", "message": "Large count"}
  ],
  "elif_blocks": [
    {
      "condition": "count > 50",
      "steps": [{"action": "log", "message": "Medium count"}]
    },
    {
      "condition": "count > 10",
      "steps": [{"action": "log", "message": "Small count"}]
    }
  ],
  "else_steps": [
    {"action": "log", "message": "Very small count"}
  ]
}
```

### for

Iterate over a list of items:

```json
{
  "action": "for",
  "items": "['Item A', 'Item B', 'Item C']",
  "item_var": "item",
  "index_var": "idx",
  "loop_steps": [
    {"action": "tap", "text": "{{item}}"},
    {"action": "wait", "timeout": 0.5}
  ],
  "max_iterations": 100
}
```

**Using a variable as items:**
```json
{
  "variables": {"products": ["Phone", "Tablet", "Laptop"]},
  "steps": [
    {
      "action": "for",
      "items": "products",
      "item_var": "product",
      "loop_steps": [
        {"action": "tap", "text": "{{product}}"}
      ]
    }
  ]
}
```

### while

Loop while condition is true:

```json
{
  "action": "while",
  "expr": "counter < 5",
  "counter_var": "iteration",
  "loop_steps": [
    {"action": "log", "message": "Iteration {{iteration}}"},
    {"action": "set_variable", "variable": "counter", "expr": "counter + 1"}
  ],
  "max_iterations": 100
}
```

### until

Loop until condition becomes true:

```json
{
  "action": "until",
  "expr": "element_exists(text='Success')",
  "counter_var": "attempt",
  "loop_steps": [
    {"action": "log", "message": "Attempt {{attempt}}"},
    {"action": "tap", "text": "Retry"},
    {"action": "wait", "timeout": 2}
  ],
  "max_iterations": 10
}
```

### break / continue

Control loop execution:

```json
{
  "action": "for",
  "items": "range(10)",
  "item_var": "i",
  "loop_steps": [
    {
      "action": "if",
      "expr": "i == 5",
      "then_steps": [{"action": "break"}]
    },
    {"action": "log", "message": "Processing {{i}}"}
  ]
}
```

---

## Actions Reference

### set_variable

Set a variable value.

| Field | Required | Description |
|-------|----------|-------------|
| `variable` | Yes | Variable name |
| `value` | No | Direct value to set |
| `expr` | No | Expression to evaluate |

**Examples:**
```json
{"action": "set_variable", "variable": "count", "value": "0"}
{"action": "set_variable", "variable": "doubled", "expr": "count * 2"}
{"action": "set_variable", "variable": "name", "expr": "'Hello, ' + username"}
```

### extract

Extract data from a UI element into a variable.

| Field | Required | Description |
|-------|----------|-------------|
| `variable` | Yes | Variable name to store result |
| `text/id/desc` | Yes | Element locator |
| `extract_source` | No | What to extract: `text`, `attribute`, `bounds`, `resource_id`, `content_desc`, `class` (default: `text`) |
| `extract_attr` | No | Attribute name when `extract_source="attribute"` |
| `regex` | No | Regex pattern to extract substring |

**Examples:**
```json
{"action": "extract", "variable": "balance", "text": "Balance:", "extract_source": "text"}
{"action": "extract", "variable": "amount", "id": "price", "regex": "\\$([\\d,]+\\.\\d{2})"}
```

### log

Log a message.

| Field | Required | Description |
|-------|----------|-------------|
| `message` | Yes | Message to log |
| `level` | No | Log level: `debug`, `info`, `warning`, `error` (default: `info`) |

**Examples:**
```json
{"action": "log", "message": "Starting login process"}
{"action": "log", "message": "Error: {{error_msg}}", "level": "error"}
```

### assert

Assert a condition is true.

| Field | Required | Description |
|-------|----------|-------------|
| `expr` | Yes | Condition to assert |
| `message` | No | Error message if assertion fails |

**Examples:**
```json
{"action": "assert", "expr": "count > 0", "message": "Count must be positive"}
{"action": "assert", "expr": "element_exists(text='Success')"}
```

---

## Examples

### Login with Retry

```json
{
  "name": "login_with_retry",
  "variables": {
    "username": "testuser",
    "password": "secret123",
    "max_attempts": 3
  },
  "steps": [
    {"action": "open", "app": "MyApp"},
    {"action": "wait", "timeout": 2},
    {
      "action": "set_variable",
      "variable": "attempt",
      "value": "0"
    },
    {
      "action": "until",
      "expr": "element_exists(text='Welcome') or attempt >= max_attempts",
      "loop_steps": [
        {"action": "set_variable", "variable": "attempt", "expr": "attempt + 1"},
        {"action": "log", "message": "Login attempt {{attempt}}"},
        {"action": "tap", "text": "Login"},
        {"action": "type", "value": "{{username}}"},
        {"action": "tap", "text": "Next"},
        {"action": "type", "value": "{{password}}"},
        {"action": "tap", "text": "Submit"},
        {"action": "wait", "timeout": 3}
      ],
      "max_iterations": 5
    },
    {
      "action": "assert",
      "expr": "element_exists(text='Welcome')",
      "message": "Login failed after max attempts"
    }
  ]
}
```

### Process List of Items

```json
{
  "name": "process_items",
  "variables": {
    "items": ["Product A", "Product B", "Product C"]
  },
  "steps": [
    {"action": "open", "app": "Shopping"},
    {"action": "wait", "timeout": 2},
    {
      "action": "for",
      "items": "items",
      "item_var": "product",
      "index_var": "idx",
      "loop_steps": [
        {"action": "log", "message": "Processing item {{idx}}: {{product}}"},
        {"action": "tap", "text": "Search"},
        {"action": "type", "value": "{{product}}"},
        {"action": "tap", "text": "Go"},
        {"action": "wait", "timeout": 1},
        {
          "action": "if",
          "expr": "element_exists(text='Add to Cart')",
          "then_steps": [
            {"action": "tap", "text": "Add to Cart"},
            {"action": "log", "message": "Added {{product}} to cart"}
          ],
          "else_steps": [
            {"action": "log", "message": "{{product}} not available", "level": "warning"}
          ]
        },
        {"action": "press", "value": "back"}
      ]
    },
    {"action": "log", "message": "Processed all items"}
  ]
}
```

### Wait for Loading

```json
{
  "name": "wait_for_loading",
  "steps": [
    {"action": "tap", "text": "Load Data"},
    {
      "action": "until",
      "expr": "not element_exists(text='Loading...')",
      "loop_steps": [
        {"action": "log", "message": "Still loading...", "level": "debug"},
        {"action": "wait", "timeout": 1}
      ],
      "max_iterations": 30
    },
    {"action": "log", "message": "Loading complete"},
    {"action": "screenshot", "value": "loaded_screen.png"}
  ]
}
```

---

## Python API

You can also use variables and control flow from Python:

```python
from core.automation import Automation, Step

# Create automation with initial variables
auto = Automation(initial_vars={"username": "test"})

# Set variables programmatically
auto.set_variable("count", 5)

# Run with additional variables
result = auto.run(steps, initial_vars={"password": "secret"})

# Get variable value
value = auto.get_variable("count")
```

### Direct Expression Evaluation

```python
from core.variables import VariableContext
from core.expressions import SafeExpressionEngine

ctx = VariableContext({"x": 10, "name": "test"})
engine = SafeExpressionEngine(ctx)

# Evaluate expressions
result = engine.evaluate("x > 5")
print(result.value)  # True

result = engine.evaluate("name.upper()")
print(result.value)  # "TEST"

# Boolean evaluation
if engine.evaluate_bool("x > 5 and len(name) > 3"):
    print("Condition met")
```
