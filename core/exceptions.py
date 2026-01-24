"""
Custom exception classes for DittoMation.

This module provides a hierarchy of exceptions for different error types,
enabling better error handling and user-friendly error messages.
"""

from typing import Optional, List, Dict, Any


class DittoMationError(Exception):
    """Base exception for all DittoMation errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None,
                 hint: Optional[str] = None):
        """
        Initialize the exception.

        Args:
            message: The error message.
            details: Optional dictionary with additional error details.
            hint: Optional troubleshooting hint for the user.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.hint = hint

    def __str__(self) -> str:
        result = self.message
        if self.hint:
            result += f"\nHint: {self.hint}"
        return result

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging/serialization."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
            "hint": self.hint
        }


# ============================================================================
# Device Errors
# ============================================================================

class DeviceError(DittoMationError):
    """Base exception for device-related errors."""
    pass


class DeviceNotFoundError(DeviceError):
    """Raised when no Android device is connected or detected."""

    def __init__(self, message: str = "No Android device found",
                 details: Optional[Dict[str, Any]] = None):
        hint = (
            "Make sure your device is connected via USB and USB debugging is enabled. "
            "Run 'adb devices' to check connected devices."
        )
        super().__init__(message, details, hint)


class DeviceConnectionError(DeviceError):
    """Raised when connection to the device fails."""

    def __init__(self, message: str = "Failed to connect to device",
                 device_id: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        hint = (
            "Try disconnecting and reconnecting the USB cable. "
            "You may also try 'adb kill-server' followed by 'adb start-server'."
        )
        details = details or {}
        if device_id:
            details["device_id"] = device_id
        super().__init__(message, details, hint)


class DeviceOfflineError(DeviceError):
    """Raised when device is detected but offline."""

    def __init__(self, device_id: str,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Device '{device_id}' is offline"
        hint = (
            "The device may need to be authorized. Check the device screen "
            "for an authorization dialog and tap 'Allow'."
        )
        details = details or {}
        details["device_id"] = device_id
        super().__init__(message, details, hint)


class DeviceUnauthorizedError(DeviceError):
    """Raised when device is not authorized for debugging."""

    def __init__(self, device_id: str,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Device '{device_id}' is not authorized"
        hint = (
            "Check the device screen for an authorization dialog. "
            "Tap 'Allow' to authorize this computer for USB debugging."
        )
        details = details or {}
        details["device_id"] = device_id
        super().__init__(message, details, hint)


# ============================================================================
# ADB Errors
# ============================================================================

class ADBError(DittoMationError):
    """Base exception for ADB-related errors."""
    pass


class ADBNotFoundError(ADBError):
    """Raised when ADB executable cannot be found."""

    def __init__(self, searched_paths: Optional[List[str]] = None):
        message = "ADB executable not found"
        hint = (
            "Install Android SDK Platform Tools and ensure ADB is in your PATH, "
            "or set ANDROID_HOME environment variable to your SDK location."
        )
        details = {}
        if searched_paths:
            details["searched_paths"] = searched_paths
        super().__init__(message, details, hint)


class ADBCommandError(ADBError):
    """Raised when an ADB command fails."""

    def __init__(self, command: str, returncode: int,
                 stdout: str = "", stderr: str = "",
                 details: Optional[Dict[str, Any]] = None):
        message = f"ADB command failed with exit code {returncode}"
        details = details or {}
        details.update({
            "command": command,
            "returncode": returncode,
            "stdout": stdout[:500] if stdout else "",
            "stderr": stderr[:500] if stderr else ""
        })
        hint = None
        if "device not found" in stderr.lower():
            hint = "No device connected. Check USB connection and USB debugging settings."
        elif "permission denied" in stderr.lower():
            hint = "Permission denied. The device may need to be rooted for this operation."
        super().__init__(message, details, hint)


class ADBTimeoutError(ADBError):
    """Raised when an ADB command times out."""

    def __init__(self, command: str, timeout: int,
                 details: Optional[Dict[str, Any]] = None):
        message = f"ADB command timed out after {timeout} seconds"
        details = details or {}
        details.update({
            "command": command,
            "timeout": timeout
        })
        hint = (
            "The command took too long to complete. The device may be unresponsive "
            "or the operation may require more time. Try increasing the timeout."
        )
        super().__init__(message, details, hint)


# ============================================================================
# UI Errors
# ============================================================================

class UIError(DittoMationError):
    """Base exception for UI-related errors."""
    pass


class UIHierarchyError(UIError):
    """Raised when UI hierarchy cannot be captured or parsed."""

    def __init__(self, message: str = "Failed to capture UI hierarchy",
                 details: Optional[Dict[str, Any]] = None):
        hint = (
            "The UI hierarchy dump may have failed. Wait for the screen to stabilize "
            "and try again. Some screens (like video players) may not dump properly."
        )
        super().__init__(message, details, hint)


class ElementNotFoundError(UIError):
    """Raised when a UI element cannot be found."""

    def __init__(self, locator: str, strategy: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Element not found: {locator}"
        details = details or {}
        details["locator"] = locator
        if strategy:
            details["strategy"] = strategy
        hint = (
            "The element may have changed or may not be visible. "
            "Try waiting for the screen to load, or update the locator."
        )
        super().__init__(message, details, hint)


class MultipleElementsFoundError(UIError):
    """Raised when multiple elements match when only one was expected."""

    def __init__(self, locator: str, count: int,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Multiple elements ({count}) found for locator: {locator}"
        details = details or {}
        details.update({
            "locator": locator,
            "count": count
        })
        hint = (
            "Make the locator more specific to match only one element. "
            "Consider using a more unique attribute like resource-id."
        )
        super().__init__(message, details, hint)


class InvalidBoundsError(UIError):
    """Raised when element bounds are invalid."""

    def __init__(self, bounds: str, element_info: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Invalid element bounds: {bounds}"
        details = details or {}
        details["bounds"] = bounds
        if element_info:
            details["element"] = element_info
        hint = "The element may be off-screen or have zero dimensions."
        super().__init__(message, details, hint)


# ============================================================================
# Workflow Errors
# ============================================================================

class WorkflowError(DittoMationError):
    """Base exception for workflow-related errors."""
    pass


class WorkflowLoadError(WorkflowError):
    """Raised when a workflow file cannot be loaded."""

    def __init__(self, filepath: str, reason: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Failed to load workflow: {filepath}"
        if reason:
            message += f" ({reason})"
        details = details or {}
        details["filepath"] = filepath
        hint = (
            "Check that the file exists and contains valid JSON. "
            "The workflow may have been created with an incompatible version."
        )
        super().__init__(message, details, hint)


class WorkflowSaveError(WorkflowError):
    """Raised when a workflow cannot be saved."""

    def __init__(self, filepath: str, reason: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Failed to save workflow: {filepath}"
        if reason:
            message += f" ({reason})"
        details = details or {}
        details["filepath"] = filepath
        hint = "Check that you have write permissions to the directory."
        super().__init__(message, details, hint)


class WorkflowValidationError(WorkflowError):
    """Raised when a workflow fails validation."""

    def __init__(self, errors: List[str],
                 details: Optional[Dict[str, Any]] = None):
        message = f"Workflow validation failed with {len(errors)} error(s)"
        details = details or {}
        details["validation_errors"] = errors
        hint = "Review the workflow file and fix the reported errors."
        super().__init__(message, details, hint)


class StepExecutionError(WorkflowError):
    """Raised when a workflow step fails to execute."""

    def __init__(self, step_id: int, action: str, reason: str,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Step {step_id} ({action}) failed: {reason}"
        details = details or {}
        details.update({
            "step_id": step_id,
            "action": action
        })
        super().__init__(message, details)


# ============================================================================
# Gesture Errors
# ============================================================================

class GestureError(DittoMationError):
    """Base exception for gesture-related errors."""
    pass


class InvalidGestureError(GestureError):
    """Raised when a gesture is invalid or cannot be performed."""

    def __init__(self, gesture_type: str, reason: str,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Invalid gesture '{gesture_type}': {reason}"
        details = details or {}
        details["gesture_type"] = gesture_type
        super().__init__(message, details)


class GestureExecutionError(GestureError):
    """Raised when a gesture fails to execute."""

    def __init__(self, gesture_type: str, coordinates: tuple,
                 reason: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Failed to execute {gesture_type} at {coordinates}"
        if reason:
            message += f": {reason}"
        details = details or {}
        details.update({
            "gesture_type": gesture_type,
            "coordinates": coordinates
        })
        hint = (
            "The gesture may have failed due to the screen changing during execution. "
            "Try adding a wait before the gesture."
        )
        super().__init__(message, details, hint)


# ============================================================================
# Input Errors
# ============================================================================

class InputError(DittoMationError):
    """Base exception for input-related errors."""
    pass


class InvalidInputDeviceError(InputError):
    """Raised when the touch input device cannot be found."""

    def __init__(self, details: Optional[Dict[str, Any]] = None):
        message = "Touch input device not found"
        hint = (
            "The device may not have a touch screen or the input device "
            "path may have changed. Check 'getevent -p' for available devices."
        )
        super().__init__(message, details, hint)


class EventParseError(InputError):
    """Raised when an input event cannot be parsed."""

    def __init__(self, event_line: str, reason: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Failed to parse input event"
        if reason:
            message += f": {reason}"
        details = details or {}
        details["event_line"] = event_line[:100]
        super().__init__(message, details)


# ============================================================================
# Configuration Errors
# ============================================================================

class ConfigurationError(DittoMationError):
    """Base exception for configuration-related errors."""
    pass


class ConfigLoadError(ConfigurationError):
    """Raised when configuration cannot be loaded."""

    def __init__(self, filepath: str, reason: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Failed to load configuration: {filepath}"
        if reason:
            message += f" ({reason})"
        details = details or {}
        details["filepath"] = filepath
        hint = "Check that the configuration file exists and is valid YAML/JSON."
        super().__init__(message, details, hint)


class ConfigValidationError(ConfigurationError):
    """Raised when configuration fails validation."""

    def __init__(self, errors: List[str],
                 details: Optional[Dict[str, Any]] = None):
        message = f"Configuration validation failed with {len(errors)} error(s)"
        details = details or {}
        details["validation_errors"] = errors
        hint = "Review the configuration file and fix the reported errors."
        super().__init__(message, details, hint)


class InvalidConfigValueError(ConfigurationError):
    """Raised when a configuration value is invalid."""

    def __init__(self, key: str, value: Any, expected: str,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Invalid configuration value for '{key}': {value} (expected {expected})"
        details = details or {}
        details.update({
            "key": key,
            "value": value,
            "expected": expected
        })
        super().__init__(message, details)


# ============================================================================
# Natural Language Errors
# ============================================================================

class NaturalLanguageError(DittoMationError):
    """Base exception for natural language processing errors."""
    pass


class CommandParseError(NaturalLanguageError):
    """Raised when a natural language command cannot be parsed."""

    def __init__(self, command: str, reason: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Failed to parse command: '{command}'"
        if reason:
            message += f" ({reason})"
        details = details or {}
        details["command"] = command
        hint = (
            "Try rephrasing the command using simpler language. "
            "Example commands: 'tap Settings', 'scroll down', 'type hello world'"
        )
        super().__init__(message, details, hint)


class UnknownActionError(NaturalLanguageError):
    """Raised when a natural language action is not recognized."""

    def __init__(self, action: str,
                 similar_actions: Optional[List[str]] = None,
                 details: Optional[Dict[str, Any]] = None):
        message = f"Unknown action: '{action}'"
        details = details or {}
        details["action"] = action
        if similar_actions:
            details["similar_actions"] = similar_actions
            hint = f"Did you mean: {', '.join(similar_actions)}?"
        else:
            hint = (
                "Supported actions include: tap, click, swipe, scroll, type, "
                "long press, back, home, search, open"
            )
        super().__init__(message, details, hint)
