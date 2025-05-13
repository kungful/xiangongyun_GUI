# gpu_grabber.py
import time
import threading
import random # 用于模拟
from PySide6.QtCore import QObject, Signal, QThread
from api_handler import ApiHandler # <--- 添加导入

# ==============================================================================
# 模拟部署函数 - 在实际应用中替换为真实的 API 调用
# ==============================================================================
def simulate_deploy_image(params):
    """
    模拟部署镜像到 GPU 的过程。
    随机模拟成功或失败。
    成功时返回 True 和模拟的实例 ID。
    失败时返回 False 和 None。
    """
    print(f"[模拟部署] 尝试部署参数: {params}")
    # 模拟网络延迟和处理时间
    time.sleep(random.uniform(0.5, 2.0))

    # 模拟 GPU 是否可用 (例如，25% 的概率成功抢到)
    if random.random() < 0.25:
        instance_id = f"gpu-instance-{random.randint(1000, 9999)}"
        print(f"[模拟部署] 成功！获得实例: {instance_id}")
        return True, instance_id
    else:
        print("[模拟部署] GPU 资源不足或冲突，暂时无法部署。")
        return False, None

# ==============================================================================
# 提示音播放函数 - 可根据需要替换实现
# ==============================================================================
def play_success_sound():
    """尝试播放成功提示音。"""
    try:
        # 尝试使用 playsound 库 (需要 pip install playsound)
        # 你需要提供一个有效的 .wav 或 .mp3 文件路径
        # from playsound import playsound
        # sound_file = 'path/to/your/success_sound.wav'
        # playsound(sound_file)
        print("[提示音] 띠링! 部署成功!") # 暂时用打印和特殊字符模拟声音
    except ImportError:
        print("[提示音] 警告: 未安装 'playsound' 库，无法播放声音。")
    except Exception as e:
        print(f"[提示音] 播放声音时出错: {e}")

# ==============================================================================
# GPU 抢占 Worker 类 (运行在单独线程)
# ==============================================================================
class GpuGrabWorker(QObject):
    """
    负责在后台线程中循环尝试部署镜像，直到成功或被取消。
    """
    # --- 信号定义 ---
    finished = Signal() # 任务完成时（无论成功、失败或取消）发出
    success = Signal(str) # 部署成功时发出，携带实例 ID
    error = Signal(str)   # 发生无法恢复的错误时发出
    status_update = Signal(str) # 状态更新时发出，用于界面显示

    def __init__(self, api_handler: ApiHandler, deploy_params, interval=5, parent=None): # <--- 添加 api_handler 参数
        """
        初始化 Worker。
        :param api_handler: ApiHandler 的实例，用于执行 API 调用
        :param deploy_params: 部署所需的参数 (dict 或 object)
        :param interval: 每次尝试之间的间隔时间 (秒)
        :param parent: 父对象 (通常为 None)
        """
        super().__init__(parent)
        self.api_handler = api_handler # <--- 保存 api_handler 实例
        self.deploy_params = deploy_params
        self.interval = max(1, interval) # 确保间隔至少为 1 秒
        self._is_running = False
        self._request_stop = False

    def run(self):
        """启动抢占循环。此方法应由 QThread 调用。"""
        if self._is_running:
            return # 防止重复运行

        self._is_running = True
        self._request_stop = False
        self.status_update.emit("🚀 开始抢占 GPU 资源...")

        attempt_count = 0
        while self._is_running:
            if self._request_stop:
                self.status_update.emit("🛑 抢占任务已取消。")
                break

            attempt_count += 1
            self.status_update.emit(f"⏳ 第 {attempt_count} 次尝试部署...")

            try:
                # --- 调用实际的部署函数 ---
                # 注意：现在调用真实的 API Handler
                result = self.api_handler.deploy_instance(self.deploy_params)
                # --------------------------

                if result.get('success'): # <--- 检查 API 响应的 success 字段
                    # 假设成功时，实例 ID 在响应的 data 字段中，需要根据实际 API 调整
                    instance_info = result.get('data', {}) # 获取 data 字典，失败则为空字典
                    instance_id = instance_info.get('id', '未知ID') # 尝试从 data 获取 id，获取不到则显示未知
                    self.status_update.emit(f"✅ 部署请求成功！实例 ID: {instance_id}")
                    play_success_sound() # 播放成功提示音
                    self.success.emit(instance_id) # 发出成功信号，传递实例 ID
                    self._is_running = False # 任务成功，结束运行
                else:
                    # 从 API 响应获取错误消息
                    error_msg = result.get('msg', '部署失败，但未提供具体错误信息')
                    self.status_update.emit(f"❌ {error_msg} (将在 {self.interval} 秒后重试...)")
                    # 使用 QThread 的 sleep 是首选，因为它允许事件处理
                    # 但如果在非 GUI 线程直接 time.sleep 也可以
                    current_thread = QThread.currentThread()
                    if current_thread:
                        current_thread.sleep(self.interval)
                    else: # Fallback if not in a QThread context (less ideal)
                        time.sleep(self.interval)

            except Exception as e:
                error_msg = f"💥 部署过程中发生严重错误: {e}"
                self.status_update.emit(error_msg)
                self.error.emit(error_msg)
                self._is_running = False # 发生错误，结束运行

        # 循环结束后发出 finished 信号
        self._is_running = False
        self.finished.emit()
        print("[Worker] 任务执行完毕。")

    def stop(self):
        """请求停止抢占循环。"""
        if self._is_running:
            self.status_update.emit("⏳ 正在请求停止抢占任务...")
            self._request_stop = True

