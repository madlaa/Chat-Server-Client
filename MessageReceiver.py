# -*- coding: utf-8 -*-
from threading import Thread
from MessageParser import MessageParser

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        
	#self.client=client
        self.connection = connection
        # tODO: Finish initialization of MessageReceiver
        super(MessageReceiver,self).__init__()
       

    def run(self):
        # tODO: Make MessageReceiver receive and handle payloads
        self.MessageParser = MessageParser()
        #s_thread = MessageParser(payload)
        #s_thread.start()
        while True:
            payload = self.connection.recv(4096)
            #print('We now listening for input from server.' + payload)
            self.MessageParser.parse(payload)
            
