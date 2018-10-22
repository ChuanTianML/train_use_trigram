# encoding=utf-8

import sys
import argparse


# functions
def updateVocabBaseSentence(sent):
    if 1==args.recut:
        sent = ''.join(sent.split())
        ws = [w.encode('utf-8') for w in jieba.lcut(sent)]
    else:
        ws = sent.split()
    for w in ws:
        if w in w2f:
            w2f[w] += 1
        else:
            w2f[w] = 1

def w2fSortKey(elem):
    return elem[1]

# main
print '\n\nVOCAB'

## params
args = argparse.ArgumentParser('Input Parameters.')
args.add_argument('-iPath', type=str, dest='iPath', help='corpus file path.')
args.add_argument('-oPath', type=str, dest='oPath', help='vocabulary file output path.')
args.add_argument('-vocSize', type=int, dest='vocSize', help='the max size of the vocab.')
args.add_argument('-recut', type=int, dest='recut', help='whether recut using jieba.')
args = args.parse_args()
unkWord = '<unk>'
w2f = {}
if 1==args.recut:
    import jieba


## extract words and frequency
iFile = open(args.iPath, 'r')
idx = 0
for line in iFile:
    updateVocabBaseSentence(line.strip())
    idx += 1
    if 0 == idx % 10000:
        sys.stdout.write('%dw lines processed\r' % (idx/10000))
        sys.stdout.flush()
    #if idx > 100: break # debug

## output the first N words
### trans to list and sort
w2fLs =  [(k,w2f[k]) for k in w2f]
w2fLs.sort(key=w2fSortKey, reverse=True)
vocFile = open(args.oPath, 'w')
for w,f in w2fLs[:min(args.vocSize, len(w2fLs))]:
    vocFile.write('%s\t%d\n' % (w,f))

### unknown word
assert (unkWord not in w2f)
if args.vocSize >= len(w2fLs):
    vocFile.write('%s\t%d\n' % (unkWord, 0))
else:
    unkCnt = sum([ele[1] for ele in w2fLs[args.vocSize:]])
    unkNum = len(w2fLs) - args.vocSize
    vocFile.write('%s\t%d\n' % (unkWord, unkCnt/unkNum)) # use average frequency as <unk> frequency

vocFile.close()
iFile.close()
print('output %d words including <unk>.' % (min(args.vocSize, len(w2fLs))+1))

