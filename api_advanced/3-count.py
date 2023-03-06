#!/usr/bin/python3
import requests

def count_words(subreddit, word_list, after=None, count_dict=None):
    """
    Recursively queries the Reddit API, parses the title of all hot articles, and prints a sorted count of given keywords
    (case-insensitive, delimited by spaces. Javascript should count as javascript, but java should not).

    :param subreddit: string, the subreddit to search for
    :param word_list: list of strings, the keywords to count
    :param after: string, the value of the 'after' parameter in the previous API call
    :param count_dict: dictionary, a dictionary to store the counts of each keyword
    :return: None
    """

    # Base case: if count_dict is None, initialize it
    if count_dict is None:
        count_dict = {}

    # Base case: if word_list is empty, print the count_dict
    if not word_list:
        for word, count in sorted(count_dict.items(), key=lambda x: (-x[1], x[0])):
            print(f"{word}: {count}")
        return

    # Get the data from the Reddit API
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'mybot/0.0.1'}
    params = {'limit': '100', 'after': after}
    response = requests.get(url, headers=headers, params=params)

    # If the API call was unsuccessful, print an error message and return None
    if response.status_code != 200:
        print(f"Error: status code {response.status_code}")
        return

    # Get the JSON data from the API response
    data = response.json()

    # Get the next 'after' parameter, which is used for pagination
    after = data['data']['after']

    # Loop through the posts in the data
    for post in data['data']['children']:
        # Get the lowercase title of the post
        title = post['data']['title'].lower()
        # Loop through the words in word_list
        for word in word_list:
            # Get the lowercase version of the word without any punctuation at the end
            word_lower = word.rstrip('.!_').lower()
            # Check if the word is in the title
            if f" {word_lower} " in f" {title} ":
                # If the word is in the title, add it to the count_dict
                if word_lower in count_dict:
                    count_dict[word_lower] += 1
                else:
                    count_dict[word_lower] = 1

    # Recursively call count_words with the updated parameters
    count_words(subreddit, word_list, after=after, count_dict=count_dict)
