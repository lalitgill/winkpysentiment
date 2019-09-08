# -*- coding: utf8 -*-
from emojis import emojis
from afinn_en_165 import afinn
from emoticons import emoticons
from negations import negations
from afinn_en_165_2grams import afinn2Grams as affin2Grams
from tokenizer.tokenizer import tokenize
import sys,math




#/* eslint max-depth: 0 */

### normalize
"""
 *
 * Computes the normalized sentiment score from the absolute scores.
 *
 * @param {number} hss absolute sentiment scrore of hashtags.
 * @param {number} wss absolute sentiment scrore of words/emojis/emoticons.
 * @param {number} sentiHashtags number of hashtags that have an associated sentiment score.
 * @param {number} sentiWords wnumber of words that have an associated sentiment score.
 * @param {number} totalWords total number of words in the text.
 * @return {number} normalized score.
 * @private
"""


def normalize( hss, wss, sentiHashtags, sentiWords, totalWords ):
    ## **N**ormalized **h**ashtags & **w**ords **s**entiment **s**cores.
    nhss = float(0)
    nwss = float(0)
    totalWords = float(totalWords)
    ## 1. Normalize hashtags sentiment score by computing the average.
    if sentiHashtags:
        nhss = hss / sentiHashtags;
    if sentiWords:
        ## 2. Normalize words sentiment score by computing the average.
        nwss = float(wss) / float(sentiWords)
        ## 3. Normalized words sentiment score is further adjusted on the basis of the
        ## total number of words in the text.
        ## Average sentence length in words (assumed).
        avgLength = float(15)
        ## Make adjustments.
        #nwss /= Math.sqrt((totalWords > avgLength) ? (totalWords / avgLength) 1 )
        if totalWords > avgLength:
            nwss_tmp =  math.sqrt(totalWords / avgLength)
        else:
            nwss_tmp = float(1)

        nwss /= nwss_tmp
    if nhss and nwss:
        return  ((nhss + nwss) / 2)
    else:
        if nwss:
            return nwss
        else:
            return nhss
    #return ( nhss && nwss ) ? ( ( nhss + nwss ) / 2 ) : ( nwss || nhss );
### sentiment
"""
 *
 * Computes the absolue and normalized sentiment scores of the input `phrase`,
 * after tokenizing it.
 *
 * The normalized score is computed by taking into account of absolute scores of
 * words, emojis, emoticons, and hashtags and adjusting it on the basis of total
 * words in the text; this is always between -5 and +5. A score of less than 0 indicates
 * negative sentiments and a score of more than 0 indicates positive sentiments;
 * wheras a near zero score suggests a neutral sentiment. While counting tokens
 * only the ones tagged as **`word`**, **`emoji`**, or **`emoticon`** are counted;
 * and one letter words are ignored.
 *
 * It performs tokenization using [wink-tokenizer](http://winkjs.org/wink-tokenizer/).
 * During sentiment analysis, each token may be assigned up to 3 new properties.
 * These properties are:
 *
 * 1. **`score`** — contains the sentiment score of the word, emoji, emoticon or hashtag, which is always
 * between -5 and +5. This is added only when the word in question has a positive or
 * negative sentiment associated with it.
 * 2. **`negation`** — is added & set to **true** whenever the `score` of the
 * token has beeen impacted due to a negation word apprearing prior to it.
 * 3. **`grouped`** — is added whenever, the token is the first
 * word of a short idiom or a phrase. It's value provides the number of tokens
 * that have been grouped together to form the phrase/idiom.
 *
 * @param {string} phrase whoes sentiment score needs to be computed.
 * @return {object} absolute `score`, `normalizedScore` and `tokenizedPhrase` of `phrase`.
 *
 * @example
 * sentiment( 'not a good product #fail' );
 * // -> { score: -5,
 * //      normalizedScore: -2.5,
 * //      tokenizedPhrase: [
 * //        { value: 'not', tag: 'word' },
 * //        { value: 'a', tag: 'word' },
 * //        { value: 'good', tag: 'word', negation: true, score: -3 },
 * //        { value: 'product', tag: 'word' },
 * //        { value: '#fail', tag: 'hashtag', score: -2 }
 * //      ]
 * //    }
 """

