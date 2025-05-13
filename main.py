import sys
import re # <--- 添加 re 模块导入
import requests
import webbrowser
import json
import qrcode # 用于生成二维码
import io # 用于内存中处理图像数据
import time # 用于格式化时间戳
from functools import partial # 用于信号连接传递额外参数
from PySide6.QtCore import Qt, QSize, QTimer, QSettings, QThread, Signal, QObject, Slot # <--- 添加 Slot

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSizePolicy, QHBoxLayout, QMessageBox, QMenu,
    QListWidgetItem, QDialog, QLabel, QVBoxLayout, QLineEdit, QFrame,
    QPushButton, QScrollArea, QWidget, QFormLayout, QSpinBox, QComboBox,
    QCheckBox, QDialogButtonBox, QListWidget, QInputDialog, QStyleFactory,
    QGraphicsDropShadowEffect # <--- 添加阴影效果导入
)
from PySide6.QtGui import QAction, QClipboard, QPixmap, QIcon, QPalette, QColor, QMovie # <--- 添加 QMovie
from PySide6.QtCore import Qt, QSize, QTimer # <--- 添加 QTimer 导入
from ui_demo import Ui_MainWindow  # 从生成的 ui_demo.py 导入
import resources_rc # 确保资源文件被导入
from gpu_grabber import GpuGrabWorker, play_success_sound # <--- 导入抢占 Worker 和提示音函数

# --- 辅助函数：应用阴影 ---
def apply_shadow(widget):
    """给指定的控件应用标准阴影效果"""
    if not widget:
        return
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(15)
    shadow.setOffset(5, 5)
    shadow.setColor(QColor(0, 0, 0, 160))
    widget.setGraphicsEffect(shadow)
# --- 辅助函数结束 ---

from api_handler import ApiHandler # <--- 添加导入
from instance_ui import InstanceBootDialog # <--- 导入开机对话框
from integrated_browser import IntegratedBrowser # <--- 导入集成浏览器

# CONFIG_FILE = "config.json" # <--- 不再需要，使用 QSettings
# API_BASE_URL = "https://api.xiangongyun.com/open" # <--- 不再需要，移到 ApiHandler


# --- Worker Thread Class ---
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        `str` error message
    success
        `object` data returned from processing, anything
    '''
    finished = Signal()
    error = Signal(str)
    success = Signal(object)


class Worker(QThread):
    '''
    Worker thread
    Inherits from QThread to handle worker execution.
    :param callback: The function callback to run on this worker thread. Supplied args and kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            print(f"Worker Error: {e}") # 调试信息
            # Ensure error signal emits a string
            self.signals.error.emit(str(e))
        else:
            # Ensure success signal emits the result object
            self.signals.success.emit(result)
        finally:
            self.signals.finished.emit()


# --- 二维码显示对话框 ---

# === 新增主题管理类 ===
class ThemeManager:
    System = 0
    Light = 1
    Dark = 2

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_theme = cls.Dark
            cls._instance.load_theme()
        return cls._instance

    def load_theme(self):
        settings = QSettings()
        self.current_theme = int(settings.value("Theme", self.Dark))

    def save_theme(self):
        settings = QSettings()
        settings.setValue("Theme", self.current_theme)

    def set_theme(self, theme):
        self.current_theme = theme
        self.apply_theme()
        self.save_theme()

    def apply_theme(self):
        if self.current_theme == self.System:
            self.apply_system_theme()
        elif self.current_theme == self.Light:
            self.apply_light_theme()
        elif self.current_theme == self.Dark:
            self.apply_dark_theme()

    def apply_system_theme(self):
        app = QApplication.instance()
        # Check if styleHints() exists and is callable
        if hasattr(app, 'styleHints') and callable(app.styleHints):
             if app.styleHints().colorScheme() == Qt.ColorScheme.Dark:
                 print("Applying System Theme -> Dark") # Debug
                 self.apply_dark_theme()
             else:
                 print("Applying System Theme -> Light") # Debug
                 self.apply_light_theme()
        else:
             print("Warning: app.styleHints() not available, defaulting to Light for System theme.")
             self.apply_light_theme() # Fallback

    def apply_light_theme(self):
        print("Applying Light Theme...") # Debug
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))

        palette = QPalette()
        # Ensure QColor and Qt are imported from PySide6.QtGui and PySide6.QtCore respectively
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        # Add disabled colors
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, Qt.GlobalColor.darkGray)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, Qt.GlobalColor.darkGray)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, Qt.GlobalColor.darkGray)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor(211, 211, 211))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, Qt.GlobalColor.darkGray)


        app.setPalette(palette)
        app.setStyleSheet("") # Clear any global stylesheet that might override palette

    def apply_dark_theme(self):
        print("Applying Dark Theme...") # Debug
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))

        palette = QPalette()
        # Ensure QColor and Qt are imported from PySide6.QtGui and PySide6.QtCore respectively
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42)) # Darker base
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66)) # Slightly lighter alt base
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white) # Tooltips often light
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black) # Tooltip text often dark
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(75, 75, 75)) # Darker buttons
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red) # Keep bright text red
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218)) # Brighter blue link
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218)) # Highlight color
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black) # Highlighted text often dark
         # Add disabled colors
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, Qt.GlobalColor.gray)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, Qt.GlobalColor.gray)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, Qt.GlobalColor.gray)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor(80, 80, 80))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, Qt.GlobalColor.gray)

        app.setPalette(palette)
        # Optionally set a global dark stylesheet (e.g., using qdarkstyle or similar)
        # Or clear any existing one that might conflict
        app.setStyleSheet("")

