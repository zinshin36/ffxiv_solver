import datetime

_log_widget = None


def init_logger(widget=None):
    """
    Optional: attach a Tkinter text widget to display logs
    """
    global _log_widget
    _log_widget = widget


def log(message):

    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {message}"

    print(line)

    if _log_widget:
        try:
            _log_widget.insert("end", line + "\n")
            _log_widget.see("end")
        except:
            pass
