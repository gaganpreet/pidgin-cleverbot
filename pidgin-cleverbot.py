#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from cleverbot import Session
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
 
conversations = {}
 
def htmlClean(pidginHtml):
    soup = BeautifulSoup(pidginHtml)
    pidginHtml = soup.findAll('body')[-1].contents
    return str(BeautifulStoneSoup(pidginHtml[0], convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
 
def my_func(account, who, message, conversation, flags):
    global purple
    direction = "Incoming"
    if flags != 2:
        direction = "Outgoing"
    print "Account/ConvId(%s/%s): %s message - %s said: \"%s\"" % (account, conversation, direction, who, message)
    username = purple.PurpleAccountGetUsername(account)
    if flags == 2 and username == "username@gmail.com/Home":
        if conversation not in conversations.keys():
            conversations[conversation] = Session()
            purple.PurpleConvImSend(purple.PurpleConvIm(conversation), u'Hi! Gagan is not around right now...')
        else:
            question = htmlClean(message)
            response = conversations[conversation].Ask(question)
            print 'Asked: "%s" Response: "%s"' % (question, response)
            purple.PurpleConvImSend(purple.PurpleConvIm(conversation), response)
 
bus.add_signal_receiver(my_func,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="DisplayedImMsg")
 
loop = gobject.MainLoop()
loop.run()

