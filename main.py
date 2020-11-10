import subprocess
import signal
import time
from constants import *



  
def help():
  # to do
  print("help")

def kill():
  # to do
  print("kill")

def launch():
  # to do
  print("launch")


def menu():
  userin = ""
  num_commands = len(COMMANDS) - 1
  funcs = globals()

  subprocess.run(CLEAR_C)
  while(userin != "exit"):
    print("Minecraft Server Manager", VERSION)
    print("Options:", *OPTIONS, sep = OPTIONS_STYLE)
    userin = input(PROMPT)
    if userin == "exit": exit(0)
    for command in COMMANDS:
      if(userin == command):
        funcs[command]()
        continue
      elif(command.index == num_commands):
        print(userin + ":", BAD_C)
        subprocess.run(CLEAR_C)
    
    
def sig_handler(signum, frame):
  sigint = 2
  if signum == sigint:
    print("\n", EXIT)
    exit(sigint)  


def main():
  signal.signal(signal.SIGINT, sig_handler)
  menu()

if __name__ == "__main__":
  main()