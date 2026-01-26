# DittoMation

**Android automation framework with smart element detection and natural language commands.**

[![PyPI version](https://badge.fury.io/py/dittomation.svg)](https://pypi.org/project/dittomation/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## Why DittoMation?

Most Android automation tools break when the UI changes. They rely on:

- **Fixed coordinates** - break on different screen sizes
- **Hardcoded XPaths** - break when layouts shift
- **Exact element IDs** - break when developers rename them

**DittoMation solves this** with smart element location that adapts to UI changes.

---

## Quick Start

### Installation

```bash
pip install dittomation
```

### Natural Language Commands

```bash
ditto nl "open YouTube, tap search, type cats, play first video"
```

### Record & Replay

```bash
# Record your interactions
ditto record --output workflow.json

# Replay anywhere
ditto run workflow.json
```

### Python API

```python
from core import Android

android = Android()

# Smart element detection
android.tap("Login")           # by text
android.tap(id="btn_submit")   # by ID
android.tap(desc="Send")       # by content-description

# Natural gestures
android.swipe("up")
android.scroll("down")
android.long_press("Settings")
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Smart Locator** | Falls back through multiple strategies to find elements |
| **Natural Language** | Control devices with plain English commands |
| **Record & Replay** | Capture interactions and replay with smart matching |
| **Control Flow** | Variables, loops, and conditionals for complex workflows |
| **Ad Filtering** | Automatically skips ad elements |
| **Cloud Ready** | AWS Device Farm & Firebase Test Lab support |

---

## Benchmark Results

Tested across 4 UI versions (original, layout shift, redesign, tablet):

| Metric | Coordinate-based | DittoMation |
|--------|------------------|-------------|
| **Success Rate** | 70% | 100% |
| **Maintenance fixes** | 6 | 0 |

[See full benchmark details](benchmark.md)

---

## Links

- [GitHub Repository](https://github.com/OmPrakashSingh1704/DittoMation)
- [PyPI Package](https://pypi.org/project/dittomation/)
- [Getting Started Guide](getting-started.md)
