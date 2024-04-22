import utils
import fresh
import config
import updates
import minecraft

import subprocess
import psutil
import discord
from mcstatus import JavaServer


subprocess.call(f"clear", shell=True)
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


@bot.slash_command(description="Get a list of all available commands.")
@discord.guild_only()
async def help(ctx):
  if await utils.isValidUser(ctx):
    if bot.commands:
      commands = []
      for command in bot.commands:
        commands.append(f"### /{command.name}\n{command.description}")
    else:
      commands = ["Bot is still warming up, please try again in a few seconds."]
    await ctx.respond(
      embed=discord.Embed(
        color=config.color,
        description="\n".join(commands)
      ),
      ephemeral=True
    )



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
    out, err = utils.Popen("tmux ls | grep minecraft-server")
    if out.startswith("minecraft-server: "):
      if "(attached)" not in out:
        subprocess.call(f"x-terminal-emulator -e tmux a -t minecraft-server &", shell=True)
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server is already running"
        )
      )
    else:
      subprocess.call(f"x-terminal-emulator -e tmux new-session -s minecraft-server -c {config.home} './{config.start}' &", shell=True)
      subprocess.call("sleep 1 && tmux set-option -t minecraft-server -g mouse on &", shell=True)
      message = await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server is starting"
        )
      )
      minecraft.WaitForLog(message)


@bot.slash_command(description="(Admin Only) Stop server.")
@discord.guild_only()
async def stop(ctx):
  if await utils.isAdminUser(ctx):
    if utils.isTmuxActive():
      utils.tmuxSend("stop")
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server has stopped"
        )
      )
    else:
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server isn't running"
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


@bot.slash_command(description="Get server health via spark.")
@discord.guild_only()
async def health(ctx, memory: discord.commands.Option(bool, "use --memory", required=False, default=False)):
  if await utils.isValidUser(ctx):
    if utils.isTmuxActive():
      message = await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Generating..."
        ),
      )
      utils.tmuxSend(f"spark health{' --memory' if memory else ''}", message)
    else:
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server is offline"
        ),
      )


@bot.slash_command(description="(Admin Only) Get server's spark profile link.")
@discord.guild_only()
async def profile(ctx):
  if await utils.isAdminUser(ctx):
    if utils.isTmuxActive():
      message = await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Generating..."
        ),
        ephemeral=True
      )
      utils.tmuxSend("spark profiler open", message)
    else:
      await ctx.respond(
        embed=discord.Embed(
          color=config.color,
          description="Server is offline"
        ),
        ephemeral=True
      )


@bot.slash_command(description="(Admin Only) Reload from config file.")
@discord.guild_only()
async def reload(ctx):
  if await utils.isAdminUser(ctx):
    config.parse()
    await bot.change_presence(status=config.status, activity=config.game)
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
    f"Running: {updates.simpleName()}",
    "[GitHub](https://github.com/Nexumi/LinuxMCBot)"
  ]
  await ctx.respond(
    embed=discord.Embed(
      color=config.color,
      description="\n".join(message)
    )
  )


bot.run(config.token)
