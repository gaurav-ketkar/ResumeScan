import pprint
from collections import Counter

match = {'OOPs,', 'Database,', 'Github,', 'C++', 'Java,'};


c = Counter()
with open('resume.txt', 'r') as resume:
    for line in resume:
        c.update(line.split())
    # pprint.pprint(c)
for word in match:
    if(c[word]):
        print(word, c[word])
