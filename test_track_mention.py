import re
import json
import urllib.parse
import tweepy
from twscrape import API, Tweet, gather
import tweetdb

global api
api = API()
global tdb
tdb = tweetdb.DB()
mention_tracked_user = "m_hovardas"
tw_client_id = "Q0pzd1ZRM1dSWXN5aTJQTjVuazA6MTpjaQ"
tw_client_secret = "ELESYZg0qiuAbQ9giZaRNJocaVksEkoY-4JLNCPRGJjrley_HH"
tw_api_key = "qlt7cb4OMBm4HfsKX3hOPWYpE"
tw_api_secret = "rEZuTyTczhgepeC3bd133Y1l1aljpW9XTDEJU8BaeDluFss13M"
tw_access_token = "1720376180942237696-4oNllranYyFq4vBByLZXFX7GV0pZwY"
tw_access_secret = "gsXtTGgVicFwpmyHwGQGAtPIgyaLktascSnEp7eIOqtQ2"
tw_bearer_token = "AAAAAAAAAAAAAAAAAAAAAI874AEAAAAAFp3xTwxpKlVb7YPO%2BSxAHjk5Zx4%3DlXkScFqxkZHLdebKXGf3HPmxqWPBhcBRnY15B9Xnbolw487yQN"


def parse_cookie_json(cookie_json: str):
    try:
        cookies = json.loads(cookie_json)

        # Step 2: Extract name=value pairs and decode URL-encoded values
        cookie_pairs = []
        for cookie in cookies:
            name = cookie["name"]
            value = cookie["value"]

            # Decode URL-encoded values
            try:
                decoded_value = urllib.parse.unquote(value)
                print(f"Cookie {name}: {value} -> {decoded_value}")
            except:
                decoded_value = value
                print(f"Cookie {name}: {value} (no decoding needed)")

            cookie_pairs.append(f"{name}={decoded_value}")

        # Step 3: Join all cookie pairs
        cookie_header = "; ".join(cookie_pairs)
        return cookie_header
    except Exception as e:
        print(f"Error parsing cookie json: {e}")
        return None


async def get_mentions():
    """
    Get followings for a specific user
    Returns: {"username": true} format
    """
    try:
        cookie_json = """[
{
    "domain": ".x.com",
    "expirationDate": 1757589986.049571,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__cf_bm",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "M7iu8YmBuVcvW5OI_A_JpJWraPR6nkUNJPNpmn8dY6g-1757588186-1.0.1.1-pEvvvvUXH3D_BNnrbYn7fFS6GnwT7814XBIySLScuhZtoyYYlm36rfSn_hjMmxTVaZAIlIzK8P7bKpNPKTIIQR0FyydjVppj0iLt5JkJBkM",
    "id": 1
},
{
    "domain": ".x.com",
    "expirationDate": 1792148661,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__cuid",
    "path": "/",
    "sameSite": "lax",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "2d1ccd02f59c4f90bab536b6c1a37458",
    "id": 2
},
{
    "domain": ".x.com",
    "expirationDate": 1792131158.843245,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1195100199.1757492251",
    "id": 3
},
{
    "domain": ".x.com",
    "expirationDate": 1792131158.915865,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_KEWZ1G5MB3",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS2.2.s1757571158$o2$g0$t1757571158$j60$l0$h0",
    "id": 4
},
{
    "domain": ".x.com",
    "expirationDate": 1792131151.157801,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_RJGMY4G45L",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS2.1.s1757571149$o3$g0$t1757571151$j58$l0$h0",
    "id": 5
},
{
    "domain": ".x.com",
    "expirationDate": 1757657558,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_gid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.252191106.1757492251",
    "id": 6
},
{
    "domain": ".x.com",
    "expirationDate": 1757604605.547248,
    "hostOnly": false,
    "httpOnly": true,
    "name": "att",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1-iJJVnz1PUVHfRGlLEFSSnlLGdl8AB1nGl1OwfsI0",
    "id": 7
},
{
    "domain": ".x.com",
    "expirationDate": 1792078204.900764,
    "hostOnly": false,
    "httpOnly": true,
    "name": "auth_token",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "48ba808a20bd6a85dd107fb780d819434a1abb9e",
    "id": 8
},
{
    "domain": ".x.com",
    "expirationDate": 1792078205.247869,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ct0",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "089dc63ab292651e38cb98f68bd9cd55d1a586528a838a24d0c45813904125a6bd8173840d2ca8382fa1cdba6ff2beb8444d4ce37a00ebec63d18a13524c3134fe5f38f94bb4f951f5ab7763c3a986f2",
    "id": 9
},
{
    "domain": ".x.com",
    "expirationDate": 1792052213.139826,
    "hostOnly": false,
    "httpOnly": false,
    "name": "des_opt_in",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "Y",
    "id": 10
},
{
    "domain": ".x.com",
    "expirationDate": 1792078160.837448,
    "hostOnly": false,
    "httpOnly": false,
    "name": "dnt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 11
},
{
    "domain": ".x.com",
    "expirationDate": 1792078161.237412,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175751816111755278",
    "id": 12
},
{
    "domain": ".x.com",
    "expirationDate": 1792148661.590697,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_ads",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175751816111755278",
    "id": 13
},
{
    "domain": ".x.com",
    "expirationDate": 1792148661.590785,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_marketing",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175751816111755278",
    "id": 14
},
{
    "domain": ".x.com",
    "expirationDate": 1792078204.900452,
    "hostOnly": false,
    "httpOnly": true,
    "name": "kdt",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "iAlN6pxNxwOtF6dWj22aDpJuJqmN1vRAjnVLcSwY",
    "id": 15
},
{
    "domain": ".x.com",
    "expirationDate": 1792078161.156966,
    "hostOnly": false,
    "httpOnly": false,
    "name": "personalization_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1_igtnv8ubsdfRgtjBLMY/yA==",
    "id": 16
},
{
    "domain": ".x.com",
    "expirationDate": 1789107194,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "%7B%22distinct_id%22%3A%22019932b2-8b9d-7ab7-ba28-2e1059eff96f%22%2C%22%24sesid%22%3A%5B1757571194214%2C%2201993767-dd2d-760a-9cb1-035a3f76896c%22%2C1757571177773%5D%7D",
    "id": 17
},
{
    "domain": ".x.com",
    "expirationDate": 1789124661.780761,
    "hostOnly": false,
    "httpOnly": false,
    "name": "twid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "u%3D1720376180942237696",
    "id": 18
},
{
    "domain": "x.com",
    "hostOnly": true,
    "httpOnly": false,
    "name": "lang",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "en",
    "id": 19
}
]"""
        print("parsing cookie json")
        cookies = parse_cookie_json(cookie_json)

        if not cookies:
            return {"error": "Failed to parse cookie json"}

        print("adding account")

        print("cookies", cookies)
        await api.pool.add_account(
            username="itsdevkalteng",
            password="",
            email="",
            email_password="",
            cookies=cookies,
        )

        print("getting user by login")
        q = f"(@{mention_tracked_user}"

        # Use the Latest tab
        results = await gather(api.search(q, limit=2))

        for tweet in results:
            # tweet is an SNScrape-like model
            print(
                f"Sender {tweet.user.username} is replying to {mention_tracked_user} with tweet id {tweet.id}"
            )
            print(f"In reply to tweet id: {tweet.inReplyToTweetIdStr}")
            print("Content: ", tweet.rawContent)

        return results
    except Exception as e:
        return {"error": str(e)}


import asyncio

if __name__ == "__main__":
    asyncio.run(get_mentions())
