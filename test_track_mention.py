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
    "expirationDate": 1757521940.413251,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__cf_bm",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "H_iD4MzcIdpz5kQ6U8ksUixCtb3LYpgLwWogc.w5i0E-1757520140-1.0.1.1-aSh5e6OHjUzQbPx7_bo.GLRpVeIm2uOloeX3Y0cqVWeUAd7dwYo2BDI1ScZMdOd.F3I970YK.D7z3E.yd_jXruF7GUptTwWYweQ7ZqeB0C8",
    "id": 1
},
{
    "domain": ".x.com",
    "expirationDate": 1792080140,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__cuid",
    "path": "/",
    "sameSite": "lax",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "bad4ee0fba204e8d997d921ce5034bcc",
    "id": 2
},
{
    "domain": ".x.com",
    "expirationDate": 1792077947.928836,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1969507965.1757517948",
    "id": 3
},
{
    "domain": ".x.com",
    "expirationDate": 1757604347,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_gid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1104606425.1757517948",
    "id": 4
},
{
    "domain": ".x.com",
    "expirationDate": 1757590544.084566,
    "hostOnly": false,
    "httpOnly": true,
    "name": "att",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1-3WvOVGQG05fXXf9L1G8mUcvKuNpmjiUgIIBA7CSV",
    "id": 5
},
{
    "domain": ".x.com",
    "expirationDate": 1792064141.787368,
    "hostOnly": false,
    "httpOnly": true,
    "name": "auth_token",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "29b018b8df89ca23f1ba84e1561f8b83dac54226",
    "id": 6
},
{
    "domain": ".x.com",
    "expirationDate": 1792064142.57962,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ct0",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "16ea9ddfc6479f28e77619d6d48dc09337645ee6fcc17aa009d2f1f78c7d288802c230b8972bc4cb1d4fe462435d256fe8c1279cdf2e9766c35a47eefd2247c19f015d3658685647f19b9e4c4362f7e7",
    "id": 7
},
{
    "domain": ".x.com",
    "expirationDate": 1792077811.861215,
    "hostOnly": false,
    "httpOnly": false,
    "name": "des_opt_in",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "Y",
    "id": 8
},
{
    "domain": ".x.com",
    "expirationDate": 1792052410.487723,
    "hostOnly": false,
    "httpOnly": false,
    "name": "dnt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 9
},
{
    "domain": ".x.com",
    "expirationDate": 1792052410.749445,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175749241080141695",
    "id": 10
},
{
    "domain": ".x.com",
    "expirationDate": 1792080140.413022,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_ads",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175749241080141695",
    "id": 11
},
{
    "domain": ".x.com",
    "expirationDate": 1792080140.413063,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_marketing",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175749241080141695",
    "id": 12
},
{
    "domain": ".x.com",
    "expirationDate": 1792064141.787222,
    "hostOnly": false,
    "httpOnly": true,
    "name": "kdt",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "h10kCbLkVOONgD04Vz9OFsF5w1uuS8aya8xNBWrb",
    "id": 13
},
{
    "domain": ".x.com",
    "expirationDate": 1792062972.866365,
    "hostOnly": false,
    "httpOnly": false,
    "name": "personalization_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1_4SACVvqhUJ94atIv1n6uvw==",
    "id": 14
},
{
    "domain": ".x.com",
    "expirationDate": 1789053731,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "%7B%22distinct_id%22%3A%2201993438-5302-7320-88b8-76c4d55ecfe7%22%2C%22%24sesid%22%3A%5B1757517730601%2C%2201993438-5301-7d81-be1e-48f6420d0851%22%2C1757517730561%5D%7D",
    "id": 15
},
{
    "domain": ".x.com",
    "expirationDate": 1789056140.650653,
    "hostOnly": false,
    "httpOnly": false,
    "name": "twid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "u%3D1961207524385853440",
    "id": 16
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
    "id": 17
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
