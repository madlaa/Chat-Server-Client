import json

class MessageParser():
    def __init__(self):
	#self.payload = payload
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }
	#super(MessageParser, self).__init__()
	
    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            print('The server has sent us a nonvalid response. Please revise your code.')
    def parse_error(self, payload):
    	print('\n Here is an error message: \n')
        print(payload)
    def parse_info(self, payload):
    	print('\n Here is some information: \n')
    	print(payload)
    def parse_message(self, payload):
        print('\n Here is a message: \n')
        print(payload)
    def parse_history(self, payload):
        print('\n Here is the history: \n')
        print(payload)

    
    
    # Include more methods for handling the different responses... 
