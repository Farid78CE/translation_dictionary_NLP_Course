import os
import typing

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

    def preProcess(self, listOfEnglishSentences, listOfFarsiSentences):
        dictionary: dict = {}
        for outer_index, outer_words in enumerate(listOfEnglishSentences):
            for inner_index, inner_words in enumerate(listOfFarsiSentences):
                if outer_words + "-" + inner_words not in dictionary.keys():
                    # print( outer_words + "<-> " + inner_words)
                    # print(inner_words)
                    dictionary[outer_words + "-" + inner_words] = 1
                else:
                    dictionary[outer_words + "-" + inner_words] += 1



if __name__ == '__main__':
    translationDic = TranslationDictionary()
    listOfFarsiSentences = translationDic.readFiles("Farsi")
    print(listOfFarsiSentences)
    listOfEnglishSentences = translationDic.readFiles("English")
    # translationDic.preProcess(listOfEnglishSentences, listOfFarsiSentences)

