class Data:
    __slots__ = ("data", "ip")

    def __init__(self, data: str, ip: int):
        self.data = data
        self.ip = ip

    def __str__(self):
        return f"{self.data} ({self.ip})"


class ServerError(Exception): ...


class Server:

    __slots__ = ("ip", "buffer", "connected_router")
    _base_ip_address: int = 1

    def __init__(self):
        self.ip: int = Server._base_ip_address
        self.buffer: list[Data] = []
        self.connected_router: Router | None = None

        Server._base_ip_address += 1

    def get_ip(self) -> int:
        """Shows servers ip address.

        :return: ip address
        :rtype: int
        """
        return self.ip

    def get_data(self) -> list[Data]:
        """Accepts data in a list and flushes buffer.

        :return: recieved data
        :rtype: list[Data]
        """
        escaped_buffer = self.buffer
        self.buffer = []
        return escaped_buffer

    def send_data(self, data: Data):
        """Sends packet to connected router.

        :param data: packet to send
        :type data: Data
        :raises ServerError: server is disconnected from any router
        """
        if not self.connected_router:
            raise ServerError("no router available")
        self.connected_router.buffer.append(data)


class Router:

    __slots__ = ("buffer", "mapped_servers")
    def __init__(self):
        self.buffer: list[Data] = []
        self.mapped_servers: dict[int, Server] = {}

    def link(self, server: Server):
        """Connects server to a router.

        :param server: server to connect
        :type server: Server
        """
        server.connected_router = self
        self.mapped_servers[server.get_ip()] = server

    def unlink(self, server: Server):
        """Disconnects server from a router.

        :param server: server to disconnect
        :type server: Server
        """
        server.connected_router = None
        self.mapped_servers.pop(server.get_ip(), None)

    def send_data(self):
        """Scatters all packets from buffer to the corresponding server.

        Buffer would be flushed afrer every packet is sent.
        """
        for packet in self.buffer:
            self.mapped_servers[packet.ip].buffer.append(packet)
        self.buffer = []
