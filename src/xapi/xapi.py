import requests
from src.xauth.xauth import XAuth
from src.logger import logger


class X:
    def __init__(self):
        self.xauth = XAuth()

    def create_post(self, post):
        logger.debug("Posting!")
        access_token = self.xauth.get_access_token()

        response = requests.post(
            "https://api.x.com/2/tweets",
            json={"text": post},
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        return response

    def reply_to_tweet(self, tweet_id, reply, media_ids=None):
        logger.debug("Replying to tweet!")
        access_token = self.xauth.get_access_token()

        json_payload = {"text": reply, "reply": {"in_reply_to_tweet_id": tweet_id}}

        if media_ids:
            json_payload["media"] = {"media_ids": media_ids}

        response = requests.post(
            f"https://api.x.com/2/tweets",
            json=json_payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        print(response.json())

        return response
