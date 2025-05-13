pip install pyinstaller
pyinstaller --windowed --icon=app.ico --add-data "config.json;." --add-data "ico;ico" main.py