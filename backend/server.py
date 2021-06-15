# Tornado is more robust - consider using over Flask if do not need to worry about templates?

import base64
import logging
import os
import socket
import subprocess
import sys
import uuid
# from test import run

import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web
import signal

from backend import trained_network_init, predict
from mysql_client import match_herb

import urllib
import numpy as np

verbose = ((sys.argv[1] if 1 < len(sys.argv) else "")=="verbose")

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
STATIC_IMG_FOLDER = os.path.join( os.path.dirname(__file__), "img")

def parse_static_filepath(filepath):
    split_filepath = filepath.split('/')
    while len(split_filepath) > 2:
        split_filepath.pop(0)

    return '/'.join(split_filepath)

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        original_fname = 'tmp_img'

        final_filename = original_fname + '.jpg'
        output_path = os.path.join(STATIC_IMG_FOLDER,final_filename)
        output_file = open(output_path, 'wb')
        output_file.write(self.request.body)

        classProbs = predict(output_path)
        class1st = np.argmax(classProbs)
        class1st_prob = classProbs[0,class1st] * 100
        class1st_prob = np.round(class1st_prob, decimals=2)
        classProbs[0,class1st] = 0

        class2nd = np.argmax(classProbs)
        class2nd_prob = classProbs[0,class2nd] * 100
        class2nd_prob = np.round(class2nd_prob, decimals=2)
        classProbs[0,class2nd] = 0

        class3rd = np.argmax(classProbs)
        class3rd_prob = classProbs[0,class3rd] * 100
        class3rd_prob = np.round(class3rd_prob, decimals=2)

        class1st += 1 # this starts from 0 while mysql starts from 1
        class2nd += 1
        class3rd += 1

        matched1st = match_herb(int(class1st))
        matched2nd = match_herb(int(class2nd))
        matched3rd = match_herb(int(class3rd))

        matched1st['prob'] = float(class1st_prob)
        matched1st['2nd'] = matched2nd['name']
        matched1st['3rd'] = matched3rd['name']
        matched1st['2nd_prob'] = float(class2nd_prob)
        matched1st['3rd_prob'] = float(class3rd_prob)

        self.finish(matched1st)

class MainHandler(tornado.web.RequestHandler):
    def get(self):  # I *think* name is the sub endpoint?
        # NOTE - if you pass self.write a dictionary, it will automatically write out
        # JSON and set the content type to JSON
        self.render("index.html", herbInfo = "Loại thảo dược")
        # Other methods: self.redirect, self.get_argument, self.request.body,

class StaticFileHandler_NoCache(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

class MainApplication(tornado.web.Application):
    is_closing = False

    def signal_handler(self, signum, frame):
        logging.info('exiting...')
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            tornado.ioloop.IOLoop.instance().stop()
            logging.info('exit success')

    def __init__(self, **settings):
        tornado.web.Application.__init__(self, **settings)
        # Add in various member variables here that you want the handlers to be aware of
        # e.g. a database client

        # Add the handlers here - use regular expressions or hardcoded paths to link the endpoints
        # with handlers?
        self.port = settings.get('port', 25842)
        self.address = settings.get('address', "0.0.0.0")
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.logger = logging.getLogger()

        # Tie the handlers to the routes here
        self.add_handlers(".*", [
            (r"/", MainHandler),
            (r"/upload", UploadHandler),
            (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": STATIC_IMG_FOLDER}),
            (r".*/static/(.*)", StaticFileHandler_NoCache, {"path": STATIC_FOLDER})
        ])

    def run(self):
        try:
            signal.signal(signal.SIGINT, self.signal_handler)
            self.listen(self.port, self.address)
            tornado.ioloop.PeriodicCallback(self.try_exit, 100).start()

        except socket.error as e:
            self.logger.fatal("Unable to listen on {}:{} = {}".format(
                self.address, self.port, e))
            sys.exit(1)
        self.ioloop.start()


if __name__ == "__main__":

    tornado.options.define(
        "debug",
        default=False,
        help="Enable debugging mode."
    )
    tornado.options.define('port', default=25842, help='Port to listen on.')

    host = "0.0.0.0"
    if sys.platform == "win32":
        host = "127.0.0.1"
    tornado.options.define('address', default=host, help='Url')

    tornado.options.define('template_path', default=os.path.join(
        os.path.dirname(__file__), "templates"), help='Path to templates')

    tornado.options.parse_command_line()

    options = tornado.options.options.as_dict()

    if verbose:
        print(options)

    trained_network_init()

    app = MainApplication(**options)
    app.run()
