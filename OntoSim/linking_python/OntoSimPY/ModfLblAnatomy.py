from OntoSimImports import *
import OntoSimConstants as cnst

def modfWord(word):
    word = word.lower()
    wordnet_lemmatizer = WordNetLemmatizer()
    word = wordnet_lemmatizer.lemmatize(word)

    return word


def removeStopWords(word):
    stop_word_lst = ["of", "the", "system", "a", "all", "at", "or", "and", "to", "with"]
    if (word.lower() in stop_word_lst):
        return ""
    else:
        return word


def getEntityWords(entity):
    return_words = []
    entity_words = entity.replace("'", "").replace('_', ' ').replace('-', ' ').replace('/', ' ').replace('(',
                                                                                                         ' ').replace(
        ')', ' ').split()
    wordnet_lemmatizer = WordNetLemmatizer()
    for idx, w in enumerate(entity_words):
        word = entity_words[idx]
        word = word.lower()
        word = wordnet_lemmatizer.lemmatize(word)
        word = removeStopWords(word)
        if (word != ""):
            return_words.append(word)

    return return_words


def checkIfRomanNumeral(intVal):
    intVal_Tmp = intVal.upper()
    validRomanNumerals = ["M", "D", "C", "L", "X", "V", "I"]
    for letters in intVal_Tmp:
        if letters not in validRomanNumerals:
            return False

    return True


def chkAlphaNumeric(input):
    return bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', input))


def int_to_roman(input):
    intVal_Tmp = input
    intVal_Tmp = intVal_Tmp.upper()
    nums = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    sum = 0
    for i in range(len(intVal_Tmp)):
        try:
            value = nums[intVal_Tmp[i]]
            # If the next place holds a larger number, this value is negative
            if (i + 1 < len(intVal_Tmp)) and (nums[intVal_Tmp[i + 1]] > value):
                sum -= value
            else:
                sum += value
        except KeyError:
            raise (ValueError, 'input is not a valid Roman numeral: %s' % intVal_Tmp)

    return sum


def crtAltLbl(conf, data, removed_fl):
    err_key = []

    for key in data.keys():
        alt_word = ""

        if (data[key]['lbl'] is not None):
            words = getEntityWords(data[key]['lbl'])  # get all the words separated
            for word in words:
                tmp_word = word

                # if the word is numeric
                if (tmp_word.isdigit()):
                    num = str(int(tmp_word))
                    alt_word = alt_word + " " + num
                    continue

                # if the word is alpha-numeric
                if (chkAlphaNumeric(tmp_word)):
                    num = "".join(re.findall('\d+', tmp_word))

                    if (len(num) > 0):
                        num = str(int(num))
                        alt_word = alt_word + " " + num

                    abbr = tmp_word.replace(num, "").lower()
                    if (abbr == "s"):
                        alt_word = alt_word + " " + modfWord("Sacral")
                    elif (abbr == "l"):
                        alt_word = alt_word + " " + modfWord("Lumbar")
                    elif (abbr == "t"):
                        alt_word = alt_word + " " + modfWord("Thoracic")
                    elif (abbr == "c"):
                        alt_word = alt_word + " " + modfWord("Cervical")
                    elif (abbr == "ca"):
                        alt_word = alt_word + " " + modfWord("Cornu") + " " + modfWord("Ammonis")
                    else:  # CD4,CD8
                        alt_word = alt_word + " " + modfWord(abbr)
                    continue

                # if the word is Roman Integer (alpha)
                if (tmp_word.isalpha() and checkIfRomanNumeral(tmp_word)):
                    roman_num = str(int_to_roman(tmp_word))
                    if (roman_num.isdigit()):
                        alt_word = alt_word + " " + roman_num
                    continue

                # if the word is simple Literal alpha)
                if (tmp_word.isalpha() and (len(tmp_word) >= 1)):
                    alt_word = alt_word + " " + tmp_word
                else:
                    removed_fl.write(tmp_word + '\n')  # these words are removed while modifying labels

        else:
            print("label is None" + key)
            err_key.append(key)

        alt_word = ' '.join(sorted(set(alt_word.split())))  # to remove repeat words
        data[key]['altLbl'] = alt_word.strip()

    for key in err_key:
        data.pop(key, None)
        removed_fl.write(key + ' :label is None \n')  # these labels are none

    return data
