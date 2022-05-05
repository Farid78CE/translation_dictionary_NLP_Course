import os
import typing
from hazm import *
import time

class TranslationDictionary:
    counter = 0
    def readFiles(self, language):
        self.counter += 1
        cwd = os.getcwd()

        if self.counter == 1:
            os.chdir(cwd + "\\Samples\\")
            cwd = os.getcwd()

        if language == "English":
            file = open(cwd + "\\tep.lowercased.en", "r", encoding="utf8")
            listOfEnglishSentences: list = []
            for sentences in file:
                listOfEnglishSentences.append(sentences)
            return listOfEnglishSentences

        elif language == "Farsi":
            file = open(cwd + "\\tep.lowercased.fa", "r", encoding="utf8")
            listOfFarsiSentences: list = []
            for sentences in file:
                listOfFarsiSentences.append(sentences)
            return listOfFarsiSentences
        else:
            print("Not a Valid Language")


    # @classmethod
    # def dotElimination(self, englishTokens, farsiTokens):
    #     for values in englishTokens:
    #         if values == ".":
    #             pass
    #             # Do Nothing
    #         else:
    #             pass



    def preProcess(self, listOfEnglishSentences, listOfFarsiSentences):
        dictionary: dict = {}
        englishTokens: list = []
        farsiTokens:list = []


        for english_index, english_sentence  in enumerate(listOfEnglishSentences):
            listOfEnglishWords = english_sentence.split()
            englishTokens.append(listOfEnglishWords)

        for farsi_index, farsi_sentence in enumerate(listOfFarsiSentences):
            listOfFarsiWords = word_tokenize(farsi_sentence) #hazm is used here
            farsiTokens.append(listOfFarsiWords)


        # print(farsiTokens)
        # print(englishTokens)

        for word_index, word in enumerate(englishTokens):
            indexNo = englishTokens[word_index].index(".")
            del englishTokens[word_index][indexNo]
            indexNo = farsiTokens[word_index].index(".")
            del farsiTokens[word_index][indexNo]
            
            for outer_index, outer_value in enumerate(englishTokens[word_index]):
                for inner_index, inner_value in enumerate(farsiTokens[word_index]):
                    if outer_value + "-" + inner_value not in dictionary.keys():
                        dictionary[outer_value + "-" + inner_value] = 1
                    else:
                        dictionary[outer_value + "-" + inner_value] += 1

                    print(dictionary.values())
                    print(dictionary.keys())
                    # time.sleep(1.0)


if __name__ == '__main__':
    translationDic = TranslationDictionary()
    listOfFarsiSentences = translationDic.readFiles("Farsi")
    listOfEnglishSentences = translationDic.readFiles("English")
    translationDic.preProcess(listOfEnglishSentences, listOfFarsiSentences)

