#!/usr/bin/python

# Copyright (c) 2011 Paul Kulyk, Paul Olszynski
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygtk
pygtk.require( "2.0" )
import gtk
import sys
import gobject
import mplayer
import os
import subprocess
import pickle
import glob


class Main:

  # Variable to store RFID reader strings
  dataString =""

  # After the combo boxes have been initialized we set them to have the same selected value
  # as during the last run
  def load_settings( self ):
    try: 
      pickle_file = open(sys.path[0] + "/settings.p",'rb')
      list_import = pickle.load(pickle_file)
      self.list_store1.clear()
      for item in list_import:
        self.list_store1.append(list(item))
      pickle_file.close()
    except:
      print "No pickle file available"

  # Pickle the settings data for use in the next run
  def save_settings( self ):
    pickle_file = open(sys.path[0] + "/settings.p",'wb')
    list_iter = self.list_store1.get_iter_root() 
    list_dump = []
    while(list_iter):
      tup = self.list_store1.get(list_iter,0,1,2)
      list_dump.append(list(tup))
      list_iter = self.list_store1.iter_next(list_iter)
    pickle.dump(list_dump,pickle_file)
    pickle_file.close()

  def progress_bar_updater(self, timer):
    # Check for an open file first
    progressBar = self.builder.get_object("progressbar")
    if ( self.mp.filename == None):
      progress = 0
      progressBar.set_text("")
      progressBar.update(0)
      return True
    #timeData = self.builder.get_object("time_label")
    #length = self.mp.length
    #timepos = self.mp.time_pos
    # This part updates the progress bas
    progress = self.mp.percent_pos
    if progress != None:
      # +1 because progress starts from 0, it would end to 99 otherwise
      progressBar.set_text("%s %%" % progress)
      progressBar.update(progress/100.0)
    #  timeData.set_text(str(timepos) + "/" + str(length))
    else:
      progress = 0
      progressBar.set_text("")
      progressBar.update(0)
      #timeData.set_text("0.00/0.00")
    # Need to return true to reset the timer
    return True

  def gtk_main_quit( self, window ):
    self.save_settings()
    self.mp.quit()
    gtk.main_quit()

  def cb_quit(self, window, event):
    print "cb_quit"
    self.save_settings()
    self.mp.quit()
    gtk.main_quit()

  def cb_about_press( self, window ):
    response = self.about_dialog.run()
    self.about_dialog.hide()
    return response != 1

  def cb_settings_press( self, window ):
    response = self.settings_dialog.run()
    self.settings_dialog.hide()
    return response != 1

  def cb_add_scan_press( self, window ):
    response        = self.add_scan_dialog.run()
    self.add_scan_dialog.hide()
    return response != 1

  def cb_add_scan_apply_clicked( self, window ):
    new_name        = self.name_entry.get_text()
    new_rfid        = self.rfid_entry.get_text()
    new_filename    = self.filechooser.get_filename()
    self.list_store1.append([new_name, new_rfid, new_filename])
    return True
    

  def cb_remove_scan_press( self, button ):
    # Obtain selection
    sel = self.tree.get_selection()
             
    # If nothing is selected, return.
    if sel.count_selected_rows == 0:
      return

    # Get selected path
    ( model, rows ) = sel.get_selected_rows()

    for row in rows:
      iter1 = model.get_iter( row )
      model.remove(iter1)

    return

  def on_key_press_event(self, widget, event):
    keyname = gtk.gdk.keyval_name(event.keyval)
    # Grab the letter q to stop the current movie
    if keyname == 'q' or keyname == 'Q':
      self.mp.stop()
    #Pause on spacebar
    if keyname == 'space':
      self.mp.pause()
    #Strings from the reader end witha new line... so we take in all characters and process the last 10 on a newline
    if keyname == 'Return':
      rfid_string_scanned = self.dataString[-10::]

      # This code aims to check if the file is already playing so we don't continually start
      # the movie over if we are on the border of one of the tags
      # Need to check this sometimes, so always call it
      current_file = self.mp.filename
      #Search for the matching rfid string and play the associated file
      # Get the tree to iterate over
      list_iter = self.list_store1.get_iter_root() 
      while(list_iter):
        rfid_entry  = self.list_store1.get_value(list_iter, 1)
        rfid_entry = rfid_entry.strip()
        if rfid_entry == rfid_string_scanned:
          filename  = self.list_store1.get_value(list_iter, 2)
          # If we are not playing a video start the one requested
          if current_file == None:
            self.play_video(filename)
            return filename
          # If this filename doesn't match the current playing one, fire it up
          elif filename.find(current_file) == -1:
            self.play_video(filename)
            return filename
          else:
            print "Not playing %s because it is already playing" % filename
            return None
        list_iter   = self.list_store1.iter_next(list_iter)
      print "ID %s is not in the list." % rfid_string_scanned
        

    else:
      self.dataString += keyname
      self.dataString = self.dataString[-10::]
      return None


  # Play video 
  def play_video( self, filename):
    print "Playing " + filename
    self.mp.loadfile("'" + filename + "'")

  # Callback for radio button
  def toggle_fs(self,widget,data=None):
    print "Fullscreen %s" % (("OFF", "ON")[widget.get_active()])
    if widget.get_active():
      self.mainWindow.fullscreen()
    else:
      self.mainWindow.unfullscreen()


  def __init__( self ):
    self.builder = gtk.Builder()
    self.builder.add_from_file(sys.path[0] + "/EDUS2.glade")
    # Add a timer and a function to update the progress bar
    self.timer = gobject.timeout_add (200, self.progress_bar_updater, self)

    self.window           = self.builder.get_object( "window1" )
    self.settings_dialog  = self.builder.get_object( "settings_dialog" )
    self.add_scan_dialog  = self.builder.get_object( "add_scan_dialog" )
    self.about_dialog     = self.builder.get_object( "aboutdialog1")
    self.tree             = self.builder.get_object( "treeview2" )
    self.list_store1      = self.builder.get_object( "treeview" )
    self.rfid_entry       = self.builder.get_object( "rfid_entry" )
    self.name_entry       = self.builder.get_object( "name_entry" )
    self.filechooser      = self.builder.get_object( "filechooserbutton1" )


    self.load_settings()

    self.builder.connect_signals( self )

    # Start mplayer up
    self.drawingarea = self.builder.get_object("drawingarea1")
    self.drawingarea.set_size_request(640,480)
    self.drawingarea.realize()
    xid = self.drawingarea.window.xid
    errorLog = open("mplayer.log", 'w')
    self.mp = mplayer.Player("-vo x11 -zoom -wid %i" % (xid), stderr=errorLog)

    self.mainWindow = self.builder.get_object("window1")

    self.mainWindow.connect("key-press-event",self.on_key_press_event)
    self.window.show_all()
    self.mainWindow.fullscreen()

if __name__ == "__main__":
  win = Main()
  win.window.show_all()
  gtk.main()
