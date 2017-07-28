# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

if len(sys.argv)<2:
  print "using:\n python ./koref.py subjList.txt"
  exit(-1)

lw=[w.decode("utf8").strip().lower() for w in open(sys.argv[1]).readlines()]
#for w in lw: print w

from gensim.models.keyedvectors import KeyedVectors

#wiki = KeyedVectors.load_word2vec_format("models/ruwikiruscorpora_rusvectores2.bin", binary=True)
rkw = KeyedVectors.load_word2vec_format("models/ruwikiruscorpora_0_300_20.bin", binary=True)

subjVec = dict([(w,rkw[w+"_NOUN"]) for w in lw if rkw.__contains__(w+"_NOUN")])
print len(lw), "subjects in file;", len(subjVec), "subjects in w2v model."

def get_coref_subject(s):
  '''Интерфейс. Получает слово
  проверяет, есть ли оно в списке терминов, если есть - возвращает исходное;
  проверяет, есть ли оно в модели w2v, если есть - возвращает наиболее семантически близкий термин из списка;
  в другом случае возвращает пустую строку '''
  if s in lw: return s
  elif rkw.__contains__(s+"_NOUN"): return max([(rkw.similarity(s+"_NOUN", w+"_NOUN"), w) for w in subjVec])[1]
  else: return ""

def print_coref(subj_list):
  for s in subj_list:
    print s,"->",get_coref_subject(s),": ",
    if s in lw: print "The term"
    elif rkw.__contains__(s+"_NOUN"):
      wn = [(rkw.similarity(s+"_NOUN", w+"_NOUN"), w) for w in subjVec]
      print "co-ref:",
      for w in sorted(wn, key=lambda vw: -vw[0])[:10]: print w[1],w[0],
      print
    else: print "not in model"

test_list = (
 (u"украина",u"россия",-10,u""),
 (u"россия",u"украина",-3,u""),
 (u"россия",u"сирия",3,u""),
 (u"кремль",u"сирия",3,u""),
 (u"сша",u"сирия",-3,u""),
 (u"пентагон",u"сирия",-4,u""),
)

sl1 = [t[0] for t in test_list]
sl2 = [t[1] for t in test_list]
print_coref(set(sl1)|set(sl2))
