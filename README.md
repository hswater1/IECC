Coding Challenge Submission by Shen Huang
===========================================================

The program will keep a list for the tweets in the 60s window. Only the creation time, hashtags, and the distinct hashtag pairs are stored. New qualified tweets will be added into the list, and the expired ones will be evicted. The program will calculate the average degree every time there is any tweet added or evicted. The program will keep a dictionary as a counter to store distinct pairs and a dictionary to store distinct hashtags. The average degree is calculated as: The average degree = (the number of distinct pairs) x 2 / (the number of distinct hashtags) 

The script was tested under Linux with Python 2.7 and Windows 10 with Python 3.4. A tweets file size of 1 giga has been processed sucessfully by this script. The I/O file name and path can be changed by running the script with arguments.

The future work is to add error handlers.

I have two approaches to calculate the average degrees. First one forms a set of distinct hashtags and a set of pairs every time the windiw is updated. The second one keeps two sets in memory and updates them every time. The second approach is always faster than the first one on different size files. Thus, I submit the second.
