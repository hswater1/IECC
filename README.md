Coding Challenge Submission by Shen Huang
===========================================================

The program will keep a list for the tweets in the 60s window. Only the creation time and the distinct hashtag pairs are stored. New qualified tweets will be added into the list, and the expired ones will be evicted. The program will calculate the average degree evry time there is any tweet added or evicted. The program will form a list of distinct pairs and a list of distinct hashtags ever time. The average degree is calculated as: The average degree = (the number of distinct pairs) x 2 / (the number of distinct hashtags) 

The script was tested under Linux with Python 2.7 and Windows 10 with Python 3.4.
The script can be called by running run.sh. By default, the input is "./tweet_input/tweets.txt", and the output is "./tweet_output/output.txt". The file name and path can be changed by running the script with arguments.
