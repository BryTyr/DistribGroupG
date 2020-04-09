from Middleware.MessageHandler.MessageHandler import MessageHandler
import socket
import struct
import sys

class ConnectionSystem:

    messageHandler = ""
    IPAddress = ""
    Port = ""


    # default constructor
    def __init__(self,UserID):
        self.messageHandler = MessageHandler(self,UserID)


    def SendMessage(self, message):
        multicast_group = ('224.3.29.71', 10000)

        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        sock.settimeout(0.5)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        try:

            # Send data to the multicast group
            print (sys.stderr, 'sending "%s"' % message)
            sent = sock.sendto(message.encode(encoding='UTF-8',errors='strict'), multicast_group)

            # Look for responses from all recipients
            while True:
                print (sys.stderr, 'waiting to receive')
                try:
                    data, server = sock.recvfrom(160)
                except socket.timeout:
                    print (sys.stderr, 'timed out, no more responses')
                    break
                else:
                    print (sys.stderr, 'received "%s" from %s' % (data, server))
                    return data.decode(encoding="utf-8", errors="strict")


        finally:
            print(sys.stderr, 'closing socket')
            sock.close()


    def ReceiveMessages(self):

        multicast_group = '224.3.29.71'
        server_address = ('', 10000)
        #server_address = ("", self.Port)
        # Create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #sock.setsockopt(socket.SO_REUSEPORT)
        # Bind to the server address
        #sock.bind(server_address)

        # #settimeout
        # sock.settimeout(0.5)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
        sock.setblocking(0)
        sock.settimeout(4.5)

        sock.bind(server_address)

        # Receive/respond loop

        while True:
            print (sys.stderr, '\nwaiting to receive message')
            try:
                data, address = sock.recvfrom(1024)

                print (sys.stderr, 'received %s bytes from %s' % (len(data.decode(encoding="utf-8", errors="strict")), address))
                print (sys.stderr, data.decode(encoding="utf-8", errors="strict"))

                self.messageHandler.handleMessage(data.decode(encoding="utf-8", errors="strict"))

                #print("Response is: "+data.decode(encoding="utf-8", errors="strict"))

                # print (sys.stderr, 'sending acknowledgement to', address)
                # sock.sendto(response.encode(encoding="UTF-8",errors="strict"), address)


            except Exception as e:
                if e =="timed out":
                    print("Check for user Input")
                else:
                    print(e)
