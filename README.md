# TileGame

## Setup

The setup below is for beginners. Technically all you need is an HTTP client to play this game, so in theory you could write the client in any preferred language.

### Install Python 3

If you do not already have python installed, please go [here](https://www.python.org/downloads/) and download it to install it (IMPORTANT: Select the box for adding to PATH). If you are not sure whether or not Python is installed, you may do the following:

- on Windows: Open command prompt and type ```python -V```. You should see a version number for python if it's installed
- on MacOs/Unix: Open terminal and type ```python -V```. You should see a version number for python if it's installed

Note: Make sure your python version is 3.x.x, and not 2.x.x. If 2 is installed, you need to download python 3 and install.

### Install Git
You need to install git in order to download the entire repository. Please go [here](https://git-scm.com/downloads) to download and install it. Like with Python, make sure Git is added to PATH during the installation process

### Install libraries
Open terminal/command prompt and run ```pip install requests```

### Clone this repository
Navigate to a folder within Command prompt/terminal that you want to use this code in. Use the command ```git clone https://github.com/fendull-streamer/tilegame.git``` to copy this repository to your local machine. If you're not sure how to navigate a terminal, see [here](https://www.vikingcodeschool.com/web-development-basics/a-command-line-crash-course)

### (Optional) Download and install a text editor
Some great options are VSCode, Atom, or Sublime text. Having a text editor other than Notepad makes editing code much nicer.


## Getting started
Follow these steps in order to actually play the game.

### Obtain your Id_Token
First, go to [Fendull.com](https://fendull.com/code) to obtain an id token. Copy the token to the clipboard. Change the value of ID_TOKEN in the file play_tile_game.py to the copied id token.

### Start python
Open a terminal/cmd prompt and navigate to the tilegame directory. In there, run the following command:
```python -i play_tile_game.py```

This will execute the play_tile_game.py script and then start an interpreter.

### Respond to questions
To respond to a question, type:
```client.respond(<Your answer>)```