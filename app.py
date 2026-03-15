from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# DB 초기화 함수 (테이블이 없으면 자동으로 생성)
def init_db():
    conn = sqlite3.connect('cat_care.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  cat_name TEXT,
                  action TEXT,
                  timestamp DATETIME DEFAULT (datetime('now', 'localtime')))''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('cat_care.db')
    c = conn.cursor()
    # 최근 기록 20개 가져오기
    c.execute("SELECT cat_name, action, timestamp FROM logs ORDER BY timestamp DESC LIMIT 20")
    logs = c.fetchall()
    conn.close()
    return render_template('index.html', logs=logs)

# 기록 추가하기 로직
@app.route('/add', methods=['POST'])
def add():
    cat_name = request.form['cat_name']
    action = request.form['action']
    
    conn = sqlite3.connect('cat_care.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (cat_name, action) VALUES (?, ?)", (cat_name, action))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)