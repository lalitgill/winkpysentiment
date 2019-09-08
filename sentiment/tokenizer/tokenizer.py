#!/usr/bin/python
# -*- coding: utf8 -*-
import re,sys
from engcontractions import *

rgxSpaces = r"\s+"

rgxOrdinalL1 = r"1\dth|[04-9]th|1st|2nd|3rd|[02-9]1st|[02-9]2nd|[02-9]3rd|[02-9][04-9]th|\d+\d[04-9]th|\d+\d1st|\d+\d2nd|\d+\d3rd"

rgxNumberL1 = r"\d+\/\d+|\d(?:[\.,-\/]?\d)*(?:\.\d+)?"

rgxMention = r"@\w+"

rgxHashtagL1 = r"#[A-z][a-z0-9]*"

rgxEmail = r"[-!#$%&'*+\/=?^\w{|}~](?:\.?[-!#$%&'*+\/=?^\w`{|}~])*@[a-z0-9](?:-?\.?[a-z0-9])*(?:\.[a-z](?:-?[a-z0-9])*)+"

rgxCurrency = r"[₿₽₹₨$£¥€₩]"

rgxPunctuation = r"[’'‘’`“”\"\[\]\(\){}…,\.!;\?\-:\u0964\u0965]"

rgxQuotedPhrase = r"\"[^\"]*\""

rgxURL = r"(?:https?:\/\/)(?:[\da-z\.-]+)\.(?:[a-z\.]{2,6})(?:[\/\w\.\-\?#=]*)*\/?"

#rgxEmoji = r"[\U00010000-\U0010ffff]"
rgxEmoji = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

rgxEmoticon = r":-?[dps\*\/\[\]{}\(\)]|;-?[/(/)d]|<3"

rgxTime = r"(?:\d|[01]\d|2[0-3]):?(?:[0-5][0-9])?\s?(?:[ap]\.?m\.?|hours|hrs)"

#rgxWordL1 = r"[a-z\u00C0\u00D6\u00D8\u00F6\u00F8\u00FF][a-z\u00C0\u00D6\u00D8\u00F6\u00F8\u00FF']*"
rgxWordL1 = r"[A-z\u00C0\u00D6\u00D8\u00F6\u00F8\u00FF][a-z\u00C0\u00D6\u00D8\u00F6\u00F8\u00FF']*"

rgxSymbol = r"[\u0950~@#%\^\+=\*\|\/<>&]"

rgxContraction = r"'"

rgxPosSingular = r"([a-z]+)('s)$"

rgxPosPlural = r"([a-z]+s)(')$"

rgxsMaster = [
    {'regex': rgxQuotedPhrase, 'category': 'quoted_phrase'},
    {'regex': rgxURL, 'category': 'url'},
    {'regex': rgxEmail, 'category': 'email'},
    {'regex': rgxMention, 'category': 'mention'},
    {'regex': rgxHashtagL1, 'category': 'hashtag'},
    {'regex': rgxEmoji, 'category': 'emoji'},
    {'regex': rgxEmoticon, 'category': 'emoticon'},
    {'regex': rgxTime, 'category': 'time'},
    {'regex': rgxOrdinalL1, 'category': 'ordinal'},
    {'regex': rgxNumberL1, 'category': 'number'},
    {'regex': rgxCurrency, 'category': 'currency'},
    {'regex': rgxWordL1, 'category': 'word'},
    {'regex': rgxPunctuation, 'category': 'punctuation'},
    {'regex': rgxSymbol, 'category': 'symbol'}

]
rgxs = rgxsMaster

fingerPrintCodes = {
  'emoticon': 'c',
  'email': 'e',
  'emoji': 'j',
  'hashtag': 'h',
  'mention': 'm',
  'number': 'n',
  'ordinal': 'o',
  'quoted_phrase': 'q', # eslint-disable-line camelcase
  'currency': 'r',
  # symbol: 's',
  'time': 't',
  'url': 'u',
  'word': 'w',
  'alien': 'z'
}

finalTokens = []

def delfirstelementlist(list):
    if len(list) != 0:
        lenlist = len(list) - 1
        if lenlist != 1:
            return list[-lenlist:]
        else:
            return []

    else:
        return list




def manageContraction( word, tokens ):
    ct = contractions[word]
    matches = ''
    if ct == 'undefined':
        # Try possesive of sigular & plural forms
        matches = re.findall(rgxPosSingular, word)
        if matches:
            tokens.append( { 'value': matches[ 1 ], 'tag': 'word' } )
            tokens.append( { 'value': matches[ 2 ], 'tag': 'word' } )
        else:
            matches = re.findall(rgxPosPlural, word)
            if  matches:
                tokens.append( { 'value': matches[ 1 ], 'tag': 'word' } )
                tokens.append( { 'value': matches[ 2 ], 'tag': 'word' } );
            else:
                tokens.push( { 'value': word, 'tag': 'word' } )

    else:
      # Manage via lookup; ensure cloning!
      tokens.append( ct[ 0 ] );
      tokens.append( ct[ 1 ] );
      if ct[ 2 ]:
          tokens.push( ct[ 2 ] );

    return tokens
   # manageContraction()


def tokenizeTextUnit( text, rgxSplit ):
    # Regex matches go here; note each match is a token and has the same tag
    # as of regex's category.
    if rgxSplit['category'] == 'emoji':
        text = unicode(text, "utf-8")
    matches = re.findall(rgxSplit['regex'], text)
    # Balance is "what needs to be tokenized".
    balance = re.compile(rgxSplit['regex']).split(text)

    if rgxSplit['category'] == 'emoji':
        balancetmp = balance
        balance = []
        [balance.append(bal.encode('utf-8')) for bal in balancetmp]

    # The result, in form of combination of tokens & matches, is captured here.
    tokens = []
    # The tag;
    tag = rgxSplit['category']
    # Helper variables.

    k = 0

    # Combine tokens & matches in the following pattern [ b0 m0 b1 m1 ... ]
    if matches:
        matches = matches
    else:
        matches = []

    for i in range(len(balance)):
        t = balance[ i ]
        t = t.strip()
        if t:
            tokens.append(t)
        if k < len(matches):
            if tag == 'word':
                #Tag type `word` token may have a contraction.
                aword = matches[k]
                if rgxContraction == aword:
                    tokens = manageContraction(aword, tokens)
                else:
                    #// Means there is no contraction.
                    tokens.append( { 'value': aword, 'tag': tag } )
            else:
                tokens.append({'value': matches[k], 'tag': tag})

        k += 1

    return tokens



def tokenizeTextRecursively( text, regexes ):
    sentence = text.strip()
    global finalTokens
    if len(regexes) == 0:
      # No regex left, split on `spaces` and tag every token as **alien**.
        for tkn in re.compile(rgxSpaces).split(text):
            finalTokens.append({'value': tkn, 'tag': 'alien'})
        return finalTokens

    rgx = regexes[ 0 ]
    tokens = tokenizeTextUnit( sentence, rgx )

    for i in range(len(tokens)):
        if type(tokens[i]) is str:
            tokenizeTextRecursively(tokens[i], delfirstelementlist(regexes))
        else:
            finalTokens.append(tokens[i])



def tokenize( sentence ):
    global finalTokens
    tokenizeTextRecursively( sentence, rgxs )
    response = finalTokens
    finalTokens = []
    return response


#print(tokenize( '@superman: hit me up on my email r2d2@gmail.com, 2 of us plan party🎉 tom at 3pm:) #fun' ))
