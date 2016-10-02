#!/usr/bin/env python

import praw

user_agent = ("Overwatch Info Fetcher by /u/Verinix v1.0")

r = praw.Reddit(user_agent = user_agent)

subreddit = r.get_subreddit("overwatch")
