# -- coding: utf-8 --
import pymysql
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

# User API 구현을 위한 새로운 패키지 로드
from flask import jsonify
from flask import request
from flask import session

# 암호화
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
# 토큰
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies)

#flask_cors 사용
from flask_cors import CORS, cross_origin

import datetime

app = Flask(__name__)
api = Api(app)

#flask_cors 사용
CORS(app)

# db 연결
db = pymysql.connect(
        user = 'root',
        passwd = '',
        host = '127.0.0.1',
        port = 3306,
        db = 'webportfolio',
        charset = 'utf8'
    )

cursor = db.cursor(pymysql.cursors.DictCursor)

"""
User APIs : 유저 SignUp / Login / Logout

SignUp API : *fullname*, *email*, *password* 를 입력받아 새로운 유저를 가입시킵니다.
Login API : *email*, *password* 를 입력받아 특정 유저로 로그인합니다.
Logout API : 현재 로그인 된 유저를 로그아웃합니다.
"""
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('fullname')
parser.add_argument('email')
parser.add_argument('password')

# 토큰 생성에 사용될 Secret Key를 flask 환경 변수에 등록
app.config.update(
			DEBUG = True,
			JWT_SECRET_KEY = "I'M DAIN"
		)
# JWT 확장 모듈을 flask 어플리케이션에 등록
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

@app.route('/signup', methods=["POST"])
def register():
    args = parser.parse_args()
    sql = "INSERT INTO `user` (`fullname`, `email`, `password`) VALUES (%s, %s, %s)"
    cursor.execute(sql, (args['fullname'],args['email'],generate_password_hash(args['password'])))

    sql2 = "SELECT id FROM `user` WHERE email = (%s)"
    cursor.execute(sql2, (args['email'])) 
    result = cursor.fetchone()

    sql3 = "INSERT INTO `profile` (`image_path`, `bio`, `user_id`) VALUES (null, null, %s)"
    cursor.execute(sql3, (result.get('id')))

    db.commit()
    
    return jsonify(status = "success", result = {"fullname": args["fullname"]})
        
@app.route('/login', methods=["POST"])
def login():
    args = parser.parse_args()
    sql = "SELECT * FROM `user` WHERE email = %s"
    cursor.execute(sql, (args['email'],))
    user = cursor.fetchone()  
    if check_password_hash(user['password'], args['password']):
        sql2 = "UPDATE `user` SET visit = %s WHERE id = %s" #추가
        visit = user['visit'] + 1
        cursor.execute(sql2, (visit,user['id'])) #추가
        token_identity = {'id': user['id'], 'name': user['fullname'], 'email':user['email'], 'visit':user['visit']} #추가
        access_token = create_access_token(identity=token_identity)
        return jsonify(status = "success", access_token=access_token)
    else: #아이디, 비밀번호가 일치하지 않는 경우
        return jsonify(result = "Invalid Params!")

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print("welcome to vip zone")
    return jsonify(logged_in_as=current_user)

"""
Education APIs - 학력 CRUD

Create API : 학교이름(college), 전공(major), 학위(degree) 정보를 입력받습니다.
Read API : 이미 저장되어 있는 학력 내용을 가져옵니다.
Update API : 이미 저장되어 있는 정보를 변경합니다.
Delete API : 특정 학력을 제거합니다.
"""
parser.add_argument('college')
parser.add_argument('major')
parser.add_argument('degree')
parser.add_argument('id')

