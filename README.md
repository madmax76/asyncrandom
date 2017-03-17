Asyncrandom
===========

Utility for fetching one more more random numbers from the 
ANU Quantum Random Numbers Server by calling the endpoint at
https://qrng.anu.edu.au/API/jsonI.php. 
Requests are executed asynchronously using the tornado networking framework.

More information about how the numbers are generated can be found on https://qrng.anu.edu.au/.

Requires tornado and its IOLoop to run.

Usage
-----

A simple example of generating a single random ``uint8``:

    def handle_random_int(f):
        print(f.result())

    f = asyncrandom.fetch()
    f.add_done_callback(handle_random_int)

    tornado.ioloop.IOLoop.current().start()

Multiple numbers can be generated as well. In this example we generate 10:

    def handle_random_int(f):
        print(f.result())

    f = asyncrandom.fetch(10)
    f.add_done_callback(handle_random_int)

    tornado.ioloop.IOLoop.current().start()

By default 8-bit unsigned integers are generated. Optionally, this can be
changed to 16-bit. Example of generating 10 16-bit integers:

    def handle_random_int(f):
        print(f.result())

    f = asyncrandom.fetch(10, asyncrandom.IntegerType.UINT16)
    f.add_done_callback(handle_random_int)

    tornado.ioloop.IOLoop.current().start()


If called from the command issues a request with ``length`` set to 1, and ``type`` set to ``"uint8"``, printing a single random int with a max value of 255. In this case, the call is synchronous.

Command line example:
        $ asyncrandom --int-type=uint8 --length=1
        105

