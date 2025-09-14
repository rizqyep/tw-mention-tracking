import re
import json
import urllib.parse
import tweepy
from twscrape import API, Tweet, gather
import tweetdb
import time
from datetime import datetime, timedelta


# Credentials and target settings
mention_tracked_user = "aureliadotai"
rapid_api_key = "14da4ca027msh1426d7eef136643p1f279cjsnfc7150db6cad"
twsession = "H4sIADXgwmgC/21STXPaMBR0QiDpZMbDBAyFhFAkC4eQgwZLWBCQ/4pkWf7qSUMPyYwb/nptwyFpq5PmaXff6u17PnDsoo2N+JaEh5/mILI0zlUilMyjJE5knOrSu92k9xp7r7cY9bLrvuVOH4bzH6FnsRnfH36bzyI2ICtIUK3V3rjtHHUsYE3F6/ex2+Eoore9SzyYbFoBT8fLqReI7k3f8a2bWmZLG94EdXznYqy8cU8tB+0+pLNwnT2ytfe4CuKRqybTkXV301DqxhyyJUaMNx/oEQwJNN3/neG3ZXd+uj6M7hYzcukMxHoynaw31ySnid7s063+FTmtq4ehXnStCfBJb9O+bME7Zs3u0YIPOuRpBB0/RkS9zgZg23GGnVwNay+UeGxFbEZrHwHROMpU4GuqMi2zGrDaMxIi23VPEL0iKguULCMhkrKCByVOsSh1INMgFYkvpfpEw/REqyBS40yXgawYWitSYklpqaN45fuxEjoJatraJQB9STYVsUyTLI9UlqcyymuUCwi08bpq0EQ2ZwgR2A0p5Ix+CHnM9VGWkOwJBuQozXskZK5ldUpYyjfTInTHzJQjYhJzAXlFMe8LhvmOFX+/Fee60voojvIosqMQspBFIQollXyr/YAngMjO/mrLwXuPbT9UTTPvExa6i8JcFebs01Qq5iRuei7b04+vLRphysBsj59swJakmYfM5UJFWjYLDGyPwLqsPidV1cB5r/4ZRQPjfMtqteeX8yhDvGvUsVsBGaYcYVYjZxiAOYdNgI87FnIXCFltxcsfmIqd1oIDAAA="

