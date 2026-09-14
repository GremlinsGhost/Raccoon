"""Wayland-protokollan perusta: header, send, recv, bufferointi.

Tämä moduuli ei tiedä mistään Wayland-olioista (wl_surface, wl_shm jne.)
Se tietää vain:
  - Miten viestit paketoidaan (8 tavun header + payload)
  - Miten ne lähetetään socketin yli (send / sendmsg fd n kanssa)
  - Miten vastaanotettu tavuvirta jaetaan kokonaisiksi viesteiksi
"""

import socket
import struct
import select
import array


class Wire:
    def __init__(self, socket_path):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(socket_path)
        self._recv_buf = b""
        self.closed = False

    def send(self, obj_id, opcode, payload=b""):
        length = 8 + len(payload)
        header = struct.pack("IHH", obj_id, opcode, length)
        self.sock.sendall(header + payload)

    def send_with_fd(self, obj_id, opcode, payload, fd):
        length = 8 + len(payload)
        header = struct.pack("IHH", obj_id, opcode, length)
        msg = header + payload
        fds = array.array("i", [fd])
        self.sock.sendmsg(
            [msg],
            [(socket.SOL_SOCKET, socket.SCM_RIGHTS, fds)]
        )

    def recv_available(self, timeout=0.01):
        r, _, _ = select.select([self.sock], [], [], timeout)
        if not r:
            return False
        chunk = self.sock.recv(65536)
        if not chunk:
            self.closed = True
            return False
        self._recv_buf += chunk
        return True

    def drain(self):
        while len(self._recv_buf) >= 8:
            obj_id, opcode, length = struct.unpack("IHH", self._recv_buf[:8])

            if length < 8:
                self._recv_buf = b""
                return

            if len(self._recv_buf) < length:
                return

            payload = self._recv_buf[8:length]
            self._recv_buf = self._recv_buf[length:]

            yield obj_id, opcode, payload

    def close(self):
        self.closed = True
        try:
            self.sock.close()
        except OSError:
            pass