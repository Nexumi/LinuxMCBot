import utils
import config

from urllib.request import urlopen, urlretrieve
from discord.ext import tasks, commands


def check():
  url = "https://raw.githubusercontent.com/Nexumi/LinuxMCBot/main/LinuxMCBot/config.py"
  try:
    version = eval("\n".join([line.decode("utf-8") for line in urlopen(url).read().splitlines()[-5:]]).replace("version = ", ""))
  except:
    return None

  if new(version):
    print("[\033[34mnotice\033[0m] A new release of LinuxMCBot is available: \033[31m" +\
      simpleName() + "\033[0m -> \033[32m" + simpleName(version) + "\033[0m")


def new(version):
  return tuple(config.version.values()) < tuple(version.values())

def simpleName(v = config.version):
  return f"v{v['major']}.{v['minor']}.{v['patch']}"


class UpdateChecker(commands.Cog):
  def __init__(self):
    if config.update:
      self.check.start()


  @tasks.loop(hours=24)
  async def check(self):
    check()
