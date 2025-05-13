import sys
import traceback
import requests
import pprint
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QComboBox, QDialog, 
                             QMessageBox, QApplication)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon

class ApiHandler:
    def __init__(self, api_token):
        self.base_url = "https://api.xiangongyun.com/open/instance"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        print("API处理器初始化完成")

    def boot_instance(self, params):
        """修正后的开机API调用方法"""
        print("\n=== 正在准备开机请求 ===")
        instance_id = params.get("id")
        if not instance_id:
            return {"success": False, "msg": "实例ID缺失"}

        # *** 严格按API要求的格式和类型准备参数 ***
        api_payload = {
            "id": instance_id,
            # *** 直接使用从对话框获取的完整 gpu_model 字符串 ***
            "gpu_model": params.get("gpu_model"),
            # *** 确保 gpu_count 是字符串类型 ***
            "gpu_count": str(params.get("gpu_count")) # 从对话框获取的是字符串，这里用 str() 确保
        }

        # 检查参数是否存在 (防御性编程)
        if not api_payload.get("gpu_model"):
            return {"success": False, "msg": "GPU型号未提供"}
        if not api_payload.get("gpu_count"):
            return {"success": False, "msg": "GPU数量未提供"}

        print("✅ 最终请求参数 (将发送给API):")
        pprint.pprint(api_payload)

        try:
            print("\n正在发送请求到API服务器...")
            response = requests.post(
                f"{self.base_url}/boot",
                json=api_payload, # 发送构造好的 payload
                headers=self.headers,
                timeout=15 # 建议设置超时
            )

            print("\n🔍 服务器响应:")
            print(f"状态码: {response.status_code}")
            try:
                response_data = response.json()
                print("响应内容 (JSON):")
                pprint.pprint(response_data)
            except requests.exceptions.JSONDecodeError:
                print(f"响应内容 (非JSON): {response.text}")
                return {
                    "success": False,
                    "msg": f"API响应格式错误 (状态码: {response.status_code})",
                    "raw_response": response.text
                }

            # 根据实际成功响应判断，假设 success 字段存在且为 True
            if response.status_code == 200 and response_data.get("success"):
                return {
                    "success": True,
                    "msg": response_data.get("msg", "开机指令已发送"),
                    "data": response_data
                }
            else:
                # 尝试获取更详细的错误信息
                error_msg = response_data.get('msg', f'API返回失败，状态码: {response.status_code}')
                error_code = response_data.get('code', '无')
                return {
                    "success": False,
                    "msg": f"{error_msg} (代码: {error_code})",
                    "api_response": response_data
                }

        except requests.exceptions.Timeout:
             print("❌ 请求超时")
             return {"success": False, "msg": "API请求超时"}
        except requests.exceptions.RequestException as e:
            error_info = {
                "success": False,
                "msg": f"API请求异常: {str(e)}",
                "exception_type": type(e).__name__
            }
            print(f"❌ 发生网络或请求错误: {error_info}")
            traceback.print_exc()
            return error_info
        except Exception as e: # 捕获其他可能的异常
            error_info = {
                "success": False,
                "msg": f"处理开机请求时发生未知错误: {str(e)}",
                "exception_type": type(e).__name__
            }
            print(f"❌ 发生未知异常: {error_info}")
            traceback.print_exc()
            return error_info

    def shutdown_instance(self, instance_id):
        """关机API"""
        try:
            response = requests.post(
                f"{self.base_url}/shutdown",
                json={"id": instance_id},
                headers=self.headers,
                timeout=15
            )
            response_data = response.json()
            return {
                "success": response_data.get("success", False),
                "msg": response_data.get("msg", "关机请求已发送"),
                "data": response_data
            }
        except Exception as e:
            return {
                "success": False,
                "msg": f"关机请求失败: {str(e)}"
            }

