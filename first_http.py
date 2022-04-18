import socket
import sys


MAX_LINE = 64*1024
MAX_HEADERS = 100


class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                # print(conn, _)
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed ', e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        try:
            print('parsing request')
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            conn.close()
            
    def parse_request(self, conn):
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        print(method, target, ver)
        headers = self.parse_headers(rfile)
        for header in headers:
            print(header)
        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')
        if host not in (self._server_name, f'{self._server_name}:{self._port}'):
            raise Exception('Not found')
        return Request(method, target, ver, headers, rfile)

    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE+1)
        if len(raw) > MAX_LINE:
            raise Exception('Request line is too long')

        words = str(raw, 'iso-8859-1').rstrip('\r\n').split()
        if len(words) != 3:
            raise Exception('Malformed request line')

        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise Exception('Unexpected HTTP version')
        return method, target, ver

    def parse_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise Exception('Header line is too long')

            if line in (b'\r\n', b'\n', b''):
                break
            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise Exception('Too many headers')
        return headers
        hdict = {}
        for header in headers:
            h = h.decode('iso-8859-1')
            k, v = h.split(':', 1)
            hdict[k] = v
        return hdict

    def handle_request(self, req):
        pass

    def send_response(self, conn, resp):
        pass

    def send_error(self, conn, err):
        pass


class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile


if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]

    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass