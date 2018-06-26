# encoding=utf-8

import sys
import jieba
import argparse
import cPickle as pickle

# functions
def word2id(word):
    if word in w2id:
        return w2id[word]
    else:
        return w2id[unkWord]

def updUniGramFreqOne(wid1):
    if wid1 in ug2f:
        ug2f[wid1] += 1.0
    else:
        ug2f[wid1] = 1.0

def updUniGramNumOne(wid1, wid2):
    if wid1 in ug2ws:
        ug2ws[wid1].add(wid2)
    else:
        ug2ws[wid1] = set([wid2])
    if wid2 in ug2wsR:
        ug2wsR[wid2].add(wid1)
    else:
        ug2wsR[wid2] = set([wid1])

def updBiGramFreqOne(wid1, wid2):
    bgKey = (wid1, wid2)
    if bgKey in bg2f:
        bg2f[bgKey] += 1.0
    else:
        bg2f[bgKey] = 1.0

def updBiGramNumOne(wid1, wid2, wid3):
    bgKey = (wid1, wid2)
    if bgKey in bg2ws:
        bg2ws[bgKey].add(wid3)
    else:
        bg2ws[bgKey] = set([wid3])

def updTriGramOne(wid1, wid2, wid3):
    tgKey = (wid1, wid2, wid3)
    if tgKey in tg2f: 
        tg2f[tgKey] += 1.0
    else:
        tg2f[tgKey] = 1.0

def staticUnk(wid1, wid2, wid3, w1, w2, w3):
    ugKey = wid1
    bgKey = (wid1, wid2)
    tgKey = (wid1, wid2, wid3)
    if w2id[unkWord] == ugKey:
        unkWordSet.add(w1)
    if w2id[unkWord] in bgKey:
        wsCmbBg = (w1, w2)
        if bgKey in unkCmb2NumBg:
            if not wsCmbBg in unkCmb2NumBg[bgKey]: unkCmb2NumBg[bgKey].add(wsCmbBg)
        else:
            unkCmb2NumBg[bgKey] = set([wsCmbBg])
    if w2id[unkWord] in tgKey:
        wsCmbTg = (w1, w2, w3)
        if tgKey in unkCmb2NumTg:
            if not wsCmbTg in unkCmb2NumTg[tgKey]: unkCmb2NumTg[tgKey].add(wsCmbTg)
        else:
            unkCmb2NumTg[tgKey] = set([wsCmbTg])

def updateGramBaseSentence(sent):
    sent = ''.join(sent.split())
    ws = [w.encode('utf-8') for w in jieba.lcut(sent)]
    ws = [frtWord,scdWord] + ws + [lstWord]
    wids = [word2id(w) for w in ws]
    for i in range(len(ws)-2):
        wid1 = wids[i]
        wid2 = wids[i+1]
        wid3 = wids[i+2]
        updUniGramFreqOne(wid1)
        updUniGramNumOne(wid1, wid2)
        updBiGramFreqOne(wid1, wid2)
        updBiGramNumOne(wid1, wid2, wid3)
        updTriGramOne(wid1, wid2, wid3)
        staticUnk(wid1, wid2, wid3, ws[i], ws[i+1], ws[i+2])
              
    # little tail 
    updBiGramFreqOne(wids[-2], wids[-1])
    updUniGramFreqOne(wids[-2])
    updUniGramNumOne(wids[-2], wids[-1])
    updUniGramFreqOne(wids[-1])
    if wids[-2] == w2id[unkWord]:
        unkWordSet.add(ws[-2])
    if wids[-1] == w2id[unkWord]:
        unkWordSet.add(ws[-2])



# main
print '\n\nTRIGRAM.'
## params
args = argparse.ArgumentParser('Input Parameters.')
args.add_argument('-iPath', type=str, dest='iPath', help='corpus file path.')
args.add_argument('-vocPath', type=str, dest='vocPath', help='vocabulary file path.')
args.add_argument('-triGramPath', type=str, dest='triGramPath', help='tri-gram dump path.')
args = args.parse_args()

w2id = {}   # word to id; id start from 0.
ug2f = {}   # uni-gram. (wid: freq)
bg2f = {}   # bi-gram.  ((wid1, wid2): freq)
tg2f = {}   # tri-gram. ((wid1, wid2, wid3): freq)
unkWord = '<unk>'
frtWord = '<s1>'
scdWord = '<s2>'
lstWord = '</tail>'

### used by Kneser-Ney smoothing.
ug2n = {}   # mapping from   uni-gram    to  [the number of word types that occur after it].   (wid: num)
ug2nR = {}  # mapping from   uni-gram    to  [the number of word types that occur befort it].  (wid: num)
bg2n = {}   # mapping from   bi-gram     to  [the number of word types that occur after it].   ((wid1, wid2): num)

### auxiliary variables
ug2ws = {}  # mapping from   uni-gram    to  [the set of word types that occur after it].      (wid: set)
ug2wsR = {} # mapping from   uni-gram    to  [the set of word types that occur befort it].     (wid: set)
bg2ws = {}  # mapping from   bi-gram     to  [the set of word types that occur after it].      ((wid1, wid2): set)
unkCmb2NumTg = {}
unkCmb2NumBg = {}
unkCmb2NumUg = {}
unkWordSet = set()

## load vocabulary
vocFile = open(args.vocPath, 'r')
idx = 0
for line in vocFile:
    w,_ = line.strip().split('\t')
    w2id[w] = idx
    idx += 1
helpWords = [frtWord, scdWord, lstWord]
for w in helpWords:
    w2id[w] = idx
    idx += 1

## statistic n-gram
### statistic n-gram
crpFile = open(args.iPath, 'r')
idx = 0
for line in crpFile:
    updateGramBaseSentence(line.strip())
    idx += 1
    if 0 == idx % 10000:
        sys.stdout.write('%dw lines processed\r' % (idx/10000))
        sys.stdout.flush()
    #if idx > 100: break # debug
crpFile.close()

### average unk combination
if not 0 == len(unkWordSet): ug2f[w2id[unkWord]] = float(ug2f[w2id[unkWord]]) / len(unkWordSet) 
for tgK in unkCmb2NumTg: tg2f[tgK] = float(tg2f[tgK]) / len(unkCmb2NumTg[tgK])
for bgK in unkCmb2NumBg: bg2f[bgK] = float(bg2f[bgK]) / len(unkCmb2NumBg[bgK])
print 'ug2f, bg2f and tg2f: <unk> related items averaged.'

### get ngram to num, and average unk combination
for ng in ug2ws:  ug2n[ng]  = float(len(ug2ws[ng]))
for ng in ug2wsR: ug2nR[ng] = float(len(ug2wsR[ng]))
for ng in bg2ws:  bg2n[ng]  = float(len(bg2ws[ng]))
if not 0 == len(unkWordSet):
    ug2n[w2id[unkWord]]  = float(ug2n[w2id[unkWord]])  / len(unkWordSet)
    ug2nR[w2id[unkWord]] = float(ug2nR[w2id[unkWord]]) / len(unkWordSet)
for bgK in unkCmb2NumBg: bg2n[bgK] = float(bg2n[bgK]) / len(unkCmb2NumBg[bgK])
print 'ug2n, ug2nR and bg2n: <unk> related items averaged.'

## dump to disk
triGramFile = open(args.triGramPath, 'wb')
pickle.dump((ug2f, bg2f, tg2f, ug2n, ug2nR, bg2n), triGramFile, pickle.HIGHEST_PROTOCOL)
triGramFile.close()
print('model is dumped to %s.' % args.triGramPath)

