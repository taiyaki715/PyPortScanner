import socket
import sys


class Scanner:
    def __init__(self, target,
                 min_port=1, max_port=1000):
        self.target = target
        self.min_port = min_port
        self.max_port = max_port

    def scan(self):
        open_ports = []
        for port in range(self.min_port, self.max_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                res = s.connect_ex((self.target, port))
            if res == 0:
                open_ports.append(PortInfo(port, 'tcp', 'UP'))
            else:
                open_ports.append(PortInfo(port, 'tcp', 'DOWN'))
        return open_ports


class PortInfo:
    def __init__(self, port_no, protocol, state):
        self.port_no = port_no
        self.protocol = protocol
        self.state = state


if __name__ == '__main__':
    s = Scanner(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    res = s.scan()
    for port_info in res:
        print(f'{port_info.protocol}/{port_info.port_no} is {port_info.state}')
