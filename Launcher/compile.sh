pyinstaller --onefile main.py
mv -f ./dist/main ./Launcher
rm main.spec
rm -rf build
rmdir dist