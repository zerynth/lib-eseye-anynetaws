.. module:: anynetaws

************************
Eseye AnyNet AWS Library
************************

The Zerynth Eseye AnyNet AWS Library allows to easily connect to `AWS IoT platform <https://aws.amazon.com/iot-platform/>`_ thanks to Eseye AnyNet AWS AT modem.

    
.. function:: init(serdrv, serbaud=9600)

    :param serdrv: serial communication driver (e.g., :samp:`SERIAL0`, :samp:`SERIAL1`, ...)
    :param serbaud: serial communication baudrate

    Initialize serial communication with the Eseye AWS AT modem.

    
.. function:: state(string_format=True)

    :param string_format: :samp:`True` or :samp:`False` to select string or integer output format respectively

    Retrieve modem state, returned as an integer in the range :samp:`0`,:samp:`8` or a string in the list::

        [
            'Idle',
            'Waiting Keys',
            'Connecting to Network',
            'Establishing SSL',
            'SSL Connected',
            'Connecting MQTT',
            'Ready: MQTT Connected',
            'Ready: Subscribed',
            'Error'
        ]
    
.. function:: qccid()

    Retrieve the ICCD of AnyNet Secure SIM.
    
.. function:: version()

    Retrieve the version of the Eseye AWS AT modem firmware.
    
.. function:: reset()

    Force a reload of parameters from the SIM card, forcing the modem to reset
    
.. function:: pubopen(topic, sock_index)

    :param topic: a string representing a valid mqtt topic (note that the modem firmware automatically appends AWS IoT Thing name to chosen topic)
    :param sock_index: an integer representing a valid modem socket index :samp:`(0,1)`

    Open a publish *channel* to topic :samp:`topic` through socket index :samp:`sock_index`.
    Eseye AWS AT modem needs a publish *channel* to be open before starting publishing on a selected topic.
    A publish *channel* is open on top of an available socket represented by a socket index.
    Only one *channel* can be open on a single socket index, when trying to open a *channel* on an already used socket a :samp:`SocketUsageError` exception is raised.

    
.. function:: pubopen_index(topic)

    :param topic: a string representing a valid mqtt topic (note that the modem firmware automatically appends AWS IoT Thing name to chosen topic)

    Check if a publish *channel* for topic :samp:`topic` is already open on any of the available modem sockets, returning :samp:`None` if none is found, socket index otherwise.
    
.. function:: publish(topic, payload, sock_index=0, qos=1, mode=2)

    :param topic: a string representing a valid mqtt topic (note that the modem firmware automatically appends AWS IoT Thing name to chosen topic)
    :param payload: a string, bytes or bytearray object to be sent
    :param sock_index: an integer representing a valid modem socket index :samp:`(0,1)`
    :param qos: an integer representing the qos level to send the mqtt message with :samp:`(1,2,3)`
    :param mode: an integer representing a valid publish mode :samp:`(0,1,2)`

    Publish a message on a chosen topic in one of the following modes:

        0. publish the message without opening a publish *channel*, which must be already open when calling this function
        1. open (:func:`pubopen`) a publish *channel* and publish the message without checking if a publish *channel* is already open on that topic
        2. open (:func:`pubopen`) a publish *channel* and publish the message checking if a *channel* is already open on chosen topic, if so the socket index on which the *channel* is already open overwrites passed one

    
.. function:: pubclose(sock_index)

    :param sock_index: an integer representing a valid modem socket index :samp:`(0,1)`

    Close a publish *channel* open on socket :samp:`sock_index`.
    
.. function:: subopen(topic, sock_index)

    :param topic: a string representing a valid mqtt topic (note that the modem firmware automatically appends AWS IoT Thing name to chosen topic)
    :param sock_index: an integer representing a valid modem socket index :samp:`(0,1)`

    Open a subscription *channel* for topic :samp:`topic` through socket index :samp:`sock_index`.
    A subscription *channel* is open on top of an available socket represented by a socket index.
    Only one *channel* can be open on a single socket index, when trying to open a *channel* on an already used socket a :samp:`SocketUsageError` exception is raised.

    Refer to :func:`subscribe` function to associate a callback function to chosen subscription.
    
.. function:: subopen_index(topic)

    :param topic: a string representing a valid mqtt topic (note that the modem firmware automatically appends AWS IoT Thing name to chosen topic)

    Check if a subscription *channel* for topic :samp:`topic` is already open on any of the available modem sockets, returning :samp:`None` if none is found, socket index otherwise.
    
.. function:: subclose(sock_index)

    :param sock_index: an integer representing a valid modem socket index :samp:`(0,1)`

    Close a subscription open on socket :samp:`sock_index`
    
.. function:: subscribe(topic, callback, sock_index=0, mode=1)

    :param topic: a string representing a valid mqtt topic (note that the modem firmware automatically appends AWS IoT Thing name to chosen topic)
    :param callback: a function to be called when a message arrives on chosen topic
    :param sock_index: an integer representing a valid modem socket index :samp:`(0,1)`
    :param mode: an integer representing a valid subscription mode :samp:`(0,1)`

    Subscribe to topic :samp:`topic` calling :samp:`callback` function whenever a new message arrives on chosen topic.
    Example callback function::

        def my_callback(sock_index, topic, data):
            print('> callback from', topic)
            print('> on socket ', sock_index)
            print('> with content:', data)
    
    As reported, a callback function must accept three arguments.

    Depending on selected mode, the following actions are executed calling the :func:`subscribe` function:

        0. open (:func:`subopen`) a subscription *channel*, setting a callback, without checking if a *channel* is already open on chosen topic
        1. open (:func:`subopen`) a subscription *channel*, setting a callback, checking if a *channel* is already open on chosen topic, if so the socket index on which the *channel* is already open overwrites passed one
    
