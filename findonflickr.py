#!/usr/bin/env python

""" 
Find files on Flickr
"""

#   findonflickr.py version 0.1
#
#   WHAT THIS DOES
#   ==============
#   Flickr filenames are of the form "3918794531_da13193ee2_o.jpg". The first
#   part ("3918794531") is a unique photo ID, (and represents where in the
#   sequence of uploads to Flickr this image was) so, using the 
#   http://flickr.com/photo.gne?id=PHOTOID trick, we can get directly to the
#   photo page.
#
#   [The other parts of the filename - "da13193ee2" and "o" - are a secret hash
#   for that image and image size respectively]
#
#
#   INSTALLING
#   ==========
#   This is an extension to Nautilus. Copy to your .nautilus/python-extensions
#   folder and restart Nautilus. You will also need to have the python-nautilus
#   Python bindings installed.  You will see a new item in the context menu
#   when you right-click on an image called "Find on Flickr..." Clicking this
#   will opening the Flickr photo page (assuming you have permissions to view
#   that image) in your default browser.
#
#   Testing on Ubuntu Karmic 9.10 with Nautilus 2.28.1
#   
#   THANKS TO
#   =========
#   1) Seemanta Dutta's add-to-rhythmbox.py: plugin <http://seemanta.net> 
#   2) The plugin for the Postr uploader: <http://projects.gnome.org/postr/>
#   3) Bram's blog entry:
#      http://www.bram.us/2008/01/12/my-priceless-flickr-tip-how-to-find-the-original-flickr-photo-url-and-user-from-a-static-flickr-image-url/
#
#   BLAH-BLAH-BLAH
#   ==============
#   Copyright 2010 Ciaron Linstead <http://ciaron.net>
#   
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#    
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#    
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#   MA 02110-1301, USA.

import pygtk
pygtk.require('2.0')
import gtk
import nautilus, gconf, urllib, os, sys
import webbrowser

IMAGE_TYPES = ['.jpg','.JPG','.jpeg','.JPEG']
FLICKRURL = "http://flickr.com/photo.gne?id="

def error_dialog(message, dialog_title = "Error..."):
    """The extension's error dialog"""
    dialog = gtk.MessageDialog(flags=gtk.DIALOG_MODAL,
                               type=gtk.MESSAGE_ERROR,
                               buttons=gtk.BUTTONS_OK,
                               message_format=message)
    dialog.set_title(dialog_title)
    dialog.run()
    dialog.destroy()

class FlickrMenuProvider(nautilus.MenuProvider):
    def __init__(self):
        """Creates a GConfClient (Gnome Configuration Client)"""
        self.client = gconf.client_get_default()
   
    def findflickr(self, menu, files):
        filename = urllib.unquote(files[0].get_uri()).split("/")[-1]
        fileid = filename.split("_")[0]
        url = FLICKRURL + fileid
        try:
            webbrowser.open(url)
        except:
            error_dialog("Exception Error:\n%s" % sys.exc_info())
   
    def get_file_items(self, window, files):
        """Adds the 'Find on Flickr..." menu item to the context menu
           Connects its 'activate' signal to the 'run' method passing the list of selected images
           (Currently, only the first image is handled.)
        """
        if len(files) == 0:
            return

        for file in files:
            if file.is_directory() or file.get_uri_scheme() != 'file':
                return
            if not file.is_mime_type("image/*"):
                return

        item = nautilus.MenuItem('NautilusPython::findflickr',
                                 _('Find on Flickr...'),
                                 _('Find files of this name on Flickr'))
        item.connect('activate', self.findflickr, files)

        return item,

