#encoding=utf-8
from wsgiref.simple_server import make_server
from cgi import parse_qs
from uuid import uuid1
from datetime import datetime
import re, os


class Request(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

class Application:
    def __init__(self, routes):
        self.routes = routes
        self.layout = open('layout.html').read()
    def __call__(self, environ, start_response):
        request = Request()
        request.update({
            'path'  : environ['PATH_INFO'],
            'method': environ['REQUEST_METHOD'],
            'accept': environ['HTTP_ACCEPT'] if 'HTTP_ACCEPT' in environ else 'text/html',
            'GET'   : parse_qs(environ['QUERY_STRING']) if environ['REQUEST_METHOD'] == 'GET' else {}
        })
        raw_response = ""
        for pattern, controller in self.routes.items():
            they_match = re.match(pattern, request.path)
            print they_match
            if they_match:
                raw_response = controller(request, **they_match.groupdict())
                break
            else:
                raw_response = "No sé qué hacer con %s" % request.path
        
        if request.accept == 'text/plain':
            response = raw_response
        else:
            response = self.layout % {'content': raw_response}
        
        start_response(
              "200 OK",
              [('Content-Type', request.accept),
               ('Content-Length', str(len(response)))]
              )

        return [response]
    def serve(self):
        from wsgiref.simple_server import make_server
        daemon = make_server('127.0.0.1', 8000, self)
        daemon.serve_forever()
