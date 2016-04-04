# -*- coding: utf-8 -*-
import json
from datetime import datetime
from datetime import timedelta
import bisect
import itertools
import sys


if len(sys.argv) > 1:
    tweets_data_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = './tweet_output/output.txt'
else:
    tweets_data_path = './tweet_input/tweets.txt'
    output_file = './tweet_output/output.txt'

def add_twt(time, hashtags):
#to add a new tweet to the graph
    
    #Genrate hashtag pairs
    ht_pairs = gen_pairs(hashtags)
    #Add tweet into window list as traker
    if twt_window == []:
        twt_window.append([time, ht_pairs])
    else:
        time_key = [t[0] for t in twt_window]
        twt_window.insert(bisect.bisect_right(time_key, time, lo=0, hi=len(time_key)),[time, ht_pairs])
    
    return
   
    
def gen_pairs(strs): 
#Convert a list of str to a list of str pairs
    pairs = []
    ln = len(strs)
    for i in range(0, ln - 1):
        for j in range(i + 1, ln):
            pairs.append([strs[i], strs[j]])
    return pairs


def cal_avg_deg():
#Calculate the average degree
    pairs = []
    if len(twt_window) < 1: return 0
    for twt in twt_window:
        for p in twt[1]:
            pairs.append(p)
            
    #Make a list of unique pairs
    pairs.sort()    
    uq_pairs = list(pairs for pairs,_ in itertools.groupby(pairs))
    #Make a list of unique hashtags
    nodes = [ y for x in uq_pairs for y in x]
    nodes.sort()
    uq_nodes = list(nodes for nodes,_ in itertools.groupby(nodes))
    #Calculate average degree by two times of number of pairs(edges) divided by number of hashtags
    return len(uq_pairs)*2/len(uq_nodes)
    

def evict_twt(new_time, win):
#Evict expired tweets
    time_key = [t[0] for t in win]
    
    return win[bisect.bisect_right(time_key, new_time, lo=0, hi=len(time_key)):]


#Initiate window and average degree list
twt_window = []
r_avg_deg = None

#open tweet file
tweets_file = open(tweets_data_path, "r")  
for line in tweets_file:  
    try:
        tweet = json.loads(line)
    except ValueError:
        continue
    
    #Only new tweets with the creation time will be counted
    if 'created_at' in tweet:
        #Initiate rolling average degree list or add one average same as previous one
        if r_avg_deg == None:
            r_avg_deg=[0]
        else:
            r_avg_deg.append(r_avg_deg[-1])
            
        #Convert creation time to datetime type.
        new_twt_time = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        new_cutoff_time = new_twt_time - timedelta(seconds = 60)  
                
        #Ignore tweets older than cutoff
        if len(twt_window) == 0 or new_twt_time > twt_window[-1][0] - timedelta(seconds = 60):
            #Evict expired tweets from the window
            if len(twt_window) > 0 and new_cutoff_time > twt_window[0][0]:            
                twt_window = evict_twt(new_cutoff_time, twt_window)
                r_avg_deg[-1] = cal_avg_deg()
            #Check whether the tweet has more than 1 hashtags.
            if 'entities' in tweet and 'hashtags'in tweet['entities'] and len(tweet['entities']['hashtags'])>1:
                #strip hashtags from new tweet, sort, and remove duplicate
                new_twt_ht = sorted(set([ht['text'] for ht in tweet['entities']['hashtags']]))
                #Add the tweet to the window if it has 1+ distinct hashtags
                if len(new_twt_ht) > 1:
                    add_twt(new_twt_time, new_twt_ht)
                    r_avg_deg[-1] = cal_avg_deg()

        
#Write the result to the output file. No output, if there is not tweet processed.                    
if r_avg_deg != None and len(r_avg_deg) > 0:  
    with open(output_file, 'w') as f:
        for s in r_avg_deg:
            f.write('%.2f' % s + '\n')
    print(str(len(r_avg_deg)) + ' tweets have been processed')
else:
    print('No tweet has been processed')
