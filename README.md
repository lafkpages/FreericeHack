# FreericeHack
A hack for https://freerice.com (useful if you want to beat BTS ARMY)

## Usage
### PyRice (Python3)
1. Install [Python3](https://python.org) (if not already installed)
1. Open a terminal and run `pip3 install requests torpy`
   - If that doesn't work, try `python3 -m pip install requests torpy` or `python -m pip install requests torpy`
1. Download [Freerice.py](Freerice.py) and [Requester.py](Requester.py)
   - Make sure their extensions are `.py` (and not `.txt` or without an extension)
1. In the terminal, go to your downloads folder
   - Windows: `cd ~\Downloads`
   - Mac/Linux: `cd ~/Downloads`
1. Run `python3 Requests.py -u your_user_id` (see the [User ID](#user-id)s section)
   - If that doesn't work, try `python Requests.py -u your_user_id`
1. Watch your amount of rice grow. But remember to open the [Freerice website](https://freerice.com) so they have some kind of income.

**Note:** if you get blocked very quickly, try running it with an interval of 3 seconds: `python3 Requests.py -i 3`
<br>
You can change it if you want to whatever amount of seconds to wait between question.

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
### Windows/Linux

Press `F12` (or `FN + F12` on some keyboards).

## User ID
### Chrome
1. Go to [Freerice.com](https://freerice.com)
1. Open the console (see [Opening the console](#opening-the-console))
1. Go to the `application` section
1. Open the `Local storage` menu on the left, and select `https://freerice.com`
![Screenshot](README_img1.png)
1. Double-click on the `user` value, and you'll see a JSON like this:
   ```
   {
     "token": "...",
     "uuid": "..."
   }
   ```
1. Copy the value in `uuid`
