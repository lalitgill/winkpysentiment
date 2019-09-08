#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import re
#rgxEmoji = r"#[a-z][a-z0-9]*"
#test = 'fun'
#print(test.encode('utf-8'))

#matches = re.findall(rgxEmoji, test)


def monday(a):
    print(a)
    return "monday"
def tuesday():
    return "tuesday"
def wednesday():
    return "wednesday"
def thursday():
    return "thursday"
def friday():
    return "friday"
def saturday():
    return "saturday"
def sunday():
    return "sunday"
def default(a):
    return "Incorrect day"

switcher = {
    'one': monday,
    2: tuesday,
    3: wednesday,
    4: thursday,
    5: friday,
    6: saturday,
    7: sunday
    }

def switch(dayOfWeek,a):
    return switcher.get(dayOfWeek, default)(a)

a = 'lllllll'
print(switch('one',a))
print(switch(0,a))

#def switchemoji():



#switchemoji
#def switcherhandle(tag):

 #switch_function = switcher[tag]
