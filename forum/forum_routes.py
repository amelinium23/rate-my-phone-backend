import json
from typing import Any, Dict, List, Optional
from uuid import uuid1
from flask import Response, request, current_app, jsonify
from forum import FORUM
from dataclasses import asdict
from forum.model.post import Post, Comment
from forum.utils.helper_function import (
    edit_comments,
    find_comment_by_id,
    find_post_by_id,
    get_docs_of_user,
    parse_documents_to_list,
    edit_post as h_edit_post,
    sort_documents,
)
from forum.utils.image_uploader import upload_to_images_storage
from main.firebase.firebase_app import verify_token
from werkzeug.datastructures import FileStorage
from google.cloud.firestore import Client as FirestoreClient
from user.utils.user_helpers import get_user_information


@FORUM.route("/", methods=["GET"])
def get_all_posts() -> Response:
    try:
        args: Dict[str, Any] = request.args.to_dict()
        sort_mode: str = args.get("sort_mode", "ascending").lower()
        sort_by: str = args.get("sort_by", "title").lower()
        db: FirestoreClient = current_app.config.get("FIRESTORE", None)
        doc = db.collection("posts").get()
        docs = parse_documents_to_list(doc)
        sorted_docs = sort_documents(docs, sort_mode, sort_by)
        return jsonify(sorted_docs)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/find", methods=["GET"])
def get_post_by_id() -> Response:
    try:
        db: FirestoreClient = current_app.config.get("FIRESTORE", None)
        post_id: str = request.args.get("id", "")
        doc: List = db.collection("posts").get()
        posts = parse_documents_to_list(doc)
        post = find_post_by_id(post_id, posts)
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
        db: FirestoreClient = current_app.config.get("FIRESTORE", None)
        doc = db.collection("posts").document(user_uid).get().to_dict()
        posts = doc.get("posts", [])
        return jsonify(posts)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/post", methods=["POST"])
def create_new_post() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        headers: Dict[str, Any] = request.headers
        token: str = str(headers["Authorization"]).split(" ")[1]
        assert token is not None, "Authorization header is required"
        user_uid: str = verify_token(token)["uid"]
        user = get_user_information(user_uid)
        db: FirestoreClient = current_app.config.get("FIRESTORE", None)
        new_post = Post(
            id=str(uuid1()),
            uid=user_uid,
            title=data.get("title", ""),
            description=data.get("description", ""),
            type=data.get("type", ""),
            device_key=data.get("device_key", ""),
            user=user,
        )
        posts: List[Dict[str, Any]] = get_docs_of_user(db, user_uid)
        posts.append(asdict(new_post))
        db.collection("posts").document(user_uid).set({"posts": posts})
        return jsonify({"post": asdict(new_post)})
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
        post_id: str = data.get("post_id", "")
        db = current_app.config.get("FIRESTORE", None)
        posts: List[Dict[str, Any]] = get_docs_of_user(db, user_uid)
        post: Optional[Dict[str, Any]] = find_post_by_id(post_id, posts)
        assert post is not None, f"Post with id: {post_id} not found!"
        posts.remove(post)
        db.collection("posts").document(user_uid).set({"posts": posts})
        return Response(f"Removed post with id: {post_id}.", status=200)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/post", methods=["PUT"])
def edit_post() -> Response:
    try:
        json_data: Dict[str, Any] = json.loads(request.data)
        headers: Dict[str, Any] = request.headers
        token: str = str(headers["Authorization"]).split(" ")[1]
        assert token is not None, "Authorization header is required"
        user_uid: str = verify_token(token)["uid"]
        post_id: str = json_data.get("id", "")
        db = current_app.config.get("FIRESTORE", None)
        posts: List[Dict[str, Any]] = get_docs_of_user(db, user_uid)
        edited_posts: List[Dict[str, Any]] = h_edit_post(posts, post_id, json_data)
        db.collection("posts").document(user_uid).set({"posts": edited_posts})
        return Response(f"Edited post with id: {post_id}.", status=200)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/post/upload", methods=["POST"])
