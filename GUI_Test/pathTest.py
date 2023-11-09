import os

# 獲取app.py所在的目錄
app_dir = os.path.dirname('13.212.185.167:5000')
print(app_dir)

# 資料庫文件的絕對路徑
db_path = os.path.join(app_dir, "mydatabase.db")
print(db_path)
