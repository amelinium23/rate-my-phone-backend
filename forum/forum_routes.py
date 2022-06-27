import json
from typing import Any, Dict
from flask import Response, request, current_app
from forum import FORUM
from dataclasses import asdict
from forum.model.post import Post


@FORUM.route('/post', methods=['GET'])
def get_all_post() -> Response:
  try:
    data: Dict[str, Any] = json.loads(request.data)
    user_uid: str = data.get('uid', '')
    assert user_uid is not None, 'uid param is required'
    db = current_app.config.get('FIRESTORE', None)
    doc = db.collection('posts').document(user_uid).get().to_dict()
    posts = doc.get('posts', [])
    return Response(json.dumps(posts), status=200)
  except Exception as e:
    return Response(str(e), status=500)

@FORUM.route('/post', methods=['POST'])
def create_new_post() -> Response:
 try:
  data: Dict[str, Any] = json.loads(request.data)
  user_uid: str = data.get('uid', '')
  assert user_uid is not None, 'uid param is required'
  db = current_app.config.get('FIRESTORE', None)
  new_doc = db.collection('posts').document(user_uid)
  new_post = Post(title=data.get('title', ''), description=data.get('description', ''))
  posts = new_doc.get().to_dict().get('posts', [])
  posts.append(asdict(new_post))
  db.collection('posts').document(user_uid).set({'posts': posts})
  return Response(f"Created new document id: {new_doc}", status=200)
 except Exception as e:
  return Response(str(e), status=500)


@FORUM.route('/post', methods=['DELETE'])
def delete_post() -> Response:
 return Response("xd", status=200)


@FORUM.route('/post', methods=['PUT'])
def edit_post() -> Response:
 return Response("xd", status=200)
