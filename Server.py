# -*- coding: utf-8 -*-
import SocketServer
import json
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
history = []
usernames = {}


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    username = ''

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            request = json.loads(received_string);
            
            #Login request
            if request['request'] == 'login':
               if not self.check_username(request['content']):
                   self.error('invalid username, only letters and numbers allowed')
                   print('1: does this run?')
               
               if usernames.has_key(request['content']):
                   self.error('username has already been taken')
                   print('2: does this run?')
               else:
                   print('3: does this run?')
                   self.login(request['content'])
                   
            #Help request       
            elif request['request'] == 'help':
                self.halp()

            #Check if the user has logged in.
            elif self.username != '':  
                if request['request'] == 'logout':
                    self.logout()
                    
                elif request['request'] == 'names':
                    self.names()

                elif request['request'] == 'msg':
                    if request['content'] == '':
                        self.error('Error: Have you nothing to say?')
                    else:
                        self.message(request['content'])
            else:
                
                self.error('invalid request, try "help" for a list of supported requests')

    
    #Lagre valgt navn som username, og (andre ting?)
    def login(self, nick):
        username = nick
        usernames[nick] = self
        print ('Here is the username: ' + username)
        for msg in history:
            print('Now I am sending the h')
            self.connection.send(msg)

    #Enkode melding og sende til server sånn at den kan broadcastes til alle og lagres i historie. 
    def message(self, content):
        msg = {}
        msg['response'] = 'message'
        msg['timestamp'] = time.asctime( time.localtime(time.time()) )
        msg['sender'] = username
        msg['content'] = content
        msg = json.dumps(msg)
        history.append(msg)
        self.broadcast(msg)
        
        
        
    #Terminere tilkobling og fjerne brukernavn fra aktive brukere.
    def logout(self):
        msg = {}
        msg['response'] = 'info'
        msg['timestamp'] = time.asctime( time.localtime(time.time()) )
        msg['sender'] = username
        msg['content'] = 'logging out...'
        msg = json.dumps(msg)
        self.connection.send(msg)
        #mangler litt på denne
        self.connection.shutdown(SHUT_RDWR)
        username = 'logged_out'
        #shut down the thread.
        
        
    #Hente liste av brukernavn og sende de til klient
    def names(self):
        msg = {}
        msg['response'] = 'info'
        msg['timestamp'] = time.asctime( time.localtime(time.time()) )
        msg['sender'] = 'server'
        userlist = ''
        for user in usernames:
            userlist += user + ' \n'
        msg['content'] = userlist
        msg = json.dumps(msg)
        self.connection.send(msg)
        
        
        

    #Sende forhondsdefinert
    def halp(self):
        msg = {}
        msg['response'] = 'info'
        msg['timestamp'] = time.asctime( time.localtime(time.time()) )
        msg['sender'] = 'server'
        msg['content'] = 'Here is some usefull help.'#helptext
        msg = json.dumps(msg)
        self.connection.send(msg)

    #Sende feilmelding med en beskrivelse (error_msg)
    def error(self, error_msg):
        msg = {}
        msg['response'] = 'error'
        msg['timestamp'] = time.asctime( time.localtime(time.time()) )
        msg['sender'] = 'server'
        msg['content'] = error_msg
        msg = json.dumps(msg)
        self.connection.send(msg)
        

    def broadcast(self, msg):
        for user in usernames:
            usernames[user].connection.send(msg)
        
    def check_username(self, username):
    	for i in username:
        	if (ord(i) < 48) or (ord(i)>57 and ord(i)<65) or (ord(i)>90 and ord(i)<97) or (ord(i)>122):
          	  return False
    		elif:
    		return True    


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True
      

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()



 
