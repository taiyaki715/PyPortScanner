import argparse
import socket
import sys
import threading


class Scanner:
    def __init__(self, target, min_port, max_port):
        self.target = target
        self.min_port = min_port
        self.max_port = max_port + 1

        self.scan_result = []

    def run(self):
        threads = []
        for port in range(self.min_port, self.max_port):
            thread = threading.Thread(target=self.tcp_scan, args=(port,))
            thread.start()
            threads.append(thread)
        while True:
            if len(self.scan_result) == (self.max_port - self.min_port):
                return self.scan_result

    def tcp_scan(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            res = s.connect_ex((self.target, port))
        if res == 0:
            self.scan_result.append(PortInfo(port, 'TCP', 'UP'))
        else:
            self.scan_result.append(PortInfo(port, 'TCP', 'DOWN'))

    def udp_scan(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            res = s.connect_ex((self.target, port))
        if res == 0:
            self.scan_result.append(PortInfo(port, 'UDP', 'UP'))
        else:
            self.scan_result.append(PortInfo(port, 'UDP', 'DOWN'))


class PortInfo:
    def __init__(self, port_no, protocol, state):
        self.port_no = port_no
        self.protocol = protocol
        self.state = state


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('-s', '--start', type=int, default=1)
    parser.add_argument('-e', '--end', type=int, default=1000)
    parser.add_argument('-u', '--udp', action='store_true')
    args = parser.parse_args()
    return args


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
    args = parse_arguments()
    s = Scanner(args.target, args.start, args.end)
    print(f'Port scan for {args.target} had started.')
    res = s.run()
    show_result(res)
