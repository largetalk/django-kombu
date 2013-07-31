
class PrintTestHandler(object):
    def match(self, _, message):
        #return message.delivery_info['routing_key'] == 'test.test'
        #return key.startswith('test.')
        return True

    def handle(self, body, message):
        print '### in print_test ###'
        print 'body : ', body
        print 'message : ', message

        message.ack()
