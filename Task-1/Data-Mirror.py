import asyncio

class MirrorServerListener:
    def connection_made(self, transport):
        self.transport = transport

    def mirror(self, data, addr):
        msg = data.decode ()
        reversed_msg=msg[::-1]
        print('Received %r from %s, send back %r'% (msg, reversed_msg, addr))
        return bytearray(reversed_msg, 'utf-8')

    def datagram_received(self, data, addr):
        self.transport.sendto(self.mirror(data, addr), addr)

if __name__ == '__main__':
    print ("Starting UDP Mirror")
    loop = asyncio.get_event_loop()
    # here listen is a coroutine
    listen = loop.create_datagram_endpoint(
        MirrorServerListener, local_addr=('127.0.0.1', 7100))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()
