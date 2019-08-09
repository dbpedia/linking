from OntoSimImports import *
import OntoSimConstants as cnst


def assignVar():
    conf_1 = {
        'src_ip_fl_nm': 'ontodata/eclipse/source.json',
        'trgt_ip_fl_nm': 'ontodata/eclipse/target.json',
        'src_op_fl_nm': 'ontodata/modifylbl/source.json',
        'trgt_op_fl_nm': 'ontodata/modifylbl/target.json',
        'removed_utl_fl_nm': 'ontodata/util/removed.txt'
    }

    conf_arr = []
    conf_arr.append(conf_1)

    return conf_arr


def loadSourceTarget(conf):
    source_fl_nm = conf['src_ip_fl_nm']
    target_fl_nm = conf['trgt_ip_fl_nm']
    source_fl_nm = cnst.code_path + source_fl_nm
    with open(source_fl_nm) as f:
        source_data = json.load(f)

    target_fl_nm = cnst.code_path + target_fl_nm
    with open(target_fl_nm) as f:
        target_data = json.load(f)

    return source_data, target_data


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
    entity_words = entity.replace("'", "").replace('_', ' ') \
        .replace('-', ' ').replace('/', ' ').replace('(', ' ') \
        .replace(')', ' ').replace('[', ' ').replace(']', ' ') \
        .replace(',', ' ').replace(':', ' ').replace(';', ' ') \
        .replace('.', ' ').replace('{', ' ').replace('}', ' ') \
        .replace('+', ' ').replace('^', ' ').replace('!', ' ').split()

    wordnet_lemmatizer = WordNetLemmatizer()
    for idx, w in enumerate(entity_words):
        word = entity_words[idx]
        word = word.lower()
        word = wordnet_lemmatizer.lemmatize(word)
        word = removeStopWords(word)
        if (word != ""):
            return_words.append(word)

    # This is very special case, where the label is entirely a stop word
    # In that case do not use stop words
    if (len(return_words) == 0):
        for idx, w in enumerate(entity_words):
            word = entity_words[idx]
            word = word.lower()
            word = wordnet_lemmatizer.lemmatize(word)
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
    return bool(re.match('^(?=.*[0-9])(?=.*[a-zA-Z])', input))


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
                    alt_word = alt_word + " " + abbr
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

    return data


def crtAltLblUtl(conf, source_data, target_data):
    removed_fl = open(cnst.code_path + conf['removed_utl_fl_nm'], "w")
    source_data = crtAltLbl(conf, source_data, removed_fl)
    target_data = crtAltLbl(conf, target_data, removed_fl)
    removed_fl.close()

    return source_data, target_data


def saveSrcTrgt(source_data, target_data, conf):
    with open(cnst.code_path + conf['src_op_fl_nm'], 'w') as outfile:
        json.dump(source_data, outfile, indent=4)

    with open(cnst.code_path + conf['trgt_op_fl_nm'], 'w') as outfile:
        json.dump(target_data, outfile, indent=4)


#################### MAIN CODE START ####################
def modifyLblMain():
    print("#################### ModifyLabel START ####################")
    try:
        conf_arr = assignVar()

        for conf in conf_arr:
            source_data, target_data = loadSourceTarget(conf)

            source_data, target_data = crtAltLblUtl(conf, source_data, target_data)

            saveSrcTrgt(source_data, target_data, conf)

            time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### ModifyLabel FINISH ####################")

#################### MAIN CODE END ####################
