#!/usr/bin/env python
import os.path, os, sys
from urlparse import urlparse
from datetime import datetime, date, time
from time import sleep
import json
import logging
import pprint
from pprint import pformat

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.web
import unicodedata


# import and define tornado-y things
from tornado.options import define, options
define("port", default=5000, help="run on the given port", type=int)

# application settings and handle mapping info
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/([^/]+)?", MainHandler)
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
	pass

# the main page
class MainHandler(BaseHandler):
	@tornado.web.asynchronous
	def get(self, q):
		url = 'http://search.twitter.com/search.json?q=coffee&amp;rpp=5&amp;include_entities=true&amp;result_type=mixed'
		http = tornado.httpclient.AsyncHTTPClient()
		http.fetch(url, self._on_fetch)

	def _on_fetch(self, response):
		# render it up!
		body = json.loads(response.body)
		pp = pprint.PrettyPrinter(indent=4)
		pp_body = pformat(body)


		self.render(
			"main.html",
			body = body,
			pp = pp,
			pp_body = pp_body
		)		
		self.finish()

# RAMMING SPEEEEEEED!
def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)

	# start it up
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()
