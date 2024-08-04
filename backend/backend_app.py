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
    """
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
    global POSTS
    id = request.args.get("id")
    json_data = request.get_json()

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

    # If key not in keys.
    keys = ["id", "title", "content"]
    for key in json_data.keys():
        if key not in keys:
            response = {"error": "Bad Request", "message": f"{key} is not a valid key."}
            return response, 400

    for data in POSTS:
        if data["id"] == int(id):
            old_data = {
                "id": data["id"],
                "title": data["title"],
                "content": data["content"],
            }

    new_data = {}
    for key in old_data.keys():
        if key in json_data:
            new_data[key] = json_data[key]
        else:
            new_data[key] = old_data[key]

    POSTS = [data for data in POSTS if data["id"] != int(id)]
    POSTS.append(new_data)

    return new_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
