###############################################################################
##
##  Copyright (C) 2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import random

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from twitter.util import printNicely
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
from twitter.oauth import OAuth
from twitter.oauth2 import OAuth2, read_bearer_token_file

class Component(ApplicationSession):
    """
    An application component that publishes events with no payload
    and with complex payload every second.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        auth = OAuth(
	    consumer_key='gKaAE8q1gtSiKxxsTBZUA',
            consumer_secret='zvLMiCy1Lx49OsBGksAVLPYfXBEn2iASvHSJGXtw8',
            token='19982211-kCJThkO6AWRO6yGQkO00b3rqGUg44Zr35RHTacRB4',
            token_secret='nTAhC1Wb9QoZM28NGcbrbfdunuPlnWM0Nk8bDaG0zKw'
        )
        while True:
            try:
		for obj in self.connectToStream(auth):
			self.publish('com.tweettrek.tweet',data = obj)
	   		yield sleep(0.2)
            except:
	        e = sys.exc_info()[0]	
	        printNicely("Exception")
	        printNicely(e)
	        printNicely("Sleeping for 1 minute")
	        sleep(60);
 
        #stream = TwitterStream(auth = auth, secure = True, heartbeat_timeout=9000)
    def connectToStream(self, auth):
        printNicely("-- Connecting to Stream --")
        stream = TwitterStream(auth = auth, secure = True, timeout = 20, heartbeat_timeout = 90)
        tweet_iter = stream.statuses.filter(track = "love")

       # while True:
        #    print(".")
         #   self.publish('com.myapp.heartbeat')
          #  yield sleep(1)

        for tweet in tweet_iter:
            # check whether this is a valid tweet
            if tweet is None:
                printNicely("-- None --")
                return
            elif tweet is Timeout:
                printNicely("-- Timeout --")
                sleep(5);
                return
            elif tweet is HeartbeatTimeout:
                printNicely("-- Heartbeat Timeout --")
                return
            elif tweet is Hangup:
                printNicely("-- Hangup --")
                return
            elif tweet.get('text'):
            #   obj = {'text': tweet["text"], 'user': tweet["user"]["screen_name"]}
                obj = {'text': tweet["text"]}
                yield obj


if __name__ == '__main__':
   from autobahn.twisted.wamp import ApplicationRunner
   runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
   runner.run(Component)
