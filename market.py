#!/usr/bin/python

import csv, re, pprint

responders = dict()
n_threads = 0 
total_replies = 0
three_plus = 0
files = ['/home/nodice/Desktop/revised questions and answers for article.csv',
         '/home/nodice/Desktop/new messages.csv']
keywords = ['regulations',
            'expert',
            'health',
            'poverty',
            'class',
            'privilege',
            'alternative food',
            'legitimate',
            'leadership',
            'leader',
            'learning',
            'outreach',
            'equality',
            'unity',
            'progress',
            'growth']

for file in files:
    with open(file) as csvfile:
        r = csv.reader(csvfile)
        for row in r:
            n_threads += 1
            thread_replies = 0
            response_lines = row[3].split('\n')
            for line in response_lines:
                m = re.match('^([^\s|\d]+(\w|\s)+?):', line)
                if m:
                    if re.search('http', m.group(1)):
                        continue
                    word_count = len(re.findall('\w+', m.group(1)))
                    if word_count < 4:
                        thread_replies += 1
                        if m.group(1) in responders:
                            responders[m.group(1)] += 1
                        else:
                            responders[m.group(1)] = 1
            total_replies += thread_replies
            if thread_replies >= 3:
                three_plus += 1

pp = pprint.PrettyPrinter(indent=4)
responders = sorted(responders.items(), key=lambda x:x[1], reverse=True)
print 'threads: {}, replies: {}. {:.2f} replies per thread.'.format(n_threads,
      total_replies, float(total_replies)/n_threads)
print 'threads with 3+ responses: {}'.format(three_plus)
pp.pprint(responders)