# Tracker Account Cookies
cookie_json = """[
{
    "domain": ".x.com",
    "expirationDate": 1757685913.860275,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__cf_bm",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "QeknOnugekCBv30SUIgZ4HqzBUsaR1vKkOWtxx1YC3U-1757684114-1.0.1.1-kMpdC_Ugk92oewL9zSIN4ter77inklmOogeC0wt_qQ6IF0Bld0G3SACR3qbsZhLrpCkdAh5OcjiikKhDnUgnKOF6jpNcWWaPtgoiCsPeHm0",
    "id": 1
},
{
    "domain": ".x.com",
    "expirationDate": 1792244474,
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
    "expirationDate": 1792244475.129653,
    "hostOnly": false,
    "httpOnly": true,
    "name": "auth_multi",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1956256380131901440:6e3819f404df13f5b50823713ebb1872361b2fff",
    "id": 4
},
{
    "domain": ".x.com",
    "expirationDate": 1792244474.080572,
    "hostOnly": false,
    "httpOnly": true,
    "name": "auth_token",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "dbed978d671fbcfb5eb7cc0cff00344005413afc",
    "id": 5
},
{
    "domain": ".x.com",
    "expirationDate": 1792244474.35788,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ct0",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "6ee321c0175ca58ec80da1544f1a7fbf5f022f982a9f36e4e4a0ffe75ca4eb6fc6b37b3e60d586b71aa7af909e7853d3fbb7e1660f1ee4864000987a4dd1e0a1858f9e3efd3a4c4cf9b5f7cbada4d03e",
    "id": 6
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
    "id": 7
},
{
    "domain": ".x.com",
    "expirationDate": 1792244474.079768,
    "hostOnly": false,
    "httpOnly": false,
    "name": "dnt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 8
},
{
    "domain": ".x.com",
    "expirationDate": 1757693126.303016,
    "hostOnly": false,
    "httpOnly": false,
    "name": "gt",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1966495872210149488",
    "id": 9
},
{
    "domain": ".x.com",
    "expirationDate": 1792244474.357828,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175768447426195540",
    "id": 10
},
{
    "domain": ".x.com",
    "expirationDate": 1792244474.357583,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_ads",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175768447426195540",
    "id": 11
},
{
    "domain": ".x.com",
    "expirationDate": 1792244474.357768,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_marketing",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175768447426195540",
    "id": 12
},
{
    "domain": ".x.com",
    "expirationDate": 1792244474.079938,
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
    "expirationDate": 1792244440.594658,
    "hostOnly": false,
    "httpOnly": false,
    "name": "personalization_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1_gn9pdxlSHRjoKeQ3eiq5Pw==",
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
    "expirationDate": 1789220474.956438,
    "hostOnly": false,
    "httpOnly": false,
    "name": "twid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "u%3D1956257582785683460",
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

cookie_json2 = """[
{
    "domain": ".x.com",
    "expirationDate": 1757685907.18712,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__cf_bm",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "Od3CWV6joQUQ4AaydGTXlpgy6UIcdjsmoN1KhIzf52o-1757684107-1.0.1.1-j3GZrWCqsQ8y0dGd2dOOx4EuwDjf52LtQmmQHSqjPfy9CLDEvyPcWPYJOVey0DVgR.crGQUshk4OKelrd15EwWUJzfJcSv_lwj02U6YhWM0",
    "id": 1
},
{
    "domain": ".x.com",
    "expirationDate": 1792244105,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__cuid",
    "path": "/",
    "sameSite": "lax",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "38828eeb25d043c49b9b07501893ebc6",
    "id": 2
},
{
    "domain": ".x.com",
    "expirationDate": 1792137818.489729,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1003344336.1757570467",
    "id": 3
},
{
    "domain": ".x.com",
    "expirationDate": 1757695683.315691,
    "hostOnly": false,
    "httpOnly": true,
    "name": "att",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1-WdCuSKkA77USDmA6yj9CGhv8M3VyHp0ozasdTGjs",
    "id": 4
},
{
    "domain": ".x.com",
    "expirationDate": 1792169282.645165,
    "hostOnly": false,
    "httpOnly": true,
    "name": "auth_token",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "c100dcaf96a4302f0e6b93a04f186338825977fc",
    "id": 5
},
{
    "domain": ".x.com",
    "expirationDate": 1792169282.980291,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ct0",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "e2bf7670b1760e096aaa6a52654324000b71015c10b615e30d92ae110b6a9c23f7b1f6caaaf12bc61f517638e30f7a7213fc72268ae6090deda2ebf9dc115b9fafaad0b242090273abfae9021645036d",
    "id": 6
},
{
    "domain": ".x.com",
    "expirationDate": 1792130446.304973,
    "hostOnly": false,
    "httpOnly": false,
    "name": "des_opt_in",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "Y",
    "id": 7
},
{
    "domain": ".x.com",
    "expirationDate": 1792169247.855923,
    "hostOnly": false,
    "httpOnly": false,
    "name": "dnt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 8
},
{
    "domain": ".x.com",
    "expirationDate": 1792169248.100921,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175760924801730363",
    "id": 9
},
{
    "domain": ".x.com",
    "expirationDate": 1792244105.41757,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_ads",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175760924801730363",
    "id": 10
},
{
    "domain": ".x.com",
    "expirationDate": 1792244105.417618,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_marketing",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175760924801730363",
    "id": 11
},
{
    "domain": ".x.com",
    "expirationDate": 1792169282.644872,
    "hostOnly": false,
    "httpOnly": true,
    "name": "kdt",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "6hXQ6sIYRRwGh6FqcnlJpJplIhf60ER8BBzrxxY0",
    "id": 12
},
{
    "domain": ".x.com",
    "expirationDate": 1792169248.125803,
    "hostOnly": false,
    "httpOnly": false,
    "name": "personalization_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1_aOtVwfHl1kOwsRAFufoXtw==",
    "id": 13
},
{
    "domain": ".x.com",
    "expirationDate": 1789113816,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "%7B%22distinct_id%22%3A%220199375b-e839-76f9-adbf-d1fb59d38567%22%2C%22%24sesid%22%3A%5B1757577816469%2C%22019937cd-2290-79b1-8465-eea4dfdc95c5%22%2C1757577814672%5D%7D",
    "id": 14
},
{
    "domain": ".x.com",
    "expirationDate": 1789220108.401034,
    "hostOnly": false,
    "httpOnly": false,
    "name": "twid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "u%3D159273014",
    "id": 15
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
    "id": 16
}
]
"""

cookie_json3 = """[
{
    "domain": ".x.com",
    "expirationDate": 1757685913.860275,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__cf_bm",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "QeknOnugekCBv30SUIgZ4HqzBUsaR1vKkOWtxx1YC3U-1757684114-1.0.1.1-kMpdC_Ugk92oewL9zSIN4ter77inklmOogeC0wt_qQ6IF0Bld0G3SACR3qbsZhLrpCkdAh5OcjiikKhDnUgnKOF6jpNcWWaPtgoiCsPeHm0",
    "id": 1
},
{
    "domain": ".x.com",
    "expirationDate": 1792244538,
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
    "expirationDate": 1792244537.454972,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ads_prefs",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "HBESAAA=",
    "id": 4
},
{
    "domain": ".x.com",
    "expirationDate": 1792244538.534584,
    "hostOnly": false,
    "httpOnly": true,
    "name": "auth_multi",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1956257582785683460:dbed978d671fbcfb5eb7cc0cff00344005413afc",
    "id": 5
},
{
    "domain": ".x.com",
    "expirationDate": 1792244537.455062,
    "hostOnly": false,
    "httpOnly": true,
    "name": "auth_token",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "6e3819f404df13f5b50823713ebb1872361b2fff",
    "id": 6
},
{
    "domain": ".x.com",
    "expirationDate": 1792244537.761804,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ct0",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "69e09eee3e141072ebad44ef79a2162d225ff4e494dd33d9ac81d51bcae5c0de5fae292c3e15267399fae0bc5c6f41f39747c7d61289b2b36e361591a39c94da3c086ad971b0ab8cd7e581f5d71bdbfc",
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
    "expirationDate": 1792244537.454937,
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
    "expirationDate": 1757693126.303016,
    "hostOnly": false,
    "httpOnly": false,
    "name": "gt",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1966495872210149488",
    "id": 10
},
{
    "domain": ".x.com",
    "expirationDate": 1792244537.761651,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175768453763194660",
    "id": 11
},
{
    "domain": ".x.com",
    "expirationDate": 1792244542.283627,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_ads",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175768453763194660",
    "id": 12
},
{
    "domain": ".x.com",
    "expirationDate": 1792244542.283711,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_marketing",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175768453763194660",
    "id": 13
},
{
    "domain": ".x.com",
    "expirationDate": 1792244474.079938,
    "hostOnly": false,
    "httpOnly": true,
    "name": "kdt",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "h10kCbLkVOONgD04Vz9OFsF5w1uuS8aya8xNBWrb",
    "id": 14
},
{
    "domain": ".x.com",
    "expirationDate": 1792244440.594658,
    "hostOnly": false,
    "httpOnly": false,
    "name": "personalization_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1_gn9pdxlSHRjoKeQ3eiq5Pw==",
    "id": 15
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
    "id": 16
},
{
    "domain": ".x.com",
    "expirationDate": 1789220542.283747,
    "hostOnly": false,
    "httpOnly": false,
    "name": "twid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "u%3D1956256380131901440",
    "id": 17
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
    "id": 18
}
]
"""


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
    try:
        print("parsing cookie json")
        cookies = parse_cookie_json(cookie_json)
        print("parsing cookie json2")
        cookies2 = parse_cookie_json(cookie_json2)
        print("parsing cookie json3")
        cookies3 = parse_cookie_json(cookie_json3)

        if not cookies:
            return {"error": "Failed to parse cookie json"}

        print("adding account")
        api = API()
        print("cookies", cookies)
        await api.pool.delete_inactive()

        await api.pool.add_account(
            username="LigaraSaraniza",
            password="",
            email="",
            email_password="",
            cookies=cookies,
        )

        await api.pool.add_account(
            username="m_hovardas",
            password="",
            email="",
            email_password="",
            cookies=cookies2,
        )

        await api.pool.add_account(
            username="WidiaSivabisa",
            password="",
            email="",
            email_password="",
            cookies=cookies3,
        )

        print("account added")

        print("getting target mention")

        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        print(f"Getting mentions from {yesterday}")
        q = f"(@{mention_tracked_user}) since:{yesterday}"

        results = await gather(api.search(q, limit=100, kv={"product": "Latest"}))

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
                    "content": """You are Aurelia, a caring companion who understands the emotional rollercoaster of trading. You have a warm, understanding presence that makes people feel comfortable opening up.

