# Social Media Post Drafts for DittoMation

## Show HN (Hacker News)

**Title:** Show HN: DittoMation – Android automation with natural language commands

**Post:**
```
I built DittoMation because I was frustrated with how often Android automation scripts break. Change the screen size? Broken. App updates the UI? Broken. Element ID renamed? Broken.

DittoMation uses smart element location with multiple fallback strategies (resource-id → content-desc → text → xpath → visual AI → coordinates), so your automation keeps working even when the UI changes.

Key features:
- Natural language commands: `ditto nl "open YouTube, search for cats, play first video"`
- Record & replay with smart element matching
- Variables and control flow for complex automation
- ~98% success rate vs ~70% for coordinate-based tools

Try the interactive demo (no install): https://omprakashsingh1704.github.io/DittoMation/demo/

GitHub: https://github.com/OmPrakashSingh1704/DittoMation

Would love feedback on what commands or features would be most useful!
```

---

## Reddit r/androiddev

**Title:** I built an Android automation tool that uses natural language commands and doesn't break when UI changes

**Post:**
```
Hey r/androiddev!

I've been working on DittoMation, an open-source Android automation framework that solves a problem I kept running into: automation scripts that break every time the UI changes.

**The Problem:**
Most automation tools rely on fixed coordinates or exact element IDs. Change your screen resolution? Script breaks. App gets updated? Script breaks.

**The Solution:**
DittoMation uses a smart locator with multiple fallback strategies. It tries resource-id first, then content-desc, text, xpath, and finally coordinates. This means your scripts are much more resilient.

**Cool Features:**
- **Natural Language Commands**: Just describe what you want in English
  ```
  ditto nl "open Chrome, search for weather, tap first result"
  ```
- **Record & Replay**: Record your actions once, replay anywhere
- **Variables & Control Flow**: Build complex automation with conditions and loops
- **~98% success rate** across different devices/UI versions

**Try it:**
- Interactive demo (no install): https://omprakashsingh1704.github.io/DittoMation/demo/
- GitHub: https://github.com/OmPrakashSingh1704/DittoMation
- PyPI: `pip install dittomation`

Would love to hear your thoughts and what features would be useful for your workflows!
```

---

## Reddit r/Python

**Title:** DittoMation: Control Android devices with Python using natural language commands

**Post:**
```
I built a Python library for Android automation that lets you control devices using natural language:

```python
from dittomatic import DittoMation

ditto = DittoMation()
ditto.run("open YouTube, search for cats, play first video")
```

Or from CLI:
```bash
ditto nl "set alarm for 7:30 am"
```

**Why I built this:**
Existing tools use fixed coordinates or exact element IDs that break constantly. DittoMation uses smart element location with fallbacks, achieving ~98% success rate vs ~70% for coordinate-based tools.

**Features:**
- Natural language command parsing
- Smart element locator with fallback chain
- Record and replay workflows
- Variables and control flow (if/else, loops)
- AWS Device Farm & Firebase Test Lab support

**Links:**
- Interactive Demo: https://omprakashsingh1704.github.io/DittoMation/demo/
- GitHub: https://github.com/OmPrakashSingh1704/DittoMation
- Docs: https://omprakashsingh1704.github.io/DittoMation/

Install: `pip install dittomation`

Feedback welcome!
```

---

## Reddit r/automation

**Title:** Open source Android automation that uses plain English commands

**Post:**
```
Just released DittoMation - an Android automation tool where you can write commands in plain English:

"Open YouTube, search for cooking tutorial, play first video"
"Set alarm for 7:30 am"
"Call 1234567890, wait 30 seconds, end call"

**What makes it different:**
- **Natural Language**: No need to learn complex APIs
- **Smart Locator**: Doesn't break when UI changes (98% success rate)
- **Record & Replay**: Record once, replay anywhere
- **Open Source**: MIT license, free forever

Try the interactive demo without installing anything:
https://omprakashsingh1704.github.io/DittoMation/demo/

GitHub: https://github.com/OmPrakashSingh1704/DittoMation

What automation tasks would you use this for?
```

---

## Twitter/X

**Post 1:**
```
🚀 Just released DittoMation - Android automation that actually works!

Write commands in plain English:
"open YouTube, search for cats, play first video"

Smart locator with 98% success rate vs 70% for coordinate-based tools.

Try the demo: https://omprakashsingh1704.github.io/DittoMation/demo/

#Android #Python #Automation #OpenSource
```

**Post 2 (Thread starter):**
```
🧵 Why do Android automation scripts keep breaking?

1/ Screen size changes → Broken
2/ App updates → Broken
3/ Element ID renamed → Broken

I built DittoMation to fix this. Here's how 👇
```

---

## LinkedIn

**Post:**
```
🚀 Excited to share DittoMation - an open-source Android automation framework I've been building!

The Problem: Traditional automation tools break constantly when UIs change. Fixed coordinates and exact element IDs are fragile.

The Solution: DittoMation uses smart element location with multiple fallback strategies, achieving ~98% success rate compared to ~70% for coordinate-based approaches.

Key Features:
✅ Natural language commands - describe what you want in plain English
✅ Smart locator with fallback chain
✅ Record & replay workflows
✅ Variables and control flow for complex automation

Try the interactive demo (no installation required):
https://omprakashsingh1704.github.io/DittoMation/demo/

GitHub: https://github.com/OmPrakashSingh1704/DittoMation

Would love to connect with others working on test automation and mobile development!

#Android #Automation #Python #OpenSource #TestAutomation #QA
```

---

## How to Add GitHub Topics

Go to your repository page and:
1. Click the gear icon ⚙️ next to "About" (right sidebar)
2. In the "Topics" field, add these tags:

```
android
automation
testing
python
natural-language-processing
adb
ui-testing
mobile-testing
android-automation
test-automation
```

---

## How to Add Social Preview Image

1. Open `social-preview.html` in your browser
2. Take a screenshot (or use browser dev tools to capture at 1280x640)
3. Go to your GitHub repo → Settings → General
4. Scroll to "Social preview" and upload the image

Alternatively, use a tool like https://socialify.git.ci/ to generate one automatically.