def upload_image() -> Response:
    try:
        data: Dict[str, Any] = request.form
        headers: Dict[str, Any] = request.headers
        files: Dict[str, FileStorage] = request.files
        token: str = str(headers["Authorization"]).split(" ")[1]
        assert token is not None, "Authorization header is required"
        user_uid: str = verify_token(token)["uid"]
        post_id: str = data.get("id", "")
        db = current_app.config.get("FIRESTORE", None)
        client = current_app.config.get("GOOGLE_CLOUD_CLIENT", None)
        folder_name = f"{user_uid}/{post_id}"
        file_names = upload_to_images_storage(files, folder_name, client)
        posts: List[Dict[str, Any]] = get_docs_of_user(db, user_uid)
        post = find_post_by_id(post_id, posts) or {}
        post["images"] = file_names
        db.collection("posts").document(user_uid).set({"posts": posts})
        return jsonify(file_names)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/comment/add", methods=["POST"])
def add_comment() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        headers: Dict[str, Any] = request.headers
        token: str = str(headers["Authorization"]).split(" ")[1]
        user_uid: str = verify_token(token)["uid"]
        assert token is not None, "Authorization header is required"
        db: FirestoreClient = current_app.config.get("FIRESTORE", None)
        post_id: str = data.get("id", "")
        author_uid: str = data.get("authorId", "")
        author = get_user_information(user_uid)
        posts: List[Dict[str, Any]] = get_docs_of_user(db, author_uid)
        comment_body: str = data.get("comment", "")
        post = find_post_by_id(post_id, posts) or {}
        comments = post.get("comments", []) or []
        new_comment = asdict(
            Comment(id=str(uuid1()), user=author, uid=user_uid, comment=comment_body)
        )
        comments.append(new_comment)
        post["comments"] = comments
        edited_posts: List[Dict[str, Any]] = h_edit_post(posts, post_id, post)
        db.collection("posts").document(user_uid).set({"posts": edited_posts})
        return jsonify(new_comment)
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/comment/delete", methods=["DELETE"])
def delete_comment() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        headers: Dict[str, Any] = request.headers
        token: str = str(headers["Authorization"]).split(" ")[1]
        user_uid: str = verify_token(token)["uid"]
        assert token is not None, "Authorization header is required"
        db: FirestoreClient = current_app.config.get("FIRESTORE", None)
        comment_id: str = data.get("id", "")
        post_id: str = data.get("postId", "")
        author_uid: str = data.get("authorId", "")
        posts: List[Dict[str, Any]] = get_docs_of_user(db, author_uid)
        post = find_post_by_id(post_id, posts) or {}
        comments = post.get("comments", []) or []
        comment = find_comment_by_id(comment_id, comments) or {}
        comments.remove(comment)
        post["comments"] = comments
        edited_posts: List[Dict[str, Any]] = h_edit_post(posts, post_id, post)
        db.collection("posts").document(user_uid).set({"posts": edited_posts})
        return Response(f"Deleted comment with id: {comment_id}.")
    except Exception as e:
        return Response(str(e), status=500)


@FORUM.route("/comment/edit", methods=["PUT"])
def edit_comment() -> Response:
    try:
        data: Dict[str, Any] = json.loads(request.data)
        headers: Dict[str, Any] = request.headers
        token: str = str(headers["Authorization"]).split(" ")[1]
        user_uid: str = verify_token(token)["uid"]
        assert token is not None, "Authorization header is required"
        db: FirestoreClient = current_app.config.get("FIRESTORE", None)
        comment_id: str = data.get("id", "")
        post_id: str = data.get("postId", "")
        user = get_user_information(user_uid)
        author_uid: str = data.get("authorId", "")
        comment_body: str = data.get("comment", "")
        votes: int = data.get("votes", 0)
        edited_comment: Dict[str, Any] = asdict(
            Comment(
                id=comment_id,
                user=user,
                uid=user_uid,
                comment=comment_body,
                votes=votes,
            )
        )
        posts: List[Dict[str, Any]] = get_docs_of_user(db, author_uid)
        post = find_post_by_id(post_id, posts) or {}
        comments = post.get("comments", []) or []
        comments = edit_comments(comments, comment_id, edited_comment)
        post["comments"] = comments
        edited_posts: List[Dict[str, Any]] = h_edit_post(posts, post_id, post)
        db.collection("posts").document(user_uid).set({"posts": edited_posts})
        return Response(f"Edited comment with id: {comment_id}.")
    except Exception as e:
        return Response(str(e), status=500)
