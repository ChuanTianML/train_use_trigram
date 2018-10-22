# encoding=utf-8

import sys
import argparse
import cPickle as pickle

# functions
def word2id(word):
    if word in w2id: return w2id[word]
    else:            return w2id[unkWord]

def updTriGramOne(wid1, wid2, wid3):
    tgKey = (wid1, wid2, wid3)
    if tgKey in tg2f: tg2f[tgKey] += 1.0
    else:             tg2f[tgKey] = 1.0

def staticUnk(wid1, wid2, wid3, w1, w2, w3):
    tgKey = (wid1, wid2, wid3)
    if w2id[unkWord] in tgKey:
        wsCmbTg = (w1, w2, w3)
        if tgKey in unkCmb2NumTg:
            if not wsCmbTg in unkCmb2NumTg[tgKey]: unkCmb2NumTg[tgKey].add(wsCmbTg)
        else:
            unkCmb2NumTg[tgKey] = set([wsCmbTg])

def updateGramBaseSentence(sent):
    if 1==args.recut:
        sent = ''.join(sent.split())
        ws = [w.encode('utf-8') for w in jieba.lcut(sent)]
    else:
        ws = sent.split()
    ws = [frtWord,scdWord] + ws + [lstWord]
    wids = [word2id(w) for w in ws]
    for i in range(len(ws)-2):
        [wid1,wid2,wid3] = wids[i:i+3]
        updTriGramOne(wid1, wid2, wid3)
        staticUnk(wid1, wid2, wid3, ws[i], ws[i+1], ws[i+2])
              

# main
print '\n\nTRIGRAM.'
## params
args = argparse.ArgumentParser('Input Parameters.')
args.add_argument('-iPath', type=str, dest='iPath', help='corpus file path.')
args.add_argument('-vocPath', type=str, dest='vocPath', help='vocabulary file path.')
args.add_argument('-triGramPath', type=str, dest='triGramPath', help='tri-gram dump path.')
args.add_argument('-recut', type=int, dest='recut', help='whether recut using jieba.')
args = args.parse_args()
if 1==args.recut:
    import jieba

w2id = {}   # word to id; id start from 0.
tg2f = {}   # tri-gram. ((wid1, wid2, wid3): freq)
unkWord = '<unk>'
frtWord = '<s1>'
scdWord = '<s2>'
lstWord = '</tail>'

### auxiliary variable
unkCmb2NumTg = {}

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
for tgK in unkCmb2NumTg: tg2f[tgK] = float(tg2f[tgK]) / len(unkCmb2NumTg[tgK])
for k in tg2f: 
    tg2f[k] = int(tg2f[k]) # trans to int
    assert not 0 == tg2f[k]
print '<unk> related items averaged.'

## dump to disk
triGramFile = open(args.triGramPath, 'wb')
pickle.dump(tg2f, triGramFile, pickle.HIGHEST_PROTOCOL)
triGramFile.close()
print('model is dumped to %s.' % args.triGramPath)


