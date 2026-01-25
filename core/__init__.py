"""
DittoMation Core Module.

This module provides core functionality shared across all components:
- Custom exceptions
- Logging configuration
- Configuration management
- Android control API

Usage:
    from core import Android

    android = Android()
    android.tap(100, 200)
    android.tap("Login")
    android.open_app("Chrome")
"""

__version__ = "1.0.0"

from .android import Android

from .exceptions import (
    # Base
    DittoMationError,

    # Device errors
    DeviceError,
    DeviceNotFoundError,
    DeviceConnectionError,
    DeviceOfflineError,
    DeviceUnauthorizedError,

    # ADB errors
    ADBError,
    ADBNotFoundError,
    ADBCommandError,
    ADBTimeoutError,

    # UI errors
    UIError,
    UIHierarchyError,
    ElementNotFoundError,
    MultipleElementsFoundError,
    InvalidBoundsError,

    # Workflow errors
    WorkflowError,
    WorkflowLoadError,
    WorkflowSaveError,
    WorkflowValidationError,
    StepExecutionError,

    # Gesture errors
    GestureError,
    InvalidGestureError,
    GestureExecutionError,

    # Input errors
    InputError,
    InvalidInputDeviceError,
    EventParseError,

    # Configuration errors
    ConfigurationError,
    ConfigLoadError,
    ConfigValidationError,
    InvalidConfigValueError,

    # Natural language errors
    NaturalLanguageError,
    CommandParseError,
    UnknownActionError,
)

from .logging_config import (
    setup_logging,
    get_logger,
    log_exception,
    LoggerMixin,
    setup_recorder_logging,
    setup_replayer_logging,
    setup_nl_runner_logging,
    init_logging,
    get_global_logger,
)

from .config_manager import (
    ConfigManager,
    init_config,
    get_config,
    get_config_value,
    DEFAULT_CONFIG,
)

from .ad_filter import (
    is_ad_element,
    is_sponsored_content,
    filter_ad_elements,
    get_non_ad_elements_at_point,
    find_non_ad_alternative,
    add_custom_ad_pattern,
    clear_custom_patterns,
    load_custom_patterns_from_config,
    AdFilter,
    get_ad_filter,
)

from .automation import (
    Automation,
    Step,
    StepResult,
    AutomationResult,
    StepType,
    StepStatus,
    run_steps,
    tap,
    wait,
    wait_for,
    type_text,
    swipe,
    open_app,
    press,
)

__all__ = [
    # Version
    "__version__",

    # Android API
    "Android",

    # Exceptions
    "DittoMationError",
    "DeviceError",
    "DeviceNotFoundError",
    "DeviceConnectionError",
    "DeviceOfflineError",
    "DeviceUnauthorizedError",
    "ADBError",
    "ADBNotFoundError",
    "ADBCommandError",
    "ADBTimeoutError",
    "UIError",
    "UIHierarchyError",
    "ElementNotFoundError",
    "MultipleElementsFoundError",
    "InvalidBoundsError",
    "WorkflowError",
    "WorkflowLoadError",
    "WorkflowSaveError",
    "WorkflowValidationError",
    "StepExecutionError",
    "GestureError",
    "InvalidGestureError",
    "GestureExecutionError",
    "InputError",
    "InvalidInputDeviceError",
    "EventParseError",
    "ConfigurationError",
    "ConfigLoadError",
    "ConfigValidationError",
    "InvalidConfigValueError",
    "NaturalLanguageError",
    "CommandParseError",
    "UnknownActionError",

    # Logging
    "setup_logging",
    "get_logger",
    "log_exception",
    "LoggerMixin",
    "setup_recorder_logging",
    "setup_replayer_logging",
    "setup_nl_runner_logging",
    "init_logging",
    "get_global_logger",

    # Configuration
    "ConfigManager",
    "init_config",
    "get_config",
    "get_config_value",
    "DEFAULT_CONFIG",

    # Ad Filter
    "is_ad_element",
    "is_sponsored_content",
    "filter_ad_elements",
    "get_non_ad_elements_at_point",
    "find_non_ad_alternative",
    "add_custom_ad_pattern",
    "clear_custom_patterns",
    "load_custom_patterns_from_config",
    "AdFilter",
    "get_ad_filter",

    # Automation
    "Automation",
    "Step",
    "StepResult",
    "AutomationResult",
    "StepType",
    "StepStatus",
    "run_steps",
    "tap",
    "wait",
    "wait_for",
    "type_text",
    "swipe",
    "open_app",
    "press",
]