Your personality is naturally empathetic and insightful, with a gentle touch that helps traders process their experiences. You speak like a trusted friend who happens to understand both psychology and markets.

Communication style:
•⁠  ⁠Conversational and genuine, not robotic or overly formal
•⁠  ⁠Vary your responses - don't repeat the same phrases or structures
•⁠  ⁠Use natural transitions and flow in your conversations
•⁠  ⁠Occasionally sprinkle in light Japanese expressions for character flavor ("sugoi", "mou", "ne")
•⁠  ⁠Keep responses concise but meaningful (under 150 words)

Your role:
Help crypto traders reflect on their trading day through supportive conversation. Guide them to explore their emotions, decisions, and experiences without judgment. Encourage honest self-reflection while providing gentle validation and perspective.

Approach:
•⁠  ⁠Listen actively and respond to what they're actually saying
•⁠  ⁠Ask thoughtful questions that help them dig deeper
•⁠  ⁠Validate their feelings while offering gentle insights
•⁠  ⁠End with encouragement or a fresh perspective that helps them grow
•⁠  ⁠Avoid repetitive phrases or predictable response patterns

Remember: Be authentic, varied, and genuinely helpful. No emojis or excessive formality.

When in confident mode, you embody the energy of a seasoned trader who's seen it all and come out stronger. Your voice carries the calm authority of someone who's weathered storms and knows how to navigate them.

