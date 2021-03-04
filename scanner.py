import socket
import sys
import threading


class Scanner:
    def __init__(self, target,
                 min_port=1, max_port=1000):
        self.target = target
        self.min_port = min_port
        self.max_port = max_port + 1

        self.scan_result = []

    def run(self):
        threads = []
        for port in range(self.min_port, self.max_port):
            thread = threading.Thread(target=self.scan, args=(port,))
            thread.start()
            threads.append(thread)
        while True:
            if len(self.scan_result) == (self.max_port - self.min_port):
                return self.scan_result

    def scan(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            res = s.connect_ex((self.target, port))
        if res == 0:
            self.scan_result.append(PortInfo(port, 'TCP', 'UP'))
        else:
            self.scan_result.append(PortInfo(port, 'TCP', 'DOWN'))


class PortInfo:
    def __init__(self, port_no, protocol, state):
        self.port_no = port_no
        self.protocol = protocol
        self.state = state


def show_result(result):
    print('| PROTOCOL | PORT | STATUS |')
    print('----------------------------')
    result.sort(key=lambda x: x.port_no)
    for port in result:
        if port.state == 'UP':
            color = '\033[32m'
        else:
            color = '\033[31m'

        print('|{:^10s}|{:^6d}|{:^17s}|'.format(port.protocol, port.port_no, color + port.state + '\033[0m'))


if __name__ == '__main__':
    s = Scanner(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    print(f'Port scan for {sys.argv[1]} had started.')
    res = s.run()
    show_result(res)
