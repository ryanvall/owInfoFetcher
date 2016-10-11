#!/usr/bin/env python

import praw
import re
import requests
import time
import utils

username = open("username.txt").read().rstrip()
password = open("password.txt").read().rstrip()
user_agent = ("Overwatch Info Fetcher by /u/Verinix v1.0")
BOT_TAIL = "\n\nBeep boop, I am a bot. Message /u/Verinix for feedback or other suggestions!"
API_BASE_URL = 'https://api.lootbox.eu'

reddit = praw.Reddit(user_agent = user_agent)
reddit.login(username = username, password = password)

# Various needed variables
subreddit = reddit.get_subreddit("test")
already_done_comments = set()
already_done_submissions = set()
call_pattern = re.compile("\[\[(?P<call>.*?)\]\]")

# Function to return player profile information based on a battletag
def get_player_profile(battletag):
  battletag = battletag.replace("#", '-')
  #todo get region/platform from battletag
  req_url = "%s/%s/%s/%s/profile" % (API_BASE_URL, platform, region, battletag)
  r = requests.get(req_url)
  if r.status_code == 200:
    json = r.json()
    #todo format response into pretty table
    result = "pretty table here"
  else:
    raise utils.APIConnectionException("Error contacting Lootbox API, error code %d." % r.status_code)
    result = "Error"
  return result

# Function to return the patch notes for submission that contain "Patch Notes" in the title
def get_patch_notes():
  request = "patch_notes"
  req_url = "%s/%s" % (API_BASE_URL, request)
  r = requests.get(req_url)
  if r.status_code == 200:
    json = r.json()
    result = json["patchNotes"][0]["detail"]
  else:
    raise utils.APIConnectionException("Error contacting Lootbox API.")
    result = "Error contacting Lootbox API."
  return result

# Helper function to parse out bot requests and call the appropriate response method
def bot_reply(bot_request):
  request_arr = bot_request.split(' ')
  if request_arr[0].lower() == "profile":
    reply_body = get_player_profile(request_arr[1])
  # other calls here as needed
  else:
    raise utils.InvalidRequestException("Invalid method %s requested." % request_arr[0])
  return reply_body

# Main bot loop
running = True
while running:
  # check threads for patch notes
  for submission in subreddit.get_new(limit = SUBMISSION_LIMIT):
    if submission not in already_done_submissions:
      already_done_submissions.add(submission)
      # todo if submission title contains patch notes, run following:
      try:
        reply_body = get_patch_notes()
      except APIConnectionException as ex:
        print("API Error: {0}".format(ex))
        continue
      reply = reply_body + "\n" + BOT_TAIL
      submission.add_comment(reply)
      # else continue if patchnotes not in title
    else:
      continue
  # check comments for calls about heros/etc
  for comment in praw.helpers.flatten_tree(subreddit.get_comments()):
    if comment not in already_done_comments:
      already_done_comments.add(comment)
      match = call_pattern.search(comment.body)
      if not match:
        continue
      bot_request = match.group("call")
      # parse bot request
      try:
        reply_body = bot_reply(bot_request)
      except InvalidRequestException as ex:
        print("Request Error: {0}".format(ex))
        continue
      comment.reply(reply_body + "\n" + BOT_TAIL)
    else:
      continue

  # sleep for a minute
  time.sleep(60)
