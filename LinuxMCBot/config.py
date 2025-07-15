import utils

import os
import discord


def parse():
  global token, admins, game, status, color, mods, forge, guide, name, ip, home, start

  with open("config.txt") as cfg:
    data = cfg.read().splitlines()
    for line in data:
      if line != "" and not line.startswith("#"):
        if line.startswith("token = "):
          token = line[8:]
        elif line.startswith("admins = "):
          ids = line[9:]
          if ids.startswith("[") and ids.endswith("]"):
            ids = ids[1:-1].replace(", ", ",").split(",")
            for ID in ids:
              try:
                ID = int(ID)
              except:
                continue
              if ID not in admins:
                admins.append(ID)
        elif line.startswith("roles = "):
          rolls = line[8:]
          if rolls.startswith("[") and rolls.endswith("]"):
            rolls = rolls[1:-1].replace(", ", ",").split(",")
            for role in rolls:
              if role and role not in roles:
                roles.append(role)
        elif line.startswith("game = "):
          message = line[7:]
          if message.startswith("Playing "):
            message = message[8:]
            game = discord.Activity(name=message, type=discord.ActivityType.playing)
          elif message.startswith("Listening to "):
            message = message[13:]
            game = discord.Activity(name=message, type=discord.ActivityType.listening)
          elif message.startswith("Watching "):
            message = message[9:]
            game = discord.Activity(name=message, type=discord.ActivityType.watching)
        elif line.startswith("status = "):
          mode = line[9:]
          if mode == "ONLINE":
            status = discord.Status.online
          elif mode == "IDLE":
            status = discord.Status.idle
          elif mode == "DND":
            status = discord.Status.dnd
          elif mode == "INVISIBLE":
            status = discord.Status.invisible
        elif line.startswith("color = "):
          color = utils.hexaToDeci(line[8:])
        elif line.startswith("mods = "):
          mods = line[7:]
        elif line.startswith("forge = "):
          forge = line[8:]
        elif line.startswith("guide = "):
          guide = line[8:]
        elif line.startswith("name = "):
          name = line[7:]
        elif line.startswith("ip = "):
          ip = line[5:]
        elif line.startswith("start = "):
          parts = os.path.split(line[8:])
          home = parts[0]
          start = parts[1]


token = ""
admins = []
roles = []
game = None
status = discord.Status.online
color = 0
mods = ""
forge = ""
guide = ""
name = ""
ip = ""
home = ""
start = ""


version = {
  "major": 1,
  "minor": 2,
  "patch": 1
}