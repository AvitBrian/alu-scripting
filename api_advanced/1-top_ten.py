#!/usr/bin/python3
import requests
import json

def top_ten(subreddit):
    """
        fetches the top 10 hot posts.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        "User-Agent": "Linux:MyRedditApp:1.0 (by /u/Few-Area5580)"
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()["data"]["children"]
        for i in range(10):
            return (data[i]["data"]["title"])
    else:return ("None")
    
