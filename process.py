import pandas as pd
from ast import literal_eval

# process different lyrics into one paragraph, for n-gram to learn
data = pd.read_csv("./text/Jolin2.csv")
data2 = pd.read_csv("./text/PiggyLo.csv")

lyrics = data['lyric_line']
lyrics2 = data2['lyric_line']
with open('jolin2.txt', 'w') as f:
    for song in lyrics:
        e = literal_eval(song)
        if (len(e) != 0):
            tmp = "".join(e)
            f.write(tmp)
            f.write('\n')

with open('piggyLo.txt', 'w') as f:
    for song in lyrics2:
        e = literal_eval(song)
        if (len(e) != 0):
            tmp = "".join(e)
            f.write(tmp)
            f.write('\n')