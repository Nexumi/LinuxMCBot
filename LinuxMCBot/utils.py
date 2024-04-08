import config

import discord


# Helpful Functions

def getProp(props, prop):
  serverPort = props.index(f"{prop}=") + len(prop) + 1
  endl = props.index("\n", serverPort)
  return props[serverPort:endl]


def botReady(info):
  if config.game is None:
    print(f"{info.name} is ready")
  else:
    to = ' to' if config.game.type.name == 'listening' else ''
    print(f"{info.name} is {config.game.type.name}{to} {config.game.name}")


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