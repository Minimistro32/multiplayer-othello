from random import randint
import socket
import selectors
import types
import board

# BOARD EXTENSION FOR SERVER FUNCTIONALITY
class Board(board.Board):
    def __init__(self, size):
        super().__init__(size)
        self.was_sent = False
        self.players = []

    def play(self, row, col):
        super().play(row, col)
        self.was_sent = False

    def getDisplayAsBinary(self):
        return self.getDisplay().encode('utf-8')

# SERVER GLOBALS
HOST = '127.0.0.1'
PORT = randint(61000, 65999)
sel = selectors.DefaultSelector()

# OTHELLO GLOBALS
board = Board(8)


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    board.players.append(addr)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            cursor = str(recv_data, 'utf-8')
            print("recieved data: ", cursor)
            board.play(int(cursor[0]), int(cursor[-1]))
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not board.was_sent:
            data.outb += board.getDisplayAsBinary()
            board.was_sent = True
        if data.outb:
            print('sending board to', data.addr)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


# MAIN
# configure listening socket
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print('listening on', (HOST, PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True and not board.isFull():
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                if len(board.players) < 2:  # max is two clients
                    accept_wrapper(key.fileobj)
            else:
                if len(board.players) == 2:
                    if key.data.addr == board.players[board.getCurrentPlayer()]:
                        service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()