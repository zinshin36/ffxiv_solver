import datetime
import os

_log_widget = None
_log_file = None


def init_logger(widget=None):
    global _log_widget, _log_file

    _log_widget = widget

    os.makedirs("logs", exist_ok=True)

    filename = datetime.datetime.now().strftime("logs/log_%Y%m%d_%H%M%S.txt")

    _log_file = open(filename, "w", encoding="utf-8")


def set_widget(widget):
    global _log_widget
    _log_widget = widget


def log(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {message}"

    print(line)

    if _log_file:
        _log_file.write(line + "\n")
        _log_file.flush()

    if _log_widget:
        try:
            _log_widget.insert("end", line + "\n")
            _log_widget.see("end")
        except Exception:
            pass
