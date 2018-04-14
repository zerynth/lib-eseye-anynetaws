# Eseye Anynet AWS Publish and Subscribe example
# Created at 2018-04-11 09:09:21.039592

import streams
from eseye.anynetaws import anynetaws as aws

def my_callback(index, topic, data):
    print('> callback from', topic)
    print('> content:', data)

main_ser = streams.serial()
aws.init(SERIAL2) # select the serial driver the modem is connected to

print('> subscribe...')
# subscribe to mychannel/commands/thingname and mychannel/cloudmessages/thingname topics
aws.subscribe('mychannel/commands', my_callback, sock_index=0)
aws.subscribe('mychannel/cloudmessages', my_callback, sock_index=1)
print('> subscriptions completed!')

while True:
    print('> [ENTER] to publish')
    main_ser.readline()
    print('> publish...')
    # publish a message on topic mychannel/devices/thingname
    aws.publish('mychannel/devices', 'hello!')
    print('> publish completed!')