class InstanceBootDialog(QDialog):
    def __init__(self, parent=None, instance_id=None, current_gpu_model=None, current_gpu_count=None):
        super().__init__(parent)
        self.instance_id = instance_id
        self.setWindowTitle(f"实例开机设置 (ID: {instance_id})")
        self.setMinimumWidth(400)
        self.setup_ui(current_gpu_model, current_gpu_count)

    def setup_ui(self, current_gpu_model, current_gpu_count):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 实例ID显示
        id_layout = QHBoxLayout()
        id_label = QLabel("实例ID:")
        self.id_display = QLineEdit(self.instance_id)
        self.id_display.setReadOnly(True)
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_display)
        layout.addLayout(id_layout)

        # GPU型号选择
        gpu_layout = QHBoxLayout()
        gpu_label = QLabel("GPU型号:")
        self.gpu_combo = QComboBox()
        self.gpu_combo.addItems([
            "NVIDIA GeForce RTX 4090 D",
            "NVIDIA GeForce RTX 4090"
            # 如果 API 支持其他型号，也按完整格式添加
        ])
        # *** 确保 current_gpu_model 也是完整格式来匹配 ***
        if current_gpu_model:
            # 查找并设置当前项，需要 current_gpu_model 存储的是完整名称
            index = self.gpu_combo.findText(current_gpu_model, Qt.MatchFixedString)
            if index >= 0:
                self.gpu_combo.setCurrentIndex(index)
            else:
                # 如果传入的 current_gpu_model 不在选项中，默认选第一个
                print(f"警告: 当前GPU型号 '{current_gpu_model}' 不在可选列表中，将默认选中第一个。")
                self.gpu_combo.setCurrentIndex(0) # 或者不设置，让用户必须选

        gpu_layout.addWidget(gpu_label)
        gpu_layout.addWidget(self.gpu_combo)
        layout.addLayout(gpu_layout)

        # GPU数量选择
        count_layout = QHBoxLayout()
        count_label = QLabel("GPU数量:")
        self.count_combo = QComboBox()

        # API 要求 0-8，但开机通常至少需要1？根据实际需求调整范围
        # 如果允许开机时选择 0 个 GPU，请包含 "0"
        self.count_combo.addItems([str(i) for i in range(1, 9)]) # 当前是 1-8
        if current_gpu_count is not None: # 检查 None，因为 0 是有效值
             # current_gpu_count 传入时可能是 int 或 str，确保用 str 比较
            self.count_combo.setCurrentText(str(current_gpu_count))

        count_layout.addWidget(count_label)
        count_layout.addWidget(self.count_combo)
        layout.addLayout(count_layout)

        # 按钮
        btn_box = QHBoxLayout()
        confirm_btn = QPushButton("确认开机")
        confirm_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        confirm_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("background-color: #6c757d; color: white;") # 修改为灰色
        cancel_btn.clicked.connect(self.reject)
        btn_box.addStretch()
        btn_box.addWidget(cancel_btn)
        btn_box.addWidget(confirm_btn)
        layout.addLayout(btn_box)

        self.setLayout(layout)

    def get_selected_params(self):
        """返回严格符合API要求的参数格式"""
        return {
            "id": self.instance_id,
            "gpu_model": self.gpu_combo.currentText(),
            "gpu_count": int(self.count_combo.currentText())
        }

