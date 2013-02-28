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

__plugin_name__ = "Mysql"
__plugin_version__ = "0.2"


import os
import commands
import gtk
import gettext

APP_NAME = "services-manager-plugin-mysql"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")
gettext.install(APP_NAME, LOCALE_DIR)

MYSQL_RUNNING_MESSAGE = _('Mysql is running')
MYSQL_STOPPED_MESSAGE = _('Mysql is not running')
MYSQL_TURN_OFF_MESSAGE = _('Turn Off Mysql')
MYSQL_TURN_ON_MESSAGE = _('Turn On Mysql')
MYSQL_RESTART_MESSAGE = _('Restart Mysql')

def run(widget):
    plugin = mysql_plugin(widget)
    plugin.show_mysql()
    #widget.update_menu()

class mysql_plugin:

    def __init__(self, widget):
        self.widget = widget

    def show_mysql(self):
    	if self.is_mysql_installed():
	        if self.is_mysql_running():
	            self.widget.tray_menu.append(gtk.SeparatorMenuItem())

	            image = gtk.Image()
	            image.set_from_file(self.widget.image_green)
	            self.widget.menu_mysql = gtk.ImageMenuItem(MYSQL_RUNNING_MESSAGE)
	            self.widget.menu_mysql.set_image(image)
	            self.widget.tray_menu.append(self.widget.menu_mysql)

	            self.widget.menu_mysql_off = gtk.ImageMenuItem(MYSQL_TURN_OFF_MESSAGE)
	            self.widget.menu_mysql_off.connect("activate", self.mysql_off)
	            self.widget.tray_menu.append(self.widget.menu_mysql_off)

	            self.widget.menu_mysql_restart = gtk.ImageMenuItem(MYSQL_RESTART_MESSAGE)
	            self.widget.menu_mysql_restart.connect("activate", self.mysql_restart)
	            self.widget.tray_menu.append(self.widget.menu_mysql_restart)
	        else:
	            self.widget.tray_menu.append(gtk.SeparatorMenuItem())

	            image = gtk.Image()
	            image.set_from_file(self.widget.image_red)
	            self.widget.menu_mysql = gtk.ImageMenuItem(MYSQL_STOPPED_MESSAGE)
	            self.widget.menu_mysql.set_image(image)
	            self.widget.tray_menu.append(self.widget.menu_mysql)

	            self.widget.menu_mysql_on = gtk.ImageMenuItem(MYSQL_TURN_ON_MESSAGE)
	            self.widget.menu_mysql_on.connect("activate", self.mysql_on)
	            self.widget.tray_menu.append(self.widget.menu_mysql_on)

    def is_mysql_installed(self, *args ):
        output = commands.getoutput("which mysqld")
        if output:
            return  1
        else:
            return 0

    def is_mysql_running(self, *args ):
        #output = os.system("service mysql status")
        output = commands.getoutput("ps -e|grep mysqld")
        #if output == 0:
        if output:
            return  1
        else:
            return 0

    def mysql_on(self, *args):
        os.system("gksudo service mysql start")
        if self.is_mysql_running() == 1:
            self.widget.update_menu()
            self.notify_mysql_running()
        else:
            self.notify_mysql_stopped()
        
    def mysql_off(self,*args):
        os.system("gksudo service mysql stop")
        if self.is_mysql_running() == 0:
            self.widget.update_menu()
            self.notify_mysql_stopped()
        else:
            self.notify_mysql_running()

    def mysql_restart(self,*args):
        os.system("gksudo service mysql restart")
        self.widget.update_menu()
        if self.is_mysql_running() == 1:
            self.notify_mysql_running()
        else:
            self.notify_mysql_stopped()

    def notify_mysql_running(self):
        self.widget.notify(MYSQL_RUNNING_MESSAGE)

    def notify_mysql_stopped(self):
        self.widget.notify(MYSQL_STOPPED_MESSAGE)