# LinuxMCBot
> Discord Bot Code

## Direct Run
### First Time Setup
```
sudo apt update
sudo apt install git screen python3
git clone https://github.com/Nexumi/LinuxMCBot.git
cd LinuxMCBot/LinuxMCBot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run
```
cd /path/to/LinuxMCBot/LinuxMCBot
source .venv/bin/activate
python main.py
```

## Build
```
sudo apt update
sudo apt install git python3
git clone https://github.com/Nexumi/LinuxMCBot.git
cd LinuxMCBot/LinuxMCBot
chmod +x compile.sh
./compile.sh
```