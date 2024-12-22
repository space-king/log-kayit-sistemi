import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Log dosyasının yolu
LOG_FILE_PATH = "/home/ahmetu/bsm/logs/changes.json"

# Event Handler sınıfı
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.record_change("Modified", event.src_path)

    def on_created(self, event):
        self.record_change("Created", event.src_path)

    def on_deleted(self, event):
        self.record_change("Deleted", event.src_path)

    def record_change(self, action, path):
        # Zaman damgası
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # JSON formatında log kaydı
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "path": path
        }

        # Log dosyasına yazma
        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_entry)

        with open(LOG_FILE_PATH, "w") as f:
            json.dump(logs, f, indent=4)

# Dizini takip etme
def monitor_directory(path):
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            pass  # Sonsuz döngü ile sürekli çalışmasını sağlıyoruz
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# İzlemek istediğimiz dizin
monitor_directory("/home/ahmetu/bsm/test")
