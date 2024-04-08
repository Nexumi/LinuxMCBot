# Launcher
> Simple script to launch LinuxMCBot in a terminal

## Direct Run
### First Time Setup
```
sudo apt update
sudo apt install git screen python3
git clone https://github.com/Nexumi/LinuxMCBot.git
cd LinuxMCBot/Launcher
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run
```
cd /path/to/LinuxMCBot/Launcher
source .venv/bin/activate
python main.py
```

## Build
```
sudo apt update
sudo apt install git python3
git clone https://github.com/Nexumi/LinuxMCBot.git
cd LinuxMCBot/Launcher
chmod +x compile.sh
./compile.sh
```