from flask import Flask
from db import init_db, close_db, get_db
from auth import auth
from board import board
from admin import admin_bp

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# 블루프린트 등록
app.register_blueprint(auth)
app.register_blueprint(board)
app.register_blueprint(admin_bp)

# DB 연결 해제 등록
app.teardown_appcontext(close_db)

if __name__ == '__main__':
    init_db()        # DB 테이블 생성 및 관리자 계정 초기화
    app.run(debug=True)