class QRCodeDialog(QDialog):
    def __init__(self, qr_pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("微信支付二维码")
        self.setModal(True)
        layout = QVBoxLayout(self)
        self.qr_label = QLabel(self)
        self.qr_label.setPixmap(qr_pixmap)
        layout.addWidget(self.qr_label)
        info_label = QLabel("请使用微信扫描二维码完成支付", self)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        self.setLayout(layout)
        self.adjustSize()

# --- 图片显示对话框 (支持缩放) ---
class ImageDialog(QDialog):
    def __init__(self, image_path, title="查看图片", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.original_pixmap = QPixmap(image_path)
        if self.original_pixmap.isNull():
            print(f"错误：无法加载图片 {image_path}")
            self.image_label = QLabel("无法加载图片", self)
        else:
            self.image_label = QLabel(self)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        self.setLayout(layout)
        initial_size = self.original_pixmap.size() * 0.5
        if initial_size.width() < 300 or initial_size.height() < 300:
            initial_size = QSize(300, 300)
        self.resize(initial_size)
        self.update_image()

    def resizeEvent(self, event):
        self.update_image()
        super().resizeEvent(event)

    def update_image(self):
        if not self.original_pixmap.isNull():
            label_size = self.image_label.size()
            scaled_pixmap = self.original_pixmap.scaled(label_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

# --- 部署镜像对话框 ---

# 镜像类型中英文映射
IMAGE_TYPE_MAP = {
    "public": "官方",
    "community": "社区",
    "private": "私有"
}
# 反向映射，用于从中文获取英文
IMAGE_TYPE_MAP_REVERSE = {v: k for k, v in IMAGE_TYPE_MAP.items()}

class DeployImageDialog(QDialog):
    def __init__(self, image_id, image_type, parent=None):
        super().__init__(parent)
        self.setWindowTitle("部署镜像")
        self.setMinimumWidth(450) # 设置最小宽度

        self.layout = QFormLayout(self)
        self.layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow) # 让输入框扩展
        self.layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight) # 标签右对齐

        # --- 输入字段 ---
        self.gpu_model_combo = QComboBox(self)
        self.gpu_model_combo.addItems(["NVIDIA GeForce RTX 4090", "NVIDIA GeForce RTX 4090 D"])
        self.layout.addRow("GPU型号 (gpu_model):", self.gpu_model_combo)

        self.gpu_count_spin = QSpinBox(self)
        self.gpu_count_spin.setRange(0, 8)
        self.gpu_count_spin.setValue(1)
        self.layout.addRow("GPU数量 (gpu_count):", self.gpu_count_spin)

        self.data_center_id_spin = QSpinBox(self)
        self.data_center_id_spin.setRange(1, 99) # 假设数据中心ID从1开始
        self.data_center_id_spin.setValue(1)
        self.layout.addRow("数据中心ID (data_center_id):", self.data_center_id_spin)

        self.image_id_input = QLineEdit(image_id, self)
        self.image_id_input.setReadOnly(True) # 镜像ID通常不可编辑
        self.layout.addRow("镜像ID (image):", self.image_id_input)

        self.image_type_combo = QComboBox(self)
        # 使用映射的中文值填充下拉框
        self.image_type_combo.addItems(list(IMAGE_TYPE_MAP.values()))
        # 根据传入的英文 image_type 设置对应的中文默认值
        default_display_text = IMAGE_TYPE_MAP.get(image_type, IMAGE_TYPE_MAP.get("private")) # 默认显示"私有"
        self.image_type_combo.setCurrentText(default_display_text)
        self.image_type_combo.setStyleSheet("QComboBox { min-width: 200px; }")
        self.layout.addRow("镜像类型 (image_type):", self.image_type_combo)

        self.storage_check = QCheckBox("是否挂载云储存 (storage)", self)
        self.layout.addRow("", self.storage_check) # Checkbox 通常不需要标签

        self.storage_mount_path_input = QLineEdit("/root/cloud", self)
        self.layout.addRow("云储存挂载路径 (storage_mount_path):", self.storage_mount_path_input)

        self.ssh_key_input = QLineEdit(self)
        self.ssh_key_input.setPlaceholderText("可选")
        self.layout.addRow("SSH密钥ID (sshkey):", self.ssh_key_input)

        self.system_disk_expand_check = QCheckBox("是否扩容系统磁盘 (system_disk_expand)", self)
        self.layout.addRow("", self.system_disk_expand_check)

        self.system_disk_expand_size_spin = QSpinBox(self)
        self.system_disk_expand_size_spin.setRange(0, 1024 * 10) # 假设最大扩展10TB，单位GB？API是字节，这里用GB方便输入
        self.system_disk_expand_size_spin.setSuffix(" GB") # API需要字节，提交时转换
        self.system_disk_expand_size_spin.setValue(0)
        self.layout.addRow("系统磁盘扩容尺寸 (system_disk_expand_size):", self.system_disk_expand_size_spin)

        self.instance_name_input = QLineEdit(self)
        self.instance_name_input.setPlaceholderText("可选，设置实例名")
        self.instance_name_input = QLineEdit(self)
        self.instance_name_input.setPlaceholderText("可选，设置实例名")
        self.layout.addRow("实例名 (name):", self.instance_name_input)

        # --- 抢占相关控件 ---
        self.retry_interval_spinbox = QSpinBox(self)
        self.retry_interval_spinbox.setRange(1, 60) # 重试间隔 3-60 秒
        self.retry_interval_spinbox.setValue(5)
        self.retry_interval_spinbox.setSuffix(" 秒")
        self.layout.addRow("抢占重试间隔:", self.retry_interval_spinbox)

        self.status_label = QLabel("请选择操作", self)
        self.status_label.setStyleSheet("color: #a0aec0;") # 初始灰色
        self.status_label.setWordWrap(True)
        self.layout.addRow("状态:", self.status_label)

        # --- 按钮布局 ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.deploy_button = QPushButton("立即部署") # 原 OK 按钮
        self.deploy_button.setIcon(QIcon(":/ico/ico/play-circle.svg"))
        self.deploy_button.setStyleSheet("background-color: #48bb78; color: white; padding: 8px 15px; border-radius: 5px;")
        apply_shadow(self.deploy_button)
        self.deploy_button.clicked.connect(self.handle_normal_deploy) # 连接到普通部署处理函数
        button_layout.addWidget(self.deploy_button)

        self.grab_deploy_button = QPushButton("抢占部署")
        self.grab_deploy_button.setIcon(QIcon(":/ico/ico/zap.svg")) # 闪电图标
        self.grab_deploy_button.setStyleSheet("background-color: #ed8936; color: white; padding: 8px 15px; border-radius: 5px;") # 橙色
        apply_shadow(self.grab_deploy_button)
        self.grab_deploy_button.clicked.connect(self.start_gpu_grabbing) # 连接到抢占处理函数
        button_layout.addWidget(self.grab_deploy_button)

        self.cancel_grab_button = QPushButton("取消抢占")
        self.cancel_grab_button.setIcon(QIcon(":/ico/ico/x-circle.svg"))
        self.cancel_grab_button.setStyleSheet("background-color: #e53e3e; color: white; padding: 8px 15px; border-radius: 5px;") # 红色
        self.cancel_grab_button.setEnabled(False) # 初始禁用
        apply_shadow(self.cancel_grab_button)
        self.cancel_grab_button.clicked.connect(self.cancel_gpu_grabbing)
        button_layout.addWidget(self.cancel_grab_button)

        button_layout.addStretch() # 将按钮推到左侧

        self.cancel_button = QPushButton("关闭窗口") # 原 Cancel 按钮
        self.cancel_button.setIcon(QIcon(":/ico/ico/x.svg"))
        self.cancel_button.setStyleSheet("background-color: #718096; color: white; padding: 8px 15px; border-radius: 5px;") # 灰色
        apply_shadow(self.cancel_button)
        self.cancel_button.clicked.connect(self.reject) # 连接到 reject 关闭对话框
        button_layout.addWidget(self.cancel_button)

        self.layout.addRow(button_layout) # 将按钮行添加到表单布局

        # --- 初始化抢占任务相关变量 ---
        self.gpu_grab_thread = None
        self.gpu_grab_worker = None

    def get_data(self):
        """获取对话框中的数据，用于普通部署或抢占部署"""
        # API 需要字节，将 GB 转换为字节
        expand_size_gb = self.system_disk_expand_size_spin.value()
        expand_size_bytes = expand_size_gb * (1024**3) if expand_size_gb > 0 else 0

        data = {
            "gpu_model": self.gpu_model_combo.currentText(),
            "gpu_count": self.gpu_count_spin.value(),
            "data_center_id": self.data_center_id_spin.value(),
            "image": self.image_id_input.text(),
            # 从选中的中文获取对应的英文 key
            "image_type": IMAGE_TYPE_MAP_REVERSE.get(self.image_type_combo.currentText(), "private"), # 默认返回 "private"
            "storage": self.storage_check.isChecked(),
            "storage_mount_path": self.storage_mount_path_input.text() or None, # 可选，空则不传
            "ssh_key": self.ssh_key_input.text() or None, # 可选
            "system_disk_expand": self.system_disk_expand_check.isChecked(),
            "system_disk_expand_size": expand_size_bytes if self.system_disk_expand_check.isChecked() else None, # 仅在勾选时传递
            "name": self.instance_name_input.text() or None # 可选
        }
         # 清理 None 值，API 可能不接受 null
        return {k: v for k, v in data.items() if v is not None and v != ""}

    # --- 普通部署处理 ---
    def handle_normal_deploy(self):
        """处理普通部署按钮点击"""
        deploy_data = self.get_data()
        if deploy_data:
            # 触发一个信号或直接调用主窗口的方法来处理部署
            # 这里我们假设父窗口 (MainWindow) 有一个 deploy_image_async 方法
            if isinstance(self.parent(), MainWindow):
                self.parent().deploy_image_async(deploy_data)
            else:
                print("错误：无法获取主窗口实例来执行部署。")
                QMessageBox.critical(self, "部署错误", "无法启动部署流程。")
            self.accept() # 提交后关闭对话框

    # --- 抢占 GPU 相关方法 ---
    @Slot()
    def start_gpu_grabbing(self):
        """启动 GPU 抢占任务"""
        if self.gpu_grab_thread and self.gpu_grab_thread.isRunning():
            self.update_status_label("⚠️ 抢占任务已在运行中。")
            return

        # 1. 获取部署参数和重试间隔
        deploy_params = self.get_data()
        if not deploy_params:
            QMessageBox.warning(self, "参数错误", "无法获取部署参数。")
            return
        retry_interval = self.retry_interval_spinbox.value()

        # 2. 创建 Worker 和 Thread
        # --- 修复：添加 self.parent().api_handler 作为第一个参数 ---
        # 检查父对象是否是 MainWindow 并且有 api_handler
        main_window = self.parent()
        if not isinstance(main_window, MainWindow) or not hasattr(main_window, 'api_handler'):
            QMessageBox.critical(self, "内部错误", "无法获取 API Handler 实例，无法启动抢占任务。")
            self.reset_ui_after_grab() # 重置UI状态
            return
        api_handler_instance = main_window.api_handler

        self.gpu_grab_worker = GpuGrabWorker(api_handler_instance, deploy_params, interval=retry_interval)
        self.gpu_grab_thread = QThread()

        # 3. 移动 Worker 到 Thread
        self.gpu_grab_worker.moveToThread(self.gpu_grab_thread)

        # 4. 连接信号槽
        self.gpu_grab_thread.started.connect(self.gpu_grab_worker.run)
        self.gpu_grab_worker.finished.connect(self.gpu_grab_thread.quit)
        self.gpu_grab_worker.finished.connect(self.gpu_grab_worker.deleteLater)
        self.gpu_grab_thread.finished.connect(self.gpu_grab_thread.deleteLater)
        self.gpu_grab_worker.finished.connect(self.reset_ui_after_grab) # 任务结束后重置 UI

        self.gpu_grab_worker.success.connect(self.on_deploy_success)
        self.gpu_grab_worker.error.connect(self.on_deploy_error)
        self.gpu_grab_worker.status_update.connect(self.update_status_label)

        # 5. 启动线程
        self.gpu_grab_thread.start()

        # 6. 更新 UI
        self.deploy_button.setEnabled(False)
        self.grab_deploy_button.setEnabled(False)
        self.cancel_grab_button.setEnabled(True)
        self.retry_interval_spinbox.setEnabled(False) # 禁用间隔设置
        self.update_status_label("🚀 正在初始化抢占任务...")

    @Slot(str)
    def on_deploy_success(self, instance_id):
        """处理抢占成功信号"""
        self.update_status_label(f"✅ 抢占成功！实例 ID: {instance_id}")
        # play_success_sound() # Worker 内部已调用
        QMessageBox.information(self, "抢占成功", f"成功抢占 GPU 并部署实例！\n实例 ID: {instance_id}\n\n对话框即将关闭，请前往实例页面查看。")
        # 可以在这里触发主窗口刷新实例列表的信号
        if isinstance(self.parent(), MainWindow):
            self.parent().show_shili_page() # 切换到实例页面并刷新
        self.accept() # 关闭对话框

    @Slot(str)
    def on_deploy_error(self, error_message):
        """处理抢占错误信号"""
        self.update_status_label(f"💥 抢占失败: {error_message}")
        QMessageBox.critical(self, "抢占错误", f"抢占部署过程中发生错误:\n{error_message}")
        # UI 重置由 finished 信号触发的 reset_ui_after_grab 处理

    @Slot(str)
    def update_status_label(self, status):
        """更新状态标签文本"""
        self.status_label.setText(status)
        # 根据状态改变标签颜色（可选）
        if "✅" in status or "成功" in status:
            self.status_label.setStyleSheet("color: #48bb78;") # 绿色
        elif "💥" in status or "错误" in status or "失败" in status:
            self.status_label.setStyleSheet("color: #e53e3e;") # 红色
        elif "⚠️" in status or "警告" in status:
            self.status_label.setStyleSheet("color: #ed8936;") # 橙色
        elif "🛑" in status or "取消" in status:
             self.status_label.setStyleSheet("color: #718096;") # 灰色
        else:
            self.status_label.setStyleSheet("color: #a0aec0;") # 默认浅灰

    @Slot()
    def cancel_gpu_grabbing(self):
        """取消抢占任务"""
        if self.gpu_grab_worker:
            self.gpu_grab_worker.stop() # 请求 Worker 停止
        self.cancel_grab_button.setEnabled(False) # 禁用取消按钮
        self.update_status_label("⏳ 正在取消抢占任务...")

    @Slot()
    def reset_ui_after_grab(self):
        """任务结束后重置 UI 状态"""
        print("[DeployDialog] Resetting UI after grab task finished.") # Debug
        self.deploy_button.setEnabled(True)
        self.grab_deploy_button.setEnabled(True)
        self.cancel_grab_button.setEnabled(False)
        self.retry_interval_spinbox.setEnabled(True)
        # 清理引用，防止意外使用旧对象
        self.gpu_grab_thread = None
        self.gpu_grab_worker = None
        # 可以在这里清除状态标签或设置默认文本
        # self.status_label.setText("请选择操作")
        # self.status_label.setStyleSheet("color: #a0aec0;")

    # --- 覆盖关闭事件 ---
    def closeEvent(self, event):
        """在关闭对话框时确保停止后台任务"""
        if self.gpu_grab_thread and self.gpu_grab_thread.isRunning():
            print("[DeployDialog] Close event triggered while grab task running. Stopping task...") # Debug
            self.cancel_gpu_grabbing()
            # 可以选择等待线程结束，但可能导致 UI 卡顿
            # self.gpu_grab_thread.quit()
            # if not self.gpu_grab_thread.wait(1000): # 等待最多1秒
            #     print("[DeployDialog] Warning: Grab thread did not finish within 1 second.")
        super().closeEvent(event)

    # --- 覆盖 reject 方法 ---
    def reject(self):
        """处理 Cancel 按钮或 Esc 键"""
        # 在关闭前确保任务已停止
        if self.gpu_grab_thread and self.gpu_grab_thread.isRunning():
            self.cancel_gpu_grabbing()
        super().reject() # 调用父类的 reject 来关闭对话框


class MainWindow(QMainWindow, Ui_MainWindow):
    # --- 添加一个信号，用于部署成功后触发实例列表刷新 ---
    instance_deployed_signal = Signal()

    def __init__(self):
        super().__init__()
        # === 新增主题初始化 ===
        app = QApplication.instance()
        app.setApplicationName("顺势ai")
        app.setOrganizationName("顺势ai") # 使用实际应用名称

        # 初始化主题
        ThemeManager().apply_theme()

        # 监听系统主题变化
        app.styleHints().colorSchemeChanged.connect(
            lambda: ThemeManager().apply_theme()
            if ThemeManager().current_theme == ThemeManager.System
            else None
        )
        self.setupUi(self)
        self.api_handler = ApiHandler() # <--- 实例化 ApiHandler
        self.custom_public_images = [] # <--- 初始化自定义公共镜像列表
        self.ports = {} # <--- 初始化端口配置字典
        self.thread_pool = [] # <--- 用于保持 Worker 对象的引用
        self.is_refreshing_instances = False # <--- 添加实例刷新状态标志
        self.is_refreshing_images = False # <--- 添加镜像刷新状态标志
        self.browser_preference = "integrated" # <--- 添加浏览器偏好设置, 默认内置
        self.browser_preference = "integrated" # <--- 添加浏览器偏好设置, 默认内置

        # --- 初始化镜像页面布局 ---
        self._setup_jingxiang_page_layout()
        # --- 初始化实例页面布局 ---
        self._setup_shili_page_layout()
        # --- 初始化公共镜像列表页面布局 ---
        self._setup_list_jingxiang_page_layout() # <--- 添加公共镜像页面布局初始化调用

        # 设置令牌输入框为密码模式
        self.lingpai.setEchoMode(QLineEdit.EchoMode.Password)

        self.api_token = None
        self.last_trade_no = None

        # 加载保存的配置 (令牌和自定义镜像)
        self.load_config()


        # 确保必要的 UI 元素存在
        required_elements = [
            'help', 'bangzhu_page4', 'xinxi_page3', 'lingpai', 'pushButton_15',
            'pushButton_16', 'radioButton', 'listWidget', 'listWidget_2',
            'pushButton_3', 'comboBox', 'spinBox', 'pushButton_2', 'listWidget_4',
            'pushButton_4', 'statusbar', 'jingxiang_page7', 'coffee', 'huoqu', 'zhuce'
        ]
        for element in required_elements:
            if not hasattr(self, element):
                # 尝试从 UI 对象查找
                widget = self.findChild(QWidget, element)
                if widget:
                    setattr(self, element, widget)
                else:
                    # 如果还是找不到，则抛出错误，但对于动态创建的布局内的元素（如label_5）需要特殊处理
                    # 检查设置页面的端口输入框和按钮是否存在
                    if element.startswith('dailikuang_') or element.startswith('dailiBt_'):
                        widget = self.findChild(QWidget, element)
                        if widget:
                            setattr(self, element, widget)
                        else:
                            print(f"警告: UI中缺少设置页面元素: {element}") # 打印警告而不是抛出错误
                            # raise AttributeError(f"UI中缺少元素: {element}")
                            raise AttributeError(f"UI中缺少元素: {element}")


        # --- 页面切换连接 ---
        self.jingxiang.clicked.connect(self.show_jingxiang_page)
        self.home.clicked.connect(self.show_zhuye_page)
        self.shiliBt.clicked.connect(self.show_shili_page)
        self.menubtn.clicked.connect(self.show_zhanghao_page)
        self.help.clicked.connect(self.show_bangzhu_page)
        self.info.clicked.connect(self.show_xinxi_page)
        self.settings.clicked.connect(self.show_shezhi_page)
        self.jingxiang_2.clicked.connect(self.show_list_jingxiang_page) # <--- 添加公共镜像按钮连接

        # --- 设置页面端口保存按钮连接 ---
        # 使用 partial 传递端口名称和输入框对象
        if hasattr(self, 'dailiBt_2') and hasattr(self, 'dailikuang_2'):
            self.dailiBt_2.accepted.connect(partial(self.save_port_setting, 'comfyui', self.dailikuang_2))
        if hasattr(self, 'dailiBt_3') and hasattr(self, 'dailikuang_3'):
            self.dailiBt_3.accepted.connect(partial(self.save_port_setting, 'fengzhuang', self.dailikuang_3))
        if hasattr(self, 'dailiBt_4') and hasattr(self, 'dailikuang_4'):
            self.dailiBt_4.accepted.connect(partial(self.save_port_setting, 'fluxgym', self.dailikuang_4))
        if hasattr(self, 'dailiBt_6') and hasattr(self, 'dailikuang_6'): # 注意：输出文件是 dailikuang_6 / dailiBt_6
            self.dailiBt_6.accepted.connect(partial(self.save_port_setting, 'shuchu', self.dailikuang_6))
        if hasattr(self, 'dailiBt_5') and hasattr(self, 'dailikuang_5'): # 注意：全部文件是 dailikuang_5 / dailiBt_5
            self.dailiBt_5.accepted.connect(partial(self.save_port_setting, 'quanbu', self.dailikuang_5))

        # --- 主页令牌处理连接 ---
        self.pushButton_15.clicked.connect(self.confirm_token)
        self.pushButton_16.clicked.connect(self.clear_token)
        self.huoqu.clicked.connect(lambda: self.open_url("https://www.xiangongyun.com/console/user/accesstoken"))
        self.zhuce.clicked.connect(lambda: self.open_url("https://www.xiangongyun.com/register/WR2K3R"))

        # --- 左侧服务按钮连接 ---
        if hasattr(self, 'comfyui'):
            self.comfyui.clicked.connect(partial(self.open_service_url, 'comfyui'))
        if hasattr(self, 'fengzhuang'):
            self.fengzhuang.clicked.connect(partial(self.open_service_url, 'fengzhuang'))
        if hasattr(self, 'fluxgym'):
            self.fluxgym.clicked.connect(partial(self.open_service_url, 'fluxgym'))
        if hasattr(self, 'shuchu'):
            self.shuchu.clicked.connect(partial(self.open_service_url, 'shuchu'))
        if hasattr(self, 'quanbu'):
            self.quanbu.clicked.connect(partial(self.open_service_url, 'quanbu'))
        # --- 添加浏览器按钮连接 ---
        if hasattr(self, 'quanbu_2'):
            # self.quanbu_2.clicked.connect(partial(self.open_service_url, 'quanbu_2')) # 旧的连接，注释掉或删除
            self.quanbu_2.clicked.connect(self.show_browser_page) # <--- 连接到新的页面切换方法


        # --- 账号页面功能连接 ---
        self.pushButton_3.clicked.connect(self.get_balance)
        self.pushButton_2.clicked.connect(self.create_recharge_order)
        self.pushButton_4.clicked.connect(self.query_recharge_order)
        self.coffee.clicked.connect(self.show_sponsor_dialog)

        # --- 用户信息列表右键复制 ---
        self.listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.show_user_info_context_menu)

        # --- 其他初始化 ---
        self.spinBox.setMinimum(5)
        self.spinBox.setMaximum(10000)

        # 存储所有左侧按钮
        self.left_buttons = [
            self.menubtn, self.jingxiang, self.home, self.shiliBt,
            self.settings, self.info, self.help, self.jingxiang_2 # <--- 添加公共镜像按钮到列表
        ]

        # 确保settings按钮可以正常点击
        self.settings.setStyleSheet("QPushButton { border-radius: 10px; }")

        # 初始显示主页
        self.show_zhuye_page()
        if self.api_token:
            self.get_user_info()
            self.get_balance()

        # --- 添加定时刷新 ---
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(15000) # 每 15 秒刷新一次 (15000 毫秒)

        # --- 为所有左侧按钮添加阴影效果 ---
        for button in self.left_buttons:
            apply_shadow(button) # 使用辅助函数

        # --- 为其他静态按钮和主页添加阴影 ---
        apply_shadow(self.zhuye_page1) # 为主页容器添加阴影
        apply_shadow(self.pushButton_15) # 确认令牌
        apply_shadow(self.pushButton_16) # 清除令牌
        apply_shadow(self.huoqu)         # 获取令牌
        apply_shadow(self.zhuce)         # 注册
        apply_shadow(self.pushButton_3)  # 查余额
        apply_shadow(self.pushButton_2)  # 充值
        apply_shadow(self.pushButton_4)  # 查订单
        apply_shadow(self.coffee)        # 打赏
        # 注意：QDialogButtonBox (dailiBt_*) 不方便加阴影，暂时跳过
        # --- 阴影效果结束 ---

        # --- 创建共享的内置浏览器页面 ---
        self.browser_page = QWidget() # 创建一个新的页面容器
        self.browser_page.setObjectName("shared_browser_page")
        browser_layout = QVBoxLayout(self.browser_page) # 为新页面创建布局
        browser_layout.setContentsMargins(0, 0, 0, 0) # 无边距
        self.shared_browser = IntegratedBrowser(self.browser_page) # 创建共享浏览器实例
        browser_layout.addWidget(self.shared_browser) # 将浏览器添加到布局
        self.body.addWidget(self.browser_page) # 将新页面添加到 QStackedWidget
        # --- 共享内置浏览器页面创建结束 ---

    # === 浏览器偏好设置处理 ===
    def change_browser_preference(self, index):
        """处理浏览器选择下拉框变化"""
        if index == 0:
            self.browser_preference = "integrated"
            print("浏览器偏好设置为: 内置浏览器")
        else:
            self.browser_preference = "system"
            print("浏览器偏好设置为: 系统浏览器")
        self.save_config() # 保存设置

    # === 主题相关方法 ===
    def change_theme(self, theme):
        # 取消其他选项的选中状态
        # 确保动作已在 _setup_theme_settings 中创建
        if hasattr(self, 'system_action') and hasattr(self, 'light_action') and hasattr(self, 'dark_action'):
            for action in [self.system_action, self.light_action, self.dark_action]:
                action.setChecked(False)

            # 设置当前选中
            if theme == ThemeManager.System:
                self.system_action.setChecked(True)
            elif theme == ThemeManager.Light:
                self.light_action.setChecked(True)
            else: # Dark
                self.dark_action.setChecked(True)
        else:
            print("警告: 主题动作尚未初始化，无法更新选中状态。")

        # 应用主题
        ThemeManager().set_theme(theme) # Calls ThemeManager.apply_theme()
        self.update_all_styles()      # Calls self.style().polish()

    def update_all_styles(self):
        print("Updating styles...") # Debug
        app = QApplication.instance()
        # Re-apply the current palette (might help ensure consistency)
        # app.setPalette(app.palette()) # Re-applying same palette might not trigger update
        # Instead of polishing self, polish the application instance
        app.style().unpolish(app)
        app.style().polish(app)
        # Also polish the main window
        self.style().unpolish(self)
        self.style().polish(self)
        # Polish existing dialogs and all child widgets
        for child in self.findChildren(QWidget): # Polish all child widgets
            if isinstance(child, QDialog):
                print(f"Polishing dialog: {child.windowTitle()}") # Debug
            # 检查控件是否有可调用的style方法
            if hasattr(child, 'style') and callable(child.style):
                try:
                    child.style().unpolish(child)
                    child.style().polish(child)
                except Exception as e:
                    print(f"  - Failed to polish widget {child.objectName()}: {e}") # Debug
        self.update()  # 更新当前控件
        app.processEvents()  # 处理事件队列，确保更新可见

        # 处理完事件后再次更新所有子控件
        for child in self.findChildren(QWidget):
            if hasattr(child, 'update') and callable(child.update):
                try:
                    child.update()
                except Exception as e:
                     print(f"  - Failed to update widget {child.objectName()}: {e}") # Debug

        print("Style update finished.")  # 调试信息

    def _setup_theme_settings(self):
        """添加主题设置到设置页面"""
        print("--- Setting up theme settings ---") # 确认函数被调用
        # Ensure shezhi_page2 exists and is a QWidget
        if not hasattr(self, 'shezhi_page2') or not isinstance(self.shezhi_page2, QWidget):
            print("ERROR: self.shezhi_page2 not found or not a QWidget!")
            return

        print(f"shezhi_page2 object: {self.shezhi_page2}") # 确认对象存在
        page_layout = self.shezhi_page2.layout()
        print(f"shezhi_page2 layout: {page_layout}") # 检查是否有布局

        if not page_layout:
            print("ERROR: shezhi_page2 has no layout! Cannot add theme settings.")
            # Optionally, create a layout here if it's missing, though it's better fixed in Designer
            # page_layout = QVBoxLayout(self.shezhi_page2)
            # self.shezhi_page2.setLayout(page_layout)
            # print("Dynamically added QVBoxLayout to shezhi_page2.")
            return # Or return if you expect layout to exist

        # 查找或创建主题设置容器
        theme_frame = self.findChild(QFrame, "theme_frame")
        if not theme_frame:
            print("Creating theme_frame...")
            theme_frame = QFrame(self.shezhi_page2) # Set parent
            theme_frame.setObjectName("theme_frame")
            # theme_frame.setStyleSheet("QFrame#theme_frame { background-color: red; border: 2px solid yellow; padding: 10px; min-height: 80px; }") # Removed hardcoded style
            # theme_frame.setMinimumHeight(80)

            layout = QVBoxLayout(theme_frame) # Set layout for the frame
            print("Theme frame layout created.")

            # 主题设置标题
            theme_label = QLabel("外观(只能应用弹窗)")
            # theme_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: white;") # Removed hardcoded style
            layout.addWidget(theme_label)
            print(f"Theme label added: {theme_label.text()}")

            # 主题选择按钮
            self.theme_btn = QPushButton("选择主题")
            # self.theme_btn.setStyleSheet("background-color: blue; color: white; padding: 5px;") # Removed hardcoded style
            self.theme_menu = QMenu(self.theme_btn) # Pass parent to menu

            # 创建主题选项
            self.system_action = QAction("跟随系统", self)
            self.light_action = QAction("白天模式", self)
            self.dark_action = QAction("夜间模式", self)

            # 设置可选中
            for action in [self.system_action, self.light_action, self.dark_action]:
                action.setCheckable(True)

            # 连接信号
            self.system_action.triggered.connect(lambda: self.change_theme(ThemeManager.System))
            self.light_action.triggered.connect(lambda: self.change_theme(ThemeManager.Light))
            self.dark_action.triggered.connect(lambda: self.change_theme(ThemeManager.Dark))

            # 添加选项到菜单
            self.theme_menu.addAction(self.system_action)
            self.theme_menu.addAction(self.light_action)
            self.theme_menu.addAction(self.dark_action)
            self.theme_btn.setMenu(self.theme_menu)

            # 添加到布局
            layout.addWidget(self.theme_btn)
            apply_shadow(self.theme_btn) # 为主题按钮添加阴影
            print(f"Theme button added: {self.theme_btn.text()}")

            # 检查是否设置了布局到 theme_frame (QVBoxLayout constructor does this)
            print(f"theme_frame's layout: {theme_frame.layout()}")

            # 插入到现有设置页面布局
            print(f"Inserting theme_frame into page layout ({page_layout}) at index 0...")
            page_layout.insertWidget(0, theme_frame)
            # theme_frame.show() # Generally not needed when inserted into a visible layout
            print("Insertion done. Checking geometry...")
            # Force layout recalculation (might help, might not be needed)
            # self.shezhi_page2.layout().activate()
            # Give Qt a chance to process events, then check geometry
            QApplication.processEvents()
            print(f"theme_frame.isVisible(): {theme_frame.isVisible()}")
            print(f"theme_frame.geometry(): {theme_frame.geometry()}") # More informative than size

        else:
            print("theme_frame already exists.")
            # DEBUG: If it exists, ensure it's visible
            # theme_frame.setStyleSheet("QFrame#theme_frame { background-color: red; border: 2px solid yellow; padding: 10px; min-height: 80px; }") # Removed hardcoded style
            theme_frame.setVisible(True)
            QApplication.processEvents()
            print(f"Existing theme_frame.isVisible(): {theme_frame.isVisible()}")
            print(f"Existing theme_frame.geometry(): {theme_frame.geometry()}")

    def change_theme(self, theme):
        # 取消其他选项的选中状态
        for action in [self.system_action, self.light_action, self.dark_action]:
            action.setChecked(False)
    
        # 设置当前选中
        if theme == ThemeManager.System:
            self.system_action.setChecked(True)
        elif theme == ThemeManager.Light:
            self.light_action.setChecked(True)
        else: # Dark
            self.dark_action.setChecked(True)
    
        # 应用主题
        ThemeManager().set_theme(theme) # Calls ThemeManager.apply_theme()
        self.update_all_styles()      # Calls self.style().polish()



    # --- 令牌管理 ---
    def load_token(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                saved_token = config.get("api_token")
                remember_token = config.get("remember_token", False)
                if saved_token and remember_token:
                    self.api_token = saved_token
                    self.lingpai.setText(saved_token)
                    self.radioButton.setChecked(True)
                    self.statusbar.showMessage("已加载保存的访问令牌", 3000)
                    self.api_handler.set_access_token(saved_token) # <--- 设置 Handler 的令牌
                else:
                    self.radioButton.setChecked(False)
        except FileNotFoundError:
            self.radioButton.setChecked(False)
        except json.JSONDecodeError:
            QMessageBox.warning(self, "配置错误", f"无法解析配置文件 {CONFIG_FILE}")
            self.radioButton.setChecked(False)
            self.custom_public_images = [] # 加载失败则清空
        except Exception as e:
            QMessageBox.warning(self, "加载配置错误", f"加载配置时出错: {e}")
            self.radioButton.setChecked(False)
            self.custom_public_images = [] # 加载失败则清空
            self.ports = { # 加载失败，使用默认端口
                "comfyui": 8188, "fengzhuang": 7861, "fluxgym": 7860,
                "shuchu": 8080, "quanbu": 8081
            }

    def save_config(self):
        """使用 QSettings 保存配置"""
        settings = QSettings()
        settings.setValue("api_token", self.lingpai.text() if self.radioButton.isChecked() else None)
        settings.setValue("remember_token", self.radioButton.isChecked())
        # QSettings 可以保存列表和字典
        settings.setValue("custom_public_images", self.custom_public_images)
        settings.setValue("ports", self.ports)
        settings.setValue("browser_preference", self.browser_preference) # <--- 保存浏览器偏好
        # 主题由 ThemeManager 单独保存，这里不再重复保存
        # settings.setValue("theme", ThemeManager().current_theme)
        settings.sync() # 确保写入磁盘
        print("配置已使用 QSettings 保存")

    def show_shezhi_page(self):
        """显示设置页面并加载当前端口配置"""
        print("--- Entering show_shezhi_page ---") # Debug
        self.update_button_state(self.settings)
        self.body.setCurrentWidget(self.shezhi_page2)

        page_layout = self.shezhi_page2.layout()
        if not page_layout:
            print("CRITICAL ERROR: shezhi_page2 has no layout! Cannot add settings.")
            # Attempt to create a layout (though this indicates a deeper issue)
            page_layout = QVBoxLayout(self.shezhi_page2)
            self.shezhi_page2.setLayout(page_layout)
            print("WARNING: Dynamically added QVBoxLayout to shezhi_page2.")
            # If we added a layout, continue, otherwise return or raise error
            if not page_layout:
                print("CRITICAL ERROR: Failed to ensure layout for shezhi_page2.")
                return # Cannot proceed

        print(f"Initial page_layout count: {page_layout.count()}") # Debug

        # Call theme setup FIRST
        self._setup_theme_settings() # Adds theme frame at index 0 if needed
        print(f"Page_layout count after theme setup: {page_layout.count()}") # Debug
        theme_frame_widget = self.findChild(QFrame, "theme_frame") # Re-find after potential creation
        if theme_frame_widget:
             print(f"Theme frame found: visible={theme_frame_widget.isVisible()}, geometry={theme_frame_widget.geometry()}")
        else:
             print("Theme frame NOT found after setup.")


        # --- 添加浏览器选择控件 ---
        browser_frame = self.findChild(QFrame, "browser_settings_frame")

        if not browser_frame:
            print("Creating browser_settings_frame...")
            browser_frame = QFrame(self.shezhi_page2) # Parent is the page itself
            browser_frame.setObjectName("browser_settings_frame")
            # browser_frame.setStyleSheet("QFrame#browser_settings_frame { border: 1px solid lime; padding: 5px; }") # Debug style
            browser_layout = QHBoxLayout(browser_frame) # Layout for the frame
            browser_label = QLabel("链接打开方式:", browser_frame)
            self.browser_combo = QComboBox(browser_frame)
            self.browser_combo.addItems(["内置浏览器", "系统默认浏览器"])
            if self.browser_preference == "system":
                self.browser_combo.setCurrentIndex(1)
            else:
                self.browser_combo.setCurrentIndex(0)
            self.browser_combo.currentIndexChanged.connect(self.change_browser_preference)
            browser_layout.addWidget(browser_label)
            browser_layout.addWidget(self.browser_combo)
            browser_layout.addStretch()
            apply_shadow(self.browser_combo)

            # --- Simplified Add Widget Logic ---
            print(f"Adding NEW browser_settings_frame to page layout (at the end)") # Debug
            page_layout.addWidget(browser_frame)
            # --- End Simplified Add Widget Logic ---

        else:
            # Frame exists, update its value and ensure visibility
            print("browser_settings_frame already exists. Updating value and visibility.")
            if hasattr(self, 'browser_combo'):
                current_index = 1 if self.browser_preference == "system" else 0
                if self.browser_combo.currentIndex() != current_index:
                    try:
                        self.browser_combo.currentIndexChanged.disconnect(self.change_browser_preference)
                    except RuntimeError: pass
                    self.browser_combo.setCurrentIndex(current_index)
                    try:
                        self.browser_combo.currentIndexChanged.connect(self.change_browser_preference)
                    except RuntimeError: pass
            browser_frame.setVisible(True) # Ensure it's visible if it already exists

        # --- 加载端口号到输入框 (Load AFTER dynamic widgets are potentially added) ---
        if hasattr(self, 'dailikuang_2'):
            self.dailikuang_2.setText(str(self.ports.get('comfyui', '')))
        if hasattr(self, 'dailikuang_3'):
            self.dailikuang_3.setText(str(self.ports.get('fengzhuang', '')))
        if hasattr(self, 'dailikuang_4'):
            self.dailikuang_4.setText(str(self.ports.get('fluxgym', '')))
        if hasattr(self, 'dailikuang_6'): # 输出文件
            self.dailikuang_6.setText(str(self.ports.get('shuchu', '')))
        if hasattr(self, 'dailikuang_5'): # 全部文件
            self.dailikuang_5.setText(str(self.ports.get('quanbu', '')))

        # --- 添加浏览器选择控件 ---
        browser_frame = self.findChild(QFrame, "browser_settings_frame")
        page_layout = self.shezhi_page2.layout() # Get layout *after* theme setup potentially modified it

        if not page_layout:
            print("严重错误: 设置页面 (shezhi_page2) 没有布局。无法添加任何设置。")
            # Maybe try to add a default layout?
            # page_layout = QVBoxLayout(self.shezhi_page2)
            # self.shezhi_page2.setLayout(page_layout)
            # print("警告: 动态添加了 QVBoxLayout 到 shezhi_page2。")
            # If we added a layout, continue, otherwise return or raise error
            if not page_layout: return # Cannot proceed

        if not browser_frame:
            print("Creating browser_settings_frame...") # Debug
            browser_frame = QFrame(self.shezhi_page2)
            browser_frame.setObjectName("browser_settings_frame")
            # browser_frame.setStyleSheet("QFrame#browser_settings_frame { border: 1px solid red; padding: 5px; }") # Debug style
            browser_layout = QHBoxLayout(browser_frame)
            browser_label = QLabel("链接打开方式:", browser_frame)
            self.browser_combo = QComboBox(browser_frame)
            self.browser_combo.addItems(["内置浏览器", "系统默认浏览器"])
            # 根据加载的设置设置初始选项
            if self.browser_preference == "system":
                self.browser_combo.setCurrentIndex(1)
            else:
                self.browser_combo.setCurrentIndex(0)
            # 连接信号
            self.browser_combo.currentIndexChanged.connect(self.change_browser_preference)
            browser_layout.addWidget(browser_label)
            browser_layout.addWidget(self.browser_combo)
            browser_layout.addStretch()

            # --- Simplified Add Widget Logic ---
            print(f"Adding NEW browser_settings_frame to page layout (at the end)") # Debug
            page_layout.addWidget(browser_frame)
            # --- End Simplified Add Widget Logic ---

            apply_shadow(self.browser_combo)
        else:
            # Frame exists, update its value and ensure visibility
            print("browser_settings_frame already exists. Updating value and visibility.") # Debug
            if hasattr(self, 'browser_combo'):
                current_index = 1 if self.browser_preference == "system" else 0
                if self.browser_combo.currentIndex() != current_index:
                     # 临时断开信号避免触发保存
                     try:
                         self.browser_combo.currentIndexChanged.disconnect(self.change_browser_preference)
                     except RuntimeError: # 可能已经断开或从未连接
                         pass
                     self.browser_combo.setCurrentIndex(current_index)
                     # 重新连接信号
                     try:
                         self.browser_combo.currentIndexChanged.connect(self.change_browser_preference)
                     except RuntimeError: pass
            # Ensure the frame itself is visible
            browser_frame.setVisible(True)
            # Force layout update maybe?
            # page_layout.activate()
            # QApplication.processEvents()
            print(f"Existing browser_frame.isVisible(): {browser_frame.isVisible()}") # Debug
            print(f"Existing browser_frame.geometry(): {browser_frame.geometry()}") # Debug


    def load_config(self):
        """使用 QSettings 加载配置"""
        settings = QSettings()

        # 加载令牌
        saved_token = settings.value("api_token")
        remember_token = settings.value("remember_token", False, type=bool) # 指定类型和默认值

        if saved_token and remember_token:
            self.api_token = saved_token
            self.lingpai.setText(saved_token)
            self.radioButton.setChecked(True)
            self.statusbar.showMessage("已加载保存的访问令牌", 3000)
            self.api_handler.set_access_token(saved_token)
        else:
            self.radioButton.setChecked(False)
            self.api_token = None # 确保清除
            self.lingpai.clear() # 清空输入框

        # 加载自定义镜像列表
        loaded_images = settings.value("custom_public_images", []) # 提供默认空列表
        # QSettings 返回的可能是 QVariantList 或其他类型，需要确保是 Python list of dicts/strs
        if isinstance(loaded_images, list):
             # 进一步验证列表内容是否符合预期 (字典或字符串)
             self.custom_public_images = [img for img in loaded_images if isinstance(img, (dict, str))]
             if len(self.custom_public_images) != len(loaded_images):
                 print("警告：从 QSettings 加载的 custom_public_images 列表中包含无效类型的数据。")
        else:
             print(f"警告：从 QSettings 加载的 custom_public_images 类型不是 list: {type(loaded_images)}")
             self.custom_public_images = []


        # 加载端口配置
        loaded_ports = settings.value("ports", {}) # 提供默认空字典
        default_ports = {
            "comfyui": 8188, "fengzhuang": 7861, "fluxgym": 7860,
            "shuchu": 8080, "quanbu": 8081
        }
        self.ports = default_ports.copy()
        # 确保加载的是字典且值是整数
        if isinstance(loaded_ports, dict):
            valid_loaded_ports = {}
            for key, value in loaded_ports.items():
                # 尝试将值转换为整数，处理可能的类型问题
                try:
                    port_int = int(value)
                    if isinstance(key, str) and 0 < port_int < 65536: # 检查 key 类型和端口范围
                         valid_loaded_ports[key] = port_int
                    else:
                         print(f"警告：从 QSettings 加载的端口配置 '{key}': '{value}' 无效 (类型或范围错误)，已忽略。")
                except (ValueError, TypeError):
                     print(f"警告：从 QSettings 加载的端口值 '{key}': '{value}' 无法转换为整数，已忽略。")
            self.ports.update(valid_loaded_ports)
        else:
            print(f"警告：从 QSettings 加载的 ports 类型不是 dict: {type(loaded_ports)}")
            # 保留默认端口

        # 主题由 ThemeManager 单独加载，这里不再处理
        # theme = settings.value("theme", ThemeManager.System, type=int)
        # self.change_theme(theme)

        # 加载浏览器偏好设置
        self.browser_preference = settings.value("browser_preference", "integrated") # 默认内置
        print(f"加载的浏览器偏好: {self.browser_preference}")

        print("配置已从 QSettings 加载")

    def confirm_token(self):
        token = self.lingpai.text().strip()
        if not token:
            QMessageBox.warning(self, "输入错误", "请输入访问令牌")
            return
        self.api_token = token
        self.api_handler.set_access_token(token) # <--- 设置 Handler 的令牌
        self.statusbar.showMessage("访问令牌已设置", 3000)
        self.save_config() # <--- 保存配置 (包括令牌状态)
        self.get_user_info()
        self.get_balance()
        self.show_zhanghao_page() 

    def clear_token(self):
        self.lingpai.clear()
        self.api_token = None
        self.api_handler.set_access_token(None) # <--- 清除 Handler 的令牌
        self.radioButton.setChecked(False)
        self.save_config() # <--- 保存配置 (清除令牌状态)
        self.statusbar.showMessage("访问令牌已清除", 3000)
        self.listWidget.item(0).setText(" 昵称：")
        self.listWidget.item(1).setText(" uuid:")
        self.listWidget.item(2).setText(" 电话：")
        self.listWidget_2.item(0).setText(" 余额：")

    # --- 异步 API 调用封装 ---
    def _run_task(self, api_call, success_handler, error_handler=None, finished_handler=None, *args, **kwargs):
        """通用函数，用于在后台线程中运行 API 调用"""
        if not self.api_token:
            self.statusbar.showMessage("错误：请先设置访问令牌", 3000)
            if error_handler:
                error_handler("访问令牌未设置") # 调用错误处理
            return

        worker = Worker(api_call, *args, **kwargs)
        worker.signals.success.connect(success_handler)
        # 使用通用的错误处理或特定的错误处理
        worker.signals.error.connect(error_handler if error_handler else self._handle_api_error)
        if finished_handler:
            worker.signals.finished.connect(finished_handler)
        else:
            # 默认完成时从线程池移除
             worker.signals.finished.connect(lambda w=worker: self.thread_pool.remove(w) if w in self.thread_pool else None)


        self.thread_pool.append(worker) # 保留引用
        worker.start()
        return worker # 可以返回 worker 实例以便于管理 (例如取消)

    def _handle_api_error(self, error_message):
        """通用的 API 错误处理"""
        print(f"API Error Handler: {error_message}") # 调试信息
        QMessageBox.warning(self, "API 错误", f"操作失败: {error_message}")
        self.statusbar.showMessage(f"操作失败: {error_message}", 5000)
        # 可能需要在这里重置一些 UI 状态，例如重新启用按钮

    # --- 功能实现 (改为异步) ---
    def get_user_info(self):
        """异步获取用户信息"""
        self.statusbar.showMessage("正在获取用户信息...", 2000)
        self._run_task(self.api_handler.get_whoami, self._handle_get_user_info_success)

    def _handle_get_user_info_success(self, result):
        """处理获取用户信息成功的结果"""
        if result and result.get("success"):
            data = result.get("data", {})
            # 检查 data 是否存在且非空
            if data:
                self.listWidget.item(0).setText(f" 昵称：{data.get('nickname', 'N/A')}")
                self.listWidget.item(1).setText(f" uuid: {data.get('uuid', 'N/A')}")
                self.listWidget.item(2).setText(f" 电话：{data.get('phone', 'N/A')}")
                self.statusbar.showMessage("用户信息已更新", 3000)
            else:
                # 成功但没有数据？理论上不应发生，但也处理一下
                self.listWidget.item(0).setText(" 昵称：无数据")
                self.listWidget.item(1).setText(" uuid: 无数据")
                self.listWidget.item(2).setText(" 电话：无数据")
                self.statusbar.showMessage("成功获取用户信息，但数据为空", 3000)
        else:
            # 处理 API 调用失败或业务逻辑未成功的情况
            error_msg = result.get("msg", "无法获取用户信息") if result else "无法连接或获取响应" # 处理 result 为 None 的情况
            print(f"获取用户信息失败: {error_msg}") # 打印错误信息到控制台

            # --- 新增：根据错误消息判断原因 ---
            display_msg = f"获取用户信息失败: {error_msg}" # 默认显示原始错误
            error_msg_lower = error_msg.lower() # 转小写方便比较

            # 检查是否是网络相关错误 (关键词基于 api_handler._make_request 的错误返回)
            network_error_keywords = ["请求错误", "connection", "timeout", "dns", "network", "无法连接"]
            is_network_error = any(keyword in error_msg_lower for keyword in network_error_keywords)

            # 检查是否是令牌相关错误 (需要根据实际 API 返回调整关键词)
            # 常见的令牌错误关键词: token, 令牌, unauthorized, 认证失败, 登录失效, access token is not set (来自 api_handler)
            token_error_keywords = ["token", "令牌", "unauthorized", "认证失败", "登录失效", "access token is not set"]
            is_token_error = any(keyword in error_msg_lower for keyword in token_error_keywords)

            if is_token_error:
                display_msg = "获取用户信息失败：访问令牌无效、过期或未设置，请检查或重新输入令牌。"
            elif is_network_error:
                display_msg = "获取用户信息失败：网络连接错误，请检查网络连接或稍后再试。"
            # --- 结束新增判断 ---

            # 使用 display_msg 显示给用户
            self.statusbar.showMessage(display_msg, 5000)
            QMessageBox.warning(self, "获取失败", display_msg) # 同时弹窗提示

            # 清空或标记用户信息区域
            self.listWidget.item(0).setText(" 昵称：获取失败")
            self.listWidget.item(1).setText(" uuid: 获取失败")
            self.listWidget.item(2).setText(" 电话：获取失败")

    def get_balance(self):
        """异步获取账户余额"""
        self.statusbar.showMessage("正在获取账户余额...", 2000)
        self._run_task(self.api_handler.get_balance, self._handle_get_balance_success)

    def _handle_get_balance_success(self, result):
        """处理获取余额成功的结果"""
        if result and result.get("success"):
            data = result.get("data", {})
            balance_str = f"{data.get('balance', 0.0):.6f}"
            self.listWidget_2.item(0).setText(f" 余额：{balance_str}")
            self.statusbar.showMessage("账户余额已更新", 3000)
        else:
            error_msg = result.get("msg", "无法获取余额")
            print(f"获取余额失败: {error_msg}")
            self.statusbar.showMessage(f"获取余额失败: {error_msg}", 5000)
            self.listWidget_2.item(0).setText(" 余额：获取失败")


    def create_recharge_order(self):
        """异步创建充值订单"""
        # --- UI 交互部分（主线程）---
        amount = self.spinBox.value()
        if amount < 5:
            QMessageBox.warning(self, "金额错误", "充值金额不能低于 5 元")
            return
        payment = self.comboBox.currentText()

        # 禁用按钮，防止重复点击
        self.pushButton_2.setEnabled(False)
        self.statusbar.showMessage("正在创建充值订单...", 3000)

        # --- 后台任务 ---
        self._run_task(
            self.api_handler.create_recharge_order,
            self._handle_create_recharge_success,
            error_handler=self._handle_create_recharge_error, # 可以用通用错误处理，或自定义
            finished_handler=lambda: self.pushButton_2.setEnabled(True), # 结束后重新启用按钮
            amount=amount,
            payment=payment
        )

    def _handle_create_recharge_success(self, result):
        """处理创建充值订单成功的结果"""
        if result and result.get("success"):
            data = result.get("data", {})
            url = data.get('url')
            self.last_trade_no = data.get('trade_no')
            amount_returned = data.get('amount')
            payment_returned = data.get('payment')
            if not url:
                QMessageBox.warning(self, "订单信息不完整", "API 未返回支付信息 (URL/二维码内容)")
                return
            if payment_returned == 'wechat':
                try:
                    qr_img = qrcode.make(url)
                    buffer = io.BytesIO(); qr_img.save(buffer, "PNG"); buffer.seek(0)
                    qr_pixmap = QPixmap(); qr_pixmap.loadFromData(buffer.getvalue())
                    qr_dialog = QRCodeDialog(qr_pixmap, self); qr_dialog.exec()
                    self.statusbar.showMessage("请扫描微信二维码完成支付", 5000)
                except Exception as e:
                    QMessageBox.critical(self, "生成二维码错误", f"无法生成或显示微信支付二维码: {e}")
            elif payment_returned == 'alipay':
                reply = QMessageBox.information(self, "订单创建成功", f"订单创建成功！\n交易号: {self.last_trade_no}\n金额: {amount_returned}\n支付方式: {payment_returned}\n\n点击 'OK' 将打开支付页面。", QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                if reply == QMessageBox.StandardButton.Ok:
                    self.open_url(url)
            else:
                QMessageBox.warning(self, "未知支付方式", f"不支持的支付方式: {payment_returned}")
        else:
            error_msg = result.get("msg", "创建订单失败")
            QMessageBox.warning(self, "订单创建失败", error_msg)
            self.statusbar.showMessage(f"订单创建失败: {error_msg}", 5000)

    def _handle_create_recharge_error(self, error_message):
        """处理创建充值订单的特定错误（如果需要）"""
        QMessageBox.warning(self, "订单创建失败", f"创建充值订单时出错: {error_message}")
        self.statusbar.showMessage(f"订单创建失败: {error_message}", 5000)
        # 按钮已在 finished_handler 中重新启用


    def query_recharge_order(self):
        """异步查询充值订单"""
        # --- UI 交互部分（主线程）---
        if not self.last_trade_no:
            QMessageBox.information(self, "无法查询", "没有可查询的最近充值订单号。请先成功发起一笔充值。")
            return

        # 禁用按钮
        self.pushButton_4.setEnabled(False)
        self.statusbar.showMessage(f"正在查询订单 {self.last_trade_no}...", 2000)
        self.listWidget_4.clear()
        self.listWidget_4.addItem("正在查询...")

        # --- 后台任务 ---
        self._run_task(
            self.api_handler.query_recharge_order,
            self._handle_query_recharge_success,
            error_handler=self._handle_query_recharge_error,
            finished_handler=lambda: self.pushButton_4.setEnabled(True),
            trade_no=self.last_trade_no
        )

    def _handle_query_recharge_success(self, result):
        """处理查询充值订单成功的结果"""
        self.listWidget_4.clear() # 清除“正在查询...”
        if result: # 无论 success 是 True 或 False，都显示信息
            msg = result.get('msg', '无消息')
            success = result.get('success', False)
            code = result.get('code', 'N/A')
            status_text = f"状态: {msg} (Code: {code}, Success: {success})"
            self.listWidget_4.addItem(QListWidgetItem(status_text))
            order_data = result.get('data')
            if isinstance(order_data, dict):
                for key, value in order_data.items():
                    self.listWidget_4.addItem(QListWidgetItem(f"  {key}: {value}"))
            # 根据 success 状态显示不同的状态栏消息
            if success:
                self.statusbar.showMessage(f"订单 {self.last_trade_no} 查询完成", 3000)
            else:
                 self.statusbar.showMessage(f"订单 {self.last_trade_no} 查询信息: {msg}", 5000) # 显示 API 返回的消息
        # except requests.exceptions.RequestException as e: # <--- 移除 requests 异常处理
        #     QMessageBox.critical(self, "网络错误", f"查询订单时出错: {e}")
        #     self.listWidget_4.clear(); self.listWidget_4.addItem(QListWidgetItem(f"查询失败: {e}"))
        else:
            # 处理完全无法连接或 ApiHandler 返回 None 的情况
            QMessageBox.critical(self, "查询失败", f"查询订单时发生错误: {error_message}")
            self.listWidget_4.clear()
            self.listWidget_4.addItem(QListWidgetItem(f"查询失败: {error_message}"))
            self.statusbar.showMessage(f"订单查询失败: {error_message}", 5000)


    def open_url(self, url):
        """根据偏好设置打开 URL"""
        try:
            if self.browser_preference == "system":
                webbrowser.open(url)
                self.statusbar.showMessage(f"已在系统浏览器中打开链接", 3000)
            else: # 默认或 "integrated"
                # 确保共享浏览器存在
                if hasattr(self, 'shared_browser') and self.shared_browser:
                    self.body.setCurrentWidget(self.browser_page) # 切换到浏览器页面
                    self.shared_browser.open_url_in_new_tab(url) # 在新标签页打开
                    self.statusbar.showMessage(f"已在内置浏览器中打开链接", 3000)
                    # 更新左侧按钮状态 (如果是由按钮触发的)
                    sender_button = self.sender()
                    if isinstance(sender_button, QPushButton) and sender_button in self.left_buttons:
                         self.update_button_state(sender_button)
                else:
                    # Fallback to system browser if integrated one is not ready
                    print("警告: 内置浏览器未初始化，将使用系统浏览器打开。")
                    webbrowser.open(url)
                    self.statusbar.showMessage(f"内置浏览器不可用，已在系统浏览器中打开链接", 3000)

        except Exception as e:
            QMessageBox.critical(self, "打开链接错误", f"无法打开链接 {url}: {e}")
            self.statusbar.showMessage(f"打开链接失败: {e}", 5000)

    def show_sponsor_dialog(self):
        image_path = ":/ico/ico/zanzhu.jpg"
        dialog = ImageDialog(image_path, title="请作者喝咖啡", parent=self)
        dialog.exec()

    # --- 镜像页面相关方法 ---

    def _setup_jingxiang_page_layout(self):
        """初始化镜像页面的滚动布局"""
        old_layout = self.jingxiang_page7.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget: widget.deleteLater()
            QWidget().setLayout(old_layout)

        page_layout = QVBoxLayout(self.jingxiang_page7)
        page_layout.setContentsMargins(5, 5, 5, 5)
        page_layout.setSpacing(10)

        # 查找或创建 label_5
        self.label_5 = self.jingxiang_page7.findChild(QLabel, "label_5")
        if not self.label_5:
             self.label_5 = QLabel("镜像总数：0", self.jingxiang_page7)
             self.label_5.setObjectName("label_5") # 设置对象名以便将来查找
             self.label_5.setStyleSheet("QLabel { background-color: #3F454F; border-radius: 5px; padding: 5px; color: white; }")
        page_layout.addWidget(self.label_5)

        self.image_scroll_area = QScrollArea(self.jingxiang_page7)
        self.image_scroll_area.setWidgetResizable(True)
        self.image_scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        scroll_content_widget = QWidget()
        scroll_content_widget.setStyleSheet("QWidget { background-color: transparent; }")

        self.image_list_layout = QVBoxLayout(scroll_content_widget)
        self.image_list_layout.setContentsMargins(0, 0, 0, 0)
        self.image_list_layout.setSpacing(10)
        self.image_list_layout.addStretch()

        scroll_content_widget.setLayout(self.image_list_layout)
        self.image_scroll_area.setWidget(scroll_content_widget)
        page_layout.addWidget(self.image_scroll_area)
        # self.jingxiang_page7.setLayout(page_layout) # 这一步可能不需要，因为 page_layout 的 parent 已经是 jingxiang_page7


    # --- 公共镜像列表页面布局初始化 ---
    def _setup_list_jingxiang_page_layout(self):
        """初始化公共镜像列表页面的滚动布局和添加区域"""
        # 检查 list_jingxiang 页面是否存在
        if not hasattr(self, 'list_jingxiang') or not isinstance(self.list_jingxiang, QWidget):
            print("错误: UI 中未找到 list_jingxiang 页面。")
            widget = self.findChild(QWidget, "list_jingxiang")
            if widget:
                setattr(self, 'list_jingxiang', widget)
            else:
                QMessageBox.critical(self, "UI错误", "公共镜像页面 (list_jingxiang) 未在 UI 文件中定义。")
                return

        # 清理旧布局
        old_layout = self.list_jingxiang.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget: widget.deleteLater()
            QWidget().setLayout(old_layout)

        # 创建新主布局 (垂直)
        page_layout = QVBoxLayout(self.list_jingxiang)
        page_layout.setContentsMargins(10, 10, 10, 10) # 增加边距
        page_layout.setSpacing(10)

        # --- 添加自定义镜像区域 ---
        add_frame = QFrame(self.list_jingxiang)
        add_frame.setObjectName("add_custom_image_frame")
        add_frame.setStyleSheet("QFrame#add_custom_image_frame { background-color: #2d3848; border-radius: 8px; padding: 8px; }")
        add_layout = QHBoxLayout(add_frame)
        add_layout.setSpacing(10)

        self.custom_image_id_input = QLineEdit(add_frame) # 重命名 ID 输入框
        self.custom_image_id_input.setPlaceholderText("镜像 ID (必填)")
        self.custom_image_id_input.setStyleSheet("QLineEdit { background-color: #4a5568; border-radius: 5px; padding: 5px; color: white; }")
        add_layout.addWidget(self.custom_image_id_input, 1) # ID 输入框

        self.custom_image_name_input = QLineEdit(add_frame) # 新增名称输入框
        self.custom_image_name_input.setPlaceholderText("名称/说明 (可选)")
        self.custom_image_name_input.setStyleSheet("QLineEdit { background-color: #4a5568; border-radius: 5px; padding: 5px; color: white; }")
        add_layout.addWidget(self.custom_image_name_input, 1) # 名称输入框

        add_button = QPushButton("添加镜像", add_frame)
        add_button.setIcon(QIcon(":/ico/ico/plus-circle.svg"))
        add_button.setStyleSheet("QPushButton { background-color: #3182ce; border-radius: 5px; padding: 5px 10px; color: white; } QPushButton:hover { background-color: #2b6cb0; }")
        add_button.clicked.connect(self.add_custom_public_image)
        apply_shadow(add_button) # 为添加按钮添加阴影
        add_layout.addWidget(add_button)

        page_layout.addWidget(add_frame) # 添加到主布局顶部

        # --- 镜像列表滚动区域 ---
        self.public_image_scroll_area = QScrollArea(self.list_jingxiang)
        self.public_image_scroll_area.setWidgetResizable(True)
        self.public_image_scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        scroll_content_widget = QWidget()
        scroll_content_widget.setStyleSheet("QWidget { background-color: transparent; }")

        self.public_image_list_layout = QVBoxLayout(scroll_content_widget)
        self.public_image_list_layout.setContentsMargins(0, 0, 0, 0)
        self.public_image_list_layout.setSpacing(10)
        self.public_image_list_layout.addStretch() # 底部伸缩项

        scroll_content_widget.setLayout(self.public_image_list_layout)
        self.public_image_scroll_area.setWidget(scroll_content_widget)
        page_layout.addWidget(self.public_image_scroll_area) # 添加滚动区域到主布局

        # self.list_jingxiang.setLayout(page_layout) # 不需要，父对象已设置

    # --- 公共镜像相关方法 ---

    def _create_public_image_widget(self, image_data, is_custom=False):
        """为单个公共/社区镜像数据创建显示部件 (QFrame)"""
        # image_data 可以是字符串 (旧格式) 或字典 {'id': ..., 'name': ...}
        if isinstance(image_data, dict):
            image_id = image_data.get('id', 'N/A')
            image_name = image_data.get('name') # 可能为 None
        else: # 兼容旧的字符串列表格式
            image_id = str(image_data)
            image_name = None

        frame = QFrame()
        frame.setObjectName(f"public_image_frame_{image_id}")
        # 开发者预设和用户自定义的样式可以略有不同，或保持一致
        frame.setStyleSheet("QFrame { background-color: #2d3848; border-radius: 8px; border: 1px solid #4a5568; padding: 10px; }")
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame.setProperty("image_id", image_id) # 存储 ID 以便删除等操作

        layout = QHBoxLayout(frame) # 使用水平布局
        layout.setSpacing(10)

        # --- 左侧信息区 (ID 和可选的名称) ---
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        # 镜像 ID 标签
        id_label = QLabel(f"ID: {image_id}")
        id_label.setStyleSheet("color: white; font-size: 11pt;")
        id_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse) # 允许复制 ID
        info_layout.addWidget(id_label)

        # 如果有名称，显示名称标签
        if image_name:
            name_label = QLabel(f"名称: {image_name}")
            name_label.setStyleSheet("color: #a0aec0; font-size: 9pt;") # 灰色小字体
            name_label.setWordWrap(True) # 允许换行
            info_layout.addWidget(name_label)

        layout.addLayout(info_layout, 1) # 信息区占更多空间

        # --- 右侧按钮区 ---
        button_layout = QVBoxLayout() # 按钮垂直排列可能更好看？或者保持水平
        button_layout.setSpacing(5)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # 按钮靠上

        # 部署按钮
        deploy_button = QPushButton("部署")
        deploy_button.setIcon(QIcon(":/ico/ico/shopping-bag.svg"))
        deploy_button.setStyleSheet("QPushButton { background-color: #48bb78; border-radius: 5px; padding: 5px 10px; color: white; min-width: 60px; } QPushButton:hover { background-color: #38a169; } QPushButton:pressed { background-color: #2f855a; }")
        # --- 根据镜像 ID 和是否自定义设置默认镜像类型 ---
        default_image_type = "public" # 默认公共
        if image_id == "7b36c1a3-da41-4676-b5b3-03ec25d6e197":
            default_image_type = "community" # 开发者镜像默认社区
        elif is_custom:
            default_image_type = "public" # 用户添加的默认官方 (public)
        # --- 修改结束 ---
        deploy_button.clicked.connect(partial(self.show_deploy_dialog, image_id, default_image_type)) # 传递 ID 和计算出的类型
        apply_shadow(deploy_button) # 为部署按钮添加阴影
        layout.addWidget(deploy_button)

        # 删除按钮 (仅对用户自定义的镜像显示)
        if is_custom:
            delete_button = QPushButton("删除")
            delete_button.setIcon(QIcon(":/ico/ico/trash-2.svg"))
            delete_button.setStyleSheet("QPushButton { background-color: #e53e3e; border-radius: 5px; padding: 5px 10px; color: white; min-width: 60px; } QPushButton:hover { background-color: #c53030; } QPushButton:pressed { background-color: #9b2c2c; }")
            delete_button.clicked.connect(partial(self.delete_custom_public_image, image_id, frame))
            apply_shadow(delete_button) # 为删除按钮添加阴影
            layout.addWidget(delete_button)
        else:
            # 可以添加一个占位符或者留空，保持对齐
            layout.addStretch(0) # 添加一个小的伸缩项

        return frame

    def get_and_display_public_images(self):
        """加载并显示开发者预设和用户自定义的公共/社区镜像"""
        # 清空旧的镜像部件
        while self.public_image_list_layout.count() > 1: # 保留最后的 stretch item
            item = self.public_image_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # --- 开发者预设镜像 (硬编码) ---
        # !!! 请在这里添加开发者预设的公共/社区镜像 ID !!!
        developer_images = [
            {"id": "7b36c1a3-da41-4676-b5b3-03ec25d6e197", "description": "软件作者(推荐): h开发者的镜像 更新于 2025-03-31_160.86GB 镜像描述: free；永久免费，持续开发"},
            # {"id": "another-preset-id", "description": "另一个预设镜像描述"},
        ]

        # 显示开发者预设镜像
        for img_data in developer_images:
            # 可以创建一个更复杂的部件来显示描述信息，这里先用简单的
            desc_label = QLabel(img_data["description"])
            desc_label.setStyleSheet("color: #a0aec0; padding-left: 5px; font-size: 9pt;")
            desc_label.setWordWrap(True)
            self.public_image_list_layout.insertWidget(self.public_image_list_layout.count() - 1, desc_label)

            image_widget = self._create_public_image_widget(img_data["id"], is_custom=False) # is_custom=False
            self.public_image_list_layout.insertWidget(self.public_image_list_layout.count() - 1, image_widget)
            # 添加分隔线
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            line.setStyleSheet("color: #4a5568;")
            self.public_image_list_layout.insertWidget(self.public_image_list_layout.count() - 1, line)


        # --- 用户自定义镜像 ---
        if self.custom_public_images:
            custom_title = QLabel("--- 用户添加的镜像 ---")
            custom_title.setStyleSheet("color: #cbd5e0; font-size: 10pt; margin-top: 10px; margin-bottom: 5px;")
            custom_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.public_image_list_layout.insertWidget(self.public_image_list_layout.count() - 1, custom_title)

            # 遍历用户自定义镜像列表 (现在可能是字典列表或旧的字符串列表)
            for image_data in self.custom_public_images:
                # 传递整个 image_data (可能是 dict 或 str) 给创建函数
                image_widget = self._create_public_image_widget(image_data, is_custom=True)
                self.public_image_list_layout.insertWidget(self.public_image_list_layout.count() - 1, image_widget)
        else:
             no_custom_label = QLabel("您还没有添加自定义镜像", self.public_image_scroll_area.widget())
             no_custom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
             no_custom_label.setStyleSheet("color: #718096; margin-top: 10px;") # 灰色提示
             self.public_image_list_layout.insertWidget(self.public_image_list_layout.count() - 1, no_custom_label)


        self.statusbar.showMessage("公共镜像列表已加载", 3000)

    def add_custom_public_image(self):
        """添加用户输入的公共/社区镜像 ID 和名称"""
        image_id = self.custom_image_id_input.text().strip() # 使用新的 ID 输入框
        image_name = self.custom_image_name_input.text().strip() # 获取名称

        if not image_id:
            QMessageBox.warning(self, "输入错误", "镜像 ID 是必填项")
            return

        # 检查 ID 是否已存在 (包括开发者预设和用户自定义的)
        developer_ids = ["7b36c1a3-da41-4676-b5b3-03ec25d6e197"] # !!! 和上面保持一致 !!!
        # 检查用户自定义列表中的 ID
        existing_custom_ids = [img.get('id') for img in self.custom_public_images if isinstance(img, dict)]
        if image_id in existing_custom_ids or image_id in developer_ids:
            QMessageBox.information(self, "提示", f"镜像 ID '{image_id}' 已存在列表中")
            return

        # 创建新的镜像条目 (字典)
        new_image_entry = {"id": image_id}
        if image_name: # 如果用户输入了名称，则添加
            new_image_entry["name"] = image_name

        # 添加到列表并保存配置
        # 确保 self.custom_public_images 是列表
        if not isinstance(self.custom_public_images, list):
            self.custom_public_images = [] # 如果不是列表（例如旧配置是None），则初始化
        self.custom_public_images.append(new_image_entry)
        self.save_config()

        # 清空输入框并刷新列表
        self.custom_image_id_input.clear()
        self.custom_image_name_input.clear()
        self.get_and_display_public_images()
        self.statusbar.showMessage(f"已添加镜像 ID: {image_id}" + (f" (名称: {image_name})" if image_name else ""), 3000)

    def delete_custom_public_image(self, image_id, widget_to_remove):
        """删除用户添加的自定义镜像 ID"""
        reply = QMessageBox.question(self, "确认删除", f"您确定要从列表中删除镜像 ID '{image_id}' 吗？\n（这不会销毁实际镜像，只是从您的收藏中移除）",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # 查找要删除的镜像条目
            image_to_remove = None
            # 确保 self.custom_public_images 是列表
            if not isinstance(self.custom_public_images, list):
                self.custom_public_images = []

            for img_data in self.custom_public_images:
                current_id = None
                if isinstance(img_data, dict):
                    current_id = img_data.get('id')
                elif isinstance(img_data, str): # 兼容旧格式
                    current_id = img_data

                if current_id == image_id:
                    image_to_remove = img_data
                    break

            if image_to_remove is not None:
                self.custom_public_images.remove(image_to_remove)
                self.save_config()
                # 从布局中移除部件
                self.public_image_list_layout.removeWidget(widget_to_remove)
                widget_to_remove.deleteLater()
                self.statusbar.showMessage(f"已删除自定义镜像 ID: {image_id}", 3000)
                # 如果删除的是最后一个自定义镜像，可能需要刷新以显示提示信息
                if not self.custom_public_images:
                    self.get_and_display_public_images()
            else:
                QMessageBox.warning(self, "错误", f"无法找到要删除的镜像 ID: {image_id}")


    # --- 实例页面布局初始化 ---
    def _setup_shili_page_layout(self):
        """初始化实例页面的滚动布局"""
        # 检查 shili_page6 是否存在并且是 QWidget
        if not hasattr(self, 'shili_page6') or not isinstance(self.shili_page6, QWidget):
             print("错误: UI 中未找到 shili_page6 或类型不正确。")
             # 尝试从 UI 对象查找 shili_page6
             widget = self.findChild(QWidget, "shili_page6")
             if widget:
                 setattr(self, 'shili_page6', widget)
             else:
                 QMessageBox.critical(self, "UI错误", "实例页面 (shili_page6) 未在 UI 文件中定义。")
                 return # 无法继续

        # 清理旧布局
        old_layout = self.shili_page6.layout()
        if old_layout:
            # 安全地移除和删除旧布局中的所有部件
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            # 删除旧布局本身
            QWidget().setLayout(old_layout) # 将旧布局设置给临时QWidget以删除

        # 创建新布局
        page_layout = QVBoxLayout(self.shili_page6) # 直接将 shili_page6 作为父对象
        page_layout.setContentsMargins(5, 5, 5, 5)
        page_layout.setSpacing(10)

        # 实例计数标签 (可以稍后添加或查找)
        self.instance_count_label = QLabel("实例总数：0", self.shili_page6)
        self.instance_count_label.setObjectName("instance_count_label")
        self.instance_count_label.setStyleSheet("QLabel { background-color: #3F454F; border-radius: 5px; padding: 5px; color: white; }")
        page_layout.addWidget(self.instance_count_label)

        # 滚动区域
        self.instance_scroll_area = QScrollArea(self.shili_page6)
        self.instance_scroll_area.setWidgetResizable(True)
        self.instance_scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # 滚动区域内容部件
        scroll_content_widget = QWidget()
        scroll_content_widget.setStyleSheet("QWidget { background-color: transparent; }")

        # 实例列表布局 (垂直)
        self.instance_list_layout = QVBoxLayout(scroll_content_widget)
        self.instance_list_layout.setContentsMargins(0, 0, 0, 0)
        self.instance_list_layout.setSpacing(10)
        self.instance_list_layout.addStretch() # 添加伸缩项到底部

        scroll_content_widget.setLayout(self.instance_list_layout)
        self.instance_scroll_area.setWidget(scroll_content_widget)
        page_layout.addWidget(self.instance_scroll_area)

        # self.shili_page6.setLayout(page_layout) # 这一步是多余的，因为 page_layout 的 parent 已经是 shili_page6

    def _create_image_widget(self, image_data):
        """为单个镜像数据创建显示部件 (QFrame)"""
        image_id = image_data.get('id', 'N/A')
        image_name = image_data.get('name', 'N/A')
        image_size_bytes = image_data.get('size', 0)
        image_status = image_data.get('status', 'N/A')
        is_original = image_data.get('original_owner', False)
        create_timestamp = image_data.get('create_timestamp')
        # 尝试获取 image_type，如果 API 没返回，给个默认值或标记
        image_type = image_data.get('image_type', 'private') # 假设默认为 private

        frame = QFrame()
        frame.setObjectName(f"image_frame_{image_id}")
        frame.setStyleSheet("QFrame { background-color: #2d3848; border-radius: 10px; border: 1px solid #4a5568; padding: 8px; }")
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame.setProperty("image_id", image_id) # 存储 ID 以便后续操作

        layout = QVBoxLayout(frame)
        layout.setSpacing(5)

        list_widget = QListWidget()
        list_widget.setStyleSheet("QListWidget { border: none; background-color: transparent; color: white; }")
        list_widget.setSpacing(2)

        size_gb = f"{image_size_bytes / (1024**3):.2f} GB" if image_size_bytes else "N/A"
        create_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(create_timestamp)) if create_timestamp else "N/A"
        owner_str = "是" if is_original else "否"

        list_widget.addItem(f"   镜像ID：{image_id}")
        list_widget.addItem(f"镜像名字：{image_name}")
        list_widget.addItem(f"镜像大小：{size_gb}")
        list_widget.addItem(f"可用状态：{image_status}")
        list_widget.addItem(f"是否原主：{owner_str}")
        list_widget.addItem(f"创建时间：{create_time_str}")

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
        # 移除固定高度设置，让 QListWidget 自适应内容高度
        # list_widget.setFixedHeight(list_widget.sizeHintForRow(0) * list_widget.count() + 10)
        layout.addWidget(list_widget)

        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 5, 0, 0)
        button_layout.setSpacing(10)
        button_frame.setStyleSheet("QFrame { border: none; background: transparent; }")

        destroy_button = QPushButton("销毁镜像")
        destroy_button.setIcon(QIcon(":/ico/ico/x-octagon.svg"))
        destroy_button.setStyleSheet("QPushButton { background-color: #e53e3e; border-radius: 5px; padding: 5px 10px; color: white; } QPushButton:hover { background-color: #c53030; } QPushButton:pressed { background-color: #9b2c2c; }")
        # 使用 partial 来传递参数，避免 lambda 作用域问题
        destroy_button.clicked.connect(partial(self.destroy_image, image_id, frame))
        apply_shadow(destroy_button) # 添加阴影
        button_layout.addWidget(destroy_button, alignment=Qt.AlignmentFlag.AlignLeft)

        button_layout.addStretch()

        deploy_button = QPushButton("部署此镜像")
        deploy_button.setIcon(QIcon(":/ico/ico/shopping-bag.svg"))
        deploy_button.setStyleSheet("QPushButton { background-color: #48bb78; border-radius: 5px; padding: 5px 10px; color: white; } QPushButton:hover { background-color: #38a169; } QPushButton:pressed { background-color: #2f855a; }")
        # 传递 image_type
        deploy_button.clicked.connect(partial(self.show_deploy_dialog, image_id, image_type))
        apply_shadow(deploy_button) # 添加阴影
        button_layout.addWidget(deploy_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(button_frame)
        # frame.setLayout(layout) # QVBoxLayout 的 parent 已经是 frame，不需要再设置
        return frame

    # --- 异步获取和显示镜像 ---
    def get_and_display_images_async(self):
        """异步获取镜像列表并更新 UI"""
        if self.is_refreshing_images:
            print("获取镜像列表 - 跳过（正在刷新）")
            return
        if not self.api_token:
            # 如果没有 token，清空列表并提示 (主线程安全)
            while self.image_list_layout.count() > 1:
                item = self.image_list_layout.takeAt(0)
                widget = item.widget()
                if widget: widget.deleteLater()
            if hasattr(self, 'label_5'): self.label_5.setText("镜像总数：0 (请先设置令牌)")
            return

        self.is_refreshing_images = True # 设置刷新标志
        self.statusbar.showMessage("正在获取镜像列表...", 0) # 持续显示直到完成或错误

        # 注意：清空列表的操作已移动到 _handle_get_images_success

        self._run_task(
            self.api_handler.get_images,
            self._handle_get_images_success,
            error_handler=self._handle_get_images_error,
            finished_handler=self._handle_get_images_finished
        )

    def _handle_get_images_success(self, result):
        """处理获取镜像成功的结果 (在主线程中更新 UI)"""
        # --- 在添加新内容前，清空旧的镜像部件 ---
        while self.image_list_layout.count() > 1: # 保留最后的 stretch item
            item = self.image_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # --- 清空结束 ---

        if result and result.get("success"):
            data = result.get("data", {})
            images = data.get('list', [])
            total = data.get('total', len(images))

            if hasattr(self, 'label_5'):
                 self.label_5.setText(f"镜像总数：{total}")

            if not images:
                 no_image_label = QLabel("您还没有任何镜像。", self.image_scroll_area.widget())
                 no_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                 no_image_label.setStyleSheet("color: #a0aec0;") # 灰色提示
                 self.image_list_layout.insertWidget(self.image_list_layout.count() - 1, no_image_label)
                 self.statusbar.showMessage("未找到镜像", 3000)
            else:
                for image_data in images:
                    image_widget = self._create_image_widget(image_data)
                    self.image_list_layout.insertWidget(self.image_list_layout.count() - 1, image_widget)
                self.statusbar.showMessage(f"成功加载 {len(images)} 个镜像", 3000)
        else:
            # API 请求成功但业务逻辑失败
            error_msg = result.get("msg", "获取镜像列表失败") if result else "未知错误"
            self._handle_get_images_error(error_msg) # 调用错误处理

    def _handle_get_images_error(self, error_message):
        """处理获取镜像列表时的错误 (主线程)"""
        print(f"获取镜像列表错误: {error_message}")
        # 清空加载提示和旧内容
        while self.image_list_layout.count() > 1:
            item = self.image_list_layout.takeAt(0)
            widget = item.widget()
            if widget: widget.deleteLater()

        if hasattr(self, 'label_5'):
             self.label_5.setText("镜像总数：获取失败")
        error_label = QLabel(f"无法加载镜像列表: {error_message}", self.image_scroll_area.widget())
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("color: #f56565;") # 红色错误提示
        self.image_list_layout.insertWidget(self.image_list_layout.count() - 1, error_label)
        self.statusbar.showMessage(f"获取镜像列表失败: {error_message}", 5000)

    def _handle_get_images_finished(self):
        """获取镜像列表任务完成后的处理 (主线程)"""
        self.is_refreshing_images = False # 清除刷新标志
        # 从线程池移除 worker (如果 _run_task 中没有设置 finished_handler)
        sender_worker = self.sender().parent() # QSignalMapper or Worker itself? Let's assume Worker
        if isinstance(sender_worker, Worker) and sender_worker in self.thread_pool:
             self.thread_pool.remove(sender_worker)
        print("获取镜像列表任务完成")


    def destroy_image(self, image_id, widget_to_remove):
        """异步销毁指定 ID 的镜像"""
        reply = QMessageBox.question(self, "确认销毁", f"您确定要销毁镜像 {image_id} 吗？此操作不可恢复！",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel, # Use Cancel for safety
                                     QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Yes:
            # 禁用相关按钮 (如果能找到的话)
            widget_to_remove.setEnabled(False) # 禁用整个卡片
            self.statusbar.showMessage(f"正在提交销毁镜像 {image_id} 请求...", 0)

            self._run_task(
                self.api_handler.destroy_image,
                # 使用 partial 传递额外参数给成功处理器
                partial(self._handle_destroy_image_success, image_id=image_id, widget_to_remove=widget_to_remove),
                # 使用 partial 传递额外参数给错误处理器
                partial(self._handle_destroy_image_error, image_id=image_id, widget_to_remove=widget_to_remove),
                image_id=image_id # 参数传递给 api_handler.destroy_image
            )

    def _handle_destroy_image_success(self, result, image_id, widget_to_remove):
        """处理销毁镜像成功的结果"""
        if result and result.get("success"):
            success_msg = result.get("msg", f"镜像 {image_id} 已成功销毁。")
            QMessageBox.information(self, "销毁成功", success_msg)
            # 从布局中移除并删除部件
            self.image_list_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
            self.statusbar.showMessage(f"镜像 {image_id} 已销毁", 3000)
            # 重新获取列表以更新总数和列表状态
            self.get_and_display_images_async()
        else:
            # API 调用成功但业务逻辑失败
            error_msg = result.get("msg", "销毁失败") if result else "未知错误"
            self._handle_destroy_image_error(error_msg, image_id, widget_to_remove)

    def _handle_destroy_image_error(self, error_message, image_id, widget_to_remove):
        """处理销毁镜像失败"""
        QMessageBox.warning(self, "销毁失败", f"无法销毁镜像 {image_id}: {error_message}")
        self.statusbar.showMessage(f"销毁镜像 {image_id} 失败", 5000)
        widget_to_remove.setEnabled(True) # 重新启用卡片

    def show_deploy_dialog(self, image_id, image_type):
        """显示部署镜像对话框"""
        dialog = DeployImageDialog(image_id, image_type, self)
        # dialog.exec() 会阻塞直到对话框关闭
        # 部署逻辑已在 DeployImageDialog 的 handle_normal_deploy 或 on_deploy_success (抢占) 中处理
        # 因此这里不需要再调用 deploy_image_async
        dialog.exec()

    def deploy_image_async(self, deploy_data):
        """异步调用 API 部署镜像"""
        image_id_to_deploy = deploy_data.get('image')
        self.statusbar.showMessage(f"正在提交部署镜像 {image_id_to_deploy} 请求...", 0)
        # 这里可以考虑禁用触发部署的按钮，但按钮在对话框关闭后可能已不存在
        # 如果是从列表部署，可以禁用对应的部署按钮

        self._run_task(
            self.api_handler.deploy_instance,
            partial(self._handle_deploy_image_success, image_id=image_id_to_deploy),
            partial(self._handle_deploy_image_error, image_id=image_id_to_deploy),
            deploy_data=deploy_data
        )

    def _handle_deploy_image_success(self, result, image_id):
        """处理部署镜像成功"""
        if result and result.get("success"):
            data = result.get("data", {})
            instance_id = data.get('id')
            if instance_id:
                QMessageBox.information(self, "部署成功", f"镜像 {image_id} 已成功部署！\n实例 ID: {instance_id}")
                self.statusbar.showMessage(f"实例 {instance_id} 部署成功", 3000)
                # 部署成功后切换到实例页面并异步刷新
                self.show_shili_page() # show_shili_page 内部会调用异步刷新
            else:
                # 成功但未返回 ID？
                 QMessageBox.warning(self, "部署部分成功", f"镜像 {image_id} 部署请求成功，但未返回实例ID。请稍后在实例列表查看。")
                 self.statusbar.showMessage(f"镜像 {image_id} 部署请求成功，但未返回实例ID", 5000)
                 self.show_shili_page() # 仍然切换并刷新
            # --- 触发刷新信号 ---
            self.instance_deployed_signal.emit()
        else:
            # API 调用成功但业务逻辑失败
            error_msg = result.get("msg", "部署失败") if result else "未知错误"
            self._handle_deploy_image_error(error_msg, image_id)

    def _handle_deploy_image_error(self, error_message, image_id):
        """处理部署镜像失败 (包括普通部署和抢占部署的错误)"""
        # 检查错误消息是否指示 GPU 不足或其他资源不足
        # 注意：这里的关键词需要根据实际 API 返回的错误信息进行调整
        resource_error_keywords = ["GPU不足", "gpu insufficient", "资源不足", "insufficient resource", "no available gpu"]
        is_resource_error = any(keyword.lower() in error_message.lower() for keyword in resource_error_keywords)

        # 检查是否是抢占任务中的错误 (通过查找调用栈或传递标志位，这里简化处理，假设所有错误都可能来自抢占)
        # is_from_grab_task = ... # 实际应用中可能需要更精确的判断

        if is_resource_error:
            # 如果是资源不足错误，只显示 API 返回的错误信息
            # 对于抢占任务，这种错误是预期的，不需要弹窗，状态栏已更新
            # 对于普通部署，需要弹窗提示
            # if not is_from_grab_task: # 简化：总是弹窗，除非是抢占任务的特定处理
            display_message = f"实例 {image_id} 部署失败: {error_message}"
            QMessageBox.warning(self, "部署失败", display_message)
        else:
            # 其他错误，显示包含额外提示的错误信息
            display_message = f"实例 {image_id} 部署失败: {error_message}\n(可能原因: 镜像类型选择错误、镜像ID不正确或API内部错误)"
            QMessageBox.warning(self, "部署失败", display_message)

        self.statusbar.showMessage(f"部署镜像 {image_id} 失败: {error_message}", 5000) # 状态栏仍然显示原始错误信息
        # 如果是从列表部署，需要重新启用按钮 (这部分逻辑可能需要根据实际情况调整)
        # 如果是抢占任务失败，UI 重置由 GpuGrabWorker 的 finished 信号处理

    # --- 实例页面相关方法 ---

    def _create_instance_widget(self, instance_data):
        """为单个实例数据创建显示部件 (QFrame) - 水平布局"""
        instance_id = instance_data.get('id', 'N/A')
        instance_name = instance_data.get('name') or f"实例 {instance_id[:6]}..." # 如果没有名字，显示部分ID
        status = instance_data.get('status', 'N/A')
        gpu_model = instance_data.get('gpu_model', 'N/A')
        gpu_used = instance_data.get('gpu_used', 'N/A')
        cpu_model = instance_data.get('cpu_model', 'N/A')
        cpu_cores = instance_data.get('cpu_core_count', 'N/A')
        memory_bytes = instance_data.get('memory_size', 0)
        memory_gb = f"{memory_bytes / (1024**3):.1f} GB" if memory_bytes else "N/A"
        system_disk_bytes = instance_data.get('system_disk_size', 0)
        system_disk_gb = f"{system_disk_bytes / (1024**3):.1f} GB" if system_disk_bytes else "N/A"
        data_disk_bytes = instance_data.get('data_disk_size', 0)
        data_disk_gb = f"{data_disk_bytes / (1024**3):.1f} GB" if data_disk_bytes else "N/A"
        price = instance_data.get('price_per_hour', 'N/A')
        ssh_domain = instance_data.get('ssh_domain', 'N/A')
        ssh_port = instance_data.get('ssh_port', 'N/A')
        ssh_user = instance_data.get('ssh_user', 'N/A')
        password = instance_data.get('password', 'N/A') # 注意：显示密码可能不安全
        jupyter_url = instance_data.get('jupyter_url', 'N/A')
        web_url = instance_data.get('web_url', 'N/A')
        data_center = instance_data.get('data_center_name', 'N/A')
        create_time_ts = instance_data.get('create_timestamp')
        create_time_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(create_time_ts)) if create_time_ts else "N/A"
        start_time_ts = instance_data.get('start_timestamp')
        start_time_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(start_time_ts)) if start_time_ts else "N/A"

        # --- 主框架 ---
        frame = QFrame()
        frame.setObjectName(f"instance_frame_{instance_id}")
        frame.setStyleSheet("""
            QFrame {
                background-color: #2C3E50; /* 深蓝灰色背景 */
                border-radius: 10px;
                border: 1px solid #34495E; /* 稍深边框 */
                padding: 10px;
                color: #ECF0F1; /* 浅灰色文字 */
            }
            QLabel {
                background-color: transparent; /* 标签背景透明 */
                color: #ECF0F1;
                padding: 2px;
            }
            QPushButton {
                border-radius: 5px;
                padding: 6px 12px;
                font-size: 10pt; /* 稍小字体 */
                color: white;
                min-width: 80px; /* 按钮最小宽度 */
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 0.8;
            }
            QListWidget {
                background-color: #34495E; /* 列表背景稍深 */
                border: 1px solid #4A617A;
                border-radius: 5px;
                color: #ECF0F1;
                padding: 5px;
            }
            QListWidget::item {
                 padding: 3px 0px; /* 列表项垂直间距 */
            }
        """)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame.setProperty("instance_id", instance_id) # 存储 ID

        # --- 水平主布局 ---
        main_h_layout = QHBoxLayout(frame)
        main_h_layout.setSpacing(15)

        # --- 左侧信息区 (垂直布局) ---
        left_v_layout = QVBoxLayout()
        left_v_layout.setSpacing(5)

        # 实例名和状态
        name_status_layout = QHBoxLayout()
        name_label = QLabel(f"<b>{instance_name}</b>")
        name_label.setStyleSheet("font-size: 14pt;")
        status_label = QLabel(f"({status})")
        status_color = "#2ECC71" if status == "running" else ("#F39C12" if status == "starting" or status == "stopping" else "#E74C3C") # 绿/橙/红
        status_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")
        name_status_layout.addWidget(name_label)
        name_status_layout.addWidget(status_label)
        name_status_layout.addStretch()
        left_v_layout.addLayout(name_status_layout)

        # 详细信息 ListWidget
        details_list = QListWidget()
        details_list.addItem(f"ID: {instance_id}")
        details_list.addItem(f"区域: {data_center}")
        details_list.addItem(f"GPU: {gpu_used}x {gpu_model}")
        details_list.addItem(f"CPU: {cpu_cores}核 {cpu_model}")
        details_list.addItem(f"内存: {memory_gb}")
        details_list.addItem(f"系统盘: {system_disk_gb}")
        if data_disk_gb != "N/A" and data_disk_gb != "0.0 GB":
             details_list.addItem(f"数据盘: {data_disk_gb}")
        details_list.addItem(f"价格: {price} 元/小时")
        details_list.addItem(f"创建时间: {create_time_str}")
        if status == "running":
             details_list.addItem(f"开机时间: {start_time_str}")
        # 禁用选择和交互
        for i in range(details_list.count()):
            item = details_list.item(i)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
        details_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) # 水平扩展
        left_v_layout.addWidget(details_list)

        # SSH 和 URL 信息
        conn_info_layout = QFormLayout()
        conn_info_layout.setSpacing(5)
        if ssh_domain and ssh_port:
             ssh_label = QLabel(f"{ssh_user}@{ssh_domain}:{ssh_port}")
             ssh_copy_btn = QPushButton("复制SSH")
             ssh_copy_btn.setIcon(QIcon(":/ico/ico/copy.svg"))
             ssh_copy_btn.setStyleSheet("background-color: #3498DB;") # 蓝色
             ssh_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(f"ssh {ssh_user}@{ssh_domain} -p {ssh_port}", "SSH 命令"))
             apply_shadow(ssh_copy_btn) # 添加阴影
             conn_info_layout.addRow("SSH:", ssh_label)
             conn_info_layout.addRow("", ssh_copy_btn) # 按钮单独一行
        if password != 'N/A': # 仅当有密码时显示
             pwd_label = QLabel("******") # 隐藏密码
             pwd_copy_btn = QPushButton("复制密码")
             pwd_copy_btn.setIcon(QIcon(":/ico/ico/key.svg"))
             pwd_copy_btn.setStyleSheet("background-color: #3498DB;")
             pwd_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(password, "密码"))
             apply_shadow(pwd_copy_btn) # 添加阴影
             conn_info_layout.addRow("密码:", pwd_label)
             conn_info_layout.addRow("", pwd_copy_btn)
        if jupyter_url != 'N/A':
             jupyter_btn = QPushButton("Jupyter")
             jupyter_btn.setIcon(QIcon(":/ico/ico/link.svg"))
             jupyter_btn.setStyleSheet("background-color: #F39C12;") # 橙色
             jupyter_btn.clicked.connect(lambda: self.open_url(jupyter_url))
             apply_shadow(jupyter_btn) # 添加阴影
             conn_info_layout.addRow("链接:", jupyter_btn) # 简化标签
        if web_url != 'N/A':
             web_btn = QPushButton("Web UI")
             web_btn.setIcon(QIcon(":/ico/ico/globe.svg"))
             web_btn.setStyleSheet("background-color: #F39C12;")
             web_btn.clicked.connect(lambda: self.open_url(web_url))
             apply_shadow(web_btn) # 添加阴影
             conn_info_layout.addRow("", web_btn) # 添加到链接行

        left_v_layout.addLayout(conn_info_layout)
        left_v_layout.addStretch() # 把信息推到顶部

        main_h_layout.addLayout(left_v_layout, 2) # 左侧占 2/3 空间

        # --- 分隔线 ---
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("color: #4A617A;")
        main_h_layout.addWidget(line)

        # --- 右侧按钮区 (垂直布局) ---
        right_v_layout = QVBoxLayout()
        right_v_layout.setSpacing(8)
        right_v_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # 按钮靠上对齐

        # 按钮样式
        btn_boot_style = "background-color: #2ECC71; color: white;" # 绿色
        btn_save_style = "background-color: #3498DB; color: white;" # 蓝色
        btn_shutdown_style = "background-color: #E67E22; color: white;" # 橙色
        btn_destroy_style = "background-color: #E74C3C; color: white;" # 红色
        btn_disabled_style = "background-color: #95A5A6; color: #BDC3C7;" # 灰色 (禁用)

        # --- 创建按钮 ---
        # 开机按钮 (pushButton_6 在 ui_demo.py 中可能不存在，我们动态创建)
        btn_boot = QPushButton("开机")
        btn_boot.setObjectName(f"pushButton_6_{instance_id}") # 使用唯一对象名
        btn_boot.setIcon(QIcon(":/ico/ico/power.svg"))
        btn_boot.setStyleSheet(btn_boot_style)
        # --- 修改连接，传递 gpu_count (假设 API 返回的是 gpu_count 或 gpu_used) ---
        # 注意：需要确认 instance_data 中 gpu 数量的实际字段名
        current_gpu_count = instance_data.get('gpu_count', instance_data.get('gpu_used')) # 尝试获取 gpu_count 或 gpu_used
        btn_boot.clicked.connect(partial(self.handle_boot_click, instance_id, gpu_model, current_gpu_count))
        apply_shadow(btn_boot) # 添加阴影
        right_v_layout.addWidget(btn_boot)

        # 储存镜像按钮 (pushButton_7)
        btn_save_image = QPushButton("储存为镜像")
        btn_save_image.setObjectName(f"pushButton_7_{instance_id}")
        btn_save_image.setIcon(QIcon(":/ico/ico/save.svg"))
        btn_save_image.setStyleSheet(btn_save_style)
        btn_save_image.clicked.connect(partial(self.save_instance_image, instance_id))
        apply_shadow(btn_save_image) # 添加阴影
        right_v_layout.addWidget(btn_save_image)

        # 关机保留GPU按钮 (pushButton_10)
        btn_shutdown_keep = QPushButton("关机并保留GPU")
        btn_shutdown_keep.setObjectName(f"pushButton_10_{instance_id}")
        btn_shutdown_keep.setIcon(QIcon(":/ico/ico/pause-circle.svg"))
        btn_shutdown_keep.setStyleSheet(btn_shutdown_style)
        btn_shutdown_keep.clicked.connect(partial(self.shutdown_instance_keep_gpu, instance_id))
        apply_shadow(btn_shutdown_keep) # 添加阴影
        right_v_layout.addWidget(btn_shutdown_keep)

        # 关机释放GPU按钮 (pushButton_9)
        btn_shutdown_release = QPushButton("关机并释放GPU")
        btn_shutdown_release.setObjectName(f"pushButton_9_{instance_id}")
        btn_shutdown_release.setIcon(QIcon(":/ico/ico/stop-circle.svg"))
        btn_shutdown_release.setStyleSheet(btn_shutdown_style)
        btn_shutdown_release.clicked.connect(partial(self.shutdown_instance_release_gpu, instance_id))
        apply_shadow(btn_shutdown_release) # 添加阴影
        right_v_layout.addWidget(btn_shutdown_release)

        # 关机并销毁按钮 (pushButton_8)
        btn_shutdown_destroy = QPushButton("关机并销毁实例")
        btn_shutdown_destroy.setObjectName(f"pushButton_8_{instance_id}")
        btn_shutdown_destroy.setIcon(QIcon(":/ico/ico/trash-2.svg"))
        btn_shutdown_destroy.setStyleSheet(btn_destroy_style)
        btn_shutdown_destroy.clicked.connect(partial(self.shutdown_instance_destroy, instance_id))
        apply_shadow(btn_shutdown_destroy) # 添加阴影
        right_v_layout.addWidget(btn_shutdown_destroy)

        # 储存并销毁按钮 (pushButton_13)
        btn_save_destroy = QPushButton("储存为镜像并销毁实例")
        btn_save_destroy.setObjectName(f"pushButton_13_{instance_id}")
        btn_save_destroy.setIcon(QIcon(":/ico/ico/archive.svg"))
        btn_save_destroy.setStyleSheet(btn_destroy_style)
        btn_save_destroy.clicked.connect(partial(self.save_image_and_destroy, instance_id))
        apply_shadow(btn_save_destroy) # 添加阴影
        right_v_layout.addWidget(btn_save_destroy)

        # 销毁实例按钮 (pushButton_11)
        btn_destroy = QPushButton("直接销毁实例")
        btn_destroy.setObjectName(f"pushButton_11_{instance_id}")
        btn_destroy.setIcon(QIcon(":/ico/ico/x-octagon.svg"))
        btn_destroy.setStyleSheet(btn_destroy_style)
        btn_destroy.clicked.connect(partial(self.destroy_instance_action, instance_id, frame)) # 传递 frame 以便移除
        apply_shadow(btn_destroy) # 添加阴影
        right_v_layout.addWidget(btn_destroy)

        # --- 根据实例状态启用/禁用按钮 ---
        # 转换为小写以便进行不区分大小写的比较
        status_lower = status.lower()
        print(f"Instance {instance_id}: Status received = '{status}', Lowercase = '{status_lower}'") # 调试打印

        # 定义可运行和可开机的状态列表
        running_statuses = ['running', 'starting', 'rebooting', '运行中', '启动中', '重启中', '开机中', '工作中']
        # 扩展可开机的状态列表
        bootable_statuses = ['stopped', 'shutdown', '已关机', '关机', 'off', '关机保留磁盘', '已停止']
        # 定义可能表示正在进行操作的状态 (通常禁用大多数按钮)
        pending_statuses = ['saving', 'destroying', 'pending', '处理中', '保存中', '销毁中']

        is_running = status_lower in running_statuses
        is_bootable = status_lower in bootable_statuses
        is_pending = status_lower in pending_statuses

        print(f"  - is_running: {is_running}, is_bootable: {is_bootable}, is_pending: {is_pending}") # 调试打印

        # 设置按钮的启用状态
        btn_boot.setEnabled(is_bootable and not is_pending)
        btn_save_image.setEnabled(is_bootable and not is_pending) # 假设关机状态下可以保存镜像
        btn_shutdown_keep.setEnabled(is_running and not is_pending)
        btn_shutdown_release.setEnabled(is_running and not is_pending)
        btn_shutdown_destroy.setEnabled(is_running and not is_pending)
        btn_save_destroy.setEnabled(is_bootable and not is_pending) # 假设关机状态下可以保存并销毁
        btn_destroy.setEnabled(is_bootable and not is_pending) # 假设关机状态下可以销毁

        # 更新所有按钮的样式（无论启用或禁用）
        all_buttons = {
            btn_boot: btn_boot_style,
            btn_save_image: btn_save_style,
            btn_shutdown_keep: btn_shutdown_style,
            btn_shutdown_release: btn_shutdown_style,
            btn_shutdown_destroy: btn_destroy_style,
            btn_save_destroy: btn_destroy_style,
            btn_destroy: btn_destroy_style
        }

        for btn, enabled_style in all_buttons.items():
            if btn.isEnabled():
                btn.setStyleSheet(enabled_style)
                print(f"  - Button '{btn.text()}' ENABLED, Style: {enabled_style}") # 调试
            else:
                btn.setStyleSheet(btn_disabled_style)
                print(f"  - Button '{btn.text()}' DISABLED, Style: {btn_disabled_style}") # 调试

        right_v_layout.addStretch() # 将按钮推到顶部

        main_h_layout.addLayout(right_v_layout, 1) # 右侧占 1/3 空间

        return frame

    # --- 异步获取和显示实例 ---
    def get_and_display_instances_async(self):
        """异步获取实例列表并更新 UI"""
        if self.is_refreshing_instances:
            print("获取实例列表 - 跳过（正在刷新）")
            return
        # 确保 ApiHandler 有 token
        if not self.api_handler._access_token:
            # 清空列表并提示 (主线程安全)
            while self.instance_list_layout.count() > 1:
                item = self.instance_list_layout.takeAt(0)
                widget = item.widget();
                if widget: widget.deleteLater()
            if hasattr(self, 'instance_count_label'): self.instance_count_label.setText("实例总数：0 (请先设置令牌)")
            return

        self.is_refreshing_instances = True # 设置刷新标志
        self.statusbar.showMessage("正在获取实例列表...", 0) # 持续显示

        # 注意：清空列表和加载提示的操作已移至 _handle_get_instances_success

        self._run_task(
            self.api_handler.get_instances,
            self._handle_get_instances_success,
            error_handler=self._handle_get_instances_error,
            finished_handler=self._handle_get_instances_finished
        )

    def _handle_get_instances_success(self, result):
        """处理获取实例成功的结果 (主线程)"""
        # 清空加载提示和旧内容
        while self.instance_list_layout.count() > 1:
            item = self.instance_list_layout.takeAt(0)
            widget = item.widget()
            if widget: widget.deleteLater()

        if result and result.get("success"):
            data = result.get("data", {})
            instances = data.get('list', [])
            total = data.get('total', len(instances))

            if hasattr(self, 'instance_count_label'):
                 self.instance_count_label.setText(f"实例总数：{total}")

            if not instances:
                 no_instance_label = QLabel("您还没有任何实例。", self.instance_scroll_area.widget())
                 no_instance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                 no_instance_label.setStyleSheet("color: #a0aec0;") # 灰色提示
                 self.instance_list_layout.insertWidget(self.instance_list_layout.count() - 1, no_instance_label)
                 self.statusbar.showMessage("未找到实例", 3000)
            else:
                for instance_data in instances:
                    instance_widget = self._create_instance_widget(instance_data)
                    self.instance_list_layout.insertWidget(self.instance_list_layout.count() - 1, instance_widget)
                self.statusbar.showMessage(f"成功加载 {len(instances)} 个实例", 3000)
        else:
            # API 请求成功但业务逻辑失败
            error_msg = result.get("msg", "获取实例列表失败") if result else "未知错误"
            self._handle_get_instances_error(error_msg)

    def _handle_get_instances_error(self, error_message):
        """处理获取实例列表错误 (主线程)"""
        print(f"获取实例列表错误: {error_message}")
        # 清空加载提示和旧内容
        while self.instance_list_layout.count() > 1:
            item = self.instance_list_layout.takeAt(0)
            widget = item.widget()
            if widget: widget.deleteLater()

        if hasattr(self, 'instance_count_label'):
             self.instance_count_label.setText("实例总数：获取失败")
        error_label = QLabel(f"无法加载实例列表: {error_message}", self.instance_scroll_area.widget())
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("color: #f56565;") # 红色错误提示
        self.instance_list_layout.insertWidget(self.instance_list_layout.count() - 1, error_label)
        self.statusbar.showMessage(f"获取实例列表失败: {error_message}", 5000)

    def _handle_get_instances_finished(self):
        """获取实例列表任务完成后的处理 (主线程)"""
        self.is_refreshing_instances = False # 清除刷新标志
        # 从线程池移除 worker
        sender_worker = self.sender().parent()
        if isinstance(sender_worker, Worker) and sender_worker in self.thread_pool:
             self.thread_pool.remove(sender_worker)
        print("获取实例列表任务完成")

    # --- 实例操作方法 (改为异步) ---

    def _handle_instance_action_success(self, result, action_name, instance_id):
        """通用实例操作成功处理"""
        if result and result.get("success"):
            msg = result.get("msg", f"实例 {instance_id} {action_name} 请求已提交。")
            QMessageBox.information(self, "操作成功", msg)
            self.statusbar.showMessage(f"实例 {instance_id} 正在 {action_name}...", 5000)
            self.get_and_display_instances_async() # 刷新列表以更新状态
        else:
            error_msg = result.get("msg", f"{action_name}失败") if result else "API 请求失败"
            self._handle_instance_action_error(error_msg, action_name, instance_id)

    def _handle_instance_action_error(self, error_message, action_name, instance_id):
        """通用实例操作失败处理"""
        QMessageBox.warning(self, f"{action_name}失败", f"无法对实例 {instance_id} 执行 {action_name}: {error_message}")
        self.statusbar.showMessage(f"实例 {instance_id} {action_name} 失败", 5000)
        # 考虑重新启用按钮或刷新列表以显示原始状态
        self.get_and_display_instances_async()

    def save_instance_image(self, instance_id):
        """异步执行储存镜像 API 调用"""
        reply = QMessageBox.question(self, "确认操作", f"确定要为实例 {instance_id} 创建镜像吗？\n请确保实例已关机。",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.statusbar.showMessage(f"正在提交为实例 {instance_id} 创建镜像的请求...", 0)
            self._run_task(
                self.api_handler.save_image,
                partial(self._handle_instance_action_success, action_name="储存镜像", instance_id=instance_id),
                partial(self._handle_instance_action_error, action_name="储存镜像", instance_id=instance_id),
                instance_id=instance_id
            )

    def shutdown_instance_keep_gpu(self, instance_id):
        """异步执行关机保留 GPU API 调用"""
        reply = QMessageBox.question(self, "确认操作", f"确定要关机实例 {instance_id} 并保留 GPU 吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.statusbar.showMessage(f"正在提交关机实例 {instance_id} (保留GPU) 的请求...", 0)
            self._run_task(
                self.api_handler.shutdown_instance,
                partial(self._handle_instance_action_success, action_name="关机(保留GPU)", instance_id=instance_id),
                partial(self._handle_instance_action_error, action_name="关机(保留GPU)", instance_id=instance_id),
                instance_id=instance_id
            )

    def shutdown_instance_release_gpu(self, instance_id):
        """异步执行关机释放 GPU API 调用"""
        reply = QMessageBox.question(self, "确认操作", f"确定要关机实例 {instance_id} 并释放 GPU 吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.statusbar.showMessage(f"正在提交关机实例 {instance_id} (释放GPU) 的请求...", 0)
            self._run_task(
                self.api_handler.shutdown_release_gpu,
                partial(self._handle_instance_action_success, action_name="关机(释放GPU)", instance_id=instance_id),
                partial(self._handle_instance_action_error, action_name="关机(释放GPU)", instance_id=instance_id),
                instance_id=instance_id
            )

    def shutdown_instance_destroy(self, instance_id):
        """异步执行关机并销毁 API 调用"""
        reply = QMessageBox.warning(self, "危险操作确认", f"确定要关机并彻底销毁实例 {instance_id} 吗？\n此操作不可恢复，所有数据将丢失！",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
                                     QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.Yes:
            self.statusbar.showMessage(f"正在提交关机并销毁实例 {instance_id} 的请求...", 0)
            self._run_task(
                self.api_handler.shutdown_destroy,
                partial(self._handle_instance_action_success, action_name="关机并销毁", instance_id=instance_id),
                partial(self._handle_instance_action_error, action_name="关机并销毁", instance_id=instance_id),
                instance_id=instance_id
            )

    def save_image_and_destroy(self, instance_id):
        """异步执行储存并销毁 API 调用"""
        reply = QMessageBox.warning(self, "确认操作", f"确定要先储存实例 {instance_id} 的镜像，然后彻底销毁实例吗？\n请确保实例已关机。销毁操作不可恢复！",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
                                     QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.Yes:
            self.statusbar.showMessage(f"正在提交储存并销毁实例 {instance_id} 的请求...", 0)
            self._run_task(
                self.api_handler.save_image_destroy,
                partial(self._handle_instance_action_success, action_name="储存并销毁", instance_id=instance_id),
                partial(self._handle_instance_action_error, action_name="储存并销毁", instance_id=instance_id),
                instance_id=instance_id
            )

    def destroy_instance_action(self, instance_id, widget_to_remove):
        """异步执行直接销毁实例 API 调用"""
        reply = QMessageBox.warning(self, "危险操作确认", f"确定要直接销毁实例 {instance_id} 吗？\n此操作不可恢复，且仅适用于已关机实例！",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
                                     QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.Yes:
            widget_to_remove.setEnabled(False) # 禁用卡片
            self.statusbar.showMessage(f"正在提交销毁实例 {instance_id} 的请求...", 0)
            self._run_task(
                self.api_handler.destroy_instance,
                partial(self._handle_destroy_instance_success, instance_id=instance_id, widget_to_remove=widget_to_remove),
                partial(self._handle_destroy_instance_error, instance_id=instance_id, widget_to_remove=widget_to_remove),
                instance_id=instance_id
            )

    def _handle_destroy_instance_success(self, result, instance_id, widget_to_remove):
        """处理直接销毁实例成功"""
        if result and result.get("success"):
            QMessageBox.information(self, "操作成功", f"实例 {instance_id} 已成功销毁。")
            # 从布局中移除并删除部件
            self.instance_list_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
            self.statusbar.showMessage(f"实例 {instance_id} 已销毁", 3000)
            # 异步刷新列表以更新总数
            self.get_and_display_instances_async()
        else:
            error_msg = result.get("msg", "销毁失败") if result else "API 请求失败"
            self._handle_destroy_instance_error(error_msg, instance_id, widget_to_remove)

    def _handle_destroy_instance_error(self, error_message, instance_id, widget_to_remove):
        """处理直接销毁实例失败"""
        QMessageBox.warning(self, "操作失败", f"无法销毁实例 {instance_id}: {error_message}")
        self.statusbar.showMessage(f"实例 {instance_id} 销毁失败", 5000)
        widget_to_remove.setEnabled(True) # 重新启用卡片


    def handle_boot_click(self, instance_id, current_gpu_model, current_gpu_count):
        """处理开机按钮点击，显示 InstanceBootDialog 并异步调用 API"""
        # --- UI 交互部分 (主线程) ---
        # 尝试将 current_gpu_count 转换为 int，如果失败则设为 None
        try:
            gpu_count_int = int(current_gpu_count) if current_gpu_count is not None else None
        except (ValueError, TypeError):
            gpu_count_int = None

        dialog = InstanceBootDialog(self, instance_id, current_gpu_model, gpu_count_int)
        if dialog.exec():
            params = dialog.get_selected_params()
            if 'id' in params:
                # --- 后台任务 ---
                self.statusbar.showMessage(f"正在提交开机实例 {instance_id} 的请求...", 0)
                # 这里可以考虑禁用对应的开机按钮，但需要找到它
                # button = self.findChild(QPushButton, f"pushButton_6_{instance_id}")
                # if button: button.setEnabled(False)

                self._run_task(
                    self.api_handler.boot_instance,
                    partial(self._handle_boot_instance_success, instance_id=instance_id),
                    partial(self._handle_boot_instance_error, instance_id=instance_id),
                    # finished_handler=lambda: button.setEnabled(True) if button else None, # 结束后启用按钮
                    params=params
                )
            else:
                 QMessageBox.critical(self, "错误", "未能获取实例ID，无法开机。")

    def _handle_boot_instance_success(self, result, instance_id):
        """处理开机实例成功"""
        if result and result.get('success'):
            QMessageBox.information(self, "成功", f"实例 {instance_id} 开机请求已发送。")
            self.statusbar.showMessage(f"实例 {instance_id} 开机中...", 5000)
            self.get_and_display_instances_async() # 刷新列表
        else:
            error_msg = result.get('msg', '开机失败') if result else 'API 请求失败'
            self._handle_boot_instance_error(error_msg, instance_id)

    def _handle_boot_instance_error(self, error_message, instance_id):
        """处理开机实例失败"""
        QMessageBox.warning(self, "开机失败", f"实例 {instance_id} 开机失败: {error_message}")
        self.statusbar.showMessage(f"实例 {instance_id} 开机失败", 5000)
        # 按钮应该在 finished_handler 中重新启用，或者在这里刷新列表以恢复按钮状态
        self.get_and_display_instances_async()


    # --- 辅助方法 ---
    def copy_to_clipboard(self, text, description):
        """复制文本到剪贴板并显示状态消息"""
        if not text or text == 'N/A':
             self.statusbar.showMessage(f"没有可复制的{description}", 2000)
             return
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.statusbar.showMessage(f"{description} 已复制到剪贴板", 2000)
        except Exception as e:
            QMessageBox.warning(self, "复制失败", f"无法复制 {description}: {e}")
            self.statusbar.showMessage(f"复制 {description} 失败", 2000)

    # --- 页面切换方法 ---
    def show_list_jingxiang_page(self):
        """显示公共镜像列表页面并刷新内容"""
        self.update_button_state(self.jingxiang_2) # 更新按钮状态
        self.body.setCurrentWidget(self.list_jingxiang)
        self.get_and_display_public_images() # <--- 切换时加载并显示镜像
        # self.statusbar.showMessage("已切换到公共镜像列表", 3000) # get_and_display_public_images 会更新状态栏

    # --- 右键菜单 ---
    def show_user_info_context_menu(self, pos):
        item = self.listWidget.itemAt(pos)
        if not item: return
        menu = QMenu(self)
        copy_action = QAction("复制", self)
        copy_action.triggered.connect(lambda: self.copy_list_item_text(item))
        menu.addAction(copy_action)
        menu.exec(self.listWidget.mapToGlobal(pos))

    def copy_list_item_text(self, item):
        full_text = item.text()
        try: value = full_text.split(':', 1)[1].strip()
        except IndexError: value = full_text
        clipboard = QApplication.clipboard()
        clipboard.setText(value)
        self.statusbar.showMessage(f"'{value}' 已复制到剪贴板", 2000)

    # --- 页面切换方法 ---
    def show_jingxiang_page(self):
        """显示镜像页面并刷新列表"""
        self.update_button_state(self.jingxiang)
        self.body.setCurrentWidget(self.jingxiang_page7)
        # 切换时异步刷新
        self.get_and_display_images_async()

    def show_zhuye_page(self):
        self.update_button_state(self.home)
        self.body.setCurrentWidget(self.zhuye_page1)

    def show_shili_page(self):
        """显示实例页面并刷新列表"""
        self.update_button_state(self.shiliBt)
        self.body.setCurrentWidget(self.shili_page6)
        # 切换时异步刷新实例列表
        self.get_and_display_instances_async()

    def show_zhanghao_page(self):
        self.update_button_state(self.menubtn)
        self.body.setCurrentWidget(self.zhanghao_page5)
        # 切换页面后异步获取信息
        if self.api_token:
            self.get_user_info() # 已经是异步的
            self.get_balance()   # 已经是异步的

    def show_shezhi_page(self):
        """显示设置页面并加载当前端口配置"""
        self.update_button_state(self.settings)
        self.body.setCurrentWidget(self.shezhi_page2)
        self._setup_theme_settings()  # 新增
        self.update_button_state(self.settings)
        self.body.setCurrentWidget(self.shezhi_page2)
        # --- 加载端口号到输入框 ---
        if hasattr(self, 'dailikuang_2'):
            self.dailikuang_2.setText(str(self.ports.get('comfyui', '')))
        if hasattr(self, 'dailikuang_3'):
            self.dailikuang_3.setText(str(self.ports.get('fengzhuang', '')))
        if hasattr(self, 'dailikuang_4'):
            self.dailikuang_4.setText(str(self.ports.get('fluxgym', '')))
        if hasattr(self, 'dailikuang_6'): # 输出文件
            self.dailikuang_6.setText(str(self.ports.get('shuchu', '')))
        if hasattr(self, 'dailikuang_5'): # 全部文件
            self.dailikuang_5.setText(str(self.ports.get('quanbu', '')))

    def show_xinxi_page(self):
        try:
            self.update_button_state(self.info)
            self.body.setCurrentWidget(self.xinxi_page3)
        except Exception as e:
            print(f"切换信息页面失败: {e}")
            self.body.setCurrentWidget(self.zhuye_page1)

    def show_bangzhu_page(self):
        try:
            self.update_button_state(self.help)
            self.body.setCurrentWidget(self.bangzhu_page4)
        except Exception as e:
            print(f"切换帮助页面失败: {e}")
            self.body.setCurrentWidget(self.zhuye_page1)

    # --- 新增：显示浏览器页面 ---
    def show_browser_page(self):
        """切换到内置浏览器页面"""
        self.update_button_state(self.quanbu_2) # 高亮浏览器按钮
        self.body.setCurrentWidget(self.browser_page) # 切换到浏览器页面
        # 可选：加载默认页面，例如空白页
        if hasattr(self, 'shared_browser') and self.shared_browser:
             # 检查浏览器是否已经有标签页，如果没有，则打开一个空白页
             if self.shared_browser.tab_widget.count() == 0:
                 self.shared_browser.open_url_in_new_tab("about:blank")
        self.statusbar.showMessage("已切换到内置浏览器", 3000)

    def update_button_state(self, clicked_button):
        base_style = "QPushButton { border-radius: 10px; text-align:left; padding:2px 5px; }"
        selected_style = base_style + "QPushButton { background-color: #46006e; }"
        for button in self.left_buttons:
            if button is None or not hasattr(button, 'style') or not callable(button.style):
                print(f"警告: 按钮 {button} 无效或缺少 style()")
                continue
            is_selected = (button == clicked_button)
            button.setProperty("selected", is_selected)
            button.setStyleSheet(selected_style if is_selected else base_style)
            button.style().unpolish(button); button.style().polish(button); button.update()

    # --- 定时刷新方法 ---
    def refresh_data(self):
        """根据当前显示的页面刷新数据"""
        current_widget = self.body.currentWidget()
        if current_widget == self.shili_page6:
            # 使用异步刷新，并检查刷新标志
            if not self.is_refreshing_instances:
                print("定时刷新：实例列表") # 调试信息
                self.get_and_display_instances_async()
            else:
                print("定时刷新：实例列表 - 跳过（正在刷新）")
        elif current_widget == self.jingxiang_page7:
             # 使用异步刷新，并检查刷新标志
            if not self.is_refreshing_images:
                print("定时刷新：镜像列表") # 调试信息
                self.get_and_display_images_async()
            else:
                print("定时刷新：镜像列表 - 跳过（正在刷新）")
        # 可以根据需要添加其他页面的刷新逻辑
        # else:
        #     print(f"定时刷新：当前页面 ({current_widget.objectName() if current_widget else 'None'}) 无需刷新")

    # --- 端口设置保存方法 ---
    def save_port_setting(self, port_name, line_edit_widget):
        """保存单个端口设置"""
        if not hasattr(self, 'ports'):
            self.ports = {} # 以防万一


        port_value_str = line_edit_widget.text().strip()
        try:
            port_value_int = int(port_value_str)
            if 0 < port_value_int < 65536: # 验证端口范围
                self.ports[port_name] = port_value_int
                self.save_config()
                self.statusbar.showMessage(f"{port_name.capitalize()} 端口已更新为 {port_value_int}", 3000)
            else:
                QMessageBox.warning(self, "端口无效", f"端口号 {port_value_int} 无效，请输入 1 到 65535 之间的数字。")
                # 可以选择将输入框恢复为旧值
                line_edit_widget.setText(str(self.ports.get(port_name, '')))
        except ValueError:
            QMessageBox.warning(self, "输入无效", f"端口号必须是数字。您输入的是 '{port_value_str}'。")
            # 恢复旧值
            line_edit_widget.setText(str(self.ports.get(port_name, '')))
        except Exception as e:
            QMessageBox.critical(self, "保存错误", f"保存端口设置时发生错误: {e}")

        def save_config(self):
            config = {
                # ... 原有配置 ...
                "theme": ThemeManager().current_theme
            }
            # ... 原有保存代码 ...
            # --- 服务 URL 打开逻辑 (改为异步) ---

    def get_running_instances(self):
        """(不再直接使用) 获取当前运行中的实例列表 (只包含必要信息) - 旧的同步方法"""
        # 注意：这个同步方法现在只作为参考，实际调用将通过异步任务
        if not self.api_handler._access_token:
            return None

        result = self.api_handler.get_instances() # 同步调用
        running_instances = []
        if result and result.get("success"):
            instances = result.get('data', {}).get('list', [])
            # 定义表示运行中的状态 (需要根据实际 API 返回调整)
            running_statuses = ['running', 'starting', 'rebooting', '运行中', '启动中', '重启中', '开机中', '工作中']
            for inst in instances:
                # 确保状态是字符串并转小写比较
                status = inst.get('status', '').lower()
                if status in running_statuses:
                    # 只提取需要的字段，简化后续处理
                    running_instances.append({
                        'id': inst.get('id'),
                        'name': inst.get('name') or f"实例 {inst.get('id', 'N/A')[:6]}...", # 提供默认名
                        'web_url': inst.get('web_url') # 必须有 web_url
                    })
            return running_instances
        else:
            error_msg = result.get("msg", "获取实例列表失败") if result else "API 请求失败"
            self.statusbar.showMessage(f"获取实例列表时出错: {error_msg}", 5000)
            return None

    def show_instance_selection_dialog(self, instances):
        """显示实例选择对话框 (UI 交互，保持在主线程)"""
        # 创建实例名称和 ID 的映射
        instance_choices = {f"{inst['name']} ({inst['id']})": inst['id'] for inst in instances if inst.get('id')}
        if not instance_choices:
            QMessageBox.warning(self, "无有效实例", "未找到可供选择的有效实例。")
            return None

        items = list(instance_choices.keys())
        item, ok = QInputDialog.getItem(self, "选择实例", "检测到多个正在运行的实例，请选择一个：", items, 0, False)

        if ok and item:
            return instance_choices[item] # 返回选择的实例 ID
        else:
            return None

    def open_service_url(self, service_name):
        """异步处理左侧服务按钮点击事件"""
        # --- UI 交互部分 (主线程) ---
        self.statusbar.showMessage(f"正在获取运行实例以打开 {service_name.capitalize()}...", 0)
        # 禁用对应的按钮
        button = self.sender() # 获取触发信号的按钮
        original_enabled_state = False
        if isinstance(button, QPushButton):
            original_enabled_state = button.isEnabled()
            button.setEnabled(False)

        # --- 后台任务 ---
        self._run_task(
            self.api_handler.get_instances, # 获取所有实例
            partial(self._handle_get_running_instances_success, service_name=service_name, button=button),
            partial(self._handle_get_running_instances_error, service_name=service_name, button=button, original_state=original_enabled_state),
            # finished_handler 在成功或失败处理中调用 re-enable
        )

    def _handle_get_running_instances_success(self, result, service_name, button):
        """处理获取实例成功，用于打开服务 URL (主线程)"""
        running_instances = []
        if result and result.get("success"):
            instances = result.get('data', {}).get('list', [])
            running_statuses = ['running', 'starting', 'rebooting', '运行中', '启动中', '重启中', '开机中', '工作中']
            for inst in instances:
                status = inst.get('status', '').lower()
                if status in running_statuses:
                    running_instances.append({
                        'id': inst.get('id'),
                        'name': inst.get('name') or f"实例 {inst.get('id', 'N/A')[:6]}...",
                        'web_url': inst.get('web_url')
                    })
        else:
            # API 调用成功但业务逻辑失败
            error_msg = result.get("msg", "获取实例列表失败") if result else "API 请求失败"
            self._handle_get_running_instances_error(error_msg, service_name, button, True) # 调用错误处理
            return # 不再继续

        # --- 继续 UI 交互 (主线程) ---
        selected_instance_id = None
        selected_instance_web_url = None

        if not running_instances:
            # --- 修改：即使没有实例，也打开浏览器 ---
            QMessageBox.information(self, "无运行中实例", f"没有找到正在运行的实例来打开 {service_name.capitalize()}。\n将打开一个空白标签页。")
            self.statusbar.showMessage("未找到运行中实例，打开空白页", 3000)
            # 切换到浏览器并打开空白页
            self.body.setCurrentWidget(self.browser_page)
            self.shared_browser.open_url_in_new_tab("about:blank") # 打开空白页
            # 更新左侧按钮状态
            if isinstance(button, QPushButton):
                 self.update_button_state(button)
            return # 结束处理，因为没有实例URL可以构建
            # --- 修改结束 ---

        if len(running_instances) == 1:
            instance = running_instances[0]
            if instance.get('id') and instance.get('web_url'):
                selected_instance_id = instance['id']
                selected_instance_web_url = instance['web_url']
            else:
                 QMessageBox.warning(self, "实例信息不完整", "唯一的运行实例缺少 ID 或 Web URL。")
                 if isinstance(button, QPushButton): button.setEnabled(True) # 重新启用按钮
                 return
        else:
            selected_instance_id = self.show_instance_selection_dialog(running_instances)
            if not selected_instance_id:
                self.statusbar.showMessage("操作已取消", 2000)
                if isinstance(button, QPushButton): button.setEnabled(True) # 重新启用按钮
                return # 用户取消选择
            # 根据 ID 找到对应的 web_url
            for inst in running_instances:
                if inst.get('id') == selected_instance_id:
                    selected_instance_web_url = inst.get('web_url')
                    break
            if not selected_instance_web_url:
                 QMessageBox.warning(self, "实例信息不完整", f"选择的实例 {selected_instance_id} 缺少 Web URL。")
                 if isinstance(button, QPushButton): button.setEnabled(True) # 重新启用按钮
                 return

        # 获取配置的端口号
        target_port = self.ports.get(service_name)
        if not target_port or not isinstance(target_port, int):
            QMessageBox.warning(self, "端口配置错误", f"服务 '{service_name}' 的端口未配置或配置无效。请在设置中检查。")
            if isinstance(button, QPushButton): button.setEnabled(True) # 重新启用按钮
            return

        # --- 构建最终 URL (主线程) ---
        final_url = None
        try:
            # 正则表达式匹配基础 URL 和端口号
            # 匹配 https://<any-non-slash-chars>-<digits>.<any-chars>
            match = re.match(r'^(https?://[^/]+-)(\d+)(\..*)$', selected_instance_web_url, re.IGNORECASE)
            if match:
                base_url_part1 = match.group(1) # e.g., "https://abc-"
                base_url_part2 = match.group(3) # e.g., ".domain.com/" or ".container.x-gpu.com/"
                # 替换端口号
                intermediate_url = f"{base_url_part1}{target_port}{base_url_part2}"

                # 添加 /files/ 后缀（如果需要）
                if service_name in ['shuchu', 'quanbu']:
                    # 确保 URL 以 / 结尾，然后再添加 files/
                    if not intermediate_url.endswith('/'):
                        intermediate_url += '/'
                    final_url = intermediate_url + 'files/'
                else:
                    final_url = intermediate_url

                print(f"原始 Web URL: {selected_instance_web_url}") # 调试
                print(f"目标端口: {target_port}") # 调试
                print(f"构建的最终 URL: {final_url}") # 调试

            else:
                 QMessageBox.warning(self, "URL 格式未知", f"实例的 Web URL '{selected_instance_web_url}' 格式无法识别，无法自动替换端口。请检查实例信息或手动访问。")
                 if isinstance(button, QPushButton): button.setEnabled(True) # 重新启用按钮
                 return

        except Exception as e:
            QMessageBox.critical(self, "URL 构建错误", f"构建 {service_name.capitalize()} 的 URL 时出错: {e}")
            if isinstance(button, QPushButton): button.setEnabled(True) # 重新启用按钮
            return

        # 打开最终 URL (主线程)
        if final_url:
            # --- 根据偏好设置打开 URL ---
            if self.browser_preference == "system":
                try:
                    webbrowser.open(final_url)
                    self.statusbar.showMessage(f"已在系统浏览器中打开 {service_name.capitalize()} 服务", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "打开链接错误", f"无法在系统浏览器中打开链接 {final_url}: {e}")
                    self.statusbar.showMessage(f"打开链接失败: {e}", 5000)
            else: # 默认或 "integrated"
                if hasattr(self, 'shared_browser') and self.shared_browser:
                    self.body.setCurrentWidget(self.browser_page) # 切换到浏览器页面
                    self.shared_browser.open_url_in_new_tab(final_url) # 在新标签页打开
                    self.statusbar.showMessage(f"已在内置浏览器中打开 {service_name.capitalize()} 服务", 3000)
                else:
                    print("警告: 内置浏览器未初始化，将尝试使用系统浏览器打开。")
                    try:
                        webbrowser.open(final_url)
                        self.statusbar.showMessage(f"内置浏览器不可用，已在系统浏览器中打开 {service_name.capitalize()} 服务", 3000)
                    except Exception as e:
                         QMessageBox.critical(self, "打开链接错误", f"内置浏览器不可用，且无法在系统浏览器中打开链接 {final_url}: {e}")
                         self.statusbar.showMessage(f"打开链接失败: {e}", 5000)

            # 更新左侧按钮状态 (高亮最后点击的按钮)
            if isinstance(button, QPushButton):
                 self.update_button_state(button)
            # --- 修改结束 ---
        else:
             QMessageBox.warning(self, "无法打开", f"未能成功构建 {service_name.capitalize()} 的 URL。")

        # 无论成功失败，最后都尝试恢复按钮状态 (如果之前禁用了)
        # 注意：这里不再禁用按钮，所以不需要恢复
        # if isinstance(button, QPushButton): button.setEnabled(True)

    def _handle_get_running_instances_error(self, error_message, service_name, button, original_state):
        """处理获取实例列表失败，用于打开服务 URL (主线程)"""
        QMessageBox.warning(self, "无法操作", f"获取运行实例列表时出错: {error_message}")
        self.statusbar.showMessage(f"获取实例列表失败: {error_message}", 5000)
        if isinstance(button, QPushButton):
            button.setEnabled(original_state) # 恢复按钮原始状态


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
