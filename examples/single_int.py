import asyncrandom
import tornado

def handle_random_int(f):
    print(f.result())

f = asyncrandom.fetch()
f.add_done_callback(handle_random_int)

tornado.ioloop.IOLoop.current().start()
