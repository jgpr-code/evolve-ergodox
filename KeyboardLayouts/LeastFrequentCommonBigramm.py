# I want to replace some letters on the common Neo2 layout which for me currently is
#
# xvlcw khgfq ß
# uiaeo snrtd y
# üöäpz bm,.j
# (for the neo.ini it is xvlcwkhgfqßuiaeosnrtdyüöäpzbm,.j)

#
# Things that are annoying atm are:
# - the position of the 'th' bigram
# - the position of 'y'
# - Neo2 is optimized for German, but I probably type 80% English

# Just some ideas
#
#
#
#
# In general I want the movement that the 'th', 'ht' or 'ic', 'ci' and 'tk', 'kt' or 'iw', 'wi'
# bigrams cause to be on the most infrequent bigrams that still contain very common letters
#
# Also I want to consider the movements of the most common bigrams more explicitly
# Still not fully decided if letter frequency is always more important than the comfort of typing the most common bigrams,
# but for now I assume I want to put the most frequent keys on the home row then top row then bottom row.

# The most common letters in English (and for üöäß German) according to http://norvig.com/mayzner.html and https://en.wikipedia.org/wiki/Letter_frequency are:
# 01-10: etaoi nsrhl
# 11-20: dcumf pgwyb
# 21-30: vkxjq züäöß

# 01-10: etaoi nshrd
# 11-20: lcumw fgypb
# 21-30: vkjxq züäöß
 
# Common shortcuts (Ctrl or Alt + ...):
# f, c, x, v, z, s, a (Emacs additions: b, y, w, u)
# left handed operations (while using mouse with right hand)
# copy, paste, cut, undo, redo, delete, enter, esc, save

# The 50 most common bigrams
# TH  100.3 B (3.56%)  TH
# HE   86.7 B (3.07%)  HE
# IN   68.6 B (2.43%)  IN
# ER   57.8 B (2.05%)  ER
# AN   56.0 B (1.99%)  AN
# RE   52.3 B (1.85%)  RE
# ON   49.6 B (1.76%)  ON
# AT   41.9 B (1.49%)  AT
# EN   41.0 B (1.45%)  EN
# ND   38.1 B (1.35%)  ND
# TI   37.9 B (1.34%)  TI
# ES   37.8 B (1.34%)  ES
# OR   36.0 B (1.28%)  OR
# TE   34.0 B (1.20%)  TE
# OF   33.1 B (1.17%)  OF
# ED   32.9 B (1.17%)  ED
# IS   31.8 B (1.13%)  IS
# IT   31.7 B (1.12%)  IT
# AL   30.7 B (1.09%)  AL
# AR   30.3 B (1.07%)  AR
# ST   29.7 B (1.05%)  ST
# TO   29.4 B (1.04%)  TO
# NT   29.4 B (1.04%)  NT
# NG   26.9 B (0.95%)  NG
# SE   26.3 B (0.93%)  SE
# HA   26.1 B (0.93%)  HA
# AS   24.6 B (0.87%)  AS
# OU   24.5 B (0.87%)  OU
# IO   23.5 B (0.83%)  IO
# LE   23.4 B (0.83%)  LE
# VE   23.3 B (0.83%)  VE
# CO   22.4 B (0.79%)  CO
# ME   22.4 B (0.79%)  ME
# DE   21.6 B (0.76%)  DE
# HI   21.5 B (0.76%)  HI
# RI   20.5 B (0.73%)  RI
# RO   20.5 B (0.73%)  RO
# IC   19.7 B (0.70%)  IC
# NE   19.5 B (0.69%)  NE
# EA   19.4 B (0.69%)  EA
# RA   19.3 B (0.69%)  RA
# CE   18.4 B (0.65%)  CE
# LI   17.6 B (0.62%)  LI
# CH   16.9 B (0.60%)  CH
# LL   16.3 B (0.58%)  LL
# BE   16.2 B (0.58%)  BE
# MA   15.9 B (0.57%)  MA
# SI   15.5 B (0.55%)  SI
# OM   15.4 B (0.55%)  OM
# UR   15.3 B (0.54%)  UR

# TODO: Read in AllBigramsCounts.txt and convert to a more readable sorted list.
# TODO: Do some plotting somehow

import re

all_letters = "abcdefghijklmnopqrstuvwxyz"

frequent_letters = "etaoinsrhd"
common_letters = "lcumwfgypb"
uncommon_letters = "vkjxqzüäöß"

def is_bigram_of(bigram, letters1, letters2):
    return any([a in bigram for a in letters1]) + any([])

def is_frequent_frequent(bigram):
    return sum([a in bigram for a in frequent_letters]) == 2

def is_frequent_common(bigram):
    return any([a in bigram for a in frequent_letters]) and any([a in bigram for a in common_letters])

def is_frequent_uncommon(bigram):
    return any([a in bigram for a in frequent_letters]) and any([a in bigram for a in common_letters])

def is_common_common(bigram):
    return sum([a in bigram for a in common_letters])

def main():

    with open("AllBigramsCounts.txt", "r") as file:
        data = file.read()

    bigrams = re.findall("\"([A-Z]{2}): [0-9.%]*; ([0-9,]*)\"", data)
    for i in range(len(bigrams)):
        bigrams[i] = (bigrams[i][0].lower(), int(bigrams[i][1].replace(',', '')))


    bigrams.sort(key=lambda x: x[1], reverse=True)
    for bigram in bigrams:
        print(bigram)

    uniform_bigrams = []
    for i in range(len(all_letters)):
        for j in range(i, len(all_letters)):
            uniform_bigram = all_letters[i] + all_letters[j]
            count = 0
            for bigram in bigrams:
                if sorted(bigram[0]) == sorted(uniform_bigram):
                    count += bigram[1]
            uniform_bigrams.append((uniform_bigram, count))

    print("uniform bigrams (e.g. sum of 'th' and 'ht' and so on")                    
    uniform_bigrams.sort(key=lambda x: x[1], reverse=True)
    for uniform_bigram in uniform_bigrams:
        print(uniform_bigram)

    print("rarest frequent-frequent")
    for uniform_bigram in reversed(uniform_bigrams):
        if is_frequent_frequent(uniform_bigram[0]):
            print(uniform_bigram)

    print("rarest frequent-common")
    for uniform_bigram in reversed(uniform_bigrams):
        if is_frequent_common(uniform_bigram[0]):
            print(uniform_bigram)

if __name__ == "__main__":
    main()