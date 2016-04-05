# -*- coding: utf-8 -*-
import json
from datetime import datetime
from datetime import timedelta
import bisect
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


def gen_pairs(strs): 
#Convert a list of str to a list of str pairs
    pairs = []
    ln = len(strs)
    for i in range(0, ln - 1):
        for j in range(i + 1, ln):
            pairs.append([strs[i], strs[j]])
    return pairs


def add_twt(time, hashtags):
#to add a new tweet to the graph
    
    #Genrate hashtag pairs
    ht_pairs = gen_pairs(hashtags)
    #Add tweet into window list as traker
    if twt_window == []:
        twt_window.append([time, hashtags, ht_pairs])
        dist_pairs.clear()
        dist_hashtags.clear()
            
    else:
        time_key = [t[0] for t in twt_window]
        twt_window.insert(bisect.bisect_right(time_key, time, lo=0, hi=len(time_key)),[time, hashtags, ht_pairs])
    
    #Update pair dictionary and hashtag dictionary
    for pair in ht_pairs:
        dist_pairs.update({tuple(pair):dist_pairs.get(tuple(pair), 0) + 1})   
    for ht in hashtags:
        dist_hashtags.update({ht:dist_hashtags.get(ht, 0) + 1})    
    
    return


def evict_twt(new_time):
#Evict expired tweets
    
    time_key = [t[0] for t in twt_window]
    idx = bisect.bisect_left(time_key, new_time, lo=0, hi=len(time_key))
    if idx == 0:
        return
    
    if idx == len(time_key):
        #In this case all tweets are expired
        dist_pairs.clear()
        dist_hashtags.clear()
        del twt_window[:]
        return
        
    else:
        #Remove Hashtags and pairs from dictionary
        for t in twt_window[:idx]:
            for ht in t[1]:
                cnt_ht = dist_hashtags.get(ht, 0)
                if cnt_ht < 1:
                    print('Cannot evict: ')
                    print(t)
                    return
                elif cnt_ht == 1:
                    del dist_hashtags[ht]
                else:
                    dist_hashtags[ht] = cnt_ht - 1
            
            for p in t[2]:
                cnt_p = dist_pairs.get(tuple(p), -1)
                if cnt_p < 1:
                    print('Cannot evict: ')
                    print(t)
                    return
                elif cnt_p == 1:
                    del dist_pairs[tuple(p)]
                else:
                    dist_pairs[tuple(p)] = cnt_p - 1 
            
        del twt_window[:idx]
    return
    
    
def cal_avg_deg():
#Calculate the average degree
    
    if len(twt_window) < 1: return 0
  
    #Calculate average degree by two times of number of pairs(edges) divided by number of hashtags
    return len(dist_pairs)*2/len(dist_hashtags)
    

#Initiate window and average degree list
twt_window = []
r_avg_deg = None
dist_pairs = {}
dist_hashtags = {}
exp_twts = []


#open tweet file
tweets_file = open(tweets_data_path, "r")  
for line in tweets_file:  
    try:
        tweet = json.loads(line)
    except ValueError:
        continue
    
    #Only new tweets with the creation time will be counted
    if 'created_at' in tweet:
        #Initiate rolling average degree list or add one average same as previous one that will be updated if adding or evicting happens
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
                evict_twt(new_cutoff_time)
                r_avg_deg[-1] = cal_avg_deg()
            #Check whether the tweet has more than 1 hashtags.
            if 'entities' in tweet and 'hashtags'in tweet['entities'] and len(tweet['entities']['hashtags'])>1:
                #strip hashtags from new tweet, sort, and remove duplicate
                new_twt_ht = sorted(set([ht['text'] for ht in tweet['entities']['hashtags']]))
                #Add the tweet to the window if it has 1+ distinct hashtags
                if len(new_twt_ht) > 1:
                    add_twt(new_twt_time, new_twt_ht)
                    r_avg_deg[-1] = cal_avg_deg()
    else:
        exp_twts.append(tweet)
        
#Write the result to the output file. No output, if there is not tweet processed. 
                
if r_avg_deg != None and len(r_avg_deg) > 0:  
    with open(output_file, 'w') as f:
        for s in r_avg_deg:
            f.write('%.2f' % s + '\n')
    print(str(len(r_avg_deg)) + ' tweets have been processed')
    
else:
    print('No tweet has been processed')
