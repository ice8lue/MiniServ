MiniServ v0.2.0.0
=================

MiniServ binds itself to specified port (configurable inside of settings.ini) for all network interfaces.
Start it inside a console using: start_server.bat

There is a service console, startable by typing (into another console): service_console.bat

Copy your HTML[,...] -Files into the 'htdocs'-Directory.

Feature list (so far):
	- basic Webserver functions (receives Request, sends answer, including correct date 
	  and filesize and transfers the website (at this time as a whole package))
	- prints connection information to the server console
	- basic administration commands available at the service console
	- little 'easteregg'^^
	- uses 'htdocs' directory
	- sub-directories work
	- possibility to control ammount of logging information
	- possibility (and force) to connect to a server on an user-input-based IP
	- basic login authentification on client/server
	- FINALLY: Images, JS and XML work, basic AJAX too
	- new console command: check update -- checks the website for updated MiniServ builds
	- first-use setup to configure the login information

ToDo:
	- secure login
	
