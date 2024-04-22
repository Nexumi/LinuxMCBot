# Launcher
> Simple script to launch LinuxMCBot in a terminal

Workaround code to launch precompiled version in a terminal. NOT required if running bot from source.

## Build
```
sudo apt update
sudo apt install git python3 python3.10-venv
git clone https://github.com/Nexumi/LinuxMCBot.git
cd LinuxMCBot/Launcher
python3 -m venv .venv
source .venv/bin/activate
chmod +x compile.sh
./compile.sh
```