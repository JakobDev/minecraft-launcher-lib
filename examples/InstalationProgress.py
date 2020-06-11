#!/usr/bin/env python3
#This example shows how to show the progress of installation to the user.
import minecraft_launcher_lib

#Taken from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def maximum(max_value,value):
    max_value[0] = value

def main():
    #lambda doesn't allow setting vars, so we need this little hack
    max_value = [0]

    callback = {
        "setStatus": lambda text: print(text),
        "setProgress": lambda value: printProgressBar(value,max_value[0]),
        "setMax": lambda value: maximum(max_value,value)
    }

    version = minecraft_launcher_lib.utils.get_latest_version()["release"]
    directory = minecraft_launcher_lib.utils.get_minecraft_directory()

    minecraft_launcher_lib.install.install_minecraft_version(version,directory,callback=callback)

if __name__ == "__main__":
    main()

