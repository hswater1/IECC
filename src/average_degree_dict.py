# -*- coding: utf-8 -*-
import json
from datetime import datetime
from datetime import timedelta
#import bisect
import sys


if len(sys.argv) > 1:
    tweets_data_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = '../tweet_output/output.txt'
else:
    tweets_data_path = './tweet_input/tweets.txt'
    output_file = './tweet_output/output_dict.txt'


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
    
    
    #Add tweet into window list as traker
    if time in twt_window:
        twt_window.update({time: twt_window.get(time) + [hashtags]})
    else:
        twt_window.update({time: [hashtags]})
    #Update pair dictionary and hashtag dictionary
    #Genrate hashtag pairs
    ht_pairs = gen_pairs(hashtags)    
    for pair in ht_pairs:
        dist_pairs.update({tuple(pair):dist_pairs.get(tuple(pair), 0) + 1})   
    
    for ht in hashtags:
        dist_hashtags.update({ht:dist_hashtags.get(ht, 0) + 1})    
    
    return


def evict_twt(new_time):
#Evict expired tweets
    if new_time > max(twt_window):
        #In this case all tweets are expired
        dist_pairs.clear()
        dist_hashtags.clear()
        twt_window.clear()
        return
        
    else:
        #Remove Hashtags and pairs from dictionary
        for k,v in list(twt_window.items()):
            if k < new_time:
                for hts in v:
                    for ht in hts:
                        cnt_ht = dist_hashtags.get(ht, 0)
                        if cnt_ht > 1:
                            dist_hashtags[ht] = cnt_ht - 1
                        elif cnt_ht == 1:
                            del dist_hashtags[ht]
                        else:
                            print('Cannot evict: ')
                            print(v)
                            return
                    ht_pairs = gen_pairs(hts) 
                    for p in ht_pairs:
                        cnt_p = dist_pairs.get(tuple(p), -1)
                        if cnt_p > 1:
                            dist_pairs[tuple(p)] = cnt_p - 1
                        elif cnt_p == 1:
                            del dist_pairs[tuple(p)]
                        else:
                            print('Cannot evict: ')
                            print(ht_pairs)
                            return 
            
                del twt_window[k]
    return
    
    
def cal_avg_deg():
#Calculate the average degree
    
    if len(twt_window) < 1: return 0
  
    #Calculate average degree by two times of number of pairs(edges) divided by number of hashtags
    return len(dist_pairs)*2/len(dist_hashtags)
    

#Initiate window and average degree list
twt_window = {}
r_avg_deg = None
dist_pairs = {}
dist_hashtags = {}


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
               
        #Ignore tweets older than cutoff
        if not twt_window or new_twt_time > max(twt_window) - timedelta(seconds = 60):
            new_cutoff_time = new_twt_time - timedelta(seconds = 60)  
            #Evict expired tweets from the window
            if bool(twt_window) and new_cutoff_time > min(twt_window):            
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
    
#Write the result to the output file. No output, if there is not tweet processed. 
                
if r_avg_deg != None and len(r_avg_deg) > 0:  
    with open(output_file, 'w') as f:
        for s in r_avg_deg:
            f.write('%.2f' % s + '\n')
    print(str(len(r_avg_deg)) + ' tweets have been processed')
    
else:
    print('No tweet has been processed')
