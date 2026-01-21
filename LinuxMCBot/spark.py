import utils
import config

from datetime import datetime, timedelta
import discord
from discord.ext import tasks, commands
from discord.utils import escape_markdown

class WaitForLog(commands.Cog):
  def __init__(self, message):
    self.message = message

    self.timeout = 20
    self.seconds = 0
    self.currentTime = datetime.now()
    self.check.start()


  async def showURL(self, url):
    url = url[url.index("https"):]
    await self.message.edit(
      embed=discord.Embed(
        color=config.color,
        description=f"[Spark Profile]({url})"
      )
    )


  async def showHealth(self, health):
    i = 0
    while i < len(health):
      health[i] = health[i].replace("    ", "　　")
      if "┃" in health[i] or "╻" in health[i]:
        health.pop(i)
      else:
        i += 1
    await self.message.edit(
      embed=discord.Embed(
        color=config.color,
        description=escape_markdown("\n".join(health))
      )
    )


  @tasks.loop(seconds=1)
  async def check(self):
    if self.seconds < self.timeout:
      self.seconds += 1
      with open(f"{config.home}/logs/latest.log") as log:
        data = log.read().splitlines()[-50:]
        for i in range(-1, -len(data) - 1, -1):
          line = data[i]
          if (link := "[⚡] Profiler live viewer:" in line) or "[⚡] Generating server health report..." in line:
            try:
              logTime = datetime.strptime(line[1:line.index("]")], "%d%b%Y %H:%M:%S.%f")
            except:
              logTime = datetime.strptime(line[1:line.index("]")], "%H:%M:%S")
              logTime = datetime.combine(self.currentTime.date(), logTime)
              if self.currentTime.hour == 23 and logTime.hour == 0:
                logTime += timedelta(days=1)
            if logTime >= self.currentTime:
              if link:
                await self.showURL(data[i + 1])
              else:
                await self.showHealth(data[i + 2:])
              self.check.cancel()
            return
    else:
      await self.message.edit(
        embed=discord.Embed(
          color=config.color,
          description="Could not find spark output"
        )
      )
      self.check.cancel()
