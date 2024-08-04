from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def generate_id(storage):
    """Get a list of dict and sum 1 to the latest id and returns it"""
    max_id = 0
    for data in storage:
        if max_id < data["id"]:
            max_id = data["id"]
    return max_id + 1


@app.route("/api/posts", methods=["GET"])
def get_posts():
    """
    Returns the Data.
    If the request contains sort and direction keys will sorted before return.
    """
    sort = request.args.get("sort")
    direction = request.args.get("direction")

    # Validate if value for sort argument is valid
    if sort and sort not in ["post", "title"]:
        response = {
            "error": "Bad Request",
            "message": f"value {sort} is not allowed! Please choose between post and title!",
        }
        return jsonify(response), 400

    # Validate if value for sort argument is valid
    if direction and direction not in ["asc", "desc"]:
        response = {
            "error": "Bad Request",
            "message": f"value {sort} is not allowed! Please choose between asc and desc!",
        }
        return jsonify(response), 400

    # If value for sort argument is title.
    if sort == "title":
        if direction == "asc":
            sorted_posts = sorted(POSTS, key=lambda x: x["title"])
        elif direction == "desc":
            sorted_posts = sorted(POSTS, key=lambda x: x["title"], reverse=True)
        return jsonify(sorted_posts)

    # If value for sort argument is post.
    if sort == "post":
        if direction == "asc":
            sorted_posts = sorted(POSTS, key=lambda x: x["post"])
        elif direction == "desc":
            sorted_posts = sorted(POSTS, key=lambda x: x["post"], reverse=True)
        return jsonify(sorted_posts)

    return jsonify(POSTS)


@app.route("/api/posts", methods=["POST"])
def add_post():
    """
    Gets a JSON file and store the data into Storage and returns new Data.
    """
    post_json = request.get_json()

    # Validate Data
    if (
        "title" not in post_json and "content" not in post_json
    ):  # If response JSON didnt have title and content.
        response = {
            "error": "Bad Request",
            "message": "Missing fields: 'title', 'content'",
        }
        return response, 400

    elif "title" not in post_json:  # If response JSON didnt have title
        response = {"error": "Bad Request", "message": "Missing fields: 'title'"}
        return response, 400

    elif "content" not in post_json:  # If response JSON didnt have content
        response = {"error": "Bad Request", "message": "Missing fields: 'content'"}
        return response, 400

    # add new data to storage.
    id = generate_id(POSTS)
    new_data = {"id": id, "title": post_json["title"], "content": post_json["content"]}
    POSTS.append(new_data)
    return jsonify(POSTS)


@app.route("/api/posts", methods=["DELETE"])
def delete_post():
    """
    Get a id as argument and delete it from POSTS.
    """
    global POSTS
    id = request.args.get("id")

    # Checks if id is in POSTS.
    id_in_posts = False
    for data in POSTS:
        if int(id) == data["id"]:
            id_in_posts = True

    # If id not in POSTS.
    if not id_in_posts:
        response = {
            "error": "Bad Request",
            "message": "There is no post with the given id",
        }
        return response, 400

    # Save new data and retun success message.
    POSTS = [data for data in POSTS if data["id"] != int(id)]
    message = {"message": f"Post with id {id} has been deleted successfully."}
    return jsonify(message)


@app.route("/api/posts", methods=["PUT"])
def update_post():
    """
    Get a id as argument and gets a json which data have to be changed.
    Changes the Data and replace it in POSTS.
    """
    global POSTS
    id = request.args.get("id")
    json_data = request.get_json()

    # Checks if id is in POSTS.
    id_in_posts = False
    for data in POSTS:
        if int(id) == data["id"]:
            id_in_posts = True

    # If id not in POSTS return 404
    if not id_in_posts:
        response = {
            "error": "Bad Request",
            "message": "There is no post with the given id",
        }
        return response, 400

    # Validate if keys are in Data.
    keys = ["id", "title", "content"]
    for key in json_data.keys():
        if key not in keys:
            response = {"error": "Bad Request", "message": f"{key} is not a valid key."}
            return response, 400

    # Fetch old data from POSTS
    for data in POSTS:
        if data["id"] == int(id):
            old_data = {
                "id": data["id"],
                "title": data["title"],
                "content": data["content"],
            }

    # Iterate throught old data and replace it with new
    new_data = {}
    for key in old_data.keys():
        if key in json_data:
            new_data[key] = json_data[key]
        else:
            new_data[key] = old_data[key]

    # Delete old data and insert new data.
    POSTS = [data for data in POSTS if data["id"] != int(id)]
    POSTS.append(new_data)

    return jsonify(new_data)


@app.route("/api/posts/search", methods=["GET"])
def search_post():
    """
    Get a Keyword as argument and returns all the matching post titles.
    """
    title_query = request.args.get("title")
    content_query = request.args.get("content")

    # Checks if the given key is title
    # Append to list if title_query in title
    if title_query:
        post_list = []
        for data in POSTS:
            if title_query.lower() in data["title"].lower():
                post_list.append(data)

    # Checks if the given key is post
    # Append to list if post_query in post
    if content_query:
        post_list = []
        for data in POSTS:
            if content_query.lower() in data["content"].lower():
                post_list.append(data)

    return jsonify(post_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
