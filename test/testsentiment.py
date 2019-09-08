# -*- coding: utf8 -*-
import unittest
import sys,os
sys.path.append(os.path.abspath('..'))
from sentiment.sentiment import sentiment as sen


class TestSentimentScore(unittest.TestCase):

    def setUp(self):
        pass

    # Returns True if the string contains 4 a.
    def test1(self):
        global sen
        self.assertEqual(sen('I am feeling Good'), {'normalizedScore': 2.0,
                                                    'score': 4,
                                                    'tokenizedPhrase': [
                                                        {'tag': 'word', 'value': 'I'},
                                                        {'tag': 'word', 'value': 'am'},
                                                        {'tag': 'word', 'score': 1, 'value': 'feeling'},
                                                        {'tag': 'word', 'score': 3, 'value': 'Good'}]
                                                    }
                         )

    def test2(self):
        global sen
        self.assertEqual(sen('Not a good product'), {'normalizedScore': -3.0,
                                                     'score': -3,
                                                     'tokenizedPhrase': [
                                                         {'tag': 'word', 'value': 'Not'},
                                                         {'tag': 'word', 'negation': True, 'value': 'a'},
                                                         {'score': -3, 'tag': 'word', 'negation': True, 'value': 'good'},
                                                         {'tag': 'word', 'negation': True, 'value': 'product'}]
                                                     }
                         )

    def test1(self):
        global sen
        self.assertEqual(sen('Not good product'), {'normalizedScore': -3.0,
                                                   'score': -3,
                                                   'tokenizedPhrase': [{'tag': 'word', 'value': 'Not'},
                                                                       {'score': -3, 'tag': 'word', 'negation': True, 'value': 'good'},
                                                                       {'tag': 'word', 'negation': True, 'value': 'product'}]
                                                   }
                         )

    def test3(self):
        global sen
        self.assertEqual(sen('good product'), {'normalizedScore': 3.0,
                                               'score': 3,
                                               'tokenizedPhrase': [{'tag': 'word', 'score': 3, 'value': 'good'},
                                                                   {'tag': 'word', 'value': 'product'}]
                                               }
                         )

    def test4(self):
        global sen
        self.assertEqual(sen('it was my bad Luck'), {'normalizedScore': -2.0,
                                                     'score': -2,
                                                     'tokenizedPhrase': [{'tag': 'word', 'value': 'it'},
                                                                         {'tag': 'word', 'value': 'was'},
                                                                         {'tag': 'word', 'value': 'my'},
                                                                         {'grouped': 1, 'tag': 'word', 'score': -2, 'value': 'bad'},
                                                                         {'tag': 'word', 'value': 'Luck'}]
                                                     }
                         )

    def test5(self):
        global sen
        self.assertEqual(sen('it was not my bad luck'), {'normalizedScore': 2.0,
                                                         'score': 2,
                                                         'tokenizedPhrase': [{'tag': 'word', 'value': 'it'},
                                                                             {'tag': 'word', 'value': 'was'},
                                                                             {'tag': 'word', 'value': 'not'},
                                                                             {'tag': 'word', 'negation': True, 'value': 'my'},
                                                                             {'score': 2, 'grouped': 1, 'tag': 'word', 'negation': True, 'value': 'bad'},
                                                                             {'tag': 'word', 'value': 'luck'}]
                                                         }
                         )

    def test6(self):
        global sen
        self.assertEqual(sen('love you <3'), {'normalizedScore': 3.0,
                                              'score': 6,
                                              'tokenizedPhrase': [{'tag': 'word', 'score': 3, 'value': 'love'},
                                                                  {'tag': 'word', 'value': 'you'},
                                                                  {'tag': 'emoticon', 'score': 3, 'value': '<3'}]
                                              }
                         )

    def test7(self):
        global sen
        self.assertEqual(sen('love you<3'), {'normalizedScore': 3.0,
                                             'score': 6,
                                             'tokenizedPhrase': [{'tag': 'word', 'score': 3, 'value': 'love'},
                                                                 {'tag': 'word', 'value': 'you'},
                                                                 {'tag': 'emoticon', 'score': 3, 'value': '<3'}]
                                             }
                         )


    def test8(self):
        global sen
        self.assertEqual(sen('love you<3 😍😃'), {'normalizedScore': 3.0,
                                                  'score': 6,
                                                  'tokenizedPhrase': [{'tag': 'word', 'score': 3, 'value': 'love'},
                                                                      {'tag': 'word', 'value': 'you'},
                                                                      {'tag': 'emoticon', 'score': 3, 'value': '<3'},
                                                                      {'tag': 'emoji', 'value': u'\U0001f60d\U0001f603'}]
                                                  }
                         )


    def test9(self):
        global sen
        self.assertEqual(sen('unknownword'), {'normalizedScore': 0.0,
                                              'score': 0,
                                              'tokenizedPhrase': [{'tag': 'word', 'value': 'unknownword'}]
                                              }
                         )


    def test10(self):
        global sen
        self.assertEqual(sen('🚀'), {'normalizedScore': 0.0,
                                     'score': 0,
                                     'tokenizedPhrase': [{'tag': 'emoji', 'value': u'\U0001f680'}]
                                     }
                         )

    def test11(self):
        global sen
        self.assertEqual(sen(';/'), {'normalizedScore': 0.0,
                                     'score': 0,
                                     'tokenizedPhrase': [{'tag': 'emoticon', 'value': ';/'}]
                                     }
                         )

    def test12(self):
        global sen
        self.assertEqual(sen('useless🚀 product;/'), {'normalizedScore': -2.0,
                                                      'score': -2,
                                                      'tokenizedPhrase': [{'tag': 'word', 'score': -2, 'value': 'useless'},
                                                                          {'tag': 'emoji', 'value': u'\U0001f680'},
                                                                          {'tag': 'word', 'value': 'product'},
                                                                          {'tag': 'emoticon', 'value': ';/'}]
                                                      }
                         )

    def test13(self):
        global sen
        self.assertEqual(sen('#love you<3 😍😃 #unknown'), {'normalizedScore': 3.0,
                                                            'score': 6,
                                                            'tokenizedPhrase': [{'tag': 'hashtag', 'score': 3, 'value': '#love'},
                                                                                {'tag': 'word', 'value': 'you'},
                                                                                {'tag': 'emoticon', 'score': 3, 'value': '<3'},
                                                                                {'tag': 'emoji', 'value': u'\U0001f60d\U0001f603'},
                                                                                {'tag': 'hashtag', 'value': '#unknown'}]
                                                            }
                         )

    def test14(self):
        global sen
        self.assertEqual(sen('I am feeling Good'), {'normalizedScore': 2.0,
                                                    'score': 4,
                                                    'tokenizedPhrase': [
                                                        {'tag': 'word', 'value': 'I'},
                                                        {'tag': 'word', 'value': 'am'},
                                                        {'tag': 'word', 'score': 1, 'value': 'feeling'},
                                                        {'tag': 'word', 'score': 3, 'value': 'Good'}]
                                                    }
                         )

    def test15(self):
        global sen
        self.assertEqual(sen('I am feeling Good'), {'normalizedScore': 2.0,
                                                    'score': 4,
                                                    'tokenizedPhrase': [
                                                        {'tag': 'word', 'value': 'I'},
                                                        {'tag': 'word', 'value': 'am'},
                                                        {'tag': 'word', 'score': 1, 'value': 'feeling'},
                                                        {'tag': 'word', 'score': 3, 'value': 'Good'}]
                                                    }
                         )

    def test16(self):
        global sen
        self.assertEqual(sen('I am feeling Good'), {'normalizedScore': 2.0,
                                                    'score': 4,
                                                    'tokenizedPhrase': [
                                                        {'tag': 'word', 'value': 'I'},
                                                        {'tag': 'word', 'value': 'am'},
                                                        {'tag': 'word', 'score': 1, 'value': 'feeling'},
                                                        {'tag': 'word', 'score': 3, 'value': 'Good'}]
                                                    }
                         )

    def test17(self):
        global sen
        self.assertEqual(sen('I am feeling Good'), {'normalizedScore': 2.0,
                                                    'score': 4,
                                                    'tokenizedPhrase': [
                                                        {'tag': 'word', 'value': 'I'},
                                                        {'tag': 'word', 'value': 'am'},
                                                        {'tag': 'word', 'score': 1, 'value': 'feeling'},
                                                        {'tag': 'word', 'score': 3, 'value': 'Good'}]
                                                    }
                         )



if __name__ == '__main__':
    unittest.main()