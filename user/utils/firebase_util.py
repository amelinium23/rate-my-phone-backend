from firebase_admin.auth import UserRecord
from typing import Dict


def get_user_mapping(user: UserRecord) -> Dict[str, str]:
  return {
      'uid': user.uid,
      'email': user.email,
      'display_name': user.display_name,
      'photo_url': user.photo_url,
  }
