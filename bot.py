#!/usr/bin/env python

import praw

username = open("username.txt").read().rstrip()
password = open("password.txt").read().rstrip()
user_agent = ("Overwatch Info Fetcher by /u/Verinix v1.0")

reddit = praw.Reddit(user_agent = user_agent)
reddit.login(username = username, password = password)

subreddit = r.get_subreddit("overwatch")
