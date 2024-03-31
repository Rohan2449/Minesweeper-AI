from minesweeper import *


sentence_1 = Sentence({(1,2), (2,3) }, 1)
sentence_2 = Sentence({(1,2)}, 1)
sentence_3 = Sentence({(1,3)}, 0)

print(is_subset(sentence_1, sentence_2))
print(is_subset(sentence_1, sentence_3))
