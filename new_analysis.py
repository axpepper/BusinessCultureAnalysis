#!/usr/bin/env python3
import requests
import os
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from textwrap import wrap
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Patch
from scipy.misc import imsave

def readFile(filename):
    filehandle = open(filename)
    tx=filehandle.read()
    filehandle.close()
    return tx

plt.rcParams['figure.figsize'] = (11, 8.5)
rcParams.update({'figure.autolayout': True})


token = '4bYRajAx3tYxSDUMGZug91gEQPvF3Z7rZgDoaRaqfyM4'
form_id = 'kdxQzF'
header = {'Authorization': 'Bearer 4bYRajAx3tYxSDUMGZug91gEQPvF3Z7rZgDoaRaqfyM4'}

r = requests.get('https://api.typeform.com/forms/kdzQzF/responses?page_size=999',
                 headers=header)
df = pd.read_json(r.text)
df = df['items']
q_list = [i['answers'] for i in df if 'answers' in i]
type_list = {i['field']['id']: i['type'] for i in q_list[2]} #must be pointing at a proper answer set 
acc = []
for person in q_list:
    miniacc = {}
    for q in person:
        t = q['type']
        i = q['field']['id']
        try:
            if t == 'text':
                miniacc[i] = q[t]
            if t == 'choice':
                miniacc[i] = q[t]['label']
            if t == 'number':
                miniacc[i] = q[t]
        except:
            pass
    acc += [miniacc]

new_dict = {ind: [] for ind in type_list.keys()}
for p in acc:
    for ind in new_dict.keys():
        try:
            new_dict[ind] += [p[ind]]
        except:
            new_dict[ind] += [np.nan]

df = pd.DataFrame(new_dict)


comp_list = dict(enumerate(sorted(list(set([i.lower() for i in
                                            df['FQFwPSSA4daE'] if pd.notna(i)])))))
print('Select all of the corresponding company names:')
for k, v in comp_list.items():
    print(str(k) + ':' + v)
input_string = input('Enter a list element separated by space ')
ls = [int(i) for i in input_string.split()]
rel_comp_names = [comp_list[i] for i in ls]
new_df = df[[k in rel_comp_names for k in [i.lower() if pd.notna(i) else False for i in
                                           df['FQFwPSSA4daE']]]]
df = new_df
print(df)
op = df[df[list(type_list.keys())[2]] == 'Staff / Team Member']
legend_elements = [Patch(facecolor='white', edgecolor='black', hatch='////', label='Staff / Team Member'), Patch(facecolor='white', edgecolor='black', label='All')]
rel_keys = [i for i in type_list.keys() if (i != 'FQFwPSSA4daE' and i !=
                                            'VcTH8WhPdygA')]
[rel_keys[0],
    rel_keys[1],
    rel_keys[10],
    rel_keys[2],
    rel_keys[3],
    rel_keys[4],
    rel_keys[5],
    rel_keys[9],
    rel_keys[6],
    rel_keys[7],
    rel_keys[8]] = rel_keys

ID_to_qn = dict(zip(rel_keys, ['q'+str(n) for n in range(1, 12)]))


