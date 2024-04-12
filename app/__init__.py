from flask_restx import Api
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app,  title='WITH CHAT API 문서', description='Swagger 문서', doc="/docs")
jwt = JWTManager(app)

jwt_blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    if request.endpoint == 'sign_api.logout':
        print("토큰 파기")
        jti = jwt_payload['jti']
        return jti in jwt_blocklist
    else:
        # 다른 요청에 대해서는 블록 리스트 확인하지 않음
        return False


app.config['JWT_SECRET_KEY'] = os.getenv("T_S_KEY")
app.config['SECRET_KEY'] = os.getenv("S_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=20)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=3)

from app.routes.sign import sign_api
from app.routes.user import user_api
from app.routes.comment import comment_api
from app.routes.category import cate_api
from app.routes.board import board_api

api.add_namespace(sign_api)
api.add_namespace(user_api)
api.add_namespace(comment_api)
api.add_namespace(cate_api)
api.add_namespace(board_api)





if __name__ == '__main__':
    app.run(debug=True, port=3000, host='192.168.0.18')
