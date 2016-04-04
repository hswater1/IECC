# -*- coding: utf-8 -*-


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "2998449209-p16thglATy3g4zV5MXxQi8nW9s2anjBaKq5S0hU"
access_token_secret = "AzA65r9gTV7gebJ9niUOerEiGccPThGjFJlE03wAeBe3e"
consumer_key = "5oB1jdPOzdaje0QwXZTv90dLq"
consumer_secret = "TQFJL0tu2nnr706Mh4Vadt7CoNwIG4OsU2QL9lbyVafrkQOdq6"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'big data'
    stream.filter(locations=[-180,-90,180,90])