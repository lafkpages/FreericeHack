# FreericeHack
A hack for https://freerice.com

## Usage
### PyRice (Python3)
1. Install [Python3](https://python.org)
1. Open a terminal and run `pip3 install requests`
   - If that doesn't work, try `python3 -m pip install requests` or `python -m pip install requests`
1. Download [Freerice.py](Freerice.py) and [Requester.py](Requester.py)
   - Make sure their extensions are `.py` and not `.txt`
1. Edit the `Requests.py` file at the _CONFIG_ section, near line _6_.
   - Change the variable `user` to your user ID
     - See the section about [User ID](#User_ID)s
1. In the terminal, go to your downloads folder
   - Windows: `cd C:\Users\YOU\Downloads`
   - Mac: `cd /Users/YOU/Downloads`
1. Run `python3 Requests.py`
   - If that doesn't work, try `python Requests.py`
1. Watch your rice grow. No need to open the [Freerice](https://freerice.com) website, this will do everything automatically.

### Auto bot (JavaScript)
1. Go to the [multiplication table category](https://freerice.com/categories/multiplication-table) in Freerice.
1. Open your browser's console (see [Opening the console](#opening-the-console)).
1. Copy all the code from [Client_JavaScript/interval.js](Client_JavaScript/interval.js).
1. Paste it into the console and press `Enter`.
1. The correct answers will be clicked automatically.

### Space bar (JavaScript)
1. Go to the [multiplication table category](https://freerice.com/categories/multiplication-table) in Freerice.
1. Open your browser's console (see [Opening the console](#opening-the-console)).
1. Copy all the code from [Client_JavaScript/spacebar.js](Client_JavaScript/spacebar.js).
1. Paste it into the console and press `Enter`.
1. Close the console and click anywhere on the Freerice page.
1. Press the spacebar and the correct answer will be clicked automatically.

## Opening the console
### MAC
#### Chrome

Press `Cmd + Alt + J`.
### Windows

Press `F12` (or `FN + F12`).

## User ID
### Chrome
1. Go to [Freerice.com](https://freerice.com)
1. Open the console (see [Opening the console](#opening-the-console))
1. Go to the `application` section
1. Open the `Local storage` menu on the left, and select `https://freerice.com`
1. Double-click on the `user` value, and you'll see a JSON like this:
```
{
  "token": "...",
  "uuid": "..."
}
```
1. Copy the value in `uuid`
