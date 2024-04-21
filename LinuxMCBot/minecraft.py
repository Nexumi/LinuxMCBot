import config

import discord
from discord.ext import tasks, commands


class WaitForLog(commands.Cog):
  def __init__(self, message):
    self.message = message

    self.timeout = 300
    self.seconds = 0
    self.check.start()


  async def stop(self):
    if self.seconds < self.timeout:
      status = "Server has started"
    else:
      status = f"Something went wrong while trying to start the server"
    
    await self.message.edit(
      embed=discord.Embed(
        color=config.color,
        description=status
      )
    )

    self.check.cancel()


  async def dotX3(self):
    await self.message.edit(
      embed=discord.Embed(
        color=config.color,
        description=f"Server is starting.{'.' * ((self.seconds - 1) % 3)}"
      )
    )


  @tasks.loop(seconds=1)
  async def check(self):
    self.seconds += 1
    await self.dotX3()

    if self.seconds < 5:
      return

    if self.seconds < self.timeout:
      with open(f"{config.home}/logs/latest.log") as log:
        data = log.read()
        if "]: Done (" in data and ')! For help, type "help"' in data:
          await self.stop()
          return
    else:
      await self.stop()