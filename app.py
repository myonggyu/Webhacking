# Flask 앱을 생성하고 각 기능별 블루프린트를 등록하는 파일입니다.
from flask import Flask
from db import init_db
from auth import auth_bp
from board import board_bp
from admin import admin_bp


def create_app():
    # 애플리케이션 기본 설정과 DB 초기화를 수행하는 함수입니다.
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-this-secret-key"

    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(board_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()

if __name__ == "__main__":
    # 개발용 서버를 실행합니다.
    app.run(debug=True)