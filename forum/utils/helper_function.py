from typing import Dict, Optional, Any, List
from google.cloud.firestore import Client as FirestoreClient


def find_post_by_id(
    post_id: str, posts: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    for post in posts:
        if post_id == post.get("id", ""):
            return post
    return None


def edit_post(
    posts: List[Dict[str, Any]], post_id: str, edited_post: Dict[str, Any]
) -> List[Dict[str, Any]]:
    for index, post in enumerate(posts):
        if post_id == post.get("id", ""):
            posts[index] = edited_post
    return posts


def parse_documents_to_list(collection) -> List[Dict[str, Any]]:
    posts = []
    for doc in collection:
        doc_posts = doc.get("posts") if doc.get("posts") is not None else []
        for post in doc_posts:
            posts.append(post)
    return posts


def get_docs_of_user(db: FirestoreClient, user_uid: str) -> List[Dict[str, Any]]:
    doc = db.collection("posts").document(user_uid).get().to_dict()
    return doc.get("posts", [])


def find_comment_by_id(
    comment_id: str, comments: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    for comment in comments:
        if comment_id == comment.get("id", ""):
            return comment
    return None


def edit_comments(
    comments: List[Dict[str, Any]], comment_id: str, edited_comment: Dict[str, Any]
) -> List[Dict[str, Any]]:
    for index, comment in enumerate(comments):
        if comment_id == comment.get("id", ""):
            comments[index] = edited_comment
    return comments
