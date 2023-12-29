# Kecker

The Python-based keyboard auto clicker with commands system.

# Quick start

```shell
git clone https://github.com/Moderrek/kecker.git
cd kecker/
pip install pynput
python main.py
> toggle .
Set toggle key to .
> key i
Current tapping key is i
> speed 2
Set tap/sec to 2.0
```
Enjoy usage :)

# How to run

 * Download [Python](https://www.python.org/downloads/).
 * Execute in terminal ``pip install pynput``
 * Then run downloaded file.

# Usage

Kecker is terminal program with commands.
1. Set the clicking key "a" by command ``key a``
2. Set the clicking speed (x per sec) by ``speed x``
3. Start by command ``start`` (end by ``stop``) or set toggle key ``toggle .``
4. Then tap the "." to start end clicking

# Commands
| Command            | Description                   |
|--------------------|-------------------------------|
| info               | Prints the program info       |
| start              | Starts tapping the key        |
| stop               | Stops tapping the key         |
| end                | Kills the program             |
| config             | Prints the config             |
| key <character>    | Sets/Gets the tap key         |
| speed <per sec>    | Sets/Gets the key tap per sec |
| toggle <character> | Sets/Gets the toggle key      |