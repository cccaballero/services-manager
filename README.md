services-manager
================

<b>Control tool for services</b>

![services-manager snapshoot](http://s21.postimage.org/hump3izlj/image.png)

Is an application that allows control services such as Apache and MySQL from the system notification area, the purpose of it is to achieve similar functionality to the control panel of XAMPP in the Linux desktop.

<b>Features:</b>

* Written in Python using the GTK 2 libraries.
* Extensible with plugins.
* Apache Plugin:
    - Start, stop and restart Apache.
    - Enable and disable Apache modules.
    - Start Phpmyadmin in the browser.
* Mysql plugin:
    - Start, stop and restart Mysql server.
* Postgresql plugin:
    - Start, stop and restart Postgresql server.

<b>Plugins:</b>

Services Manager has a simple plugin system, which can extend its functionality by adding new services. The plugins are located in the ".services-manager" folder at the user home, and in the "plugins" folder of the application. With only a few modifications to the existing plug-ins can be created new ones with basic support for other services.