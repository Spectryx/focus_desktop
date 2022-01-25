import win32gui
import re
import configparser
from pathlib import Path

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

if __name__ == "__main__":
    cur_path = Path(__file__).parent.absolute()
    config_file_path = cur_path.joinpath("config.ini")

    if not config_file_path.is_file():
        raise FileNotFoundError(config_file_path)

    config = configparser.ConfigParser()
    config.read(config_file_path)

    window_name = config["main"]["window_name"]
    w = WindowMgr()
    w.find_window_wildcard(f".*{window_name}.*")
    w.set_foreground()