import requests
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# ⚠️ 구글 설문지 정보
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScue2gDW0CP4LPX9EJrXsl6YxMAuVa4SAGBH8IsmD5MxA45og/formResponse"
NAME_ID = "entry.1151854322"
ACTION_ID = "entry.563449125"

# 서버가 켜져 있는 동안만 임시로 보여줄 기록 리스트 (DB 대신 사용)
temp_logs = []

@app.route('/')
def index():
    # 임시 리스트에 있는 최근 기록 20개를 화면에 전달
    return render_template('index.html', logs=temp_logs[:20])

@app.route('/add', methods=['POST'])
def add():
    cat_name = request.form['cat_name']
    action = request.form['action']
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. 구글 설문지(시트)로 전송 (이게 진짜 저장!)
    payload = {
        NAME_ID: cat_name,
        ACTION_ID: action
    }
    try:
        requests.post(GOOGLE_FORM_URL, data=payload)
    except Exception as e:
        print(f"Google 전송 실패: {e}")

    # 2. 화면에 바로 보여주기 위해 임시 리스트 맨 앞에 추가
    temp_logs.insert(0, (cat_name, action, now))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # init_db() 같은 DB 관련 호출 다 삭제됨
    app.run(host='0.0.0.0', port=5001, debug=True)