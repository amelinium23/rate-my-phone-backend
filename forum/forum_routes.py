import json
from typing import Any, Dict, List, Optional
from flask import Response, request, current_app, jsonify
from forum import FORUM
from dataclasses import asdict
from forum.model.post import Post
from logging import getLogger
from forum.utils.image_uploader import upload_to_images_storage
from main.firebase.firebase_app import verify_token
from werkzeug.datastructures import FileStorage


logger = getLogger(__name__)


@FORUM.route("/", methods=["GET"])
def get_all_posts() -> Response:
    try:
        db = current_app.config.get("FIRESTORE", None)
        doc = db.collection("posts").get()
        res = _parse_documents_to_list(doc)
        return jsonify(res)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/find", methods=["GET"])
def get_post_by_id() -> Response:
    try:
        db = current_app.config.get("FIRESTORE", None)
        post_id: str = request.args.get("id", "")
        doc = db.collection("posts").get()
        posts = _parse_documents_to_list(doc)
        post = _find_post_by_id(post_id, posts)
        return jsonify(post)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/post", methods=["GET"])
def get_all_post_by_user() -> Response:
    try:
        headers: Dict[str, Any] = request.headers
        token: str = str(headers["Authorization"]).split(" ")[1]
        assert token is not None, "Authorization header is required"
        user_uid: str = verify_token(token)["uid"]
        db = current_app.config.get("FIRESTORE", None)
        doc = db.collection("posts").document(user_uid).get().to_dict()
        posts = doc.get("posts", [])
        logger.info(f"[FORUM]: Get all posts for user {user_uid}!")
        return jsonify(posts)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/post", methods=["POST"])
def create_new_post() -> Response:
    try:
        data: Dict[str, Any] = request.form
        headers: Dict[str, Any] = request.headers
        files: Dict[str, FileStorage] = request.files
        token: str = str(headers["Authorization"]).split(" ")[1]
        assert token is not None, "Authorization header is required"
        user_uid: str = verify_token(token)["uid"]
        client = current_app.config.get("GOOGLE_CLOUD_CLIENT", None)
        db = current_app.config.get("FIRESTORE", None)
        new_doc = db.collection("posts").document(user_uid)
        new_post = Post(
            uid=user_uid,
            title=data.get("title", ""),
            description=data.get("description", ""),
            type=data.get("type", ""),
        )
        folder_name = f"{user_uid}/{new_post.id}"
        posts = new_doc.get().to_dict().get("posts", [])
        if files:
            file_names = upload_to_images_storage(files, folder_name, client)
            new_post.images = file_names
        posts.append(asdict(new_post))
        db.collection("posts").document(user_uid).set({"posts": posts})
        logger.info(f"[FORUM]: Created new post with title {new_post.title}!")
        return Response(f"Created new document id: {new_post.id}", status=200)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/post", methods=["DELETE"])
def delete_post() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        headers: Dict[str, Any] = request.headers
        token: str = str(headers["Authorization"]).split(" ")[1]
        assert token is not None, "Authorization header is required"
        user_uid: str = verify_token(token)["uid"]
        post_id: str = data.get("post_id", 0)
        db = current_app.config.get("FIRESTORE", None)
        doc = db.collection("posts").document(user_uid).get().to_dict()
        posts: List[Dict[str, Any]] = doc.get("posts", [])
        post: Optional[Dict[str, Any]] = _find_post_by_id(post_id, posts)
        assert post is not None, f"Post with id: {post_id} not found!"
        posts.remove(post)
        db.collection("posts").document(user_uid).set({"posts": posts})
        logger.info(f"[FORUM]: Deleted post with id: {post_id}!")
        return Response(f"Removed post with id: {post_id}.", status=200)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/post", methods=["PUT"])
def edit_post() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        headers: Dict[str, Any] = request.headers
        token: str = str(headers["Authorization"]).split(" ")[1]
        assert token is not None, "Authorization header is required"
        user_uid: str = verify_token(token)["uid"]
        post_id: str = data.get("post_id", "")
        db = current_app.config.get("FIRESTORE", None)
        doc = db.collection("posts").document(user_uid).get().to_dict()
        posts: List[Dict[str, Any]] = doc.get("posts", [])
        edited_posts: List[Dict[str, Any]] = _edit_post(posts, post_id, data)
        logger.info(f"[FORUM]: Edited post with id: {post_id}!")
        db.collection("posts").document(user_uid).set({"posts": edited_posts})
        return Response(f"Edited post with id: {post_id}.", status=200)
    except Exception as e:
        return Response(str(e), status=500)


def _find_post_by_id(
    post_id: str, posts: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    for post in posts:
        if post_id == post.get("id", 0):
            return post
    return None


def _edit_post(
    posts: List[Dict[str, Any]], post_id: str, edited_post: Dict[str, Any]
) -> List[Dict[str, Any]]:
    for index, post in enumerate(posts):
        if post_id == post.get("id", ""):
            posts[index] = edited_post
    return posts


def _parse_documents_to_list(collection) -> List[Dict[str, Any]]:
    posts = []
    for doc in collection:
        doc_posts = doc.get("posts") if doc.get("posts") is not None else []
        for post in doc_posts:
            posts.append(post)
    return posts
