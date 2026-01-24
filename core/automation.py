"""
Automation - Robust multi-step automation runner with retry logic.

Provides a maintainable, error-resistant way to execute UI automation workflows.
Supports retries, waits, conditional steps, and detailed logging.

Usage:
    from core.automation import Automation, Step

    auto = Automation()
    auto.run([
        Step("open", app="clock"),
        Step("tap", text="Alarm"),
        Step("tap", desc="Add alarm"),
        Step("tap", text="11"),
        Step("tap", text="10"),
        Step("tap", text="OK"),
    ])
"""

import time
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, List, Dict, Any, Callable, Union
from pathlib import Path

from core.android import Android
from core.logging_config import get_logger
from core.exceptions import (
    DittoMationError,
    ElementNotFoundError,
    StepExecutionError,
)

logger = get_logger("automation")


class StepType(Enum):
    """Supported step types."""
    TAP = "tap"
    LONG_PRESS = "long_press"
    SWIPE = "swipe"
    SCROLL = "scroll"
    TYPE = "type"
    PRESS = "press"
    OPEN = "open"
    WAIT = "wait"
    WAIT_FOR = "wait_for"
    ASSERT_EXISTS = "assert_exists"
    ASSERT_NOT_EXISTS = "assert_not_exists"
    SCREENSHOT = "screenshot"
    CONDITIONAL = "conditional"


class StepStatus(Enum):
    """Step execution status."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


@dataclass
class StepResult:
    """Result of a step execution."""
    step_index: int
    step_type: str
    status: StepStatus
    message: str = ""
    attempts: int = 1
    duration_ms: float = 0
    confidence: Optional[float] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "step_index": self.step_index,
            "step_type": self.step_type,
            "status": self.status.value,
            "message": self.message,
            "attempts": self.attempts,
            "duration_ms": round(self.duration_ms, 2),
            "confidence": self.confidence,
            "error": self.error,
        }


@dataclass
class Step:
    """
    A single automation step.

    Attributes:
        action: Step type (tap, swipe, type, open, wait, etc.)
        text: Element text to find
        id: Element resource-id to find
        desc: Element content-description to find
        x: X coordinate (for coordinate-based actions)
        y: Y coordinate (for coordinate-based actions)
        app: App name (for open action)
        value: Value for type action or key for press action
        direction: Direction for swipe/scroll (up, down, left, right)
        timeout: Timeout in seconds for element search
        min_confidence: Minimum confidence for element matching (0.0-1.0)
        retries: Number of retry attempts on failure
        retry_delay: Delay between retries in seconds
        wait_before: Wait time before executing step (seconds)
        wait_after: Wait time after executing step (seconds)
        optional: If True, failure doesn't stop execution
        condition: Callable that returns True if step should execute
        on_failure: Action on failure ("stop", "continue", "retry")
        description: Human-readable description for logging
    """
    action: str
    text: Optional[str] = None
    id: Optional[str] = None
    desc: Optional[str] = None
    x: Optional[int] = None
    y: Optional[int] = None
    app: Optional[str] = None
    value: Optional[str] = None
    direction: Optional[str] = None
    timeout: float = 5.0
    min_confidence: float = 0.3
    retries: int = 2
    retry_delay: float = 1.0
    wait_before: float = 0.0
    wait_after: float = 0.3
    optional: bool = False
    condition: Optional[Callable[['Android'], bool]] = None
    on_failure: str = "stop"
    description: Optional[str] = None

    def __post_init__(self):
        """Validate step configuration."""
        valid_actions = {t.value for t in StepType}
        if self.action not in valid_actions:
            raise ValueError(f"Invalid action '{self.action}'. Valid: {valid_actions}")

        if self.on_failure not in ("stop", "continue", "retry"):
            raise ValueError(f"Invalid on_failure '{self.on_failure}'")

    def get_target_description(self) -> str:
        """Get human-readable description of target."""
        if self.description:
            return self.description

        parts = [self.action.upper()]

        if self.text:
            parts.append(f'text="{self.text}"')
        if self.id:
            parts.append(f'id="{self.id}"')
        if self.desc:
            parts.append(f'desc="{self.desc}"')
        if self.x is not None and self.y is not None:
            parts.append(f'@({self.x}, {self.y})')
        if self.app:
            parts.append(f'app="{self.app}"')
        if self.value:
            parts.append(f'value="{self.value[:20]}..."' if len(self.value or "") > 20 else f'value="{self.value}"')
        if self.direction:
            parts.append(f'direction={self.direction}')

        return " ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excludes callable)."""
        result = {}
        for key, val in asdict(self).items():
            if key == "condition":
                continue  # Skip callable
            if val is not None:
                result[key] = val
        return result


