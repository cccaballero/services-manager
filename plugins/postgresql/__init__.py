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

__plugin_name__ = "Postgresql"
__plugin_version__ = "0.2"


import os
import commands
import gtk
import gettext

APP_NAME = "services-manager-plugin-postgresql"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")
gettext.install(APP_NAME, LOCALE_DIR)

POSTGRESQL_RUNNING_MESSAGE = _('Postgresql is running')
POSTGRESQL_STOPPED_MESSAGE = _('Postgresql is not running')
POSTGRESQL_TURN_OFF_MESSAGE = _('Turn Off Postgresql')
POSTGRESQL_TURN_ON_MESSAGE = _('Turn On Postgresql')
POSTGRESQL_RESTART_MESSAGE = _('Restart Postgresql')

def run(widget):
    plugin = postgresql_plugin(widget)
    plugin.show_postgresql()
    #widget.update_menu()

class postgresql_plugin:

    def __init__(self, widget):
        self.widget = widget

    def show_postgresql(self):
        if self.is_postgresql_installed():
            if self.is_postgresql_running():
                self.widget.tray_menu.append(gtk.SeparatorMenuItem())

                image = gtk.Image()
                #image.set_from_file(self.widget.image_green)
                image.set_from_stock(gtk.STOCK_EXECUTE, gtk.ICON_SIZE_MENU)
                self.widget.menu_postgresql = gtk.ImageMenuItem(POSTGRESQL_RUNNING_MESSAGE)
                self.widget.menu_postgresql.set_image(image)
                self.widget.tray_menu.append(self.widget.menu_postgresql)

                self.widget.menu_postgresql_off = gtk.ImageMenuItem(POSTGRESQL_TURN_OFF_MESSAGE)
                self.widget.menu_postgresql_off.connect("activate", self.postgresql_off)
                self.widget.tray_menu.append(self.widget.menu_postgresql_off)

                self.widget.menu_postgresql_restart = gtk.ImageMenuItem(POSTGRESQL_RESTART_MESSAGE)
                self.widget.menu_postgresql_restart.connect("activate", self.postgresql_restart)
                self.widget.tray_menu.append(self.widget.menu_postgresql_restart)
            else:
                self.widget.tray_menu.append(gtk.SeparatorMenuItem())

                image = gtk.Image()
                #image.set_from_file(self.widget.image_red)
                image.set_from_stock(gtk.STOCK_STOP, gtk.ICON_SIZE_MENU)
                self.widget.menu_postgresql = gtk.ImageMenuItem(POSTGRESQL_STOPPED_MESSAGE)
                self.widget.menu_postgresql.set_image(image)
                self.widget.tray_menu.append(self.widget.menu_postgresql)

                self.widget.menu_postgresql_on = gtk.ImageMenuItem(POSTGRESQL_TURN_ON_MESSAGE)
                self.widget.menu_postgresql_on.connect("activate", self.postgresql_on)
                self.widget.tray_menu.append(self.widget.menu_postgresql_on)

    def is_postgresql_installed(self, *args ):
        if os.path.exists("/etc/init.d/postgresql"):
            return  1
        else:
            return 0

    def is_postgresql_running(self, *args ):
        output = commands.getoutput("ps -e|grep postgres")
        if output:
            return  1
        else:
            return 0

    def postgresql_on(self, *args):
        os.system("gksudo service postgresql start")
        if self.is_postgresql_running() == 1:
            self.widget.update_menu()
            self.notify_postgresql_running()
        else:
            self.notify_postgresql_stopped()
        
    def postgresql_off(self,*args):
        os.system("gksudo service postgresql stop")
        if self.is_postgresql_running() == 0:
            self.widget.update_menu()
            self.notify_postgresql_stopped()
        else:
            self.notify_postgresql_running()

    def postgresql_restart(self,*args):
        os.system("gksudo service postgresql restart")
        self.widget.update_menu()
        if self.is_postgresql_running() == 1:
            self.notify_postgresql_running()
        else:
            self.notify_postgresql_stopped()

    def notify_postgresql_running(self):
        self.widget.notify(POSTGRESQL_RUNNING_MESSAGE)

    def notify_postgresql_stopped(self):
        self.widget.notify(POSTGRESQL_STOPPED_MESSAGE)