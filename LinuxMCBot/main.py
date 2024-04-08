import utils
import fresh
import config
import updates

import subprocess
import psutil
import discord
from mcstatus import JavaServer


print("\033[33mPlease use ctrl + c to shutdown the bot\033[0m")
updates.UpdateChecker()

try:
  with open("config.txt", "x") as cfg:
    print("First time running detected!")
    fresh.generate(cfg)
    print("config.txt generated")
except:
  pass
config.parse()

bot = discord.Bot(status=config.status, activity=config.game)


@bot.event
async def on_ready():
  utils.botReady(await bot.application_info())


@bot.slash_command(description="Gives the server ip. Paste in minecraft server address.")
@discord.guild_only()
async def ip(ctx):
  if await utils.isValidUser(ctx):
    await ctx.respond(
      embed=discord.Embed(
        color=config.color,
        description=config.ip
      )
    )


@bot.slash_command(description="Sends a link to a google drive with the required mods.")
@discord.guild_only()
async def mods(ctx):
  if await utils.isValidUser(ctx):
    await ctx.respond(
      embed=discord.Embed(
        color=config.color,
        description=f"[Required Mods]({config.mods})"
      )
    )


@bot.slash_command(description="Sends a link to a google doc with forge install instructions.")
@discord.guild_only()
async def forge(ctx):
  if await utils.isValidUser(ctx):
    await ctx.respond(
      embed=discord.Embed(
        color=config.color,
        description=f"[Forge Installation]({config.forge})"
      )
    )


@bot.slash_command(description="Sends a link to a wiki/documentation site. Everyone say thanks to Braden.")
@discord.guild_only()
async def guide(ctx):
  if await utils.isValidUser(ctx):
    await ctx.respond(
      embed=discord.Embed(
        color=config.color,
        description=f"[Braden's Guide]({config.guide})"
      )
    )


@bot.slash_command(description="Start server.")
@discord.guild_only()
async def start(ctx):
  if await utils.isValidUser(ctx):
    p = subprocess.Popen("screen -list | grep minecraft-server", stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode("utf-8")
    if out:
      if "(Detached)" in out:
        subprocess.call(f"x-terminal-emulator -e screen -S minecraft-server -r", shell=True)
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server is already running"
        )
      )
    else:
      subprocess.call(f"x-terminal-emulator -e screen -S minecraft-server bash -c 'cd\
        {config.home} && ./{config.start}'", shell=True)
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server is starting"
        )
      )


@bot.slash_command(description="Stop server.")
@discord.guild_only()
async def stop(ctx):
  if await utils.isValidUser(ctx):
    p = subprocess.Popen("screen -list | grep minecraft-server", stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode("utf-8")
    if not out:
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server isn't running"
        )
      )
    else:
      subprocess.call("screen -S minecraft-server -X stuff 'stop\n'", shell=True)
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server is stopping"
        )
      )


@bot.slash_command(description="View server status.")
@discord.guild_only()
async def status(ctx):
  if await utils.isValidUser(ctx):
    try:
      with open(f"{config.home}/server.properties") as props:
        read = props.read()
    except:
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="server.properties not found!"
        )
      )
      return

    port = utils.getProp(read, "server-port")
    server = JavaServer.lookup(f"localhost:{port}")
    try:
      status = server.status()
      desc = status.motd.raw['text'] if type(status.motd.raw) == dict else status.description
      version = status.version.name
      online = f"{status.players.online}/{status.players.max}"
      players = [player.name for player in status.players.sample] if status.players.sample else []
    except:
      desc = "Offline"
      version = "Offline"
      online = "Offline"
      players = []


    details = [
      f"Server: {config.name}",
      f"Description: {desc}",
      f"Version: {version}",
      f"IP: {config.ip}",
      f"port: {port}",
      f"Players: {online}",
      "- " + "\n- ".join(players) if players else ""
    ]

    await ctx.respond(
      embed=discord.Embed(
        color=config.color,
        description="\n".join(details)
      )
    )


@bot.slash_command(description="(Admin Only) Get current system CPU and RAM usage.")
@discord.guild_only()
async def usage(ctx):
  if await utils.isAdminUser(ctx):
    data = []
    cpu = psutil.cpu_percent(percpu=True)
    mem = psutil.virtual_memory()
    data.append("# CPU\n- " + "\n- ".join([f"[{i}] {cpu[i]}" for i in range(len(cpu))]))
    data.append(f"# RAM\n- {(mem.used) / 2 ** 30:.2f} GB / {mem.total / 2 ** 30:.2f} GB")
    await ctx.respond(
      embed=discord.Embed(
        color=config.color,
        description="\n".join(data)
      ),
      ephemeral=True
    )


@bot.slash_command(description="(Admin Only) Reload from config file.")
@discord.guild_only()
async def reload(ctx):
  if await utils.isValidUser(ctx):
    config.parse()
    utils.botReady(await bot.application_info())
    await ctx.respond(
      embed=discord.Embed(
        color=config.color,
        description="Config reloaded"
      ),
      ephemeral=True
    )


@bot.slash_command(description="About this bot.")
@discord.guild_only()
async def about(ctx):
  message = [
    "### The LinuxMCBot Project",
    "Created By: Nexumi",
    "Running: v1.0.0",
    "[GitHub](https://github.com/Nexumi/LinuxMCBot)"
  ]
  await ctx.respond(
    embed=discord.Embed(
      color=config.color,
      description="\n".join(message)
    )
  )


bot.run(config.token)