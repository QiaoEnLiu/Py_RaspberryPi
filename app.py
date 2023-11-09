from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
# 資料庫路徑
# db_path = '/home/ubuntu/Py_Flask_sqlite_test/mydatabase.db'

# 初始化資料庫
def init_db():
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS example (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )
    ''')
    connection.commit()
    connection.close()

@app.route('/')
def index():
    init_db()
    # 取得所有資料表的名稱
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    connection.close()
    return render_template('index.html', tables=tables)

@app.route('/get_table_data', methods=['POST'])
def get_table_data():
    table_name = request.form['table_name']
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM table_name")
    records = cursor.fetchall()
    connection.close()
    records_data = [{'id': record[0], 'data': record[1]} for record in records]
    return jsonify(records_data)

#@app.route('/get_data')
#def get_data():
#    connection = sqlite3.connect(db_path+"mydatabase.db")
#    cursor = connection.cursor()
#    cursor.execute("SELECT * FROM your_table")
#    data = cursor.fetchall()
#    connection.close()
#    return jsonify(data)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0',port=5000, debug=True)
