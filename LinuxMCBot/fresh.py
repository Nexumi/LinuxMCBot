def generate(file):
	token = input("Please input BOT TOKEN: ").strip()
	cfg = \
f"""#######################################################
# Config for the LinuxMCBot                           #
#######################################################
# Any line starting with # is ignored                 #
# All other items have defaults if you don't set them #
#######################################################


# This sets the token for the bot to log in with
# This MUST be a bot token (user tokens will not work)

token = {token if token else "BOT_TOKEN_HERE"}


# This sets the owner of the bot
# This needs to be the owner's ID (a 17-18 digit number)
# Example: admins = [954230687912053468, 74108529639510753]

admins = []


# This sets the roles the bots will listen to commands from
# Users without any of the roles listed will get rejected by the bot
# Anyone can run commands if no roles are specified
# Example: roles = [Minecrafter, Person with permissions]
# Please avoid roles with commas in them as the bot seperates the roles by commas

roles = []


# If you set this, it modifies the default game of the bot
# Set this to NONE to have no game
# You can make the game "Playing X", "Listening to X", or "Watching X"
# where X is the title.

game = NONE


# If you set this, it will modify the default status of bot
# Valid values: ONLINE IDLE DND INVISIBLE

status = ONLINE


# If you set this, it will modify the color of the embed message
# Set this to a hexadecimal number

color = #000000


# Documentation

mods = https://drive.google.com/
forge = https://docs.google.com/
guide = https://docs.google.com/


# Name of the server. It can be anything you want.

name = Minecraft Server


# Set the server ip to be used when getting ip

ip = example.domain.com


# Absolute path to the server start script

start = /path/to/start.sh"""
	file.write(cfg)