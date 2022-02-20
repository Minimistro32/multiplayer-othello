import socket
import selectors
import types

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 61530        # The port used by the server
sel = selectors.DefaultSelector()
shouldPlay = False
cursor = []


def start_connection(host, port):
    server_addr = (host, port)
    print('starting connection to', server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(outb=b'')
    sel.register(sock, events, data=data)


def service_connection(key, mask):
    global shouldPlay
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print(str(recv_data, 'utf-8'))
            shouldPlay = True
        if not recv_data:
            print('closing connection')
            sel.unregister(sock)
            sock.close()

    if shouldPlay:
        cursor.append(int(input("Pick a row: ")))
        cursor.append(int(input("Pick a col: ")))
        shouldPlay = False

    if mask & selectors.EVENT_WRITE:
        if not data.outb and cursor:
            data.outb = f"{cursor[0]}:{cursor[1]}".encode('utf-8')
            cursor.clear()
        if data.outb:
            print('sending', repr(data.outb), 'to connection')
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

start_connection(HOST, PORT)

try:
    while True:
        events=sel.select(timeout = 1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()