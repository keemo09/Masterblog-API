# Flask Blog API

This is a simple Flask-based API for managing blog posts. It supports the following operations:

- **GET** /api/posts: Fetch all posts with optional sorting.
- **POST** /api/posts: Create a new post.
- **PUT** /api/posts: Update an existing post.
- **DELETE** /api/posts: Delete a post by ID.
- **GET** /api/posts/search: Search for posts by title or content.

## Requirements

- Python 3.7+
- Flask
- Flask-CORS

## Installation

1. Clone the repository:
   git clone git@github.com:keemo09/Masterblog-API.git
   
2. Install dependencies:
   pip install -r requirements.txt

3. Run the application
   uvicorn app.main:app --reload

## Contributing

Contributions are welcome! Please follow the [contribution guidelines](CONTRIBUTING.md).


## Contact

Created by [keemo09](https://github.com/keemo09) - feel free to reach out!
