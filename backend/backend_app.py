from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def generate_id(storage):
    '''Get a list of dict and sum 1 to the latest id and returns it'''
    max_id = 0
    for data in storage:
        if max_id < data["id"]:
            max_id = data["id"]
    return max_id + 1


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    post_json = request.get_json()
    
    # Validate Data
    if "title" not in post_json and "content" not in post_json:
        response = {
            "error": "Bad Request",
            "message": "Missing fields: 'title', 'content'"
        }
        return response
    
    elif "title" not in post_json:
        response = {
            "error": "Bad Request",
            "message": "Missing fields: 'title'"
        }
        return response
    
    elif "content" not in post_json:
        response = {
            "error": "Bad Request",
            "message": "Missing fields: 'content'"
        }
        return response
    
    


    #add new data to storage
    id = generate_id(POSTS)
    new_data = {"id": id, "title": post_json["title"], "content": post_json["content"]}
    POSTS.append(new_data)
    return jsonify(POSTS)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
