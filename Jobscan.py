# script name   : jobscan.py
# Author		: Gaurav Ketkar
# Created		: April 2016
# Description	: This is the naive frequency analysis of words in the job description and the resume.
#                 The 'match' counter is incremented when a word in the resume matches a word in the job description.

import sys
import string
from collections import Counter as c
from nltk.corpus import stopwords
from nltk.wsd import lesk

#########################################################
# Exclude punctuations, stop words and words from exclude_list
# 'exclude' is used later to clean the data of words to be excluded
#########################################################

exclude = set(string.punctuation)
exclude.add("\u200b")
for word in set(stopwords.words("english")):
    exclude.add(word)
# To exclude specific words, specified in the text file.
with(open('exclude_list.txt', 'r')) as exList:
    exclude_list = exList.readlines()
    for line in exclude_list:
        for word in line.split():
            exclude.add(word)


#########################################################
# Open the text files, remove unnecessary words and return a list of words.
# @returns : words
#########################################################

def wordify(file):
    with(open(file, 'r')) as f:
        lines = [line.rstrip('\n').split() for line in f]
        words = [word for sentence in lines for word in sentence if word not in exclude]
    return words, words[0]


#########################################################
# Open the text files, finds lesk meaning for each work and returns a mapping of (word, meaning)
# @returns : wordsLesk
#########################################################
def leskify(file):
    with(open(file, 'r')) as f:
        contents = f.read()
        words, describingWord = wordify(file)
        meaning = {}
        for word in words:
            meaning[word] = lesk(contents, word)
            # meaning.append((word, lesk(contents, word)))
        return meaning, describingWord
        # pprint.pprint(meaning)


#########################################################
# Calculate the matching between the resume and the job description
# by Lesk Word Sense Disambiguation Algorithm
# @returns : result
#########################################################

def leskCalcMatch(desc, resume):
    counter = 0
    total = resume.__sizeof__()
    # print(resume)
    for key in resume:
        if key in desc and resume[key] == desc[key]:
            counter += 1
    return counter


#########################################################
# Calculate the matching between the resume and the job description
# by naive frequency analysis
# @returns : result
#########################################################

def naiveCalcMatch(description, resume):
    matchCounter = 0
    descTally = c(description)
    resTally = c(resume)
    # If a word in Resume is found in the description, increment the counter
    #  by the number of occurences of the word in the resume
    for key in resTally:
        if key in descTally:
            matchCounter += resTally.get(key)
    result = matchCounter
    return round(result, 0)


def printOP(job, match):
    print('{0: <25}'.format("\t" + job) + " : " + str(match))


# Naive Frequency Analysis Algorithm
def naiveMethod():
    print()
    print("##############    BY NAIVE FREQUENCY ANALYSIS     ############")
    print()

    for everyProfession in range(1, 6):
        res_words, resumeType = wordify('resume' + str(everyProfession) + '.txt')
        print(resumeType)
        for everyJobRole in range(1, 6):
            job_des_words, descriptionType = wordify('job_description' + str(everyJobRole) + '.txt')
            # Calculate the Match
            match = naiveCalcMatch(job_des_words, res_words)
            printOP(descriptionType, match)
        print()


# Lesk Word Sense Disambiguation Algorithm
def leskMethod():
    print()
    print("############    BY LESK     ############")
    print()

    for everyProfession in range(1, 6):
        res_words_lesk, resumeType = leskify('resume' + str(everyProfession) + '.txt')
        print(resumeType)
        for everyJobRole in range(1, 6):
            job_des_words_lesk, descriptionType = leskify('job_description' + str(everyJobRole) + '.txt')
            # Calculate the Match
            matchLesk = leskCalcMatch(job_des_words_lesk, res_words_lesk)
            printOP(descriptionType, matchLesk)
        print()


if __name__ == '__main__':

    if (3 == len(sys.argv)):
        # the 'script' here refers to the file Jobscan.py itself
        script, job_des_file, resume_file = sys.argv

        # Calculations for Naive frequency analysis
        naiveMethod()
        # & lesk word sense disambiguation method
        leskMethod()
    else:
        print("No input present, exiting.")
