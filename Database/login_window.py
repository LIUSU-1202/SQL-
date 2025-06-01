from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from user_dao import register_user, login_user


class LoginWindow(QWidget):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("用户登录 / 注册")
        self.setFixedSize(350, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("学生通讯录系统")
        title.setStyleSheet("font-size:24px;font-weight:bold;color:#234;")
        layout.addWidget(title)

        # 用户名
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("用户名:"))
        self.username_input = QLineEdit()
        row1.addWidget(self.username_input)
        layout.addLayout(row1)

        # 密码
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("密  码:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        row2.addWidget(self.password_input)
        layout.addLayout(row2)

        # 按钮区
        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("登录")
        self.register_btn = QPushButton("注册")
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)
        layout.addLayout(btn_layout)

        self.login_btn.clicked.connect(self.handle_login)
        self.register_btn.clicked.connect(self.handle_register)
        self.setStyleSheet("""
            QWidget{background-color:#f6f8fa;}
            QLineEdit{padding:4px;border-radius:4px;border:1px solid #bbb;}
            QPushButton{font-size:16px;padding:6px 18px;}
            QPushButton:hover{background:#c8e6c9;}
        """)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if login_user(username, password):
            self.on_login_success()
            self.close()
        else:
            QMessageBox.warning(self, "错误", "用户名或密码错误！")

        if login_user(username, password):
            if self.on_login_success:
                self.on_login_success()
            # self.close() 不需要，主窗口会处理

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "提示", "用户名和密码不能为空")
            return
        if register_user(username, password):
            QMessageBox.information(self, "注册成功", "注册成功，请登录")
        else:
            QMessageBox.warning(self, "失败", "注册失败，用户名可能已存在")