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
from twitter import *

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

        stream = TwitterStream(auth = auth, secure = True)
        tweet_iter = stream.statuses.filter(track = "love")

       # while True:
        #    print(".")
         #   self.publish('com.myapp.heartbeat')
          #  yield sleep(1)

        for tweet in tweet_iter:
            # check whether this is a valid tweet
            if tweet.get('text'):
                print tweet.get('text')
                obj = {'text': tweet["text"], 'user': tweet["user"]["screen_name"]}
                self.publish('com.tweettrek.tweet',data = obj)
                yield sleep(0.1)

if __name__ == '__main__':
   from autobahn.twisted.wamp import ApplicationRunner
   runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
   runner.run(Component)
