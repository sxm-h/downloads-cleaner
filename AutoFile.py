import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import shutil
import datetime


x = datetime.datetime.today()
day = str(x.strftime("%d"))
month = str(x.strftime("%m"))
year = str(x.strftime("%Y"))

date = ''.join(day+'-'+month+'-'+year)


def on_modified(event):
    print("on_modified")
    directory = os.path.join(os.getenv('USERPROFILE'), 'downloads', date)

    isDirectory = os.path.isdir(directory)
    if isDirectory == False:
        os.mkdir(directory)
        
        print(event.src_path)

    elif isDirectory == True:
        try:
            name = event.src_path
            name = name.replace(os.path.join(os.getenv('USERPROFILE'), 'downloads'), '')
            #shutil.move(event.src_path, os.path.join(directory, name))
            shutil.move(event.src_path, directory)
        except:
            pass


if __name__ == "__main__": #event handler

    patterns = "*" #file patterns we WANT to handle - in this case, all the files
    ignore_patterns = "" #file patterns they we DONT wont to handle
    ignore_directories = False #boolean that we can set to True if we want to be notified just for regular files (not for directories)
    case_sensitive = True #if set to true, make the previous patterns case sensitive
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    #Activate Methods 
    my_event_handler.on_modified = on_modified

    path = os.path.join( os.getenv('USERPROFILE'), 'downloads') #path to be monitored, "." = current directory

    go_recursively = True #set to true if you want to check subfolders
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start() #start the observer
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt: #if there is a file edit
        my_observer.stop()
        my_observer.join()