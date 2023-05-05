from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder="../frontend/dist",
            static_folder="../frontend/dist/assets")


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# app.config['JSON_AS_ASCII'] = False


# @app.route("/user/login", methods=["POST"])
# def user_login():
#     """
#     用户登录
#     :return:
#     """
#     data = request.get_json()
#     userName = data.get("userName")
#     password = data.get("password")
#     if userName == "admin" and password == "123456":
#         return jsonify({
#             "code": 0,
#             "data": {
#                 "token": "666666"
#             }
#         })
#     else:
#         return jsonify({
#             "code": 99999999,
#             "msg": "用户名或密码错误"
#         })


# @app.route("/user/info", methods=["GET", "POST"])
# def user_info():
#     """
#     获取当前用户信息
#     :return:
#     """
#     token = request.headers.get("token")
#     if token == "666666":
#         return jsonify({
#             "code": 0,
#             "data": {
#                 "id": "1",
#                 "userName": "admin",
#                 "realName": "张三",
#                 "userType": 1
#             }
#         })
#     return jsonify({
#         "code": 99990403,
#         "msg": "token不存在或已过期"
#     })

if __name__ == '__main__':
    app.run(host="0.0.0.0")
