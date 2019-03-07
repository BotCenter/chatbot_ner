import os
import signal
import time
from functools import partial

import tornado.log
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape

from healthcheck import TornadoHandler, HealthCheck
from tornado.httpclient import AsyncHTTPClient

from tornadoserver.endpoints.ner import NerHandler

WAIT_SECONDS_BEFORE_SHUTDOWN = 2


general_log = tornado.log.gen_log
general_log.setLevel(os.environ['TORNADO_LOG_LEVEL'])
tornado.log.access_log.setLevel(os.environ['TORNADO_LOG_LEVEL'])


def sig_handler(server, sig, frame):
    io_loop = tornado.ioloop.IOLoop.current()

    def stop_loop(deadline):
        now = time.time()
        if now < deadline:
            io_loop.add_timeout(now + 1, stop_loop, deadline)
        else:
            io_loop.stop()

    def shutdown():
        general_log.warning('Caught signal: %s', sig)
        general_log.info('Stopping http server')
        server.stop()
        general_log.info(
           'Will shutdown in %s seconds...', WAIT_SECONDS_BEFORE_SHUTDOWN
        )
        stop_loop(time.time() + WAIT_SECONDS_BEFORE_SHUTDOWN)

    io_loop.add_callback_from_signal(shutdown)


def build_info():
    return {
        'SHA': os.environ['COMMIT']
    }

# TODO: Implement chatbot-ner health check


def make_app():
    health = HealthCheck()
    health.add_section('build', build_info)
    return tornado.web.Application([
        (r'/health', TornadoHandler, dict(checker=health)),
        (r'/ner', NerHandler)
    ], debug=True)


def main():

    AsyncHTTPClient.configure(None, max_clients=100)
    application = make_app()
    application.http_client = AsyncHTTPClient()
    server = tornado.httpserver.HTTPServer(application)
    port = os.environ['TORNADO_PORT']
    server.listen(port)

    signal.signal(signal.SIGTERM, partial(sig_handler, server))
    signal.signal(signal.SIGINT, partial(sig_handler, server))

    tornado.ioloop.IOLoop.current().start()
    general_log.info('Server exited.')


if __name__ == '__main__':
    main()
