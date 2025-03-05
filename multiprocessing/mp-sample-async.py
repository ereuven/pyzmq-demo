import asyncio
import zmq
import zmq.asyncio
from multiprocessing import Process
import time

zmqpath = "ipc:///tmp/fake_scok_test"

def parent():
    async_loop = asyncio.new_event_loop()
    ctx = zmq.asyncio.Context()
    sock = ctx.socket(zmq.PAIR, io_loop=async_loop)
    sock.bind(zmqpath)
    proc = Process(target=child)
    proc.start()

    async_loop.create_task(parentloop(sock))
    async_loop.run_forever()

async def parentloop(sock):
    while True:
        msg = b"test"
        await sock.send(msg)
        print(f"sent {msg}")
        await asyncio.sleep(1)

def child():
    child_async_loop = asyncio.new_event_loop()
    ctx = zmq.asyncio.Context()
    sock = ctx.socket(zmq.PAIR, io_loop=child_async_loop)
    sock.connect(zmqpath)
    print("child")

    child_async_loop.create_task(childloop(sock))
    child_async_loop.run_forever()

async def childloop(sock):
    while True:
        msg = await sock.recv()
        print(f"recv {msg}")

parent()