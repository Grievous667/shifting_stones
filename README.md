# Shifting Stones

## Math Research Seminar Spring 2024

Shifting Stones using Python and PyGame

## Running

To run the game, just install the dependencies with `pip install -r requirements.txt`, then
run `python main.py`.

## Creating an executable (uses `pyinstaller`)

### Windows

1. Open command prompt

2. Install the required packages:

    `>>> pip install -r requirements.txt`

3. Copy the `res` folder to the generated `dist/Shifting_Stones` directory. The `res` folder should be in the same folder as the `Shifting_Stones.exe` file

4. Run the build script in `cmd`

    `>> .\build-win.bat`

5. Run the exe

    `.\Shifting_Stones.exe`

    **You can also double click it in File Explorer.**

### macOS

1. Open command prompt

2. Install the required packages:

    `>>> pip install -r requirements.txt`

3. Run the build script in `cmd`

    `>> ./build-mac.sh`

4. Ensure that the app can access the image resources

5. Run the app

    `./Shifting_Stones.app/Contents/MacOS/Shifting_Stones`

    **You can also double click it in Finder.**
