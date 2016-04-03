# -*- coding: utf-8 -*-

#df_tt = pd.read_json('C:\cygwin64\home\Gordon\IECC\data-gen\teewts.txt')[:10]

import json  


from datetime import datetime
from datetime import timedelta
import bisect
import itertools

            
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
    
    #Add hashtag pairs into pair list as a tracker
    #add_pairs(ht_pairs)    
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



#Use given tweets file
tweets_data_path = 'C:/cygwin64/home/Gordon/IECC/data-gen/tweets.txt'

#Assumptions 1 - I will not use current time to decide the boundry of the 60s windows,
#so this program can process historic tweets.
#I will use new tweet's creation time + 60s as the cut-off, if the time is most recent.

#Initiate window and graph
twt_window = []
r_avg_deg = None
#tweets_data = []  

#open tweet file
tweets_file = open(tweets_data_path, "r")  
for line in tweets_file:  
    try:
        tweet = json.loads(line)
    except ValueError:
        continue
    
    if 'created_at' in tweet:
        
        #Initiate rolling average degree list or add one average
        if r_avg_deg == None:
            r_avg_deg=[0]
        else:
            r_avg_deg.append(r_avg_deg[-1])
            
        #Convert creation time to datetime type.
        new_twt_time = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        new_cutoff_time = new_twt_time - timedelta(seconds = 60)  
        
        #Ignore new tweets older than cut
        if len(twt_window) == 0 or new_twt_time > twt_window[0][0]:
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
            
           







##############################################    
'''twt_window = evict_twt(datetime.strptime('Tue Mar 29 00:04:51 +0000 2016','%a %b %d %H:%M:%S +0000 %Y'),twt_window)
    
pairs = []
for twt in twt_window:
    for p in twt[1]:
        pairs.append(p)
pairs.sort()

uq_pairs = list(pairs for pairs,_ in itertools.groupby(pairs))

edges = len(uq_pairs)

nodes = [ y for x in uq_pairs for y in x]
nodes.sort()
uq_nodes = list(nodes for nodes,_ in itertools.groupby(nodes))


avg_deg = edges/uq_nodes
      
def add_pairs(pairs):
#Create network graph with pairs. When incr=1, add pairs. When incr = -1, drop pairs.

    for pair in pairs:
        ht_1 = [h[0] for h in twt_graph]
        l1 = len(ht_1)
        idx_1_r = bisect.bisect_right(ht_1, pair[0], lo=0, hi=l1)
        idx_1_l = bisect.bisect_left(ht_1, pair[0], lo=0, hi=l1)
        if idx_1_r == idx_1_l:
            idx = idx_1_l
            twt_graph.insert(idx,pair)
        else:
            l2 = idx_1_r - idx_1_l
            ht_2 = [h[1] for h in twt_graph[idx_1_l:idx_1_r]]
            idx_2 = bisect.bisect_left(ht_2, pair[1], lo=0, hi=l2)
            idx = idx_1_l + idx_2
            twt_graph.insert(idx, pair)
    return



twt_u_p = list(set(twt_graph))

#p = gen_pairs(new_twt_ht)
ppp = [['b','c'], ['c', 'b'],['a','c'],['e','b'],['a', 'c']]
q= list(p for p in ppp)
set(ppp)
twt_graph=[]
dd= add_pairs(ppp)
twt_graph.append([p] for p in ppp)
twt_graph
xxx(ppp)
def xxx(qqq):
    for q in qqq:
        twt_graph.append(q)
    return

ppp = [t[0] for t in p]
ppp.insert(1,'c')
bisect.bisect_right(ppp,'b',lo=0,hi=5)
bisect.bisect_left(ppp,'b',lo=0,hi=5)     
np_tweets = np.array(tweets_data)
ppp.append(ppp[-1])'''