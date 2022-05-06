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
        englishWordsFrequencies:dict = {}
        farsiWordsFrequencies: dict = {}


        for english_index, english_sentence  in enumerate(listOfEnglishSentences):
            listOfEnglishWords = english_sentence.split()
            englishTokens.append(listOfEnglishWords)
            for eachWord in listOfEnglishWords:
                if eachWord not in englishWordsFrequencies.keys():
                    englishWordsFrequencies[eachWord] = 1
                else:
                    englishWordsFrequencies[eachWord] += 1



        for farsi_index, farsi_sentence in enumerate(listOfFarsiSentences):
            listOfFarsiWords = word_tokenize(farsi_sentence) #hazm is used here
            farsiTokens.append(listOfFarsiWords)
            for eachWord in listOfFarsiWords:
                if eachWord not in farsiWordsFrequencies.keys():
                    farsiWordsFrequencies[eachWord] = 1
                else:
                    farsiWordsFrequencies[eachWord] += 1

        farsiFile = open(os.getcwd() + "\\farsiFrequencyOutPut.txt", "w", encoding="utf8")
        farsiFile.write(str(farsiWordsFrequencies))
        farsiFile.close()

        englishFile = open(os.getcwd() + "\\ englishFrequencyOutPut.txt", "w", encoding="utf8")
        englishFile.write(str(englishWordsFrequencies))
        englishFile.close()

        # print(farsiWordsFrequencies)
        # print(englishWordsFrequencies)

        # print(farsiTokens)
        # print(englishTokens)

        for word_index, word in enumerate(englishTokens):
            try:
                indexNo = englishTokens[word_index].index(".")
                del englishTokens[word_index][indexNo]
            except Exception as e:
                # print("[-] Our Exception is :\n---->"+ str(e))
                continue

            try:
                indexNo = farsiTokens[word_index].index(".")
                del farsiTokens[word_index][indexNo]
            except Exception as e:
                # print("[-] Our Exception is :\n---->" + str(e))
                continue

            try:
                indexNo = englishTokens[word_index].index("?")
                del englishTokens[word_index][indexNo]
            except Exception as e:
                # print("[-] Our Exception is :\n---->" + str(e))
                continue

            try:
                indexNo = farsiTokens[word_index].index("?")
                del farsiTokens[word_index][indexNo]
            except Exception as e:
                # print("[-] Our Exception is :\n---->" + str(e))
                continue



            for outer_index, outer_value in enumerate(englishTokens[word_index]):
                for inner_index, inner_value in enumerate(farsiTokens[word_index]):
                    if outer_value + "-" + inner_value not in dictionary.keys():
                        dictionary[outer_value + "-" + inner_value] = 1
                    else:
                        dictionary[outer_value + "-" + inner_value] += 1

                    # print(dictionary.values())
                    # print(dictionary.keys())
                    # time.sleep(1.0)


if __name__ == '__main__':
    translationDic = TranslationDictionary()
    listOfFarsiSentences = translationDic.readFiles("Farsi")
    listOfEnglishSentences = translationDic.readFiles("English")
    translationDic.preProcess(listOfEnglishSentences, listOfFarsiSentences)

