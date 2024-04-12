from flask_restx import Namespace, Resource
from flask import Flask, request, jsonify
import sqlite3
from app.database import db_manager as DB




user_api = Namespace("User", description="사용자 정보 API", path='/with')


@user_api.route('/user')
class userinfo(Resource):
    def get(self):
        """
                회원 단건 조회

                GET 요청으로 회원 정보를 조회합니다.
                """
        return {"회원정보": "get success!!"}

    def put(self):
        """
                회원 수정

                put 요청으로 회원 정보를 수정합니다.
                """
        return {"회원수정": "put success!!"}


@user_api.route('/user/{userIdx}')
class userinfo(Resource):
    def delete(self):
        """
                        회원 삭제

                        delete 요청으로 회원을 삭제합니다.
                        """
        return {"회원삭제": "delete success!!"}


@user_api.route('/users')
class userinfo(Resource):
    def get(self):
        """
            회원 리스트 조회

            GET 요청으로 회원 리스트를 조회합니다.
        """