# Tornado is more robust - consider using over Flask if do not need to worry about templates?

import base64
import logging
import os
import socket
import subprocess
import sys
import uuid
# from test import run

import tornado.ioloop
import tornado.options
import tornado.web
import signal

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
        output_file = open(os.path.join(STATIC_IMG_FOLDER,final_filename), 'wb')
        output_file.write(self.request.body)

        outstr = f'file {final_filename} is uploaded'
        print(outstr)

class MainHandler(tornado.web.RequestHandler):
    def get(self):  # I *think* name is the sub endpoint?
        # NOTE - if you pass self.write a dictionary, it will automatically write out
        # JSON and set the content type to JSON
        self.render("index.html")
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

    app = MainApplication(**options)
    app.run()
