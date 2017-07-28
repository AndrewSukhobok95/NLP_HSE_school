# -*- coding: utf-8 -*-
import sys

if len(sys.argv)<2:
  print "using:\n python ./gen-subjList.py list-of-texts.{opin.txt,ann} > subjList.txt"
  exit(-1)

SubjSet = set([])
for fn in sys.argv[1:]:
  ll=open(fn).readlines()
  if fn.rfind(".opin.txt")>0:
    wl = [l.decode("utf8").split(", ") for l in ll if len(l.decode("utf8").split(", "))>=4]
    for l in wl: SubjSet.update([l[0].strip(), l[1].strip()])
  elif fn.rfind(".ann")>0:
    wl = [l.decode("utf8").split("\t") for l in ll if len(l.decode("utf8").split("\t"))>=3]
    for l in wl: SubjSet.update([" ".join(l[2:]).strip()])
for w in SubjSet: print w.encode("utf8")

