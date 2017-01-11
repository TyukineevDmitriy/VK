import requests
from api.tokens import fb_token

class FBRequests:
    @staticmethod
    def get_share_count(url):
        resp = requests.get("https://graph.facebook.com",
                            params={"id": url, 'access_token': fb_token})
        share_count = resp.json()['share']['share_count'] if 'share' in resp.json() else None
        return share_count