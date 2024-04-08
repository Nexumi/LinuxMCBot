python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pyinstaller
pyinstaller --onefile main.py
mv -f ./dist/main ./LinuxMCBot
rm main.spec
rm -rf build
rmdir dist