#!/usr/bin/python
# Created, cleaned and commented by Baba Orhum
# Threaded by Wascar
# Program in BETA1 (0.50-b1)
# Thanks to PapaJoke for his adviced

# Importing used modules
import os
import shutil
import tarfile
import urllib.request
import json
import glob
import tempfile
from threading import Thread

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.overrides import GLib
# Can be used in the future versions or... not :)
# from gi.overrides import GLib

# Thread for the GUI
config = json.load(open("/opt/lighttrans/config.json"))  # Values for languages and versions, don't like YAML because with its identation system
extensionname = '{e2fda1a4-762b-4020-b5ad-a41df1933103}.xpi'    # Useful in mozilla change extension name
primthundpath = '/usr/lib/thunderbird/extensions'  # Adapt it if necessary for other distros
secondthundpath = '/usr/lib/thunderbird/distribution/extensions'  # Same


class Handler:
    def onDestroy(self, *args):    # Sure if you quit with the cross the program terminates
        Gtk.main_quit()

    def onButtonClicked(self, button):   # Just starts when you click the button
        buttonswitcher.set_sensitive(False)    # Now the button is greyed, working :)
        buttonswitcher.set_label('PLEASE WAIT...')  # Sure the button text change to this
        lang = langCombo.get_active_text()          # Getting the lang value
        ver = verCombo.get_active_text()            # Getting the version value
        if lang is None:                            # If the user don't select the language ERROR BOX
            stopTrickingMe("You have to choose a target language")
            return False
        elif ver is None:                           # If the user don't select the version ERROR BOX
            stopTrickingMe("You have to choose thunderbird version")
            return False
        else:
            buttonswitcher.set_sensitive(False)     # Preparing and starting the second thread
            thread = Thread(target=patchThread, args=(tempfile.mkdtemp(), ver, lang))
            thread.daemon = True
            thread.start()


def patchThread(tempur, ver, lang):                     # The second thread
        try:
            sourcetar = 'thunderbird/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}.xpi'    # File we want to extract in the tar
            getlight = 'https://ftp.mozilla.org/pub/thunderbird/releases/' + ver + '/linux-x86_64/' + \
                       LANG[lang] + '/thunderbird-' + ver + '.tar.bz2'   #URL for Thunderbird
            print(getlight)
            filename = 'thunderbird-' + ver + '.tar.bz2'                 # Filename in variable
            urllib.request.urlretrieve(getlight, tempur + '/' + filename)  # Getting the file in URL
            os.rename(tempur + '/thunderbird-' + ver + '.tar.bz2',
                      tempur + '/thunderbird-' + ver + '-' + LANG[lang] + '.tar.bz2')    # Optionnal but can be used for debug
            if not os.path.exists(lang):         # For sure :)
                os.makedirs(tempur + '/' + lang)  # Working in temp file
                tar = tarfile.open(
                    tempur + '/thunderbird-' + ver + '-' + LANG[lang] + '.tar.bz2', 'r')   # Opening the tar file
                ioreader = tar.extractfile(sourcetar)   # Extracting
                with open(tempur + '/' + lang + '/' + extensionname, 'wb') as x:
                    x.write(ioreader.read())            # HERE :)
                tar.close()                             # Closing the tar file
                removeUserLight()                       # Have to but now without subprocess
                removeLight()                           # Get out extension not in my language :)
                shutil.copyfile(tempur + '/' + lang + '/' + extensionname, primthundpath + '/' + extensionname)    # Copy the downloaded extension in correct place
                shutil.rmtree(tempur + '/' + lang, ignore_errors=True)                                       # Last line before buttonswitcher removing temps
                os.remove(tempur + '/thunderbird-' + ver + '-' + LANG[lang] + '.tar.bz2')
                shutil.rmtree(tempur, ignore_errors=True)
                GLib.idle_add(doneSoft)                                                # Better to inform you
        except OSError:
            GLib.idle_add(errorSoft)


def doneSoft():
    buttonswitcher.set_label('DONE PLEASE CLOSE')

def errorSoft():
    stopTrickingMe("GENERAL EXCEPTION")


def stopTrickingMe(text):                            # You have to define version OK :)
    dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR,
                               buttons=Gtk.ButtonsType.OK, text="FATAL")
    dialog.format_secondary_text(text)
    dialog.run()
    dialog.destroy()


def removeLight():                                  # This removing Lightning extension
    try:
        os.remove(secondthundpath + '/' + extensionname)
    except OSError:
        pass
    try:
        os.remove(primthundpath + '/' + extensionname)
    except OSError:
        pass


def removeUserLight():                               # This removing Lightning extension in userspace
    filelist = glob.glob('/home/*/.thunderbird/*.default')
    for file in filelist:
        try:
            os.remove(file + '/extensions/' + extensionname)
        except:
            print('FILE NOT FOUND')
        try:
            os.remove(file + '/addonStartup.json.lz4')  # For solving the language collision, have to reactive all extensions at start.
        except:                                          # Don't like this complain to Mozilla or the creators of Arch or Manjaro
            print('FILE NOT FOUND')


if __name__ == '__main__':
    builder = Gtk.Builder()
    builder.add_from_file("/opt/lighttrans/transl.glade")  # Yes the GUI was created with glade and not in pure text :)
    builder.connect_signals(Handler())  # Sure connecting signals to Handler
    buttonswitcher = builder.get_object("transButton")  # If there is not, the button will be starts nothing

    # For getting language values (dictionary mode)
    LANG = config['langs']
    langCombo = builder.get_object("langCombo")
    for langloop in LANG.keys():
        langCombo.append_text(langloop)

    # For getting language values
    THUNDVER = config['versions']

    verCombo = builder.get_object("verCombo")
    for THUNDERLOOP in THUNDVER:
        verCombo.append_text(THUNDERLOOP)

    # Sorry for Main Window name :)
    window = builder.get_object("blowWinJob")
    window.show_all()

    Gtk.main()
