import socket
import time
import binascii

time.sleep(2)

class Switchc:
    def __init__(self, ip):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, 6000))

    def sendCommand(self, content):
        content += '\r\n' #important for the parser on the switch side
        self.s.sendall(content.encode())

    def sendLstick(self, direction):
        if direction == "up":
            self.sendCommand("setStick LEFT 0x0000 0x7FFF")
            time.sleep(1)
            self.sendCommand("setStick LEFT 0x0000 0x0000")

        elif direction == "left":
            self.sendCommand("setStick LEFT -0x8000 0x0000")
            time.sleep(1)
            self.sendCommand("setStick LEFT 0x0000 0x0000")
        
        elif direction == "down":
            self.sendCommand("setStick LEFT 0x0000 -0x8000")
            time.sleep(1)
            self.sendCommand("setStick LEFT 0x0000 0x0000")

        elif direction == "right":
            self.sendCommand("setStick LEFT 0x7FFF 0x0000")
            time.sleep(1)
            self.sendCommand("setStick LEFT 0x0000 0x0000")

if __name__ == "__main__":
    s = Switchc("192.168.178.37")
    s.sendLstick("up")