@dataclass
class AutomationResult:
    """Result of full automation run."""
    success: bool
    total_steps: int
    executed_steps: int
    failed_steps: int
    skipped_steps: int
    duration_ms: float
    step_results: List[StepResult] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "total_steps": self.total_steps,
            "executed_steps": self.executed_steps,
            "failed_steps": self.failed_steps,
            "skipped_steps": self.skipped_steps,
            "duration_ms": round(self.duration_ms, 2),
            "step_results": [r.to_dict() for r in self.step_results],
            "error": self.error,
        }

    def summary(self) -> str:
        """Get human-readable summary."""
        status = "SUCCESS" if self.success else "FAILED"
        lines = [
            f"Automation {status}",
            f"  Steps: {self.executed_steps}/{self.total_steps} executed",
            f"  Failed: {self.failed_steps}, Skipped: {self.skipped_steps}",
            f"  Duration: {self.duration_ms:.0f}ms",
        ]
        if self.error:
            lines.append(f"  Error: {self.error}")
        return "\n".join(lines)


class Automation:
    """
    Robust automation runner with retry logic and error handling.

    Features:
    - Automatic retries with configurable delay
    - Wait for elements with timeout
    - Conditional step execution
    - Detailed execution logging
    - Step-by-step result tracking

    Example:
        auto = Automation()
        result = auto.run([
            Step("open", app="clock"),
            Step("wait", timeout=2.0),
            Step("tap", text="Alarm", retries=3),
            Step("tap", desc="Add alarm"),
        ])

        if result.success:
            print("Automation completed!")
        else:
            print(f"Failed: {result.error}")
    """

    def __init__(
        self,
        device: Optional[str] = None,
        min_confidence: float = 0.3,
        default_timeout: float = 5.0,
        default_retries: int = 2,
        step_delay: float = 0.3,
        stop_on_failure: bool = True,
        screenshot_on_failure: bool = False,
    ):
        """
        Initialize automation runner.

        Args:
            device: Device serial (auto-detect if None)
            min_confidence: Default minimum confidence for element matching
            default_timeout: Default timeout for element search
            default_retries: Default retry count per step
            step_delay: Default delay between steps (seconds)
            stop_on_failure: Stop execution on first failure
            screenshot_on_failure: Take screenshot when step fails
        """
        self.android = Android(device=device, min_confidence=min_confidence)
        self.min_confidence = min_confidence
        self.default_timeout = default_timeout
        self.default_retries = default_retries
        self.step_delay = step_delay
        self.stop_on_failure = stop_on_failure
        self.screenshot_on_failure = screenshot_on_failure

        self._step_results: List[StepResult] = []
        self._current_step: int = 0

        logger.info(f"Automation initialized for device: {self.android.device}")

    def run(self, steps: List[Step]) -> AutomationResult:
        """
        Execute a list of automation steps.

        Args:
            steps: List of Step objects to execute

        Returns:
            AutomationResult with execution details
        """
        start_time = time.time()
        self._step_results = []
        self._current_step = 0

        executed = 0
        failed = 0
        skipped = 0
        error_msg = None

        logger.info(f"Starting automation with {len(steps)} steps")

        try:
            for i, step in enumerate(steps):
                self._current_step = i

                # Check condition
                if step.condition is not None:
                    try:
                        should_run = step.condition(self.android)
                        if not should_run:
                            result = StepResult(
                                step_index=i,
                                step_type=step.action,
                                status=StepStatus.SKIPPED,
                                message="Condition not met",
                            )
                            self._step_results.append(result)
                            skipped += 1
                            logger.debug(f"Step {i+1} skipped: condition not met")
                            continue
                    except Exception as e:
                        logger.warning(f"Step {i+1} condition check failed: {e}")

                # Execute step with retries
                result = self._execute_step(i, step)
                self._step_results.append(result)

                if result.status == StepStatus.SUCCESS:
                    executed += 1
                elif result.status == StepStatus.SKIPPED:
                    skipped += 1
                else:
                    failed += 1

                    if self.screenshot_on_failure:
                        try:
                            self.android.screenshot(f"failure_step_{i+1}.png")
                        except Exception:
                            pass

                    if step.on_failure == "stop" or (self.stop_on_failure and not step.optional):
                        error_msg = f"Step {i+1} failed: {result.error}"
                        logger.error(error_msg)
                        break

        except Exception as e:
            error_msg = f"Automation error: {str(e)}"
            logger.exception(error_msg)

        duration = (time.time() - start_time) * 1000
        success = failed == 0 and error_msg is None

        result = AutomationResult(
            success=success,
            total_steps=len(steps),
            executed_steps=executed,
            failed_steps=failed,
            skipped_steps=skipped,
            duration_ms=duration,
            step_results=self._step_results,
            error=error_msg,
        )

        logger.info(result.summary())
        return result

    def _execute_step(self, index: int, step: Step) -> StepResult:
        """Execute a single step with retry logic."""
        start_time = time.time()
        attempts = 0
        max_attempts = step.retries + 1
        last_error = None
        confidence = None

        # Wait before step
        if step.wait_before > 0:
            time.sleep(step.wait_before)

        while attempts < max_attempts:
            attempts += 1

            try:
                logger.debug(f"Step {index+1}/{self._current_step+1}: {step.get_target_description()} (attempt {attempts})")

                success, confidence = self._do_step(step)

                if success:
                    # Wait after step
                    if step.wait_after > 0:
                        time.sleep(step.wait_after)

                    duration = (time.time() - start_time) * 1000
                    return StepResult(
                        step_index=index,
                        step_type=step.action,
                        status=StepStatus.SUCCESS,
                        message=step.get_target_description(),
                        attempts=attempts,
                        duration_ms=duration,
                        confidence=confidence,
                    )
                else:
                    last_error = "Action returned False"

            except ElementNotFoundError as e:
                last_error = f"Element not found: {e.message}"
            except DittoMationError as e:
                last_error = e.message
            except Exception as e:
                last_error = str(e)

            # Retry logic
            if attempts < max_attempts:
                logger.warning(f"Step {index+1} attempt {attempts} failed: {last_error}. Retrying...")
                time.sleep(step.retry_delay)

        # All attempts failed
        duration = (time.time() - start_time) * 1000
        return StepResult(
            step_index=index,
            step_type=step.action,
            status=StepStatus.FAILED,
            message=step.get_target_description(),
            attempts=attempts,
            duration_ms=duration,
            confidence=confidence,
            error=last_error,
        )

    def _do_step(self, step: Step) -> tuple[bool, Optional[float]]:
        """
        Execute the actual step action.

        Returns:
            Tuple of (success, confidence_score)
        """
        action = step.action
        confidence = None

        if action == "tap":
            if step.x is not None and step.y is not None:
                return self.android.tap(step.x, step.y), None
            else:
                result = self.android.find_with_confidence(
                    text=step.text, id=step.id, desc=step.desc,
                    min_confidence=step.min_confidence
                )
                if result and result.confidence >= step.min_confidence:
                    success = self.android.tap(
                        step.text, id=step.id, desc=step.desc,
                        timeout=step.timeout, min_confidence=step.min_confidence
                    )
                    return success, result.confidence
                return False, result.confidence if result else 0.0

        elif action == "long_press":
            duration = int(step.timeout * 1000) if step.timeout > 1 else 1000
            if step.x is not None and step.y is not None:
                return self.android.long_press(step.x, step.y, duration_ms=duration), None
            else:
                return self.android.long_press(
                    step.text, id=step.id, desc=step.desc,
                    timeout=step.timeout, min_confidence=step.min_confidence
                ), None

        elif action == "swipe":
            direction = step.direction or "up"
            return self.android.swipe(direction), None

        elif action == "scroll":
            direction = step.direction or "down"
            return self.android.scroll(direction), None

        elif action == "type":
            if step.value:
                return self.android.type(step.value), None
            return False, None

        elif action == "press":
            key = step.value or "back"
            key_map = {
                "back": "press_back",
                "home": "press_home",
                "enter": "press_enter",
            }
            if key in key_map:
                return getattr(self.android, key_map[key])(), None
            else:
                return self.android.press_key(key), None

        elif action == "open":
            if step.app:
                return self.android.open_app(step.app), None
            return False, None

        elif action == "wait":
            time.sleep(step.timeout)
            return True, None

        elif action == "wait_for":
            result = self.android.wait_for_with_confidence(
                text=step.text, id=step.id, desc=step.desc,
                timeout=step.timeout, min_confidence=step.min_confidence
            )
            if result:
                return True, result.confidence
            return False, None

        elif action == "assert_exists":
            result = self.android.find_with_confidence(
                text=step.text, id=step.id, desc=step.desc,
                min_confidence=step.min_confidence
            )
            if result and result.confidence >= step.min_confidence:
                return True, result.confidence
            return False, result.confidence if result else 0.0

        elif action == "assert_not_exists":
            result = self.android.find_with_confidence(
                text=step.text, id=step.id, desc=step.desc,
                min_confidence=step.min_confidence
            )
            if result is None or result.confidence < step.min_confidence:
                return True, None
            return False, result.confidence

        elif action == "screenshot":
            filename = step.value or None
            try:
                self.android.screenshot(filename)
                return True, None
            except Exception:
                return False, None

        else:
            logger.warning(f"Unknown action: {action}")
            return False, None

    def run_from_file(self, filepath: Union[str, Path]) -> AutomationResult:
        """
        Load and run automation from JSON file.

        Args:
            filepath: Path to JSON file with steps

        Returns:
            AutomationResult
        """
        filepath = Path(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        steps_data = data.get("steps", data) if isinstance(data, dict) else data
        steps = [Step(**s) for s in steps_data]

        return self.run(steps)

    def save_result(self, result: AutomationResult, filepath: Union[str, Path]) -> None:
        """Save automation result to JSON file."""
        filepath = Path(filepath)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2)

        logger.info(f"Result saved to {filepath}")


# Convenience functions for simple usage
def run_steps(steps: List[Step], **kwargs) -> AutomationResult:
    """Run automation steps with default settings."""
    auto = Automation(**kwargs)
    return auto.run(steps)


def tap(text: Optional[str] = None, **kwargs) -> Step:
    """Create a tap step."""
    return Step(action="tap", text=text, **kwargs)


def wait(seconds: float) -> Step:
    """Create a wait step."""
    return Step(action="wait", timeout=seconds)


def wait_for(text: Optional[str] = None, timeout: float = 10.0, **kwargs) -> Step:
    """Create a wait_for step."""
    return Step(action="wait_for", text=text, timeout=timeout, **kwargs)


def type_text(value: str, **kwargs) -> Step:
    """Create a type step."""
    return Step(action="type", value=value, **kwargs)


def swipe(direction: str, **kwargs) -> Step:
    """Create a swipe step."""
    return Step(action="swipe", direction=direction, **kwargs)


def open_app(name: str, **kwargs) -> Step:
    """Create an open app step."""
    return Step(action="open", app=name, **kwargs)


def press(key: str, **kwargs) -> Step:
    """Create a press key step."""
    return Step(action="press", value=key, **kwargs)