# ==============================================================================
# 如何在 DeployImageDialog 中使用 (示例注释)
# ==============================================================================
"""
# 在 DeployImageDialog 的 __init__ 或相关方法中:
self.gpu_grab_thread = None
self.gpu_grab_worker = None

# 当用户点击 "抢占部署" 按钮时:
def start_gpu_grabbing(self):
    if self.gpu_grab_thread and self.gpu_grab_thread.isRunning():
        # 可以选择提示用户已经在运行，或者先停止旧的再开始新的
        print("抢占任务已在运行中。")
        return

    # 1. 获取部署参数 (从界面控件获取)
    deploy_params = {
        'image_id': self.image_combo.currentData(),
        'gpu_type': self.gpu_type_combo.currentText(),
        # ... 其他参数 ...
    }
    retry_interval = self.retry_interval_spinbox.value() # 假设有个控件设置间隔

    # 2. 创建 Worker 和 Thread
    self.gpu_grab_worker = GpuGrabWorker(deploy_params, interval=retry_interval)
    self.gpu_grab_thread = QThread()

    # 3. 移动 Worker 到 Thread
    self.gpu_grab_worker.moveToThread(self.gpu_grab_thread)

    # 4. 连接信号槽
    #    - 线程启动时运行 worker 的 run 方法
    self.gpu_grab_thread.started.connect(self.gpu_grab_worker.run)
    #    - worker 完成后退出线程
    self.gpu_grab_worker.finished.connect(self.gpu_grab_thread.quit)
    #    - worker 和线程完成后进行清理
    self.gpu_grab_worker.finished.connect(self.gpu_grab_worker.deleteLater)
    self.gpu_grab_thread.finished.connect(self.gpu_grab_thread.deleteLater)
    #    - 连接自定义信号到处理函数
    self.gpu_grab_worker.success.connect(self.on_deploy_success)
    self.gpu_grab_worker.error.connect(self.on_deploy_error)
    self.gpu_grab_worker.status_update.connect(self.update_status_label) # 连接到状态标签

    # 5. 启动线程
    self.gpu_grab_thread.start()

    # 6. 更新 UI (例如，禁用部署按钮，显示状态，显示取消按钮)
    self.deploy_button.setEnabled(False)
    self.grab_deploy_button.setEnabled(False) # 禁用抢占按钮本身
    self.cancel_grab_button.setEnabled(True) # 启用取消按钮
    self.status_label.setText("正在初始化抢占任务...")

# 处理成功信号:
def on_deploy_success(self, instance_id):
    print(f"部署成功，实例 ID: {instance_id}")
    # 跳转到实例页面等后续操作
    self.accept() # 关闭对话框或进行页面跳转
    # 可能需要重置 UI 状态
    self.reset_ui_after_grab()

# 处理错误信号:
def on_deploy_error(self, error_message):
    print(f"部署失败: {error_message}")
    QMessageBox.critical(self, "部署错误", error_message)
    # 重置 UI 状态
    self.reset_ui_after_grab()

# 更新状态标签:
def update_status_label(self, status):
    self.status_label.setText(status) # 假设有一个 QLabel叫 status_label

# 取消抢占任务 (连接到取消按钮的 clicked 信号):
def cancel_gpu_grabbing(self):
    if self.gpu_grab_worker:
        self.gpu_grab_worker.stop()
    self.cancel_grab_button.setEnabled(False) # 禁用取消按钮

# 重置 UI 状态 (在任务结束时调用):
def reset_ui_after_grab(self):
    self.deploy_button.setEnabled(True)
    self.grab_deploy_button.setEnabled(True)
    self.cancel_grab_button.setEnabled(False)
    # 清理线程和 worker 引用，以防万一 deleteLater 未及时完成
    self.gpu_grab_thread = None
    self.gpu_grab_worker = None
    # 可能需要清除状态标签
    # self.status_label.clear()

# 在对话框关闭时确保线程停止 (覆盖 closeEvent):
def closeEvent(self, event):
    if self.gpu_grab_thread and self.gpu_grab_thread.isRunning():
        self.cancel_gpu_grabbing()
        # 可以选择等待线程结束，或者直接接受关闭事件
        # self.gpu_grab_thread.quit()
        # self.gpu_grab_thread.wait(1000) # 等待最多1秒
    super().closeEvent(event)

"""
