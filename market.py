#!/usr/bin/python

import csv, re, pprint

responders = dict()
n_threads = 0 
n_replies = 0
files = ['revised questions and answers.csv', 'new messages.csv']

for file in files:
    with open(file) as csvfile:
        r = csv.reader(csvfile)
        for row in r:
            n_threads += 1
            responses = row[3].split('\n')
            for response in responses:
                m = re.match('^([^\s|\d]+[a-zA-Z ]+?):', response)
                if m:
                    if re.search('http', m.group(1)):
                        continue
                    word_count = len(re.findall('\w+', m.group(1)))
                    if word_count < 4:
                        n_replies += 1
                        if m.group(1) in responders:
                            responders[m.group(1)] += 1
                        else:
                            responders[m.group(1)] = 1

pp = pprint.PrettyPrinter(indent=4)
responders = sorted(responders.items(), key=lambda x:x[1], reverse=True)
print 'threads: {}, replies: {}. {:.2f} replies per thread.'.format(n_threads,
        n_replies, float(n_replies)/n_threads)
pp.pprint(responders)
