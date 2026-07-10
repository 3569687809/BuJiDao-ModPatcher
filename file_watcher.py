# ============================================================
# PlatformPatcher
#
# 文件监听模块（基于 watchdog）
#
# 功能：
# 1. 监听 packcache 目录下的 HudAddonScript.mcp 文件变化
# 2. 当检测到新文件时，通过回调通知 monitor
#
# ============================================================

import os
import threading
import queue

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from file_detector import SEARCH_FOLDER, TARGET_FILE, get_folder_id
from logger import info, error as log_error


class HudFileHandler(FileSystemEventHandler):
    """
    watchdog 事件处理器

    """

    def __init__(self, event_queue: queue.Queue, old_folder_id: str):
        super().__init__()
        self.event_queue = event_queue
        self.old_folder_id = old_folder_id

    def _is_target_file(self, path: str) -> bool:
        
        return os.path.basename(path) == TARGET_FILE

    def _check_and_notify(self, path: str):
        
        if not self._is_target_file(path):
            return

        current_id = get_folder_id(path)

        
        if current_id != self.old_folder_id:
            info(f"[FileWatcher] 检测到新文件: {path} (ID: {current_id})")
            self.event_queue.put({
                "type": "new_file",
                "path": path,
                "folder_id": current_id
            })

    def on_created(self, event):
        
        if not event.is_directory:
            self._check_and_notify(event.src_path)

    def on_modified(self, event):
        
        if not event.is_directory:
            self._check_and_notify(event.src_path)


class PackcacheWatcher:
    

    def __init__(self, old_folder_id: str):
        self.observer = None
        self.handler = None
        self.event_queue = queue.Queue()
        self.old_folder_id = old_folder_id
        self._lock = threading.Lock()

    def start(self) -> bool:
        
        with self._lock:
            if self.observer and self.observer.is_alive():
                return True

            if not os.path.exists(SEARCH_FOLDER):
                log_error(f"[FileWatcher] 监听目录不存在: {SEARCH_FOLDER}")
                return False

            
            self.handler = HudFileHandler(self.event_queue, self.old_folder_id)
            self.observer = Observer()
            
            self.observer.schedule(self.handler, SEARCH_FOLDER, recursive=True)
            self.observer.start()

            info(f"[FileWatcher] 已开始监听: {SEARCH_FOLDER}")
            return True

    def stop(self):
        
        with self._lock:
            if self.observer:
                self.observer.stop()
                self.observer.join(timeout=5)
                self.observer = None
                info("[FileWatcher] 已停止监听")

    def get_new_file_event(self, timeout: float = 0) -> dict | None:
        
        try:
            return self.event_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def update_old_folder_id(self, new_id: str):
        
        self.old_folder_id = new_id
        if self.handler:
            self.handler.old_folder_id = new_id
        info(f"[FileWatcher] 已更新旧文件ID: {new_id}")

    def clear_queue(self):
        
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break