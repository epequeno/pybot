#!/usr/bin
/python
import irclib
import time
import re
import os
import json
from modules import google
from modules import bitcoincharts
from modules import blockchain

TRIGGERS = ['!help', '!g ', '!news ', '!img ', '!books ', '!btc', '!bc']

class Ghost(irclib.SimpleIRCClient):
    """Ghost class extends irclib.SimpleIRCClient."""

    def getConf(self):
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
            except:
                err = ("An error occoured while loading %s") % confFile
                return err
        else:
            #  TODO: actually make the code to create a new conf file with defaults
            return "No configuration file found. Creating new file ~/.ghost/settings.conf"
        return options

    def setOptions(self):
        settings = self.getConf()
        self.network = settings['network']
        self.port = settings['port']
        self.nickname = settings['nickname']
        self.pw = settings['password']
        self.name = settings['username']
        self.use_ssl = settings['use_ssl']
        self.chanToSay = settings['defaultChan']

    def ghostStart(self):
        """ghostStart is a wrapper for self's irclib.ServerConnection.connect()
        The parameters should come from the config parser."""
        self.setOptions()
        self.connect(self.network, self.port, self.nickname, password=self.pw, 
            username=self.name, ssl=self.use_ssl)
        time.sleep(10)
        self.join(self.chanToSay)
        self.start()

    def say(self, thingToSay):
        """thingToSay should be a string for now"""
        self.connection.privmsg(self.chanToSay, thingToSay)

    def join(self, chan):
        """join chan. chan should be string"""
        self.connection.join(chan)

    def nick(self, nick):
        """change nickname to nick. nick should be string"""
        self.connection.nick(nick)

    def disconnect(self, arg="Exeunt: Ghost"):
        """disconnect ghost"""
        self.connection.disconnect(arg)

    #  main trigger caller
    def on_pubmsg(self, connection, event):
        """
        main msgHandler each branch of the nested if/else block
        should map to a trigger. Not much logic should go here beyond
        calling the function and iterating say() over its results.
        Any other formatting should be isolated to the functions module.
        I wish python had switch/case statements.
        """
        if event.target() != self.chanToSay:
            pass
        else:
            msg = ''.join(event.arguments())
            trigs = [re.compile('^' + trig) for trig in TRIGGERS]

            for trig in trigs:
                if trig.match(msg):
                    if trig == trigs[0]:
                        self.say("I will respond to: " + str(TRIGGERS))
                    elif trig == trigs[1]:
                        results = google.search(msg)
                        for result in results:
                            self.say(result)
                    elif trig == trigs[2]:
                        results = google.news(msg)
                        for result in results:
                            self.say(result)
                    elif trig == trigs[3]:
                        results = google.images(msg)
                        for result in results:
                            self.say(result)
                    elif trig == trigs[4]:
                        results = google.books(msg)
                        for result in results:
                            self.say(result)
                    elif trig == trigs[5]:
                        self.say(bitcoincharts.marketData(msg))
                    elif trig == trigs[6]:
                        self.say(blockchain.stats())

if __name__== "__main__":
    casper = Ghost()
    casper.ghostStart()