#switcher = {
#        'emoji': "switchemoji",
#        'emoticon': "switchemoticon",
#        'hashtag': "switchhashtag",
#        'word':"switchword"
#    }
#def switchemoji(t,ss,tkn,sentiWords,words):
#    global emojis
#    tss = emojis[t];
#    if tss:
#        ss += tss;
#        tkn.score = tss;
#        sentiWords += 1;
#    words += 1;

#def default():
#    return ''

#def switch(tag,a):
#    return switcher.get(tag, default)(a)


def sentiment( phrase ):
    if type(phrase) is not str:
        raise Exception('sentiment: input phrase must be a string, instead found: '. type(phrase))

    # Early exit.
    tokenizedPhrase = tokenize( phrase )
    if len(tokenizedPhrase) == 0:
        return { 'score': 0, 'normalizedScore': 0 }

    # Sentiment Score.
    ss = 0
    # Hash Tags SS.
    hss = 0
    # Number of sentiment containing hashtags and words encountered.
    sentiHashtags = 0
    sentiWords = 0
    # Number of words encountered.
    words = 0
    wc = 0
    # Helpers: for loop indexes, token, temp ss, and word count.
    #var k, kmax, t, tkn, tss, wc;
    tss = ''
    precedingNegation = False
    for k in range(len(tokenizedPhrase)):
        if wc == 2:
            wc = 0
            continue
        tkn = tokenizedPhrase[ k ]
        t = tkn['value']
        tss = 0
        if  tokenizedPhrase[ k ]['tag'] == 'punctuation':
            precedingNegation = False

        if tkn['tag'] == 'emoji':
            try:
                tss = emojis[t]
            except KeyError:
                pass
            if tss:
                ss += tss
                tkn['score'] = tss
                sentiWords += 1
            words += 1
        elif tkn['tag'] == 'emoticon':
            try:
                tss = emoticons[t]
            except KeyError:
                pass
            if tss:
                ss += tss
                tkn['score'] = tss
                sentiWords += 1
            words += 1
        elif tkn['tag'] == 'hashtag':
            if t[1:].lower() in afinn: tss = afinn[t[1:].lower()]
            if tss:
                tkn['score'] = tss
                hss += tss
                sentiHashtags += 1
        elif tkn['tag'] == 'word':
            t = t.lower()
            wc = 1
            # Check for bigram configurations i.e. token at `k` and `k+1`. Accordingly
            # compute the sentiment score in `tss`. Convert to Lower Case for case insensitive comparison.
            if k < (len(tokenizedPhrase) - 1) and t in affin2Grams:
                if tokenizedPhrase[k + 1]['value'].lower() in affin2Grams[t]:
                    tss = affin2Grams[t][tokenizedPhrase[k + 1]['value'].lower()]
                    tkn['grouped'] = 1
                    # Will have to count `2` words!
                    wc = 2
                # sentiWords += 1
            else:
                if t in afinn:
                    tss = afinn[t]
                else:
                    tss = 0
                #tss = afinn[t] || 0
                # sentiWords += 1;

            # flip the the score if negation flag is true
            if precedingNegation == True:
                tss = -tss
                tkn['negation'] = True

            # change code check negation. mark negation flag true when negation word in sentence
            if t in negations and wc == 1 :
                precedingNegation = True

            ss += tss
            k += (wc - 1)
            if tss:
                tkn['score'] = tss
                sentiWords += 1

            # Update number of words accordingly.
            words += wc

    #print(normalize(hss, ss, sentiHashtags, sentiWords, words))

    return {
        'score': (ss + hss),
        'normalizedScore': round(normalize(hss, ss, sentiHashtags, sentiWords, words),2),
        'tokenizedPhrase': tokenizedPhrase
    }