class Question:
    def __init__(self, qid):
        self.qid = qid
        if qid == 'FQFwPSSA4daE' or qid == 'VcTH8WhPdygA':
            pass
        else:
            self.qn = ID_to_qn[self.qid]
            self.qtype = type_list[qid]
            self.graph_gen()
            self.content = self.content_gen()
            self.measure = self.take_measure()
            self.case = self.case_det()
            self.cond = self.cond_content_gen()

    def __str__(self):
        return ID_to_qn[self.qid]

    def __repr__(self):
        return ID_to_qn[self.qid]

    def take_measure(self):
        important_answers = {
            'q1': ['Once a Year', 'Never', 'A year ago'],
            'q2': ['Everyday'],
            'q3': [8,9,10],
            'q4': ['Yes', 'Mostly'],
            'q5': ['We are a team with a clear goal, and I am a member.'],
            'q8': [0,1,2,3,4,5,6,7],
            'q9': [8,9,10]
        }
        answers2 = {
            'q5': ['Sometimes I feel like we are a team, and the goal is clear.'],
            'q8': [8,9,10]
        }
        try:
            relevant = important_answers[self.qn]
            if self.qn in answers2:
                rel2 = answers2[self.qn]
                store2 = 0
                for i in rel2:
                    store2 += sum(op[self.qid] == i)
                probn2 = store2/len(op[self.qid])
                self.probn2 = probn2
                self.n2 = str(int(probn2*100))+'\%'
            acc = 0
            acc2 = 0
            for i in relevant:
                acc += sum(df[self.qid] == i)
                acc2 += sum(op[self.qid] == i)
            prob = acc / len(df[self.qid])
            prob2 = acc2 / len(op[self.qid])
            probm = (acc-acc2)/(len(df[self.qid])-len(op[self.qid]))
            self.prob = prob
            self.prob2 = prob2
            self.probm = probm
            probi2 = 1-prob2
            probi = 1-prob
            self.oi = str(int(probi2*100))+'\%'
            self.o = str(int(prob2*100))+'\%'
            self.ni = str(int(probi*100))+'\%'
            self.n = str(int(prob*100))+'\%'
            self.m = str(int(probm*100))+'\%'
            return prob
        except:
            self.n = 'STOP'
            return 'STOP'

    def case_det(self):
        """Determines which case we're using"""
        if self.measure == "STOP":
            return "STOP"
        qn_to_case = {
            'q1': [75, 50, 0],
            'q2': [80, 60, 0],
            'q3': [60, 0],
            'q4': [70, 0],
            'q5': [70, 0],
            'q6': [60, 0],
            'q8': [20, 0],
            'q9': [70, 0]
        }
        try:
            lower_limits = qn_to_case[self.qn]
        except KeyError:
            print('Seems buggy ' + self.qn)
            return '1'

        for i in range(len(lower_limits)):
            if (100*self.measure) >= lower_limits[i]:
                return str(i+1)
            else:
                pass
        print('Seems buggy ' + self.qn)
        return '1'

    def graph_gen(self):
        """generates a graph using self.data and self.case"""
        if self.qtype == 'choice':
            self.gen_bar()

        elif self.qtype == 'text':
            self.gen_wc()

        elif self.qtype == 'number':
            self.gen_hist()

    def gen_wc(self):
        wordcloud = WordCloud(background_color='white', height=800, width=600,
                              scale=2).generate(str(df[self.qid].dropna().values))
        plt.imshow(wordcloud, interpolation='bilinear', aspect='equal')
        plt.axis('off')
        imsave('Graphs/'+str(self)+'.png', wordcloud)
        plt.close()

    def gen_hist(self):
        def by_color(n, bins, patches):
            for i in range(len(patches)):
                if bins1[i] >= 9:
                    plt.setp(patches[i], facecolor='g')
                elif bins1[i] >= 7:
                    plt.setp(patches[i], facecolor='b')
                elif bins1[i] >= 5:
                    plt.setp(patches[i], facecolor='y')
                elif bins1[i] >= 3:
                    plt.setp(patches[i], facecolor='orange')
                else:
                    plt.setp(patches[i], facecolor='r')

        fig, ax = plt.subplots()
        vals1 = list(map(lambda x: int(x), df[self.qid].dropna().values))
        n1, bins1, patches1 = plt.hist(vals1,
                                       bins=range(min(vals1), max(vals1)+2), edgecolor='k', align='left')
        by_color(n1, bins1, patches1)

        vals2 = list(map(lambda x: int(x), op[self.qid].dropna().values))
        n2, bins2, patches2 = plt.hist(vals2, hatch='//', bins=range(min(vals1), max(vals1)+2), edgecolor='k', align='left')
        by_color(n2, bins2, patches2)
        ax.set_xticks(bins1[:-1])
        ax.grid(False)
        plt.title(self.qn_to_question())
        plt.legend(handles=legend_elements)
        plt.xlabel('score')
        plt.ylabel('frequency')
        plt.savefig('Graphs/' + str(self)+'.pdf')
        plt.close()

    def gen_bar(self):
        g_responses = ['Monthly or more', 'Everyday', 'Yes', 'We are a team with clear goal, and I am a member.', 'Friends', 'Management is interested in my success and developing me as a person.','In the last month', 'Mostly']
        b_responses = ['Quarterly', 'Several times a week', 'Sometimes I feel like we are a team, and the goal is clear.', 'Coworkers','Motivated','Purpose Driven','Team Focused', 'A Few months ago']
        y_responses = ['Once a Year', 'Weekly','Needs Improvement', 'Somewhat', 'Sometimes I feel like we are a team, but the goal is not clear.', 'Colleagues', 'Management is only interested in my success at work.', 'Six months ago', 'Sometimes']
        o_responses = ['Monthly', 'Acquaintances', 'A year ago']
        r_responses = ['Never', 'Seldom', 'No', 'I do not feel like part of the team.', 'Management is interested in my success and developing me as a person.', 'Almost never']

        c_to_n = {'green': 5, 'blue': 4, 'yellow': 3, 'orange': 2, 'red': 1, 'black': 0}

        def response_to_color(response):
            if response in g_responses:
                return 'green'
            elif response in b_responses:
                return 'blue'
            elif response in y_responses:
                return 'yellow'
            elif response in o_responses:
                return 'orange'
            elif response in r_responses:
                return 'red'
            else:
                return 'black'

        def bars_to_color(bars):
            return [response_to_color(response) for response in bars]

        barHeight = .3
        bars1 = tuple(set(df[self.qid].fillna(value='No Response', downcast='infer')))
        pair = [(k, response_to_color(k)) for k in bars1]
        pair = sorted(pair, key=lambda tpl: c_to_n[tpl[1]])
        bars1, colors1 = zip(*pair)

        bars2 = tuple(set(op[self.qid].fillna(value='No Response', downcast='infer')))
        pair = [(k, response_to_color(k)) for k in bars1]
        pair = sorted(pair, key=lambda tpl: c_to_n[tpl[1]])
        bars2, colors2 = zip(*pair)

        BarWidth1 = [len(df[df[self.qid] == k]) for k in bars1]
        BarWidth2 = [len(op[op[self.qid] == k]) for k in bars1]
        r1 = np.arange(len(bars1))
        r2 = [x + barHeight for x in r1]
        plt.barh(r1, BarWidth1, height=barHeight, color=colors1, edgecolor='black', label='All')
        plt.barh(r2, BarWidth2, height=barHeight, color=colors2, edgecolor='black', hatch='////', label='Operator')
        plt.legend(handles=legend_elements)
        # Create names on the y-axis
        plt.yticks(r1, ['\n'.join(wrap(a, 30)) for a in bars1])
        plt.title(self.qn_to_question())
        # Show graphic
        plt.savefig('Graphs/' + str(self)+'.pdf')
        plt.close()

    def content_gen(self):
        """generates content using self.data and self.case"""
        qn = ID_to_qn[self.qid]
        return readFile('Static/'+str(qn))

    def cond_content_gen(self):
        if self.measure == 'STOP':
            return ''
        vn = self.case + '/v' + self.qn[1:]
        print('Dynamic/'+vn)
        return readFile('Dynamic/' + vn)

    def qn_to_question(self):
        q_str_ls = ['When did you last discuss your performance with your manager?',
                    'How often do you get to do your best at work?',
                    'On a scale of 0 - 10, 10 being the best score, how comfortable are you sharing new ideas and insights with co-workers?',
                    'Do you have access to the equipment, data, and resources you need to independently do your work?',
                    'Do you feel that you are part of a team working together for a common goal?',
                    'In a few words, describe your organization\'s culture',
                    'On a scale of 0 - 10, how would you describe the people you work with. 0 being a stranger, 10 being a good friend.',
                    'On a scale of 0 - 10, rate how well your  manager knows and supports you with your personal and career goals.',
                    "On a scale of 0 - 10, 10 being the highest, how inspiring is your organization's purpose?",
                    "What is your organization's purpose? In other words, who are your clients, and how do you help them?",
                    "Tell us your organization's vision."]
        qn_to_q_str = dict(zip(['q'+str(n) for n in range(1, 12)], q_str_ls))
        return qn_to_q_str[self.qn]


Q_list = [Question(i) for i in rel_keys]
