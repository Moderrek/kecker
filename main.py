# Welcome to Kecker the Python-based keyboard auto clicker
# with command system
# by Tymon Woźniak (https://github.com/Moderrek)

# Kecker = KEyboard cliCKER

# Defaults
tap_per_sec = 5  # taps 5 times per sec
key = 'a'        # tap key = a
toggle_key = ""  # DEFAULT NONE

# Cannot change by command
tap_streak = 1   # EXPERIMENTAL (like double-click)

import threading
import time

from pynput.keyboard import Key, Controller, Listener, KeyCode

program_running = True
tapping = False
commands = dict()
threads = []
key_listener = None


def print_config():
  print(f"Current config:"
        f" Delay: {1 / tap_per_sec}s\n"
        f" Tap key: {key}\n"
        f" Clicker Toggle key: {toggle_key}")


def on_press(key):
  if key == KeyCode(char=toggle_key):
    global tapping
    tapping = not tapping
    if tapping:
      print("Enabled")
    else:
      print("Disabled")


def run():
  while program_running:
    if tapping:
      for _ in range(tap_streak):
        keyboard.tap(key)
    time.sleep(1 / tap_per_sec)


def key_listener():
  with Listener(on_press=on_press) as listener:
    global key_listener
    key_listener = listener
    key_listener.join()


def process_cmd(cmd: str):
  splited = cmd.split(' ')
  label = splited[0].lower()
  args = splited[1::]
  if label not in commands:
    print("Unknown command use /help.")
    return
  commands[label].execute(args)


class Command:
  def __init__(self, label):
    self.__label = label

  def get_label(self) -> str:
    return self.__label

  def execute(self, args: list[str]) -> None:
    raise NotImplementedError()


class SimpleCommand(Command):
  def __init__(self, label, exec_fn):
    super().__init__(label)
    self.__exec_fn = exec_fn

  def execute(self, args):
    self.__exec_fn(args)


def make_cmd(label: str, fn) -> Command:
  return SimpleCommand(label, fn)


def register_command(command: Command):
  if command.get_label() in commands:
    print("Command already exists!")
    return
  commands[command.get_label()] = command


def stop_program():
  global program_running
  global tapping
  program_running = False
  tapping = False
  key_listener.stop()
  print("bye")


def set_speed(args: list[str]):
  global tap_per_sec
  if len(args) == 0:
    global key
    print(f"Current speed: tap {key} * {tap_per_sec}/s")
    return
  speed = float(args[0])
  tap_per_sec = speed
  print(f"Set tap/sec to {speed}")


def set_key(args: list[str]):
  global key
  if len(args) == 0:
    print(f"Current tapping key is {key}")
    return
  key = args[0][0]
  print(f"Set key to {key}")


def set_toggle_key(args: list[str]):
  global toggle_key
  if len(args) == 0:
    print(f"Current toggle key is {toggle_key}")
    return
  toggle_key = args[0][0]
  print(f"Set toggle key to {toggle_key}")


def start_tapping():
  global tapping
  tapping = True
  print("Enabled")


def stop_tapping():
  global tapping
  tapping = False
  print("Disabled")


def register_commands():
  register_command(make_cmd("help", lambda args: print("These are Kecker commands:\n"
                                                       " 1. start : Starts tapping the key\n"
                                                       " 2. stop : Stops tapping the key\n"
                                                       " 3. end : Kills the program\n"
                                                       " 4. speed <per sec> : Sets/Gets the key tap per sec\n"
                                                       " 5. toggle <character> : Sets/Gets the toggle key\n"
                                                       " 6. key <character> : Sets/Gets the tap key\n"
                                                       " 7. config : Prints the config\n"
                                                       " 8. info : Prints the program info")))
  register_command(make_cmd("start", lambda args: start_tapping()))
  register_command(make_cmd("stop", lambda args: stop_tapping()))
  register_command(make_cmd("end", lambda args: stop_program()))
  register_command(make_cmd("speed", set_speed))
  register_command(make_cmd("toggle", set_toggle_key))
  register_command(make_cmd("key", set_key))
  register_command(make_cmd("config", lambda args: print_config()))
  register_command(make_cmd("info", lambda args: print("Python-based Keyboard Clicked\n"
                                                       "Kecker v1.0 created by Tymon Woźniak.\n"
                                                       "https://github.com/Moderrek")))


if __name__ == "__main__":
  register_commands()
  print("Welcome to Kecker v1.0\n"
        "The Keyboard Clicker\n"
        "Created by Tymon Woźniak\n"
        "https://github.com/Moderrek")
  print_config()
  keyboard = Controller()
  threads.append(threading.Thread(target=run))
  threads.append(threading.Thread(target=key_listener))
  for thread in threads:
    thread.start()
  print("Enter command below:")
  print("For help use > help")
  while program_running:
    try:
      cmd = input("> ")
    except KeyboardInterrupt:
      stop_program()
    else:
      process_cmd(cmd)
