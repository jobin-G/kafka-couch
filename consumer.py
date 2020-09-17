#
#
# Author: Aniruddha Gokhale
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 6, 2020
#
# Purpose:
#
#    Demonstrate the use of Kafka Python streaming APIs.
#    In this example, demonstrate Kafka streaming API to build a consumer.
#

import os   # need this for popen
import time # for sleep
import json
import couchdb
from kafka import KafkaConsumer  # consumer of events

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the consumer
# (you will need to change this to your bootstrap server's IP addr)
consumer = KafkaConsumer (bootstrap_servers="192.168.15.3:9092")

# subscribe to topic
consumer.subscribe (topics=["utilizations"])

#Line assumes CouchDB was set up with admin/admin as username/password
couch = couchdb.Server('http://admin:admin@localhost:5984')

#Run once on the VM to create a db
#couch.create('test')
db = couch['test']

# we keep reading and printing
for msg in consumer:
    # what we get is a record. From this record, we are interested in printing
    # the contents of the value field. We are sure that we get only the
    # utilizations topic because that is the only topic we subscribed to.
    # Otherwise we will need to demultiplex the incoming data according to the
    # topic coming in.
    #
    # convert the value field into string (ASCII)
    #
    parsed_json = json.loads(msg.value)
    db.save({'timestamp': parsed_json['timestamp'], 'content': parsed_json['contents']})
    print('Record saved.')

# we are done. As such, we are not going to get here as the above loop
# is a forever loop.
consumer.close ()
    






