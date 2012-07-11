import json
import os

def testFunc(port=9000):
    return port+1

def getConf():
    """
    parser checks for existence of the settings file settings.conf
    in the users $HOME/.ghost/ folder. If the file is not there, one
    will be created with the default values set. Returns a dict matching
    the settings.conf file.
    """
    confFile = os.environ['HOME']+'/.ghost/settings.conf'
    if os.access(confFile, 0):
        try:
            options = json.load(open(confFile))
            print options
        except:
            err = "Malformed JSON: Something is wrong with settings.conf"
            print err
    else:
        print "nope"


if __name__=='__main__':
    parser()