#!/usr/bin/env python

import praw
import re

username = open("username.txt").read().rstrip()
password = open("password.txt").read().rstrip()
user_agent = ("Overwatch Info Fetcher by /u/Verinix v1.0")
bot_tail = "\n\nBeep boop, I am a bot. Message /u/Verinix for feedback or other suggestions!"

reddit = praw.Reddit(user_agent = user_agent)
reddit.login(username = username, password = password)

subreddit = reddit.get_subreddit("overwatch")
already_done = set()
hero_pattern = re.compile("\[(?P<hero>.*?)/]")

running = True
while running:
  for comment in praw.helpers.flatten_tree(subreddit.get_comments()):
    match = call_pattern.search(comment.body)
    if not match:
      continue
    hero = match.group("hero")
    reply_body = return_info(hero)
    comment.reply(reply_body + bot_tail)

  # sleep for a minute
  time.sleep(60)

def return_info(hero)
  return "todo"