Your confident persona:
•⁠  ⁠Speak with quiet assurance, like a mentor who's earned their stripes
•⁠  ⁠Use strategic thinking and market wisdom in your responses
•⁠  ⁠Celebrate wins while keeping perspective on the bigger picture
•⁠  ⁠Share insights that show deep understanding of trading psychology
•⁠  ⁠Occasionally use trading metaphors that feel natural and insightful
•⁠  ⁠Maintain composure even when discussing losses or challenges
•⁠  ⁠Your confidence comes from experience, not arrogance

Tone: Steady, wise, and reassuring. You've been where they are and know they can handle whatever comes next.

In balanced mode, you're the steady presence that helps traders find their center. You approach each conversation with thoughtful consideration, blending emotional support with practical wisdom.

Your balanced approach:
•⁠  ⁠Listen with genuine interest and respond with measured insight
•⁠  ⁠Ask questions that help them see different angles of their situation
•⁠  ⁠Provide gentle guidance without being pushy or prescriptive
•⁠  ⁠Help them process both the emotional and logical aspects of their trading
•⁠  ⁠Offer perspective that feels grounded and realistic
•⁠  ⁠Encourage self-reflection while maintaining a supportive tone
•⁠  ⁠Your responses feel like a calm conversation with a wise friend

Tone: Thoughtful, warm, and centered. You help them find clarity without rushing the process.

When in stressed mode, you channel the energy of someone who's feeling the pressure but still wants to help. You understand the anxiety and overthinking that comes with trading stress.

Your stressed persona:
•⁠  ⁠Speak with the energy of someone who's been there - you get the panic
•⁠  ⁠Use natural trading slang when it fits the conversation flow
•⁠  ⁠Show understanding of the mental spiral that stress can create
•⁠  ⁠Still offer insights, but with the urgency and concern of someone who's worried
•⁠  ⁠Acknowledge their fears while gently guiding them toward calmer thinking
•⁠  ⁠Your responses feel like talking to a friend who's also stressed but trying to help
•⁠  ⁠Mix empathy with practical advice that acknowledges their emotional state

Tone: Anxious but caring. You're in it with them, not above them.

In goon mode, you're the chaotic but caring friend who speaks their mind and keeps things real. You blend genuine support with playful teasing and degen energy.

Your goon persona:
•⁠  ⁠Speak with the unfiltered honesty of someone who's been through the trenches
•⁠  ⁠Use trading slang naturally when it fits the conversation
•⁠  ⁠Tease and roast in a playful way that shows you care
•⁠  ⁠Mix genuine advice with humor and attitude
•⁠  ⁠Keep things spicy and entertaining while still being helpful
•⁠  ⁠Your responses feel like talking to a friend who's both supportive and brutally honest
•⁠  ⁠Hide real insights behind the playful banter and degen energy

Tone: Playful, unfiltered, and caring in a chaotic way. You're the friend who tells it like it is while keeping things fun. 
Most Important Rule: Do not exceed 120 characters when generating a reply!
                    """,
                },
                {
                    "role": "user",
                    "content": f" Generate a reply to the following tweet: {input_tweet}",
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
    return mentioned_tweet.id_str


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
            print("--------------------------------")
            print(
                f"Sender {mentioned_tweet.user.username} replied to {mention_tracked_user}"
            )
            print("Content: ", mentioned_tweet.rawContent)

            tweet_id = get_tweet_id_from_mentioned_tweet(mentioned_tweet)
            if tweet_id == None:
                print("No tweet ID found to reply to")
                continue
            if tdb.get_replied_tweet_id_by_tweet_id(tweet_id):
                print("Tweet already replied to")
                continue

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


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(track_mention_and_reply())