class InstanceWidget(QWidget):
    def __init__(self, api_handler: ApiHandler, instance_data: dict):
        super().__init__()
        self.api_handler = api_handler
        self.instance_data = instance_data
        self.setup_ui()
        self.update_button_states()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 实例信息
        info_layout = QVBoxLayout()
        self.id_label = QLabel(f"🆔 实例ID: {self.instance_data.get('id', 'N/A')}")
        self.status_label = QLabel(f"🔄 状态: {self.instance_data.get('status', 'Unknown')}")
        self.gpu_label = QLabel(f"🎮 GPU: {self.instance_data.get('gpu_model', 'N/A')}")
        
        for widget in [self.id_label, self.status_label, self.gpu_label]:
            info_layout.addWidget(widget)
        
        # 操作按钮
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(5)
        
        self.boot_btn = QPushButton("🚀 开机")
        self.boot_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        self.boot_btn.clicked.connect(self.on_boot_clicked)
        
        self.shutdown_btn = QPushButton("⏹️ 关机")
        self.shutdown_btn.setStyleSheet("background-color: #FF9800; color: white;")
        self.shutdown_btn.clicked.connect(self.on_shutdown_clicked)
        
        btn_layout.addWidget(self.boot_btn)
        btn_layout.addWidget(self.shutdown_btn)
        
        main_layout.addLayout(info_layout, stretch=2)
        main_layout.addLayout(btn_layout, stretch=1)
        self.setLayout(main_layout)

    def update_button_states(self):
        status = self.instance_data.get('status', '').lower()
        is_running = status in ['running', 'starting']
        is_stopped = status in ['stopped', 'shutdown']
        
        self.boot_btn.setEnabled(is_stopped)
        self.shutdown_btn.setEnabled(is_running)
        
        print(f"按钮状态更新 - 开机: {'可用' if is_stopped else '禁用'}, 关机: {'可用' if is_running else '禁用'}")

    def update_data(self, new_data):
        self.instance_data = new_data
        self.id_label.setText(f"🆔 实例ID: {self.instance_data.get('id', 'N/A')}")
        self.status_label.setText(f"🔄 状态: {self.instance_data.get('status', 'Unknown')}")
        self.gpu_label.setText(f"🎮 GPU: {self.instance_data.get('gpu_model', 'N/A')}")
        self.update_button_states()

    @Slot()
    def on_boot_clicked(self):
        print("\n=== 处理开机请求 ===")
        dialog = InstanceBootDialog(
            self,
            self.instance_data.get('id'),
            self.instance_data.get('gpu_model'),
            self.instance_data.get('gpu_count')
        )
        
        if dialog.exec_() == QDialog.Accepted:
            params = dialog.get_selected_params()
            print("\n用户确认的开机参数:")
            pprint.pprint(params)
            
            result = self.api_handler.boot_instance(params)
            print("\nAPI调用结果:")
            pprint.pprint(result)
            
            if result.get('success'):
                QMessageBox.information(
                    self, 
                    "开机成功", 
                    f"实例 {self.instance_data['id']} 开机请求已发送\n{result.get('msg', '')}"
                )
                self.update_data({
                    **self.instance_data,
                    'status': 'starting',
                    'gpu_model': params.get('gpu_model'),
                    'gpu_count': params.get('gpu_count')
                })
            else:
                QMessageBox.critical(
                    self,
                    "开机失败",
                    f"无法启动实例 {self.instance_data['id']}\n错误: {result.get('msg', '未知错误')}"
                )

    @Slot()
    def on_shutdown_clicked(self):
        print("\n=== 处理关机请求 ===")
        reply = QMessageBox.question(
            self,
            "确认关机",
            f"确定要关机实例 {self.instance_data['id']} 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            result = self.api_handler.shutdown_instance(self.instance_data['id'])
            print("\n关机API响应:")
            pprint.pprint(result)
            
            if result.get('success'):
                QMessageBox.information(
                    self,
                    "关机成功",
                    f"实例 {self.instance_data['id']} 关机请求已发送\n{result.get('msg', '')}"
                )
                self.update_data({
                    **self.instance_data,
                    'status': 'stopping'
                })
            else:
                QMessageBox.critical(
                    self,
                    "关机失败",
                    f"无法关闭实例 {self.instance_data['id']}\n错误: {result.get('msg', '未知错误')}"
                )

if __name__ == '__main__':
    # 配置
    API_TOKEN = ""  # 请在此处输入有效的API令牌
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用现代样式
    
    # 初始化API处理器
    api_handler = ApiHandler(API_TOKEN)
    
    # 测试数据
    test_instances = [
        {
            "id": "8gl6ykroef04v5ot",
            "status": "stopped",
            "gpu_model": "RTX 4090 D",
            "gpu_count": 1
        },
        {
            "id": "inst-test-002",
            "status": "running",
            "gpu_model": "RTX 4090",
            "gpu_count": 2
        }
    ]
    
    # 创建主窗口
    main_window = QWidget()
    main_window.setWindowTitle("GPU云实例管理器")
    main_window.resize(600, 300)
    
    # 布局
    layout = QVBoxLayout(main_window)
    layout.addWidget(QLabel("📡 实例列表", styleSheet="font-size: 16px; font-weight: bold;"))
    
    # 添加测试实例
    for instance in test_instances:
        widget = InstanceWidget(api_handler, instance)
        layout.addWidget(widget)
    
    # 添加底部空白
    layout.addStretch()
    
    # 显示窗口
    main_window.show()
    
    # 运行应用
    sys.exit(app.exec_())
