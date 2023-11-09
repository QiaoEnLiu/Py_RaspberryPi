# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 14:21:58 2023

@author: User
"""
import requests
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout,QFileDialog
from PyQt5.QtGui import QBrush, QColor


class SQLiteGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initDatabase()

    def initUI(self):
        self.setWindowTitle("SQLite 資料表應用程式")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # 新增資料表名稱輸入框
        self.table_name_input = QLineEdit(self)
        self.layout.addWidget(self.table_name_input)

        # 建立一個水平佈局用於包含多個按鈕
        button_layout = QHBoxLayout()

        # 新增資料表名稱按鈕
        self.btn_add_table = QPushButton("新增資料表名稱", self)
        self.btn_add_table.clicked.connect(self.showTableName)
        self.btn_add_table.clicked.connect(self.addTable)
        button_layout.addWidget(self.btn_add_table)
        
        # 顯示所有資料表按鈕
        self.btn_show_tables = QPushButton("顯示所有資料表", self)
        self.btn_show_tables.clicked.connect(self.showAllTables)
        button_layout.addWidget(self.btn_show_tables)
        
        # 查詢資料表按鈕
        self.btn_query_table = QPushButton("查詢資料表", self)
        self.btn_query_table.clicked.connect(self.queryTable) # 在類別SQLiteGUI中的initUI方法中新增查詢資料表按鈕的點擊事件
        button_layout.addWidget(self.btn_query_table)
        
        
        # 刪除資料表按鈕
        self.btn_delete_table = QPushButton("刪除資料表", self)
        self.btn_delete_table.clicked.connect(self.deleteTable)
        button_layout.addWidget(self.btn_delete_table)
        
        # 將按鈕佈局添加到主佈局
        self.layout.addLayout(button_layout)

        # 顯示資料表名稱的文字方塊
        self.table_name_label = QLabel(self)
        self.layout.addWidget(self.table_name_label)

        # 資料表
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)


        # 查詢輸入框及查詢按鈕放在水平布局中
        group2_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.btn_search = QPushButton("查詢", self)
        self.btn_search.clicked.connect(self.searchRecords)
        group2_layout.addWidget(self.search_input)
        group2_layout.addWidget(self.btn_search)
        self.layout.addLayout(group2_layout)

        # 其他元件保持不變
        group2_layout = QHBoxLayout()
        self.data_input = QLineEdit(self)
        self.btn_add = QPushButton("新增", self)
        self.btn_add.clicked.connect(self.addRecord)
        group2_layout.addWidget(self.data_input)
        group2_layout.addWidget(self.btn_add)
        self.layout.addLayout(group2_layout)

        # 刪除按鈕
        self.btn_delete = QPushButton("刪除選定的資料", self)
        self.btn_delete.clicked.connect(self.deleteSelectedRecord)
        self.layout.addWidget(self.btn_delete)
        
        self.delete_result_label = QLabel(self)
        self.layout.addWidget(self.delete_result_label)

        # 其他元件保持不變

        self.db_connection = None
        self.cursor = None

        #  # 新增一個按鈕用於上傳資料表
        # self.btn_upload_table = QPushButton("上傳資料表", self)
        # self.btn_upload_table.clicked.connect(self.upload_table)
        # self.layout.addWidget(self.btn_upload_table)

    
        
    def initDatabase(self):

        self.db_connection = sqlite3.connect("mydatabase.db")
        self.cursor = self.db_connection.cursor()

    # 在類別SQLiteGUI中新增queryTable方法
    def queryTable(self):
        table_name = self.table_name_input.text()
        if not table_name:
            return
    
        # 嘗試查詢資料表是否存在
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        existing_table = self.cursor.fetchone()
        
        if existing_table:
            self.table_name_label.setText(f"資料表名稱： {table_name}")
            self.loadRecords(table_name)
        else:
            self.table_name_label.setText(f"尚未有此資料表： {table_name}")
            
    def addTable(self):
        table_name = self.table_name_input.text()
        if not table_name:
            return
    
        # 嘗試查詢資料表是否存在
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        existing_table = self.cursor.fetchone()
    
        if existing_table:
            self.table_name_label.setText(f"資料表 {table_name} 已存在")
            self.table_name_input.clear()
            
        else:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)")
            self.db_connection.commit()
            self.table_name_label.setText(f"資料表名稱： {table_name}")
            
    def showAllTables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in self.cursor.fetchall()]
        self.table_name_label.setText("所有資料表：" + ", ".join(tables))
        
    def deleteTable(self):
        table_name = self.table_name_input.text()
        if not table_name:
            return
    
        # 嘗試查詢資料表是否存在
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        existing_table = self.cursor.fetchone()
    
        if existing_table:
            # 刪除資料表
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.db_connection.commit()
            self.table_name_label.setText(f"資料表 {table_name} 已刪除")
        else:
            self.table_name_label.setText(f"尚未有此資料表： {table_name}")
            
    def showTableName(self):
        table_name = self.table_name_input.text()
        if table_name:
            self.table_name_label.setText(f"資料表名稱： {table_name}")


    def addRecord(self):
        table_name = self.table_name_input.text()
        if not table_name:
            return

        data = self.data_input.text()
        self.cursor.execute(f"INSERT INTO {table_name} (data) VALUES (?)", (data,))
        self.db_connection.commit()
        self.data_input.clear()
        self.loadRecords(table_name)

    def searchRecords(self):
        table_name = self.table_name_input.text()
        if not table_name:
            return

        search_text = self.search_input.text()
        self.highlightMatchingRecords(table_name, search_text)

    def loadRecords(self, table_name):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in self.cursor.fetchall()]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        self.cursor.execute(f"SELECT * FROM {table_name}")
        records = self.cursor.fetchall()

        self.table.setRowCount(len(records))
        for i, record in enumerate(records):
            for j, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

    def deleteSelectedRecord(self):
        table_name = self.table_name_input.text()
        if not table_name:
            return

        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        primary_key = self.table.horizontalHeaderItem(0).text()
        primary_keys = [self.table.item(item.row(), 0).text() for item in selected_items]

        for primary_key_value in primary_keys:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE {primary_key}=?", (primary_key_value,))
            self.db_connection.commit()

        self.delete_result_label.setText(f"已刪除選定的資料")
        self.loadRecords(table_name)

    def highlightMatchingRecords(self, table_name, search_text):
        self.loadRecords(table_name)
        brush = QBrush(QColor(255, 255, 0))
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if search_text in item.text():
                    item.setBackground(brush)  # 將匹配的資料反白

    # def upload_table(self):
    #     # 打開檔案選擇對話方塊以選取要上傳的資料表檔案
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.ReadOnly  # 設置為只讀模式以選取檔案
    #     file_dialog = QFileDialog(self, options=options)
    #     file_dialog.setNameFilter("SQLite 資料庫檔案 (*.db *.sqlite)")
    #     file_dialog.setWindowTitle("選取要上傳的資料表")
    #     file_dialog.setFileMode(QFileDialog.ExistingFiles)
    #     if file_dialog.exec_():
    #         selected_files = file_dialog.selectedFiles()
    #         if selected_files:
    #             # 獲取選取的檔案路徑
    #             file_path = selected_files[0]

    #             # 您需要確保將資料表上傳到 Flask 應用程式的適當路由
    #             upload_route = ""

    #             # Flask 應用程式的公共 IP 和端口
    #             flask_ip = "13.212.185.167"
    #             flask_port = 5000  # 這是 Flask 應用程式運行的端口

    #             # 設置上傳請求的目標 URL
    #             upload_url = f"http://{flask_ip}:{flask_port}/{upload_route}"

    #             # 發送 POST 請求以上傳資料表
    #             with open(file_path, "rb") as file:
    #                 files = {"file": (file_path, file)}
    #                 response = requests.post(upload_url, files=files)

    #             if response.status_code == 200:
    #                 # 上傳成功
    #                 print("資料表已成功上傳")
    #             else:
    #                 # 上傳失敗，顯示錯誤訊息
    #                 print("無法上傳資料表",response.status_code)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SQLiteGUI()
    ex.show()
    sys.exit(app.exec_())