"""
DittoMation Recorder Module.

This module provides recording functionality for capturing Android interactions:
- Interactive step-by-step recording
- Automated touch event recording via getevent
- Gesture classification (tap, swipe, long press, etc.)
- UI hierarchy capture and element matching
- Workflow storage and management

Usage:
    from recorder import InteractiveRecorder, WorkflowRecorder

    # Interactive recording
    recorder = InteractiveRecorder()
    recorder.start_recording("my_workflow.json")

    # Programmatic workflow recording
    workflow = WorkflowRecorder()
    workflow.add_step(...)
    workflow.save("my_workflow.json")
"""

from .interactive_recorder import InteractiveRecorder
from .workflow import WorkflowStep, WorkflowRecorder
from .gesture_classifier import TouchPoint, TouchTrack, Gesture, GestureClassifier
from .event_listener import TouchEvent, TouchEventListener, MultiTouchState
from .element_matcher import MatchResult
from .main import RecordingSession

__all__ = [
    # Main recording classes
    "InteractiveRecorder",
    "RecordingSession",

    # Workflow management
    "WorkflowStep",
    "WorkflowRecorder",

    # Gesture classification
    "TouchPoint",
    "TouchTrack",
    "Gesture",
    "GestureClassifier",

    # Event handling
    "TouchEvent",
    "TouchEventListener",
    "MultiTouchState",

    # Element matching
    "MatchResult",
]
