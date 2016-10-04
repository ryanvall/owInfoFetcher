#!/usr/bin/env python

import praw
import re
import requests
import time

username = open("username.txt").read().rstrip()
password = open("password.txt").read().rstrip()
user_agent = ("Overwatch Info Fetcher by /u/Verinix v1.0")
bot_tail = "\n\nBeep boop, I am a bot. Message /u/Verinix for feedback or other suggestions!"

reddit = praw.Reddit(user_agent = user_agent)
reddit.login(username = username, password = password)

subreddit = reddit.get_subreddit("test")
already_done = set()
hero_pattern = re.compile("\[\[(?P<hero>.*?)\]\]")

def return_info(hero):
  result = ""
  r = requests.get('https://api.lootbox.eu/patch_notes')
  if r.status_code == 200:
    json = r.json()
    result = json["patchNotes"][0]["detail"]
  else:
    result = "Error contacting Lootbox API."

  return result

running = True
while running:
  for comment in praw.helpers.flatten_tree(subreddit.get_comments()):
    if comment not in already_done:
      already_done.add(comment)
      match = hero_pattern.search(comment.body)
      if not match:
        continue
      hero = match.group("hero")
      reply_body = return_info(hero)
      comment.reply(hero + "\n" + reply_body + "\n" + bot_tail)
    else:
      continue

  # sleep for a minute
  time.sleep(60)

