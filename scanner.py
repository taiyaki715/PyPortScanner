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


if __name__ == '__main__':
    s = Scanner(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    print(f'Port scan for {sys.argv[1]} had started.')
    print(f'Scanning port {sys.argv[2]} to {sys.argv[3]}')
    print('| PROTOCOL | PORT | STATUS |')
    #print('----------------------------')
    res = s.run()
    res.sort(key=lambda x: x.port_no)
    for port_info in res:
        print('|{:10s}|{:6d}|{:>8s}|'.format(port_info.protocol, port_info.port_no, port_info.state))
