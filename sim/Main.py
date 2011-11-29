import os
from application.ApplicationController import *

def Main(args):
    # Copying libsimulator.so to the working directory is necessary to get gdb backtrace.
    # System.IO.File.Copy("./libsimulator.so", TORCS_DATA_PATH + "libsimulator.so", true); 

    # if System.IO.File.Exists("data/openracing.xml"):
    #    Directory.SetCurrentDirectory("data")
    # else:
    #    Directory.SetCurrentDirectory(Config.OPENRACING_DATA_PATH)
    controller = ApplicationController()
    if len(args) > 0:
        if args[0] == "--console":
            controller.InitConsoleRace()
        elif args[0] == "--quick-race":
            controller.InitQuickRace()
        else: # if (args[1] == "--help")
            print("usage: PyTorcs [options]")
            print("options:")
            print("       --console        Launch a race immediately. No GUI / No Graphics.")
            print("       --quick-race     Launch a race immediately. No GUI.")
            return 
    else:
        controller.Init()
    controller.Run()

Main(["--console"])
