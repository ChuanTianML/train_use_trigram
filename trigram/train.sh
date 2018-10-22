#!/bin/bash

VOC_SIZE=40000
#CORPUS_PATH=demo_corpus.txt
RECUT_USING_JIEBA=0
CORPUS_PATH=/mnt/t-chtian/dataClean/data/not_scored/corpus.unk.cuted.txt
VOC_PATH=./model/base/vocab.txt
TRIGRAM_PATH=./model/base/trigram.pkl

time python vocab.py -iPath $CORPUS_PATH -oPath $VOC_PATH  -vocSize $VOC_SIZE -recut $RECUT_USING_JIEBA
time python trigram.py -iPath $CORPUS_PATH -vocPath $VOC_PATH -triGramPath $TRIGRAM_PATH -recut $RECUT_USING_JIEBA

