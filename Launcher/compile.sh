python3 -m venv .venv
source .venv/bin/activate
pip install pyinstaller
pyinstaller --onefile main.py
mv -f ./dist/main ./Launcher
rm main.spec
rm -rf build
rmdir dist