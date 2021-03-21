import asyncrandom
import tornado

def handle_random_int(f):
    print(f.result())

f = asyncrandom.fetch(10)
f.add_done_callback(handle_random_int)

tornado.ioloop.IOLoop.current().start()
