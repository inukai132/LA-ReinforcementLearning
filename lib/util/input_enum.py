from enum import IntEnum

class PYBOY_INPUT(IntEnum):
  (
    QUIT,
    PRESS_ARROW_UP,
    PRESS_ARROW_DOWN,
    PRESS_ARROW_RIGHT,
    PRESS_ARROW_LEFT,
    PRESS_BUTTON_A,
    PRESS_BUTTON_B,
    PRESS_BUTTON_SELECT,
    PRESS_BUTTON_START,
    RELEASE_ARROW_UP,
    RELEASE_ARROW_DOWN,
    RELEASE_ARROW_RIGHT,
    RELEASE_ARROW_LEFT,
    RELEASE_BUTTON_A,
    RELEASE_BUTTON_B,
    RELEASE_BUTTON_SELECT,
    RELEASE_BUTTON_START,
    _INTERNAL_TOGGLE_DEBUG,
    PRESS_SPEED_UP,
    RELEASE_SPEED_UP,
    STATE_SAVE,
    STATE_LOAD,
    PASS,
    SCREEN_RECORDING_TOGGLE,
    PAUSE,
    UNPAUSE,
    PAUSE_TOGGLE,
    PRESS_REWIND_BACK,
    PRESS_REWIND_FORWARD,
    RELEASE_REWIND_BACK,
    RELEASE_REWIND_FORWARD,
    WINDOW_FOCUS,
    WINDOW_UNFOCUS,
    _INTERNAL_RENDERER_FLUSH,
    _INTERNAL_MOUSE,
    _INTERNAL_MARK_TILE,
    SCREENSHOT_RECORD,
    DEBUG_MEMORY_SCROLL_DOWN,
    DEBUG_MEMORY_SCROLL_UP,
    MOD_SHIFT_ON,
    MOD_SHIFT_OFF,
    FULL_SCREEN_TOGGLE,
  ) = range(42)