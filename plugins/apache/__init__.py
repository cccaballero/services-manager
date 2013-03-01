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

__plugin_name__ = "Apache"
__plugin_version__ = "0.2"


import os
import commands
import gtk
import webbrowser
import gettext

APP_NAME = "services-manager-plugin-apache"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")
gettext.install(APP_NAME, LOCALE_DIR)

APACHE_RUNNING_MESSAGE = _('Apache is running')
APACHE_STOPPED_MESSAGE = _('Apache is not running')
APACHE_TURN_OFF_MESSAGE = _('Turn Off Apache')
APACHE_TURN_ON_MESSAGE = _('Turn On Apache')
APACHE_RESTART_MESSAGE = _('Restart Apache')
PHPMYADMIN_MESSAGE = _('PhpMyAdmin')

def run(widget):
    plugin = apache_plugin(widget)
    plugin.show_apache()
    #widget.update_menu()

class apache_plugin:

    def __init__(self, widget):
        self.widget = widget

    def show_apache(self):
        if self.is_apache_installed():
            if self.is_apache_running():
                self.widget.tray_menu.append(gtk.SeparatorMenuItem())

                self.widget.tray_icon.set_from_file(self.widget.image_green)

                image = gtk.Image()
                image.set_from_file(self.widget.image_green)
                self.widget.menu_apache = gtk.ImageMenuItem(APACHE_RUNNING_MESSAGE)
                self.widget.menu_apache.set_image(image)
                self.widget.tray_menu.append(self.widget.menu_apache)

                self.widget.menu_apache_off = gtk.ImageMenuItem(APACHE_TURN_OFF_MESSAGE)
                self.widget.menu_apache_off.connect("activate", self.apache_off)
                self.widget.tray_menu.append(self.widget.menu_apache_off)

                self.widget.menu_apache_restart = gtk.ImageMenuItem(APACHE_RESTART_MESSAGE)
                self.widget.menu_apache_restart.connect("activate", self.apache_restart)
                self.widget.tray_menu.append(self.widget.menu_apache_restart)

                self.widget.tray_menu.append(gtk.SeparatorMenuItem())
                self.widget.menu_apachephpmyadmin = gtk.ImageMenuItem(PHPMYADMIN_MESSAGE)
                self.widget.menu_apachephpmyadmin.connect("activate", self.phpmyadmin)
                self.widget.tray_menu.append(self.widget.menu_apachephpmyadmin)
            else:
                self.widget.tray_menu.append(gtk.SeparatorMenuItem())

                image = gtk.Image()
                image.set_from_file(self.widget.image_red)
                self.widget.menu_apache = gtk.ImageMenuItem(APACHE_STOPPED_MESSAGE)
                self.widget.menu_apache.set_image(image)
                self.widget.tray_menu.append(self.widget.menu_apache)
                
                self.widget.menu_apache_on = gtk.ImageMenuItem(APACHE_TURN_ON_MESSAGE)
                self.widget.menu_apache_on.connect("activate", self.apache_on)
                self.widget.tray_menu.append(self.widget.menu_apache_on)
                self.widget.tray_icon.set_from_file(self.widget.image_red)

    def is_apache_installed(self, *args ):
        output = commands.getoutput("which apache2")
        if output:
            return  1
        else:
            return 0

    def is_apache_running(self, *args ):
        #output = os.system("service apache2 status")
        output = commands.getoutput("ps -e|grep apache2")
        #if output == 0:
        if output :
            return  1
        else:
            return 0
        
    def apache_on(self, *args):
        os.system("gksudo service apache2 start")
        if self.is_apache_running() == 1:
            self.widget.update_menu()
            self.notify_apache_running()
        else:
            self.notify_apache_stopped()
        
    def apache_off(self, *args):
        os.system("gksudo service apache2 stop")
        if self.is_apache_running() == 0:
            self.widget.update_menu()
            self.notify_apache_stopped()
        else:
            self.notify_apache_running()

    def apache_restart(self, *args):
        os.system("gksudo service apache2 restart")
        self.widget.update_menu()
        if self.is_apache_running() == 1:
            self.notify_apache_running()
        else:
            self.notify_apache_stopped()


    def phpmyadmin(self, *args ):
        new = 2 # open in a new tab, if possible
        url = "http://localhost/phpmyadmin/"
        webbrowser.open(url,new=new)

    def notify_apache_running(self):
        self.widget.notify(APACHE_RUNNING_MESSAGE)

    def notify_apache_stopped(self):
        self.widget.notify(APACHE_STOPPED_MESSAGE)

