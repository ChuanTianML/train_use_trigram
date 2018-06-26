#encoding=utf-8

from trigram.tool import *

trigram = Trigram()
ip_file = open('./test_data/test.data', 'r')
op_file = open('./test_data/result.txt', 'w')
for line in ip_file:
    log_prob = trigram.log_probability_sentence(line)
    op_file.write('%.4f\t%s' % (log_prob, line))

op_file.close()
ip_file.close()