class Education(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity() # 나중에 바꿔줘야함
        # args = parser.parse_args()     
        sql = "SELECT * FROM `education` WHERE user_id = (%s)"
        cursor.execute(sql, (current_user['id'])) #args["id"]
        result = cursor.fetchall()
        return jsonify(status = "success", result = result)

    @jwt_required()    
    def post(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "INSERT INTO `education` (`college`,`major`,`degree`,`user_id`) \
            VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (args["college"],args["major"],args["degree"],current_user['id']))
        # ----------------------------------------------------------------------
        sql2 = "SELECT * FROM `education` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result) 
    
    @jwt_required()    
    def put(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "UPDATE `education` SET college = %s, major = %s, degree = %s WHERE `id` = %s AND `user_id` = %s"
        cursor.execute(sql, (args["college"],args["major"],args["degree"], args["id"], current_user['id']))
        # ----------------------------------------------------------------------
        sql2 = "SELECT * FROM `education` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result)   
    
    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "DELETE FROM `education` WHERE `id` = %s AND `user_id` = %s"
        cursor.execute(sql, (args["id"], current_user['id']))
       # 바뀐 결과 읽어오기----------------------------------------------------------------------
        sql2 = "SELECT * FROM `education` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result)   


api.add_resource(Education, '/education')

"""
Awards APIs - 수상이력 CRUD

Create API : 수상내역(award), 상세내역(detail) 정보를 입력받습니다.
Read API : 이미 저장되어 있는 수상 내용을 가져옵니다.
Update API : 이미 저장되어 있는 정보를 변경합니다.
Delete API : 특정 수상이력을 제거합니다.
"""
parser.add_argument('award')
parser.add_argument('detail')
parser.add_argument('id')

class Awards(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity() # 나중에 바꿔줘야함    
        # args = parser.parse_args() 
        sql = "SELECT * FROM `awards` WHERE user_id = (%s)"
        cursor.execute(sql, (current_user['id'])) #args["id"]
        result = cursor.fetchall()
        return jsonify(status = "success", result = result)

    @jwt_required()    
    def post(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "INSERT INTO `awards` (`award`,`detail`,`user_id`) \
            VALUES (%s,%s,%s)"
        cursor.execute(sql, (args["award"],args["detail"],current_user['id']))
        # 바뀐 결과 읽어오기----------------------------------------------------------------------
        sql2 = "SELECT * FROM `awards` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result)  
        # return jsonify(status = "success", result = {"award": args["award"]})
    
    @jwt_required()    
    def put(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "UPDATE `awards` SET award = %s, detail = %s WHERE `id` = %s AND `user_id` = %s"
        cursor.execute(sql, (args["award"],args["detail"],args["id"], current_user['id']))
        # 바뀐 결과 읽어오기----------------------------------------------------------------------
        sql2 = "SELECT * FROM `awards` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result)  
        # return jsonify(status = "success", result = {"id": args["id"], "award": args["award"]})
    
    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "DELETE FROM `awards` WHERE `id` = %s AND `user_id` = %s"
        cursor.execute(sql, (args["id"], current_user['id']))
        # 바뀐 결과 읽어오기----------------------------------------------------------------------
        sql2 = "SELECT * FROM `awards` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result)  
        # return jsonify(status = "success", result = {"id": args["id"]})

api.add_resource(Awards, '/awards')

"""
Projects APIs - 프로젝트 CRUD

Create API : 프로젝트 이름(project)과 상세내역(detail),날짜(startDate,endDate)을 입력받습니다.
Read API : 이미 저장되어 있는 프로젝트 내용을 가져옵니다.
Update API : 이미 저장되어 있는 정보를 변경합니다.
Delete API : 특정 프로젝트를 제거합니다.
"""
parser.add_argument('project')
parser.add_argument('detail')
parser.add_argument('startDate')
parser.add_argument('endDate')
parser.add_argument('id')

class Projects(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity() # 나중에 바꿔줘야함
        # args = parser.parse_args()        
        sql = "SELECT * FROM `projects` WHERE user_id = (%s)"
        cursor.execute(sql, (current_user['id'])) #args["id"]
        result = cursor.fetchall()
        return jsonify(status = "success", result = result)

    @jwt_required()    
    def post(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "INSERT INTO `projects` (`project`,`detail`,`start_date`,`end_date`,`user_id`) \
            VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (args["project"],args["detail"],args["startDate"],args["endDate"],current_user['id']))
        # ----------------------------------------------------------------------
        sql2 = "SELECT * FROM `projects` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result) 
        # return jsonify(status = "success", result = {"project": args["project"]})
    
    @jwt_required()    
    def put(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "UPDATE `projects` SET project = %s, detail = %s, start_date = %s, end_date = %s WHERE `id` = %s AND `user_id` = %s"
        cursor.execute(sql, (args["project"],args["detail"],args["startDate"],args["endDate"],args["id"], current_user['id']))
        # ----------------------------------------------------------------------
        sql2 = "SELECT * FROM `projects` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result) 
        # return jsonify(status = "success", result = {"id": args["id"], "project": args["project"]})
    
    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "DELETE FROM `projects` WHERE `id` = %s AND `user_id` = %s"
        cursor.execute(sql, (args["id"], current_user['id']))
        # ----------------------------------------------------------------------
        sql2 = "SELECT * FROM `projects` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result) 
        # return jsonify(status = "success", result = {"id": args["id"]})


api.add_resource(Projects, '/projects')

"""
Certificates APIs - 자격증 CRUD

Create API : 자격증 이름(certificate), 공급기관(organization),날짜(get_date)을 입력받습니다.
Read API : 이미 저장되어 있는 자격증 내용을 가져옵니다.
Update API : 이미 저장되어 있는 정보를 변경합니다.
Delete API : 특정 자격증을 제거합니다.
"""
parser.add_argument('certificate')
parser.add_argument('organization')
parser.add_argument('get_date')
parser.add_argument('id')

class Certificates(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity() # 나중에 바꿔줘야함
        # args = parser.parse_args()            
        sql = "SELECT * FROM `certificates` WHERE user_id = (%s)"
        cursor.execute(sql, (current_user['id'])) #args["id"]
        result = cursor.fetchall()
        return jsonify(status = "success", result = result)

    @jwt_required()    
    def post(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "INSERT INTO `certificates` (`certificate`,`organization`,`get_date`,`user_id`) \
            VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (args["certificate"],args["organization"],args["get_date"],current_user['id']))
        # ----------------------------------------------------------------------
        sql2 = "SELECT * FROM `certificates` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result) 
        # return jsonify(status = "success", result = {"certificate": args["certificate"]})
    
    @jwt_required()    
    def put(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "UPDATE `certificates` SET certificate = %s, organization = %s, get_date = %s WHERE `id` = %s AND `user_id` = %s"
        cursor.execute(sql, (args["certificate"],args["organization"],args["get_date"],args["id"], current_user['id']))
        # ----------------------------------------------------------------------
        sql2 = "SELECT * FROM `certificates` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result) 
        # return jsonify(status = "success", result = {"id": args["id"], "certificate": args["certificate"]})
    
    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "DELETE FROM `certificates` WHERE `id` = %s AND `user_id` = %s"
        cursor.execute(sql, (args["id"], current_user['id']))
        # ----------------------------------------------------------------------
        sql2 = "SELECT * FROM `certificates` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result) 
        # return jsonify(status = "success", result = {"id": args["id"]})


api.add_resource(Certificates, '/certificates')

"""
Profile APIs - 프로필 CRUD

Create API : 이미지(image_path), 소개(bio)를 입력받습니다.
Read API : 이미 저장되어 있는 프로필 내용을 가져옵니다.
Update API : 이미 저장되어 있는 정보를 변경합니다.
"""
parser.add_argument('image_path')
parser.add_argument('bio')
parser.add_argument('id')

class Profile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity() # 나중에 바꿔줘야함
        # args = parser.parse_args()            
        sql = "SELECT * FROM `profile` WHERE user_id = (%s)"
        cursor.execute(sql, (current_user['id'])) #args["id"]
        result = cursor.fetchall()
        return jsonify(status = "success", result = result, crnt_user=current_user)

    @jwt_required()    
    def put(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        sql = "UPDATE `profile` SET image_path = %s, bio = %s WHERE `id` = %s AND `user_id` = %s"
        cursor.execute(sql, (args["image_path"],args["bio"],args["id"], current_user['id']))
        # ----------------------------------------------------------------------
        sql2 = "SELECT * FROM `profile` WHERE user_id = (%s)"
        cursor.execute(sql2, (current_user['id'])) 
        result = cursor.fetchall()
        db.commit()
        return jsonify(status = "success", result = result) 
        # return jsonify(status = "success", result = {"id": args["id"], "certificate": args["certificate"]})

"""
Users APIs - 다른유저 R

Read API : 이미 저장되어 있는 프로필 내용을 가져옵니다.

"""
class Users(Resource):
    @jwt_required()
    def get(self):
        sql = "SELECT * FROM user \
                INNER JOIN profile \
                ON user.id = profile.user_id"
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(status = "success", result = result)

api.add_resource(Users, '/users')

"""
Users APIs - 다른유저 R

Read API : 이미 저장되어 있는 프로필 내용을 가져옵니다.

"""
class Usersdetail(Resource):
    @jwt_required()
    def get(self,user_id=None):
        profile = "SELECT user.id,user.fullname,user.email, profile.image_path,profile.bio\
        FROM user INNER JOIN profile ON user.id = profile.user_id WHERE user_id = %s"
        cursor.execute(profile, (user_id))
        result_profile = cursor.fetchall()

        edu = "SELECT * FROM `education` WHERE user_id = %s"
        cursor.execute(edu, (user_id))
        result_edu = cursor.fetchall()

        award = "SELECT * FROM `awards` WHERE user_id = %s"
        cursor.execute(award, (user_id))
        result_award = cursor.fetchall()

        cert = "SELECT * FROM `certificates` WHERE user_id = %s"
        cursor.execute(cert, (user_id))
        result_cert = cursor.fetchall()

        project = "SELECT * FROM `projects` WHERE user_id = %s"
        cursor.execute(project, (user_id))
        result_project = cursor.fetchall()

        return jsonify(status = "success", result_edu = result_edu,
         result_award=result_award, result_cert = result_cert,
         result_project = result_project, result_profile=result_profile)

api.add_resource(Usersdetail, '/usersdetail/<user_id>')

# 배포할 때
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True, threaded=False)
