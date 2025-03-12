import sys
import os
import time
import logging
import ctypes
from datetime import datetime, timedelta
from collections import defaultdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Windows drive detection
if os.name == 'nt':
    import win32api

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('filesystem_monitor.log'),
        logging.StreamHandler(),
    ]
)

class FullSystemMonitor:
    def __init__(self):
        self.observers = []
        
        # Exclusion settings
        self.excluded_dirs = {
            'temp', 'tmp', 'cache', 'cookies', 'appdata',
            'windows\\temp', 'local\\temp', '$recycle.bin',
            'webcache', 'inetcache', 'chromium', 'spotlight-v100',
            'volumes', '.trashes', '.spotlight-v100'
        }
        self.excluded_extensions = {
            '.tmp', '.cache', '.cookie', '.log', '.dmp',
            '.bak', '.swp', '.crswap', '.journal', '.partial'
        }

    def get_all_drives(self):
        """Get list of all available drives"""
        drives = []
        if os.name == 'nt':
            drives = [d for d in win32api.GetLogicalDriveStrings().split('\x00') if d]
        else:
            drives = ['/']
            if os.path.exists('/Volumes'):
                drives += [os.path.join('/Volumes', d) for d in os.listdir('/Volumes')]
            if os.path.exists('/mnt'):
                drives += [os.path.join('/mnt', d) for d in os.listdir('/mnt')]
        return [d for d in drives if os.path.exists(d)]

    def is_excluded(self, path):
        """Check if path should be ignored"""
        path_lower = path.lower()
        
        # Check directory components
        path_parts = set(os.path.normpath(path_lower).split(os.sep))
        if any(excl in path_parts for excl in self.excluded_dirs):
            return True
            
        # Check file extensions
        if any(path_lower.endswith(ext) for ext in self.excluded_extensions):
            return True
            
        # Ignore hidden/system files
        if os.path.basename(path).startswith(('.', '$')):
            return True
            
        return False

class DriveWatcher(FileSystemEventHandler):
    def __init__(self, monitor):
        self.monitor = monitor
        self.last_events = defaultdict(lambda: datetime.min)
        self.cooldown = timedelta(seconds=15)

    def process_event(self, event, action):
        if event.is_directory:
            return

        path = os.path.abspath(event.src_path)
        if self.monitor.is_excluded(path):
            return

        now = datetime.now()
        if now - self.last_events[path] < self.cooldown:
            return

        logging.warning(f"FILE {action}: {path}")
        self.last_events[path] = now

    def on_modified(self, event):
        self.process_event(event, "MODIFIED")

    def on_created(self, event):
        self.process_event(event, "CREATED")

    def on_deleted(self, event):
        self.process_event(event, "DELETED")

    def on_moved(self, event):
        self.process_event(event, "MOVED")

def check_privileges():
    """Verify admin/root privileges"""
    if os.name == 'nt':
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            logging.error("Requires Administrator privileges")
            return False
    else:
        if os.geteuid() != 0:
            logging.error("Requires root privileges")
            return False
    return True

def start_monitoring():
    if not check_privileges():
        sys.exit(1)

    monitor = FullSystemMonitor()
    drives = monitor.get_all_drives()

    try:
        logging.info("Starting filesystem monitoring on: %s", drives)
        for drive in drives:
            handler = DriveWatcher(monitor)
            observer = Observer()
            observer.schedule(handler, drive, recursive=True)
            observer.start()
            monitor.observers.append(observer)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Stopping monitoring...")
        for observer in monitor.observers:
            observer.stop()
        for observer in monitor.observers:
            observer.join()

if __name__ == "__main__":
    start_monitoring()
