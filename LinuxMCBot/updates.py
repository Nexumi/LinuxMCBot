import utils
import config

import requests
from discord.ext import tasks, commands


def check():
  url = "https://api.github.com/repos/Nexumi/LinuxMCBot/releases/latest"
  response = requests.get(url)
  data = response.json()
  version = data.get("tag_name")

  if new(version):
    print("[\033[34mnotice\033[0m] A new release of LinuxMCBot is available: \033[31m" +\
      simpleName() + "\033[0m -> \033[32m" + version + "\033[0m")


def new(version):
  return tuple(config.version.values()) < tuple(map(int, version[1:].split(".")))

def simpleName(v = config.version):
  return f"v{v['major']}.{v['minor']}.{v['patch']}"


class UpdateChecker(commands.Cog):
  def __init__(self):
    if config.update:
      self.check.start()


  @tasks.loop(hours=24)
  async def check(self):
    check()
