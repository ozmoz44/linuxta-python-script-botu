import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_FILE = "/home/umut/bsm/logs/changes.json"
WATCH_DIRECTORY = "/home/umut/bsm/test"

class Watcher(FileSystemEventHandler):
    def on_any_event(self, event):
        log_entry = {
            "action": event.event_type,
            "path": event.src_path,
            "is_directory": event.is_directory,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        try:
            with open(LOG_FILE, "r") as log_file:
                logs = json.load(log_file)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        logs.append(log_entry)

        with open(LOG_FILE, "w") as log_file:
            json.dump(logs, log_file, indent=4)  # Düzenlenmiş şekilde kaydet

if __name__ == "__main__":
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
