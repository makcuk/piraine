#!/usr/bin/env python2.7
import time
import cherrypy
from cherrypy.process.plugins import Monitor
import os.path
from timetable import Table

class WebInterface(object):
        @cherrypy.expose
        def index(self):
            return file("index.html")

        @cherrypy.expose
        def zones(self):
            return table.zone_states()

if __name__ == "__main__":
    table = Table()
    conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': './'
         },

         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': os.getcwd()+'/public'
         }
     }
    cherrypy.server.socket_host = '0.0.0.0'

    Monitor(cherrypy.engine, table.current, frequency=60).subscribe()
    cherrypy.quickstart(WebInterface(), '/', conf)
