#!/usr/bin/env python
# -*- coding: utf-8 -*-


#    Copyright (C) 2013 Carlos Cesar Caballero Diaz <ccesar@linuxmail.org>
#   
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import os
import sys
import imp
import gettext


APP_NAME = "services-manager"

LOCALE_DIR = os.path.join(sys.path[0], "locale")
gettext.install(APP_NAME, LOCALE_DIR)

ABAUT_COMMENTS = _("Services Manager, Take control of your services from the desktop.\nInpired in the Apache-Switch tool:\nhttp://apache-switch.webuda.com")

class manager:

    def __init__(self):
        
        self.set_proc_name(APP_NAME)

        #folders
        self.config_folder = os.getenv('HOME')+"/.services-manager"
        self.system_plugin_folder = sys.path[0]+"/plugins"
        self.user_plugin_folder = self.config_folder+"/plugins"
        self.plugin_folder = [self.system_plugin_folder,self.user_plugin_folder]

        #plugins main module name
        self.main_module = "__init__"

        # create folders if dont exsist
        if not os.path.exists(self.config_folder):
            os.makedirs(self.config_folder)
        if not os.path.exists(self.user_plugin_folder):
            os.makedirs(self.user_plugin_folder)

        #image files
        self.image_green = sys.path[0]+"/media/green.png"
        self.image_red = sys.path[0]+"/media/red.png"
        
        #tray declaration
        self.tray_icon = gtk.status_icon_new_from_stock(gtk.STOCK_INFO)
        self.tray_menu = gtk.Menu()       
        self.update_menu()
        self.tray_icon.connect('popup-menu', self.show_menu, self.tray_menu)
        self.tray_icon.set_tooltip("Services Manager")

    def set_proc_name(self, newname):
        """Set a system name to the python process"""
        from ctypes import cdll, byref, create_string_buffer
        libc = cdll.LoadLibrary('libc.so.6')
        buff = create_string_buffer(len(newname)+1)
        buff.value = newname
        libc.prctl(15, byref(buff), 0, 0, 0)

    def getPlugins(self):
        """obtain plugins from folders"""
        plugins = []
        for folder in self.plugin_folder:
            possibleplugins = os.listdir(folder)
            for i in possibleplugins:
                location = os.path.join(folder, i)
                if not os.path.isdir(location) or not self.main_module + ".py" in os.listdir(location):
                    continue
                info = imp.find_module(self.main_module, [location])
                plugins.append({"name": i, "info": info})
        return plugins

    def loadPlugin(self, plugin):
        return imp.load_module(self.main_module, *plugin["info"])

    def update_menu (self, *args):

        #remove menu entrys
        for i in self.tray_menu.get_children():
            self.tray_menu.remove(i)

        #load plugins
        for i in self.getPlugins():
            #print("Loading plugin " + i["name"])
            plugin = self.loadPlugin(i)
            plugin.run(self)

        
        self.tray_menu.append(gtk.SeparatorMenuItem())
        
        self.menu_refresh = gtk.ImageMenuItem(gtk.STOCK_REFRESH)
        self.menu_refresh.connect("activate", self.update_menu)
        self.tray_menu.append(self.menu_refresh)

        self.menu_about = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        self.menu_about.connect("activate", self.abaut_dialog)
        self.tray_menu.append(self.menu_about)

        self.tray_menu.append(gtk.SeparatorMenuItem())

        self.menu_quit = gtk.ImageMenuItem(gtk.STOCK_CLOSE)
        self.menu_quit.connect("activate", lambda w: gtk.main_quit())
        self.tray_menu.append(self.menu_quit)

        self.tray_menu.show_all()

    

    def show_menu(self, status_icon, button, activate_time, menu):
        menu.popup(None, None, gtk.status_icon_position_menu, button, activate_time, status_icon)

    def show_icon(self, *args ):
        self.tray_icon.set_visible(True)
        return False

    def do_response(self, dialog, response):
        if response == gtk.RESPONSE_CANCEL:
            dialog.destroy()

    def notify(self, notification):
        try:
            import pynotify            
            if pynotify.init("Services Manager"):                
                n = pynotify.Notification(notification)
                #n.set_timeout(10000)                
                n.show()
        except:
            pass

    def abaut_dialog(self, *args):
        """Show the Abaut dialog"""
        about = gtk.AboutDialog()
        about.set_name("services-manager")
        about.set_version("0.1")
        about.set_comments(ABAUT_COMMENTS)
        about.set_license("GPL v3")
        #about.set_website("")
        about.set_authors(["Carlos Cesar Caballero Diaz <ccesar@linuxmail.org>"])
        #about.set_logo(self.pixbu_logo)
        about.run()
        about.hide()
        pass

if __name__ == '__main__':
    manager()
    gtk.main()
