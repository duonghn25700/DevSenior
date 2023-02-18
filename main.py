from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from utils.utils import beetoon_api
import requests
import json

mydb = beetoon_api(host='localhost',user='root',password="S@1989", db='crawl_beetoon')
app = Flask(__name__)

# Danh sach tat ca category
@app.route("/manga/categories", methods=["GET"])
def get_categories():
    
    per_page = request.args.get('page_size', 50, type=int)
    page = request.args.get('page', 1, type=int)

    data = mydb.get_categories(per_page, page)
    comics = data["data"]

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    sliced_comics = comics[start_index:end_index]
    data['data'] = sliced_comics

    return jsonify(data)

# Danh sach manga theo category id
@app.route("/manga/categories/<int:category_id>")
def get_category_by_id(category_id):
    # data = mydb.get_category_by_id(category_id)
    # comics = data["data"]

    per_page = request.args.get('page_size', 36, type=int)
    page = request.args.get('page', 1, type=int)

    data = mydb.get_category_by_id(per_page, page, category_id)
    comics = data["data"]

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    sliced_comics = comics[start_index:end_index]
    data['data'] = sliced_comics
    
    return jsonify(data)
# Danh sach tat ca manga
@app.route("/manga", methods=["GET"])
def get_manga():
    

    per_page = request.args.get('page_size', 50, type=int)
    page = request.args.get('page', 1, type=int)
    data = mydb.get_from_manga(per_page, page)
    comics = data["data"]
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    sliced_comics = comics[start_index:end_index]
    data['data'] = sliced_comics

    return jsonify(data)

# Chi tiet manga theo ID
@app.route("/manga/<int:manga_id>", methods = ['GET'])
def get_manga_by_id(manga_id):
    data = mydb.get_manga_by_id(manga_id)
    return jsonify(data)

# Danh sach chapter theo manga id
@app.route("/manga/<int:manga_id>/chapter", methods = ['GET'])
def get_chapter_list_by_manga(manga_id):
    data = mydb.get_chapter_list_by_manga(manga_id)
    return jsonify(data)

# Chi tiet chapter theo id
@app.route("/manga/<int:manga_id>/chapter/chapter-<int:chapter_id>", methods = ['GET'])
def get_chapter_by_id(manga_id, chapter_id):
    data = mydb.get_chapter_by_id(manga_id, chapter_id)
    return jsonify(data)

# User register
@app.route("/user_register", methods=["POST"])
def user_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    data = mydb.insert_user_inf(username,email, password)
    return jsonify({"Message": data})

# User login
@app.route("/login", methods=["POST"])
def user_login():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    message = mydb.check_user_login(username,email,password)
    return jsonify({"Message":message})

# User logout
@app.route("/logout", methods=["POST"])
def user_logout():
    username = request.form.get('username')
    message = mydb.user_logout(username)
    return message

# Send veirify account
@app.route("/send-verify", methods=["POST"])
def verify_email():
    email = request.form.get('email')
    message = mydb.verify_email(email)
    return jsonify({"Message":message})

# Comment theo manga
@app.route("/manga/<int:manga_id>/comments", methods=["GET", "POST"])
def comment_manga(manga_id):
    if request.method == "POST":
        comment = request.form.get('content')
        user_id = request.form.get('user_id', type=int)
        message = mydb.post_comment_manga(user_id,manga_id,comment)
        return jsonify({"Message":message})
    elif request.method == "GET":
        data = mydb.get_comment_manga(manga_id)
        return jsonify({"data": data})

# Edit, Delete comment ID
@app.route("/manga/<int:manga_id>/comments/<int:comment_id>", methods=["PUT", "DELETE"])
def comment_manga_by_id(manga_id, comment_id):
    if request.method == "PUT":
        content = request.form.get('content')
        message = mydb.update_comment_manga(manga_id, comment_id, content)
        return jsonify({"Message": message})
    elif request.method == "DELETE":
        message = mydb.delete_comment_manga(manga_id, comment_id)
        return jsonify({"Message": message})

# Get Profile User
@app.route("/info", methods=["GET"])
def user_information():
    username = request.form.get('username')
    if username == "":
        return {"Message":"No information. Please Enter username profile"}
    else:
        data = mydb.show_user_information(username)
        return jsonify(data)
# Put Profile User
@app.route("/user/update-profile", methods=["PUT"])
def update_user_information():
    username = request.form.get('username')
    data_to_update = request.form.get('data_to_update')
    val_to_update = request.form.get('val_to_update')
    data = mydb.update_user_information(username, data_to_update, val_to_update)
    return data

@app.route("/home", methods=["GET"])
def get_new():
    per_page = request.args.get('page_size', 36, type=int)
    page = request.args.get('page', 1, type=int)

    data = mydb.get_from_manga(per_page, page)
    comics = data["data"]

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    sliced_comics = comics[start_index:end_index]
    data['data'] = sliced_comics
    return data
#     return jsonify({"message":"""Welcome to Tozi Manga!\nWe are thrilled to have you here and we hope you'll enjoy exploring our extensive collection of manga titles.\nOur app is designed to make your manga reading experience as seamless and enjoyable as possible. Whether you're a long-time manga fan or a newcomer to the genre, you'll find something to love on our platform.\nWe have a wide range of manga titles available, from classic series to new releases. You can easily search and discover new titles using our intuitive interface, and our recommendation engine will help you find new manga that you'll love based on your reading history.
# """})

# Change user password
@app.route("/user/change-password", methods=["PUT"])
def change_password():
    username = request.form.get("username")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    data = mydb.change_password(username, old_password, new_password)
    return data

# Add favorite manga id
@app.route("/favorite/<int:manga_id>", methods=["POST"])
def add_favortite_manga(manga_id):
    username = request.form.get("username")
    is_favorite = request.form.get("is_favorite")
    data = mydb.add_favortite_manga(username,is_favorite, manga_id)
    return jsonify({"Message":data})

# Get favorite manga id
@app.route("/favorite", methods=["GET"])
def get_favorite_manga():
    username = request.form.get("username")
    data = mydb.get_favorite_manga(username)
    return data


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5002)