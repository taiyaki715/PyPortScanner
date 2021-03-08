import argparse
import socket
import sys
import threading


class Scanner:
    def __init__(self, target, min_port, max_port, scan_mode='t'):
        self.target = target
        self.min_port = min_port
        self.max_port = max_port

        self.scan_mode = scan_mode

        self.scan_result = []

    def run(self):
        if self.scan_mode == 't':
            target = self.tcp_scan
        elif self.scan_mode == 'u':
            target = self.udp_scan

        threads = []
        # 並列スキャン用スレッド生成
        for port in range(self.min_port, self.max_port + 1):
            thread = threading.Thread(target=target, args=(port,))
            thread.start()
            threads.append(thread)
        while True:
            if len(self.scan_result) == (self.max_port - self.min_port + 1):
                self.scan_result.sort(key=lambda x: x.port_no)
                return self.scan_result

    def tcp_scan(self, port):
        """
        指定されたポートに対してスキャンを行う
        """
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


def parse_arguments():
    """
    コマンドライン引数をパース
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('-s', '--start', type=int, default=1)
    parser.add_argument('-e', '--end', type=int, default=1000)
    parser.add_argument('-t', '--tcp', action='store_true')
    parser.add_argument('-l', '--less', action='store_true')
    parser.add_argument('-a', '--all', action='store_true')
    args = parser.parse_args()
    return args


def show_result(result, detail_mode=False):
    """
    スキャン結果の表示
    """
    print('| PROTOCOL | PORT | STATUS |')
    print('----------------------------')
    for port in result:
        if port.state == 'UP':
            color = '\033[32m'
        else:
            color = '\033[31m'

        if detail_mode or (port.state == 'UP'):
            print('|{:^10s}|{:^6d}|{:^17s}|'.format(port.protocol, port.port_no, color + port.state + '\033[0m'))


if __name__ == '__main__':
    args = parse_arguments()
    scan_mode = 't'

    # スキャン開始
    s = Scanner(args.target, args.start, args.end, scan_mode)
    print(f'Port scan for {args.target} had started.')
    res = s.run()

    # スキャン結果表示
    show_result(res, args.all)
