import os

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "system.log")

def get_all_logs():
    """
    Reads all logs from the system.log file and returns as a list of lines.
    If the file doesn't exist, returns an empty list.
    """
    if not os.path.exists(LOG_FILE_PATH):
        return []

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        logs = f.readlines()
    return [line.strip() for line in logs]