import sys
import os
import time
import requests # <-- 添加 requests
import mimetypes # <-- 用于猜测文件名
from urllib.parse import urlparse, unquote # <-- 添加 urllib.parse
from PySide6.QtCore import QUrl, QStandardPaths, Qt, QTimer, Slot
from PySide6.QtWidgets import (
    QWidget, QToolBar, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout,
    QFileDialog, QMessageBox, QDialog, QListWidget, QListWidgetItem,
    QDialogButtonBox, QLabel, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QSizePolicy, QStatusBar, QApplication # <-- 添加 QApplication
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PySide6.QtGui import QIcon, QAction


# --- 自定义 WebEnginePage 以拦截下载 ---
class CustomWebEnginePage(QWebEnginePage):
    # 定义常见可下载文件扩展名 (小写)
    DOWNLOADABLE_EXTENSIONS = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.pdf',
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.doc', '.docx',
        '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv', '.json', '.xml',
        '.mp3', '.wav', '.ogg', '.mp4', '.avi', '.mkv', '.mov', '.wmv',
        '.exe', '.msi', '.dmg', '.iso', '.deb', '.rpm'
    }

    def __init__(self, profile, view, parent=None): # <-- 添加 view 参数
        super().__init__(profile, parent)
        self._view = view # <-- 保存 view 引用

    def view(self): # <-- 添加一个方法来获取 view
        return self._view

    def acceptNavigationRequest(self, url: QUrl, type: QWebEnginePage.NavigationType, isMainFrame: bool) -> bool:
        """拦截导航请求，检查是否为文件下载"""
        print(f"DEBUG: acceptNavigationRequest - URL: {url.toString()}, Type: {type}, isMainFrame: {isMainFrame}")
        if type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked and isMainFrame:
            path = urlparse(url.toString()).path
            filename, ext = os.path.splitext(path)
            if ext.lower() in self.DOWNLOADABLE_EXTENSIONS:
                print(f"DEBUG: Detected downloadable extension '{ext}'. Triggering manual download.")
                # 异步触发下载，避免阻塞 UI 线程太久 (虽然 requests 仍然会阻塞)
                # A better approach would use QNetworkAccessManager or run requests in a thread
                QTimer.singleShot(0, lambda: self._trigger_manual_download(url))
                return False # 阻止默认导航 (直接显示文件)

        # 允许其他所有导航请求
        return super().acceptNavigationRequest(url, type, isMainFrame)

    @Slot(QUrl)
    def _trigger_manual_download(self, url: QUrl):
        """使用 requests 手动下载文件"""
        url_str = url.toString()
        try:
            # 尝试从 URL 获取建议的文件名
            parsed_url = urlparse(url_str)
            suggested_filename = os.path.basename(unquote(parsed_url.path))
            if not suggested_filename: # 如果路径为空或只有'/'
                 suggested_filename = "download" # 默认文件名

            # 弹出保存文件对话框
            # 使用 self.view() 获取关联的 QWebEngineView 作为父窗口
            parent_widget = self.view() # <-- 直接使用 self.view()
            if not parent_widget: # Fallback if view is somehow None
                parent_widget = QApplication.activeWindow()

            save_path, _ = QFileDialog.getSaveFileName(
                parent_widget, "保存文件", os.path.join(QStandardPaths.writableLocation(QStandardPaths.DownloadLocation), suggested_filename)
            )

            if not save_path:
                print("DEBUG: Manual download cancelled by user.")
                return

            # 显示下载提示 (可以改进为更复杂的进度条)
            QMessageBox.information(parent_widget, "下载", f"正在下载: {os.path.basename(save_path)}\n从: {url_str[:80]}...")

            # 使用 requests 下载文件 (stream=True 用于大文件)
            with requests.get(url_str, stream=True, timeout=30) as r: # 添加超时
                r.raise_for_status() # 如果请求失败 (4xx or 5xx), 抛出异常
                total_size = int(r.headers.get('content-length', 0))
                bytes_downloaded = 0
                # 创建进度对话框或更新状态栏 (简化版，只在完成/失败时提示)

                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        bytes_downloaded += len(chunk)
                        # 这里可以添加更新进度的代码

            QMessageBox.information(parent_widget, "下载完成", f"文件已保存到:\n{save_path}")
            print(f"DEBUG: File downloaded successfully to {save_path}")

        except requests.exceptions.RequestException as e:
            print(f"ERROR: Manual download failed: {e}")
            QMessageBox.warning(parent_widget, "下载失败", f"无法下载文件: {e}")
        except IOError as e:
             print(f"ERROR: Could not write file: {e}")
             QMessageBox.warning(parent_widget, "保存失败", f"无法写入文件: {e}")
        except Exception as e:
             print(f"ERROR: Unexpected error during manual download: {e}")
             QMessageBox.warning(parent_widget, "下载错误", f"发生意外错误: {e}")


class DownloadManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("下载管理器")
        self.setMinimumSize(600, 400)

        self.downloads = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 下载列表表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "文件名", "状态", "进度", "速度", "剩余时间", "操作"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.pause_btn = QPushButton("暂停")
        self.resume_btn = QPushButton("继续")
        self.cancel_btn = QPushButton("取消")
        self.open_btn = QPushButton("打开文件")
        self.clear_btn = QPushButton("清除已完成")

        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.resume_btn)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.open_btn)
        btn_layout.addWidget(self.clear_btn)

        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # 连接信号
        self.pause_btn.clicked.connect(self.pause_selected)
        self.resume_btn.clicked.connect(self.resume_selected)
        self.cancel_btn.clicked.connect(self.cancel_selected)
        self.open_btn.clicked.connect(self.open_selected)
        self.clear_btn.clicked.connect(self.clear_completed)

    def add_download(self, download):
        """添加新的下载任务"""
        row = self.table.rowCount()
        self.table.insertRow(row)

        # 文件名
        name_item = QTableWidgetItem(download.downloadFileName())
        name_item.setData(Qt.UserRole, download) # Store download object

        # 状态
        status_item = QTableWidgetItem("下载中")

        # 进度条
        progress = QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(0) # Start at 0

        # 速度
        speed_item = QTableWidgetItem("0 KB/s")

        # 剩余时间
        time_item = QTableWidgetItem("--")

        # 操作按钮 (Initially Pause)
        btn_widget = QWidget()
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)

        pause_btn = QPushButton("暂停")
        pause_btn.clicked.connect(lambda: self.pause_download(download))

        btn_layout.addWidget(pause_btn)
        btn_widget.setLayout(btn_layout)

        self.table.setItem(row, 0, name_item)
        self.table.setItem(row, 1, status_item)
        self.table.setCellWidget(row, 2, progress)
        self.table.setItem(row, 3, speed_item)
        self.table.setItem(row, 4, time_item)
        self.table.setCellWidget(row, 5, btn_widget)

        self.downloads.append({
            "download": download,
            "row": row,
            "start_time": time.time(),
            "last_bytes": 0,
            "last_time": time.time()
        })

        # Connect signals for this specific download
        download.receivedBytesChanged.connect(
            lambda: self.update_progress(download)
        )
        download.stateChanged.connect(
            lambda state: self.update_state(download, state)
        )

    def find_download_item(self, download):
        """Find the download item and row index."""
        for item_data in self.downloads:
            if item_data["download"] == download:
                return item_data, item_data["row"]
        return None, -1

    def update_progress(self, download):
        """更新下载进度"""
        item_data, row = self.find_download_item(download)
        if row == -1:
            return

        bytesReceived = download.receivedBytes()
        bytesTotal = download.totalBytes()

        # 计算下载速度
        current_time = time.time()
        elapsed = current_time - item_data["last_time"]
        if elapsed >= 0.5: # Update speed every 0.5 seconds
            speed = (bytesReceived - item_data["last_bytes"]) / elapsed / 1024  # KB/s
            self.table.item(row, 3).setText(f"{speed:.1f} KB/s")

            # 计算剩余时间
            if bytesTotal > 0 and speed > 0:
                remaining = (bytesTotal - bytesReceived) / (speed * 1024)
                mins = int(remaining // 60)
                secs = int(remaining % 60)
                self.table.item(row, 4).setText(f"{mins}:{secs:02d}")
            else:
                 self.table.item(row, 4).setText("--")

            item_data["last_bytes"] = bytesReceived
            item_data["last_time"] = current_time

        # 更新进度条
        progress_widget = self.table.cellWidget(row, 2)
        if isinstance(progress_widget, QProgressBar):
            if bytesTotal > 0:
                percent = int(bytesReceived * 100 / bytesTotal)
                progress_widget.setValue(percent)
            else:
                # Indeterminate progress if total size is unknown
                progress_widget.setRange(0, 0)


    def update_state(self, download, state):
        """Update download state and controls."""
        item_data, row = self.find_download_item(download)
        if row == -1:
            return

        status_item = self.table.item(row, 1)
        action_widget = self.table.cellWidget(row, 5)
        action_layout = action_widget.layout()

        # Clear existing buttons in action layout
        while action_layout.count():
            child = action_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if state == QWebEngineDownloadRequest.DownloadInProgress:
            status_item.setText("下载中")
            pause_btn = QPushButton("暂停")
            pause_btn.clicked.connect(lambda: self.pause_download(download))
            cancel_btn = QPushButton("取消")
            cancel_btn.clicked.connect(lambda: self.cancel_download(download))
            action_layout.addWidget(pause_btn)
            action_layout.addWidget(cancel_btn)
        elif state == QWebEngineDownloadRequest.DownloadCompleted:
            status_item.setText("已完成")
            # Ensure progress bar shows 100%
            progress_widget = self.table.cellWidget(row, 2)
            if isinstance(progress_widget, QProgressBar):
                 progress_widget.setRange(0, 100)
                 progress_widget.setValue(100)
            self.table.item(row, 3).setText("-") # Clear speed
            self.table.item(row, 4).setText("-") # Clear time
            open_btn = QPushButton("打开")
            open_btn.clicked.connect(lambda: self.open_file(download))
            action_layout.addWidget(open_btn)
        elif state == QWebEngineDownloadRequest.DownloadCancelled:
            status_item.setText("已取消")
            self.remove_download_row(download) # Remove directly
        elif state == QWebEngineDownloadRequest.DownloadInterrupted:
            status_item.setText(f"已中断 ({self.get_download_error(download.interruptReason())})")
            retry_btn = QPushButton("重试")
            # retry_btn.clicked.connect(lambda: self.retry_download(download)) # Retry logic needed
            cancel_btn = QPushButton("取消")
            cancel_btn.clicked.connect(lambda: self.cancel_download(download))
            # action_layout.addWidget(retry_btn)
            action_layout.addWidget(cancel_btn)
        elif state == QWebEngineDownloadRequest.DownloadPaused:
             status_item.setText("已暂停")
             resume_btn = QPushButton("继续")
             resume_btn.clicked.connect(lambda: self.resume_download(download))
             cancel_btn = QPushButton("取消")
             cancel_btn.clicked.connect(lambda: self.cancel_download(download))
             action_layout.addWidget(resume_btn)
             action_layout.addWidget(cancel_btn)


    def pause_download(self, download):
        """暂停下载"""
        download.pause()

    def resume_download(self, download):
        """继续下载"""
        download.resume()

    def cancel_download(self, download):
        """取消下载"""
        download.cancel()
        # State change handler will remove the row

    def open_file(self, download):
        """打开下载的文件"""
        # Use download.path() which includes directory and filename
        file_path = download.path()
        if os.path.exists(file_path):
            try:
                # Use os.startfile on Windows
                if sys.platform == "win32":
                    os.startfile(file_path)
                # Use open on macOS
                elif sys.platform == "darwin":
                    subprocess.call(["open", file_path])
                # Use xdg-open on Linux
                else:
                    subprocess.call(["xdg-open", file_path])
            except Exception as e:
                 QMessageBox.warning(self, "打开失败", f"无法打开文件: {e}")
        else:
            QMessageBox.warning(self, "文件未找到", f"文件不存在: {file_path}")

    def remove_download_row(self, download):
        """从列表中移除下载行"""
        item_data, row = self.find_download_item(download)
        if row != -1:
            self.table.removeRow(row)
            # Check if item_data is still in the list before removing
            if item_data in self.downloads:
                self.downloads.remove(item_data)
            # Update subsequent row indices
            for i in range(len(self.downloads)):
                if self.downloads[i]["row"] > row:
                    self.downloads[i]["row"] -= 1


    def get_selected_download(self):
        """Get the download object from the selected row."""
        selected_rows = list(set(item.row() for item in self.table.selectedItems()))
        if len(selected_rows) == 1:
            row = selected_rows[0]
            name_item = self.table.item(row, 0)
            if name_item:
                return name_item.data(Qt.UserRole)
        return None

    def pause_selected(self):
        """暂停选中的下载"""
        download = self.get_selected_download()
        if download and download.state() == QWebEngineDownloadRequest.DownloadInProgress:
            self.pause_download(download)

    def resume_selected(self):
        """继续选中的下载"""
        download = self.get_selected_download()
        if download and download.state() == QWebEngineDownloadRequest.DownloadPaused:
            self.resume_download(download)

    def cancel_selected(self):
        """取消选中的下载"""
        download = self.get_selected_download()
        if download and download.state() not in [QWebEngineDownloadRequest.DownloadCompleted, QWebEngineDownloadRequest.DownloadCancelled]:
             self.cancel_download(download)

    def open_selected(self):
        """打开选中的文件"""
        download = self.get_selected_download()
        if download and download.state() == QWebEngineDownloadRequest.DownloadCompleted:
            self.open_file(download)

    def clear_completed(self):
        """清除已完成的下载"""
        to_remove = []
        # Iterate safely over a copy if modifying the list during iteration
        for item_data in list(self.downloads):
            download = item_data["download"]
            if download.state() == QWebEngineDownloadRequest.DownloadCompleted:
                to_remove.append(download)

        for download in to_remove:
            self.remove_download_row(download)

    def get_download_error(self, reason):
        # Use QWebEngineDownloadRequest.InterruptReason enum directly
        errors = {
            QWebEngineDownloadRequest.InterruptReason.NoReason: "无原因",
            QWebEngineDownloadRequest.InterruptReason.FileError: "文件错误",
            QWebEngineDownloadRequest.InterruptReason.FileAccessDenied: "文件访问被拒绝",
            QWebEngineDownloadRequest.InterruptReason.FileNoSpace: "磁盘空间不足",
            QWebEngineDownloadRequest.InterruptReason.FileNameTooLong: "文件名太长",
            QWebEngineDownloadRequest.InterruptReason.FileTooLarge: "文件太大",
            QWebEngineDownloadRequest.InterruptReason.FileVirusInfected: "文件可能包含病毒",
            QWebEngineDownloadRequest.InterruptReason.FileTemporaryError: "临时文件错误",
            QWebEngineDownloadRequest.InterruptReason.FileBlocked: "文件被阻止",
            QWebEngineDownloadRequest.InterruptReason.FileSecurityCheckFailed: "安全检查失败",
            QWebEngineDownloadRequest.InterruptReason.FileTooShort: "文件太短",
            QWebEngineDownloadRequest.InterruptReason.FileHashMismatch: "文件哈希不匹配",
            QWebEngineDownloadRequest.InterruptReason.NetworkError: "网络错误",
            QWebEngineDownloadRequest.InterruptReason.NetworkTimeoutError: "网络超时",
            QWebEngineDownloadRequest.InterruptReason.NetworkConnectionRefusedError: "网络连接被拒绝",
            QWebEngineDownloadRequest.InterruptReason.NetworkConnectionClosedError: "网络连接已关闭",
            QWebEngineDownloadRequest.InterruptReason.NetworkServerConnectionClosedError: "服务器连接已关闭",
            QWebEngineDownloadRequest.InterruptReason.NetworkInvalidRequestError: "无效的网络请求",
            QWebEngineDownloadRequest.InterruptReason.ServerError: "服务器错误",
            QWebEngineDownloadRequest.InterruptReason.ClientError: "客户端错误",
            QWebEngineDownloadRequest.InterruptReason.DownloadCancelledByUser: "用户取消",
            QWebEngineDownloadRequest.InterruptReason.DownloadInterrupted: "下载中断 (未知原因)"
        }
        return errors.get(reason, "未知错误")


class IntegratedBrowser(QWidget):
    def __init__(self, parent=None, start_url="https://www.google.com"):
        super().__init__(parent)
        self.windows = [] # To keep track of detached windows if needed later

        # 使用独立的 Profile，避免与应用中其他可能的 WebEngine 实例冲突
        # Use a persistent profile if you want cache, cookies etc. saved
        # self.profile = QWebEngineProfile("my_unique_profile", self)
        self.profile = QWebEngineProfile(self) # Non-persistent for now

        # --- Enable relevant settings ---
        settings = self.profile.settings()
        try:
            # Standard Qt6/PySide6 way
            settings.setAttribute(QWebEngineSettings.WebAttribute.DeveloperExtrasEnabled, True)
            print("DEBUG: DeveloperExtrasEnabled set using WebAttribute.")
            settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
            print("DEBUG: FullScreenSupportEnabled set using WebAttribute.")
        except AttributeError as e:
            print(f"WARNING: Could not set standard WebAttributes: {e}. Trying WebSettingsAttribute fallback...")
            try:
                # Fallback using WebSettingsAttribute (less common for Qt6)
                if 'DeveloperExtrasEnabled' not in str(e): # Only try if the first one failed for this specific attribute
                    settings.setAttribute(QWebEngineSettings.WebSettingsAttribute.DeveloperExtrasEnabled, True)
                    print("DEBUG: DeveloperExtrasEnabled set using WebSettingsAttribute.")
                if 'FullScreenSupportEnabled' not in str(e): # Only try if the first one failed for this specific attribute
                    settings.setAttribute(QWebEngineSettings.WebSettingsAttribute.FullScreenSupportEnabled, True)
                    print("DEBUG: FullScreenSupportEnabled set using WebSettingsAttribute.")
            except AttributeError as e2:
                 # Give a more specific warning if fallbacks also fail
                 print(f"WARNING: Fallback using WebSettingsAttribute also failed: {e2}. DevTools or Fullscreen might be unavailable.")


        # --- Tab Widget Setup ---
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.current_tab_changed)
        # Allow tabs to expand
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        # --- Navigation Bar ---
        self.url_bar = QLineEdit()
        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.reload_btn = QPushButton("↻")
        self.download_manager_btn = QPushButton("下载")

        # 布局设置
        nav_bar = QHBoxLayout()
        nav_bar.addWidget(self.back_btn)
        nav_bar.addWidget(self.forward_btn)
        nav_bar.addWidget(self.reload_btn)
        nav_bar.addWidget(self.url_bar)
        nav_bar.addWidget(self.download_manager_btn)
        nav_bar.setContentsMargins(0, 0, 0, 0) # Remove margins for tighter look

        layout = QVBoxLayout()
        layout.addLayout(nav_bar)
        layout.addWidget(self.tab_widget) # Add TabWidget instead of single webview
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        # --- Signal Connections ---
        self.back_btn.clicked.connect(self.go_back)
        self.forward_btn.clicked.connect(self.go_forward)
        self.reload_btn.clicked.connect(self.reload_page)
        self.url_bar.returnPressed.connect(self.navigate_current_tab_from_bar)
        self.download_manager_btn.clicked.connect(self.show_download_manager)

        # --- Download Handling ---
        self.download_manager = None
        # Ensure the connection is made correctly
        print("DEBUG: Connecting downloadRequested signal...")
        self.profile.downloadRequested.connect(self.handle_download)
        # Removed problematic isSignalConnected check


        # --- Initial Tab ---
        self.open_url_in_new_tab(start_url) # Open the first tab
        # Initial state update will be handled by current_tab_changed

    # --- Helper to get current view ---
    def current_webview(self) -> QWebEngineView | None:
        """Returns the QWebEngineView of the currently selected tab."""
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            widget = self.tab_widget.widget(current_index)
            if isinstance(widget, QWebEngineView):
                return widget
        return None


    # --- Add context menu for DevTools ---
    def contextMenuEvent(self, event):
        """Override context menu to add Inspect Element."""
        webview = self.current_webview()
        if webview:
            menu = webview.page().createStandardContextMenu()
            # Add Inspect Element action
            inspect_action = QAction("检查元素 (Inspect)", self)
            inspect_action.triggered.connect(lambda: webview.page().triggerAction(QWebEnginePage.WebAction.InspectElement))
            menu.addAction(inspect_action)
            menu.popup(event.globalPos())
        else:
            super().contextMenuEvent(event) # Default context menu if not on a webview

    # --- URL Handling ---
    def _prepare_qurl(self, url_string: str) -> QUrl:
        """Prepares a QUrl from a string, adding scheme if necessary."""
        url = QUrl(url_string)
        if not url.scheme(): # If no scheme (http, https, file), try adding https
            url.setScheme("https")
            # Basic check if it looks like a domain or IP after adding scheme
            if not url.isValid() or '.' not in url.host():
                 # If still not valid or doesn't look like a domain, try http
                 url = QUrl(url_string)
                 url.setScheme("http")

        # If still invalid after trying schemes, return potentially invalid QUrl
        # or a default like about:blank
        if not url.isValid():
             print(f"Warning: Could not create valid QUrl from '{url_string}'. Loading about:blank.")
             return QUrl("about:blank")
        return url

    # --- Public method to open URL ---
    def open_url_in_new_tab(self, url_string: str):
        """Creates a new tab and loads the given URL string."""
        webview = QWebEngineView(self) # <-- 先创建 View
        page = CustomWebEnginePage(self.profile, webview, self) # <-- 将 webview 传递给 Page
        webview.setPage(page) # <-- 设置自定义 Page
        webview.setAttribute(Qt.WA_DeleteOnClose) # Ensure it's deleted when tab is closed

        # Connect signals for the new webview (connected to the view, not the page directly for these)
        webview.urlChanged.connect(self.update_url_bar) # <--- Corrected method name
        webview.loadFinished.connect(self.on_load_finished)
        webview.loadStarted.connect(self.on_load_started)
        webview.titleChanged.connect(self.on_title_changed)
        webview.page().linkHovered.connect(self.on_link_hovered) # Optional: show link in status bar

        # Handle new window requests (e.g., target="_blank") - page's createWindow needs setting
        page.createWindow = self._handle_create_window # <-- Set on the custom page instance

        qurl = self._prepare_qurl(url_string)
        webview.load(qurl)

        # Add the new webview as a tab
        index = self.tab_widget.addTab(webview, "加载中...")
        self.tab_widget.setCurrentIndex(index) # Make the new tab active

        # Initial update for the new tab
        self.update_nav_buttons()
        self.update_url_bar(qurl) # Show the target URL initially

    def _handle_create_window(self, window_type):
        """Handles requests to open new windows (e.g., popups, target='_blank')."""
        # For now, open in a new tab in the current browser window
        new_view = QWebEngineView(self) # <-- 先创建 View
        new_page = CustomWebEnginePage(self.profile, new_view, self) # <-- 将 new_view 传递给 Page
        new_view.setPage(new_page) # <-- 设置自定义 Page
        new_view.setAttribute(Qt.WA_DeleteOnClose)

        # Connect signals for the new view
        new_view.urlChanged.connect(self.update_url_bar) # <--- Corrected method name
        new_view.loadFinished.connect(self.on_load_finished)
        new_view.loadStarted.connect(self.on_load_started)
        new_view.titleChanged.connect(self.on_title_changed)
        new_view.page().linkHovered.connect(self.on_link_hovered)
        new_page.createWindow = self._handle_create_window # <-- Set on the new custom page instance

        # Add the new view as a tab, but don't load anything yet (page will load it)
        index = self.tab_widget.addTab(new_view, "新窗口")
        self.tab_widget.setCurrentIndex(index)
        return new_page # Return the custom page object as required


    # --- Tab Management ---
    def close_tab(self, index):
        """Closes the tab at the given index."""
        widget = self.tab_widget.widget(index)
        if widget:
            self.tab_widget.removeTab(index)
            widget.deleteLater() # Schedule the webview for deletion
        # Optional: Close window if last tab is closed
        # if self.tab_widget.count() == 0:
        #     self.window().close()

    def current_tab_changed(self, index):
        """Updates UI elements when the current tab changes."""
        webview = self.current_webview()
        if webview:
            self.update_nav_buttons()
            self.update_url_bar(webview.url())
        else:
            # Handle case where there are no tabs left (if not closing window)
            self.url_bar.clear()
            self.back_btn.setEnabled(False)
            self.forward_btn.setEnabled(False)
            self.reload_btn.setEnabled(False)


    # --- Navigation Actions ---
    def go_back(self):
        webview = self.current_webview()
        if webview: webview.back()

    def go_forward(self):
        webview = self.current_webview()
        if webview: webview.forward()

    def reload_page(self):
        webview = self.current_webview()
        if webview: webview.reload()

    def navigate_current_tab_from_bar(self):
        """Loads the URL from the address bar into the current tab."""
        webview = self.current_webview()
        if webview:
            qurl = self._prepare_qurl(self.url_bar.text())
            webview.load(qurl)

    # --- UI Update Slots ---
    def update_url_bar(self, url: QUrl):
        """Updates the URL bar if the emitting view is the current one."""
        webview = self.current_webview()
        # Check if the signal came from the currently active tab
        if webview and webview.url() == url:
             self.url_bar.setText(url.toString())
             self.url_bar.setCursorPosition(0) # Show start of URL

    def update_nav_buttons(self):
        """Updates navigation buttons based on the current tab's history."""
        webview = self.current_webview()
        if webview and webview.page() and webview.page().history(): # Add checks for page and history
            self.back_btn.setEnabled(webview.page().history().canGoBack())
            self.forward_btn.setEnabled(webview.page().history().canGoForward())
            # Consider disabling reload while loading?
            self.reload_btn.setEnabled(True)
        else:
            self.back_btn.setEnabled(False)
            self.forward_btn.setEnabled(False)
            self.reload_btn.setEnabled(False)

    def on_load_started(self):
        """Actions when a page starts loading in any tab."""
        sender_obj = self.sender()
        if isinstance(sender_obj, QWebEngineView):
            webview = sender_obj
            if webview == self.current_webview():
                self.update_nav_buttons()
                # Maybe show a loading indicator?
                index = self.tab_widget.indexOf(webview)
                if index != -1:
                     self.tab_widget.setTabText(index, "加载中...")

    def on_load_finished(self, ok: bool):
        """Actions when a page finishes loading in any tab."""
        sender_obj = self.sender()
        if isinstance(sender_obj, QWebEngineView):
            webview = sender_obj
            if webview == self.current_webview():
                self.update_nav_buttons()
                self.update_url_bar(webview.url()) # Ensure URL bar is correct
            # Update tab title even if not current
            index = self.tab_widget.indexOf(webview)
            if index != -1:
                title = webview.title() or "无标题"
                if not ok:
                    title = "加载错误"
                # Truncate long titles
                max_len = 30
                display_title = title if len(title) <= max_len else title[:max_len-3] + "..."
                self.tab_widget.setTabText(index, display_title)


    def on_title_changed(self, title: str):
        """Updates the tab title when a page's title changes."""
        sender_obj = self.sender()
        if isinstance(sender_obj, QWebEngineView):
            webview = sender_obj
            index = self.tab_widget.indexOf(webview)
            if index != -1:
                # Truncate long titles if necessary
                max_len = 30
                display_title = title if len(title) <= max_len else title[:max_len-3] + "..."
                self.tab_widget.setTabText(index, display_title)

    def on_link_hovered(self, url: str):
         """Optional: Show hovered link in status bar."""
         # Requires a QStatusBar in the main window
         try:
             status_bar = self.window().statusBar()
             if status_bar:
                 status_bar.showMessage(url if url else "")
         except AttributeError: # Handle case where window() or statusBar() might not exist yet
             pass


    # --- Download Manager ---
    def show_download_manager(self):
        """显示下载管理器 (no changes needed here for tabs)"""
        if self.download_manager is None:
            # Find the top-level window to parent the dialog
            top_level_window = self.window()
            self.download_manager = DownloadManager(top_level_window)
        self.download_manager.show()
        self.download_manager.raise_()
        self.download_manager.activateWindow()

    def handle_download(self, download: QWebEngineDownloadRequest):
        """处理下载请求"""
        print("DEBUG: handle_download function called!") # <--- 添加这行调试打印
        if self.download_manager is None:
            self.show_download_manager() # Ensure manager is visible

        # 设置默认下载目录为用户的下载文件夹
        download_dir = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        if not download_dir: # Fallback if download location is not available
            download_dir = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        if not download_dir:
            download_dir = "." # Current directory as last resort

        # 获取建议的文件名
        suggested_filename = download.downloadFileName() or "download"
        default_path = os.path.join(download_dir, suggested_filename)

        # 弹出保存文件对话框
        # Ensure self.window() is valid before using it as parent
        parent_widget = self.window() if self.window() else self
        path, _ = QFileDialog.getSaveFileName(
            parent_widget, "保存文件", default_path
        )

        if path:
            # Use setDownloadFileName which accepts the full path including the filename
            download.setDownloadFileName(path)
            download.accept()
            self.download_manager.add_download(download)
        else:
            download.cancel()

# Example usage (for testing this module directly)
if __name__ == "__main__":
    # Import subprocess for platform-specific file opening
    import subprocess
    from PySide6.QtWidgets import QApplication, QMainWindow
    app = QApplication(sys.argv)

    # Need to initialize WebEngine engine explicitly if running standalone
    # from PySide6.QtWebEngineWidgets import QWebEngineProfile # Already imported
    # profile = QWebEngineProfile.defaultProfile() # Use default profile for standalone test

    main_win = QMainWindow()
    # Add status bar for link hovering
    main_win.setStatusBar(QStatusBar()) # Import QStatusBar
    browser_widget = IntegratedBrowser(start_url="https://bing.com")
    main_win.setCentralWidget(browser_widget)
    main_win.setWindowTitle("集成浏览器测试")
    main_win.setGeometry(150, 150, 900, 600)
    main_win.show()

    sys.exit(app.exec())
