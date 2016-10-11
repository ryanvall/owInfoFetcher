#!/usr/bin/env python

import praw
import re
import requests
import time
import utils

username = open("username.txt").read().rstrip()
password = open("password.txt").read().rstrip()
user_agent = ("Overwatch Info Fetcher by /u/Verinix v1.0")
bot_tail = "\n\nBeep boop, I am a bot. Message /u/Verinix for feedback or other suggestions!"

reddit = praw.Reddit(user_agent = user_agent)
reddit.login(username = username, password = password)

subreddit = reddit.get_subreddit("test")
already_done_comments = set()
already_done_submissions = set()
hero_pattern = re.compile("\[\[(?P<hero>.*?)\]\]")

def return_info(hero):
  r = requests.get('https://api.lootbox.eu/patch_notes')
  if r.status_code == 200:
    json = r.json()
    result = json["patchNotes"][0]["detail"]
  else:
    raise utils.APIConnectionException("Error contacting Lootbox API, error code %d." % r.status_code)
    result = "Error"
  return result

def get_patch_notes():
  r = requests.get('https://api.lootbox.eu/patch_notes')
  if r.status_code == 200:
    json = r.json()
    result = json["patchNotes"][0]["detail"]
  else:
    raise utils.APIConnectionException("Error contacting Lootbox API.")
    result = "Error contacting Lootbox API."
  return result

running = True
while running:
  # check threads for patch notes
  for submission in subreddit.get_new(limit = SUBMISSION_LIMIT):
    if submission not in already_done_submissions:
      already_done_submissions.add(submission)
      reply_body = get_patch_notes()
      reply = reply_body + "\n" + bot_tail
      submission.add_comment(reply)
    else:
      continue
  # check comments for calls about heros/etc
  for comment in praw.helpers.flatten_tree(subreddit.get_comments()):
    if comment not in already_done_comments:
      already_done_comments.add(comment)
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
