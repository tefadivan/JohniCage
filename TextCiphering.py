
import sys

CIPHER_DICTIONARY_FILE = "encrypt_file"
DECIPHER_DICTIONARY_FILE = "decipher_file"

def myFilter(target_text_raw):
    target_text = ""
    for i in target_text_raw:        
        if i.isupper():
            target_text = target_text + i.lower()
        else:
            target_text = target_text + i

    return target_text

def extracVocabulary(file):
    vocabulary = dict()
    for line in file: 
        tokens = str(line).split('=')
        vocabulary[tokens[0]] = tokens[1][0]

    return vocabulary 

def extractDecipherVocabulary(file):
    vocabulary = list()

    for line in file: 
        tokens = str(line).split('=')
        vocabulary.append(tokens[0])

    return vocabulary

def extractLetters(text):
    processed = set()
    letters = dict() # letter->count
    sorted_letters = list()

    i = 0
    while i < len(text): 
        if text[i] in processed or text[i] == '\ufeff' or str(text[i]).isupper() or text[i] == ' ' or text[i] == '\n' or text[i] == ',' or text[i] == '.':
            i = i + 1
            continue
        count = 0
        j = i
        while j < len(text): 
            if text[j] == text[i]: 
                count = count + 1
            j = j + 1
        letters[text[i]] = count
        processed.add(text[i])
        i = i + 1
    

    while len(letters) > 0:
        max_count = 0
        max_char = ''
        for i in letters.keys():
            if letters[i] > max_count:
                max_count = letters[i]
                max_char = i        
        sorted_letters.append(max_char)
        letters.pop(max_char)

    return sorted_letters

if __name__ == "__main__":    
    if len(sys.argv) < 3: 
        print("Invalid number of arguments")
        sys.exit(1)
    
    option_name = sys.argv[1]
    target_name = sys.argv[2]
    option_saving = "nodefined"

    if len(sys.argv) >= 4:
        option_saving = sys.argv[3]

    if option_name == "-cipher":        
        vocabulary = extracVocabulary(open(CIPHER_DICTIONARY_FILE, 'r', encoding="utf8"))
        target_file = open(target_name, 'r', encoding="utf8")       

        ciphered_text = ""
        for i in myFilter(target_file.read()):
            if i in vocabulary.keys():
                ciphered_text += vocabulary.get(i)
            else:
                ciphered_text += i

        if option_saving == "nodefined":
            print(ciphered_text) 
            sys.exit(0)
        
        file_res = open("ciphered.txt", 'w', encoding="utf8")
        file_res.write(ciphered_text)
        sys.exit(0)


    if option_name == "-decipher":        
        target_file = open(target_name, 'r', encoding="utf8")  
        target_text = target_file.read()
        target_letters = extractLetters(target_text)
        sampleChars = extractDecipherVocabulary(open(DECIPHER_DICTIONARY_FILE, 'r', encoding="utf8"))

        vocabulary = dict()
        i = 0
        while i < len(target_letters) and i < len(sampleChars):
            if target_letters[i] in sampleChars:
                vocabulary[target_letters[i]] = sampleChars[i]
            i = i + 1
        
        deciphered_text = ""
        for i in target_text:
            if i in vocabulary.keys(): 
                deciphered_text = deciphered_text + vocabulary[i]
            else:
                deciphered_text = deciphered_text + i
        
        if option_saving == "nodefined":
            print(deciphered_text) 
            sys.exit(0)
        
        file_res = open("deciphered.txt", 'w', encoding="utf8")
        file_res.write(deciphered_text)
        sys.exit(0)                       