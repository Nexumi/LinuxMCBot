import config
import spark

import time
import subprocess
import discord


# Helpful Functions

def hexaToDeci(hexa):
  if hexa.startswith("#"):
    hexa = hexa[1:]
    if len(hexa) == 3:
      for h in hexa:
        hexa += h * 2
      hexa = hexa[3:]

    try:
      return int(hexa, 16)
    except:
      pass
  return 0


def getProp(prop):
  try:
    with open(f"{config.home}/server.properties") as infile:
      props = infile.read()
  except:
    return ""

  start = props.find(f"{prop}=")
  if start == -1:
    return ""
  start += len(prop) + 1

  end = props.find("\n", start)
  if end == -1:
    end = len(props)

  return props[start:end]

def botInvite(cid):
  print()
  print(f"Invite Link: https://discord.com/oauth2/authorize?client_id={cid}&permissions=0&integration_type=0&scope=applications.commands+bot")
  print()

def botReady(info):
  botInvite(info.id)

  if config.game is None:
    print(f"{info.name} is ready")
  else:
    to = ' to' if config.game.type.name == 'listening' else ''
    print(f"{info.name} is {config.game.type.name}{to} {config.game.name}")


# subprocess Functions

def Popen(command):
  out, err = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
  return out.decode("utf-8"), err.decode("utf-8") 


def isTmuxActive():
  out, err = Popen("tmux ls | grep minecraft-server")
  return out.startswith("minecraft-server: ")

def tmuxSend(command, message=None):
  subprocess.call(f"tmux send-keys -t minecraft-server C-z '{command}' Enter", shell=True)
  if command.startswith("spark "):
    spark.WaitForLog(message, command == "spark profiler open")


# Validation Functions

async def isAdminUser(ctx):
  valid = ctx.author.id in config.admins
  if not valid:
    await ctx.respond(
      embed=discord.Embed(
        color=8864735,
        description="UNAUTHORIZED USER"
      ),
      ephemeral=True
    )
  return valid


async def isValidUser(ctx):
  valid = not config.roles or ctx.author.id in config.admins or \
    any(role.name in config.roles for role in ctx.author.roles)
  if not valid:
    await ctx.respond(
      embed=discord.Embed(
        color=8864735,
        description=f"UNAUTHORIZED USER\nREQUIRED ROLE:\n- " + "\n- ".join(config.roles)
      ),
      ephemeral=True
    )
  return valid