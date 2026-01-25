# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-25

### Added

- **Core Module**
  - `Android` class for high-level device control
  - Comprehensive exception hierarchy for better error handling
  - Configurable logging with multiple output formats
  - Configuration management with YAML/JSON support
  - Ad filtering for cleaner automation

- **Recorder Module**
  - Interactive step-by-step recording via `InteractiveRecorder`
  - Automated touch event recording via `getevent`
  - Gesture classification (tap, swipe, long press, scroll, pinch)
  - UI hierarchy capture and element matching
  - Workflow storage in JSON format

- **Replayer Module**
  - Smart element location with fallback chain (resource-id, content-desc, text, xpath, coordinates)
  - Natural language command execution
  - Text-based command parsing
  - Gesture execution via ADB

- **Automation Features**
  - Variables and expressions with `{{variable}}` syntax
  - Control flow: if/else conditions, for/while/until loops
  - Intent-based app launching for reliable app opening
  - Step-by-step execution with detailed results

- **CLI**
  - `ditto` command-line tool
  - Commands: `run`, `record`, `replay`, `devices`, `shell`
  - Variable passing via command line or file

- **Cloud Support** (optional)
  - AWS Device Farm integration
  - Firebase Test Lab support

- **Documentation**
  - API documentation
  - CLI usage guide
  - Variables and control flow guide
  - Technical approach documentation

- **Developer Experience**
  - Type hints throughout codebase
  - Pre-commit hooks configuration
  - CI/CD with GitHub Actions
  - Docker support

### Security

- Input validation for all user-provided data
- Safe expression evaluation without `eval()`
- XPath and text escaping to prevent injection

[Unreleased]: https://github.com/OmPrakashSingh1704/DittoMation/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/OmPrakashSingh1704/DittoMation/releases/tag/v1.0.0
