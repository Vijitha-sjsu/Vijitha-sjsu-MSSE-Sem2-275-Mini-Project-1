import asyncio
from basic.payload import builder
import gc
from guppy import hpy

class AsyncBasicServer:
    def __init__(self, ipaddr, port=2000):
        self.ipaddr = ipaddr
        self.port = port

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connection from {addr}")

        while True:
            data = await reader.read(2048)
            if not data:
                break  # No data means the client closed the connection

            # Process the data
            bldr = builder.BasicBuilder()
            name, group, text = bldr.decode(data.decode())
            response = f"Received: {text}"
            print(f"from {name}, to group: {group}, text: {text}")

            # Send a response back to the client
            writer.write(response.encode())
            await writer.drain()  # Make sure the data is sent

        print(f"Closing connection from {addr}")
        writer.close()
        await writer.wait_closed()

    async def run_server(self):
        server = await asyncio.start_server(
            self.handle_client, self.ipaddr, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    ip = "127.0.0.1"
    port = 2000

    # Initialize Guppy's heap inspector
    h = hpy()
    gc.set_debug(gc.DEBUG_STATS)

    server = AsyncBasicServer(ip, port)
    asyncio.run(server.run_server())

    # Profiling and GC stats are handled differently with asyncio;
    # consider using specific tools designed for asynchronous profiling.
