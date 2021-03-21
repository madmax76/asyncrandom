.. image:: https://travis-ci.org/YavorPaunov/asyncrandom.svg?branch=master
    :target: https://travis-ci.org/YavorPaunov/asyncrandom

Asyncrandom
===========

Utility for fetching one or more random numbers from the ANU Quantum Random Numbers Server by calling the endpoint at https://qrng.anu.edu.au/API/jsonI.php. 
Requests are executed asynchronously using the tornado networking framework.

More information about how the numbers are generated can be found on https://qrng.anu.edu.au/.

Requires tornado and its IOLoop to run.

Installation
------------
Download the source and run the setup file::

    python setup.py install

Usage
-----

A simple example of generating a single random ``uint8``::

    def handle_random_int(f):
        print(f.result())

    f = asyncrandom.fetch()
    f.add_done_callback(handle_random_int)

    tornado.ioloop.IOLoop.current().start()

Multiple numbers can be generated as well. In this example we generate 10::

    def handle_random_int(f):
        print(f.result())

    f = asyncrandom.fetch(10)
    f.add_done_callback(handle_random_int)

    tornado.ioloop.IOLoop.current().start()

By default, 8-bit unsigned integers are generated. Optionally, this can be changed to 16-bit. Example of generating 10 16-bit integers::
    
    def handle_random_int(f):
        print(f.result())
    
    f = asyncrandom.fetch(10, asyncrandom.IntegerType.UINT16)
    f.add_done_callback(handle_random_int)
    
    tornado.ioloop.IOLoop.current().start()


The size of the number to be generated can be specified. In this example we generate a HEX-16 number with a size of 512::

    def handle_random_int(f):
        print(f.result())
    
    f = asyncrandom.fetch(1, asyncrandom.IntegerType.HEX16, 512)
    f.add_done_callback(handle_random_int)
    
    tornado.ioloop.IOLoop.current().start()

If called from the command, issues a synchronous call to the service. Optionally, ``--length``, ``--size`` and ``--type`` can be specified as arguments, with default values of ``1`` and ``"uint-8"`` respectively. 


Command line example::

    $ asyncrandom --int-type=hex16 --length=1 --size=32
    94057bbadaa28fb066da8b1df1fb1306bbd55551f7bb631ff3b527b6a83f1856

