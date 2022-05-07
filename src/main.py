import os
import typing
from hazm import *
import time
# Farid Zaredar
# Unive
class TranslationDictionary:
    counter = 0
    flag = False


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

        # farsiFile = open(os.getcwd() + "\\farsiFrequencyOutPut.txt", "w", encoding="utf8")
        # farsiFile.write(str(farsiWordsFrequencies))
        # farsiFile.close()
        #
        # englishFile = open(os.getcwd() + "\\englishFrequencyOutPut.txt", "w", encoding="utf8")
        # englishFile.write(str(englishWordsFrequencies))
        # englishFile.close()



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
                pass

            try:
                indexNo = farsiTokens[word_index].index(".")
                del farsiTokens[word_index][indexNo]
            except Exception as e:
                # print("[-] Our Exception is :\n---->" + str(e))
                pass

            try:
                indexNo = englishTokens[word_index].index("?")
                del englishTokens[word_index][indexNo]
            except Exception as e:
                # print("[-] Our Exception is :\n---->" + str(e))
                pass

            try:
                indexNo = farsiTokens[word_index].index("?")
                del farsiTokens[word_index][indexNo]
            except Exception as e:
                # print("[-] Our Exception is :\n---->" + str(e))
                pass



            for outer_index, outer_value in enumerate(englishTokens[word_index]):
                for inner_index, inner_value in enumerate(farsiTokens[word_index]):
                    if outer_value + "-" + inner_value not in dictionary.keys():
                        dictionary[outer_value + "<->" + inner_value] = 1
                    else:
                        dictionary[outer_value + "<->" + inner_value] += 1

            # print(dictionary.keys())


        # dictionaryFile = open(os.getcwd() + "\\dictionary.txt", "w", encoding="utf8")
        # dictionaryFile.write(str(dictionary))
        # dictionaryFile.close()

        return (dictionary, farsiWordsFrequencies, englishWordsFrequencies)

    def formDictionary(self, dictionary, farsiWordsFrequency, englishWordsFrequency):
        probabilitiesOfTranslations: dict = {}
        listOfSameTerms: list = []
        # listOfPossibilities: list = []
        farsiLength = len(farsiWordsFrequency)
        englishLength = len(englishWordsFrequency)
        maxLength = max(farsiLength, englishLength)
        minLength = min(farsiLength, englishLength)
        previousTerm = ""
        previousPossibility: float = 0.00


        for keys in dictionary:
            splitedVal = keys.split("<->")
            # print(keys)
            # print(splitedVal)
            # time.sleep(10.0)
            englishTerm = splitedVal[0]
            farsiTerm = splitedVal[1]

            denominator = farsiWordsFrequency[farsiTerm]
            numinator = dictionary[keys]
            possibility = (numinator/denominator) * 100

            # print(str(splitedVal) + ": " + str(dictionary[keys]))
            # print(farsiTerm +": "+ str(farsiWordsFrequency[farsiTerm]))
            # print(f"({englishTerm}, {farsiTerm})/{farsiTerm} =" + str(possibility))

            fullTerm =  englishTerm + "<*>" + farsiTerm
            fullTerm = fullTerm + "<->" + str(possibility)
            # print(fullTerm)

            if englishTerm != previousTerm and self.flag:

                # self.flag = False
                if previousTerm not in probabilitiesOfTranslations.keys():
                    probabilitiesOfTranslations[previousTerm] = listOfSameTerms
                    listOfSameTerms = []
                    listOfSameTerms.append(fullTerm)
                    previousTerm = englishTerm
                    # print(probabilitiesOfTranslations)

                else:
                    pass
                    tempList = probabilitiesOfTranslations[previousTerm]
                    tempList.extend(listOfSameTerms)
                    probabilitiesOfTranslations[previousTerm] = tempList
                    tempList = []
                    listOfSameTerms = []
                    previousTerm = englishTerm
                    listOfSameTerms.append(fullTerm)
                    # print(probabilitiesOfTranslations)
            else:
                self.flag = True
                listOfSameTerms.append(fullTerm)
                previousTerm = englishTerm

        # print(probabilitiesOfTranslations)
        # probabilitiesOfTranslationsFile = open(os.getcwd()+"\\probabilitiesOfTranslations.txt", "w", encoding="utf8")
        # probabilitiesOfTranslationsFile.write(str(probabilitiesOfTranslations))
        # probabilitiesOfTranslationsFile.close()
        maximum:float = 0.0
        chosenMeaning: str = ""
        savedIndex: int = 0
        finalDictionary: dict = {}

        for keys in probabilitiesOfTranslations:
            for index, item in enumerate(probabilitiesOfTranslations[keys]):
                # print(item)
                splitedItems = item.split("<->")
                # print(splitedItems)
                # time.sleep(2.5)
                englishFarsiWords = splitedItems[0]
                possibilityOfEachPairWord = float(splitedItems[1])

                if (previousPossibility <= possibilityOfEachPairWord):
                    # maximum = possibilityOfEachPairWord
                    chosenMeaning = item
                    savedIndex = index
                    previousPossibility = possibilityOfEachPairWord
                    # time.sleep(6.0)
                elif (previousPossibility > possibilityOfEachPairWord):
                    # savedIndex = index
                    # maximum = previousPossibility
                    try:
                        chosenMeaning = probabilitiesOfTranslations[keys][savedIndex]
                    except Exception as e:
                        print(str(e))
                        print(savedIndex)
                        print(len(probabilitiesOfTranslations[keys]))
                    # print(chosenMeaning)
                    # time.sleep(6.0)

            chosenSplited = chosenMeaning.split("<->")
            word = chosenSplited[0]
            # print(word)
            savedIndex = 0
            maxPossibility = chosenSplited[1]
            wordSplited = word.split("<*>")
            englishWord = wordSplited[0]
            farsiWord = wordSplited[1]
            finalDictionary[englishWord] = f"({farsiWord}, {str(maxPossibility)})"

        finalDictionaryFile = open(os.getcwd() + "\\DictionaryResult.txt", "w", encoding="utf8")
        finalDictionaryFile.write(str(finalDictionary))
        finalDictionaryFile.close()
        # print("Done")



if __name__ == '__main__':
    translationDic = TranslationDictionary()
    listOfFarsiSentences = translationDic.readFiles("Farsi")
    listOfEnglishSentences = translationDic.readFiles("English")
    getTuples = translationDic.preProcess(listOfEnglishSentences, listOfFarsiSentences)
    dictionary = getTuples[0]
    farsiWordsFrequency = getTuples[1]
    englishWordsFrequency = getTuples[2]
    translationDic.formDictionary(dictionary, farsiWordsFrequency, englishWordsFrequency)

