import re
import json
import urllib.parse
import tweepy
from twscrape import API, Tweet, gather
import tweetdb
import time

mention_tracked_user = "aureliadotai"
rapid_api_key = "14da4ca027msh1426d7eef136643p1f279cjsnfc7150db6cad"
twsession = "H4sIADXgwmgC/21STXPaMBR0QiDpZMbDBAyFhFAkC4eQgwZLWBCQ/4pkWf7qSUMPyYwb/nptwyFpq5PmaXff6u17PnDsoo2N+JaEh5/mILI0zlUilMyjJE5knOrSu92k9xp7r7cY9bLrvuVOH4bzH6FnsRnfH36bzyI2ICtIUK3V3rjtHHUsYE3F6/ex2+Eoore9SzyYbFoBT8fLqReI7k3f8a2bWmZLG94EdXznYqy8cU8tB+0+pLNwnT2ytfe4CuKRqybTkXV301DqxhyyJUaMNx/oEQwJNN3/neG3ZXd+uj6M7hYzcukMxHoynaw31ySnid7s063+FTmtq4ehXnStCfBJb9O+bME7Zs3u0YIPOuRpBB0/RkS9zgZg23GGnVwNay+UeGxFbEZrHwHROMpU4GuqMi2zGrDaMxIi23VPEL0iKguULCMhkrKCByVOsSh1INMgFYkvpfpEw/REqyBS40yXgawYWitSYklpqaN45fuxEjoJatraJQB9STYVsUyTLI9UlqcyymuUCwi08bpq0EQ2ZwgR2A0p5Ix+CHnM9VGWkOwJBuQozXskZK5ldUpYyjfTInTHzJQjYhJzAXlFMe8LhvmOFX+/Fee60voojvIosqMQspBFIQollXyr/YAngMjO/mrLwXuPbT9UTTPvExa6i8JcFebs01Qq5iRuei7b04+vLRphysBsj59swJakmYfM5UJFWjYLDGyPwLqsPidV1cB5r/4ZRQPjfMtqteeX8yhDvGvUsVsBGaYcYVYjZxiAOYdNgI87FnIXCFltxcsfmIqd1oIDAAA="


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
    "expirationDate": 1757589282.67788,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__cf_bm",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "pWuO04gF4AXn0ROdx_PvOFKKwnTZtAAGChwvj7CMmpc-1757587482-1.0.1.1-AV9iytrdGJud4EoaAwIoS3QLnqn.ZDYi_Ggv7iA.ZgKk4Es0i0eLek7Ba2Bnh9xsi7JYhAmINCueoqwRe_GnElX40xzMh3b_cCy8uXKUXy8",
    "id": 1
},
{
    "domain": ".x.com",
    "expirationDate": 1792147481,
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
    "expirationDate": 1792147481.355018,
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
    "expirationDate": 1792147481.355134,
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
    "expirationDate": 1789123481.479671,
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
        api = API()
        print("cookies", cookies)
        await api.pool.delete_inactive()

        await api.pool.add_account(
            username="dirkcharlie87008",
            password="",
            email="",
            email_password="",
            cookies=cookies,
        )

        print("account added")

        print("getting target mention")
        q = f"(@{mention_tracked_user}"

        # Use the Latest tab
        results = await gather(api.search(q, limit=10, kv={"product": "Top"}))

        for tweet in results:
            # tweet is an SNScrape-like model
            print(
                f"Sender {tweet.user.username} is replying to {mention_tracked_user} with tweet id {tweet.id}"
            )
            print("Content: ", tweet.rawContent)

        return results
    except Exception as e:
        print(f"Error in get_mentions: {e}")
        return {"error": str(e)}


async def reply_mention(tweepy_api: tweepy.API, tweet_id: str, reply_text: str):
    try:
        tweepy_api.update_status(status=reply_text, in_reply_to_status_id=tweet_id)
    except Exception as e:
        print({"error": str(e)})
        return {"error": str(e)}


from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_content(input_tweet: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates short, engaging replies to tweets. Keep replies under 80 characters. if the tweet is empty or only a mention, then reply with a random cheerful words no more than 80 characters. Mix the language with natural human interaction language, no need to be strict english. make all lowercase",
                },
                {
                    "role": "user",
                    "content": f"Generate a reply to the following tweet: {input_tweet}",
                },
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        return content.strip() if content else "Thanks for the mention! 🙏"
    except Exception as e:
        print(f"Error generating content: {e}")
        raise e


def get_tweet_id_from_mentioned_tweet(mentioned_tweet: Tweet):
    tweet_id = None
    if mentioned_tweet.inReplyToTweetIdStr:
        tweet_id = mentioned_tweet.inReplyToTweetIdStr
    elif mentioned_tweet.id_str:
        tweet_id = mentioned_tweet.id_str
    else:
        tweet_id = None
    return tweet_id


import random


def get_random_media():
    media_ids = ["1966151030372192256"]
    return random.choice(media_ids)


import requests


def create_tweet_with_rapid_api(tweet_id: str, tweet: str, media_id: str):
    try:

        data = {
            "tweet_text": tweet,
            "in_reply_to_tweet_id": tweet_id,
        }

        if media_id:
            data["media_id"] = media_id

        response = requests.post(
            "https://twttrapi.p.rapidapi.com/create-tweet",
            data=data,
            headers={
                "twttr-session": twsession,
                "x-rapidapi-key": f"{rapid_api_key}",
                "x-rapidapi-host": "twttrapi.p.rapidapi.com",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Error creating tweet with rapid api: {e}")
        return {"error": str(e)}


async def track_mention_and_reply():
    try:
        tdb = tweetdb.DB()
        tdb.setup_database()

        # Format the time in a friendly string format (e.g., "2025-02-23 14:30:00")
        print("getting mentions")
        mentioned_tweets = await get_mentions()

        mentioned_tweets = sorted(mentioned_tweets, key=lambda x: x.date, reverse=True)

        for mentioned_tweet in mentioned_tweets:
            tweet_id = get_tweet_id_from_mentioned_tweet(mentioned_tweet)
            if tweet_id == None:
                print("No tweet ID found to reply to")
                return
            if tdb.get_replied_tweet_id_by_tweet_id(tweet_id):
                print("Tweet already replied to")
                return

            print("Tweet Date: ", mentioned_tweet.date)

            comment = generate_content(mentioned_tweet.rawContent)
            print(f"Generated comment: {comment}")
            print("replying to tweet")

            print("uploading media")
            media_id = get_random_media()

            create_tweet_with_rapid_api(tweet_id, comment, media_id)
            print("Tweet replied !")
            tdb.store_replied_tweet_id(tweet_id)
            time.sleep(1)

    except Exception as e:
        print(f"Error in track_mention_and_reply: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(track_mention_and_reply())
