#!/usr/bin/python

import csv, re, pprint

class MarketAnalysis(object):
    def __init__(self):
        self.pp = pprint.PrettyPrinter(indent=4)
        self.responders = dict()
        self.code_counts = dict()
        self.n_threads = 0
        self.total_replies = 0
        self.three_plus = 0
        self.files = [
                #'/home/nodice/Desktop/revised questions and answers for article.csv',
                '/home/nodice/Desktop/clean code.csv',
                #'/home/nodice/Desktop/new messages.csv'
                ]
        self.keyword_counts = {
                'regulations': 0,
                'expert': 0,
                'health': 0,
                'poverty': 0,
                'class': 0,
                'privilege': 0,
                'alternative food': 0,
                'legitimate': 0,
                'leadership': 0,
                'leader': 0,
                'learning': 0,
                'outreach': 0,
                'equality': 0,
                'unity': 0,
                'progress': 0,
                'growth': 0}

    def analyze(self):
        for file in self.files:
            with open(file) as csvfile:
                r = csv.DictReader(csvfile)
                for row in r:
                    if filter(None, row.values()): # remove empty rows
                        self.n_threads += 1
                        self.thread_replies = 0
                        response = row['answers']

                        # find keywords
                        for k in iter(self.keyword_counts):
                            if k in response:
                                self.keyword_counts[k] += 1


                        # find codes
                        codes = filter(None,
                                       [x.lower().strip() for x in row['codes'].split(';')])
                        for code in codes:
                            if code in self.code_counts:
                                self.code_counts[code] += 1
                            else:
                                self.code_counts[code] = 1

                        # split response cell by responders
                        response_lines = response.split('\n')
                        for line in response_lines:
                            m = re.match('^([^\s|\d]+(\w|\s)+?):', line)
                            if m:
                                if re.search('http', m.group(1)):
                                    continue
                                word_count = len(re.findall('\w+', m.group(1)))
                                if word_count < 4:
                                    self.thread_replies += 1
                                    if m.group(1) in self.responders:
                                        self.responders[m.group(1)] += 1
                                    else:
                                        self.responders[m.group(1)] = 1
                        self.total_replies += self.thread_replies
                        if self.thread_replies >= 3:
                            self.three_plus += 1

                self.responders     = sort_by_val(self.responders)
                self.keyword_counts = sort_by_val(self.keyword_counts)
                self.code_counts    = sort_by_val(self.code_counts)

    def print_result(self):
        print((
            'threads: {}, replies: {}. {:.2f} replies per thread.').format(
                self.n_threads, self.total_replies,
                float(self.total_replies)/self.n_threads))
        print(('{} threads with 3+ responses').format(self.three_plus))
        print(('{} unique responders.').format(len(self.responders)))

        print '\nKeywords:'
        self.pp.pprint(self.keyword_counts)

        print '\nCodes:'
        self.pp.pprint(self.code_counts)

        print '\nResponders:'
        self.pp.pprint(self.responders)

def sort_by_val(dic):
    return sorted(dic.items(), key=lambda x:x[1], reverse=True)


market = MarketAnalysis()
market.analyze()
market.print_result()
