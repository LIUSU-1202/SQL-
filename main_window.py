import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from student_dao import add_student, delete_student, update_student, query_students, get_all_students
from login_window import LoginWindow


class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("学生通讯录管理系统")
        self.resize(1100, 600)
        self.selected_id = None
        self.init_ui()
        self.load_data()
        # 记得保存登录窗口的引用
        self.login_window = None

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("学生通讯录管理")
        title.setFont(QFont("微软雅黑", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:#1976d2;margin:12px;")
        layout.addWidget(title)

        # 输入区
        form_layout = QHBoxLayout()
        self.student_number_input = QLineEdit()
        self.name_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.major_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        for widget, label in zip(
                [self.student_number_input, self.name_input, self.gender_input, self.major_input, self.phone_input,
                 self.email_input, self.address_input],
                ["学号", "姓名", "性别", "主修专业", "电话", "邮箱", "地址"]
        ):
            v = QVBoxLayout()
            l = QLabel(label)
            l.setAlignment(Qt.AlignLeft)
            v.addWidget(l)
            v.addWidget(widget)
            form_layout.addLayout(v)
        layout.addLayout(form_layout)

        # 按钮区
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("添加")
        self.update_btn = QPushButton("修改")
        self.delete_btn = QPushButton("删除")
        self.search_btn = QPushButton("查询")
        for btn in [self.add_btn, self.update_btn, self.delete_btn, self.search_btn]:
            btn.setStyleSheet("font-size:15px;padding:7px 20px;border-radius:6px;background:#2196f3;color:white;")
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        # 新增退出登录和退出软件按钮
        top_btn_layout = QHBoxLayout()
        self.logout_btn = QPushButton("退出登录")
        self.exit_btn = QPushButton("退出软件")
        top_btn_layout.addWidget(self.logout_btn)
        top_btn_layout.addWidget(self.exit_btn)
        layout.addLayout(top_btn_layout)

        # 表格区（多一列主修专业）
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(["ID", "学号", "姓名", "性别", "主修专业", "电话", "邮箱", "地址"])
        self.table.setStyleSheet("""
            QTableWidget{background:#eef7fa;font-size:16px;}
            QHeaderView::section{background:#bbdefb;font-size:15px;}
            QTableWidget::item:selected{background:#90caf9;}
        """)
        self.table.verticalHeader().setDefaultSectionSize(28)
        layout.addWidget(self.table)

        # 信号绑定
        self.add_btn.clicked.connect(self.add)
        self.update_btn.clicked.connect(self.update)
        self.delete_btn.clicked.connect(self.delete)
        self.search_btn.clicked.connect(self.search)
        self.table.cellClicked.connect(self.select_row)
        self.logout_btn.clicked.connect(self.logout)
        self.exit_btn.clicked.connect(self.exit_app)

        self.setStyleSheet("""
            QWidget{background-color:#f6f8fa;}
            QLineEdit{padding:5px;margin:3px;border-radius:4px;border:1px solid #b0bec5;}
            QLabel{font-size:14px;}
        """)

    def logout(self):
        reply = QMessageBox.question(self, '确认', '确定要退出登录吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.hide()
            # 重新显示登录窗口
            if self.login_window:
                self.login_window.show()

    def load_data(self, rows=None):
        if rows is None:
            rows = get_all_students()
        self.table.setRowCount(0)
        for row in rows:
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            for col, item in enumerate(row):
                self.table.setItem(row_pos, col, QTableWidgetItem(str(item)))

    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.student_number_input.setText(self.table.item(row, 1).text())
        self.name_input.setText(self.table.item(row, 2).text())
        self.gender_input.setText(self.table.item(row, 3).text())
        self.major_input.setText(self.table.item(row, 4).text())
        self.phone_input.setText(self.table.item(row, 5).text())
        self.email_input.setText(self.table.item(row, 6).text())
        self.address_input.setText(self.table.item(row, 7).text())

    def add(self):
        if not self.student_number_input.text() or not self.name_input.text():
            QMessageBox.warning(self, "提示", "学号和姓名不能为空")
            return
        add_student(
            self.student_number_input.text(), self.name_input.text(), self.gender_input.text(), self.major_input.text(),
            self.phone_input.text(), self.email_input.text(), self.address_input.text()
        )
        self.load_data()

    def update(self):
        if self.selected_id:
            update_student(
                self.selected_id, self.student_number_input.text(), self.name_input.text(), self.gender_input.text(),
                self.major_input.text(), self.phone_input.text(), self.email_input.text(), self.address_input.text()
            )
            self.load_data()

    def delete(self):
        if self.selected_id:
            delete_student(self.selected_id)
            self.load_data()

    def exit_app(self):
        reply = QMessageBox.question(self, '确认', '确定要退出软件吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

    def search(self):
        rows = query_students(
            student_number=self.student_number_input.text() or None,
            name=self.name_input.text() or None,
            gender=self.gender_input.text() or None,
            major=self.major_input.text() or None,
            phone=self.phone_input.text() or None,
            email=self.email_input.text() or None,
            address=self.address_input.text() or None
        )
        self.load_data(rows)


def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    main_window = StudentWindow()
    main_window.login_window = login  # 关键：主界面持有登录界面的引用

    def show_main():
        main_window.show()
        login.hide()

    login.on_login_success = show_main
    login.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
