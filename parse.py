#Justin Smith, COMP 431

import string
import sys

curr_message = ""

def isSpace(index):
    if curr_message[index] == '\t' or curr_message[index] == ' ':
        return True
    return False

def isLetter(index):
    if string.ascii_letters.find(curr_message[index]) != -1:
        return True
    return False

def isDigit(index):
    if string.digits.find(curr_message[index]) != -1:
        return True
    return False

def isNull(index):
    return True

def isSpecial(index):
    special_chars = r'<>()[]\.,:@"';
    if special_chars.find(curr_message[index]) != -1:
        return True
    return False

def isCRLF():
    if curr_message.endswith('\n'):
        return True
    return False

def isChar(index):
    if string.printable.find(curr_message[index]) != -1 and not(isSpecial(index) or isSpace(index)):
        return True
    return False

def isLetterDigit(index):
    if isLetter(index) or isDigit(index):
        return True
    return False

def whitespace(index):
    if index >= len(curr_message):
        return -1
    if isSpace(index):
        index += 1
        return whitespace(index)
    return index

def isNullspace(index):
    if index >= len(curr_message):
        return index
    if isSpace(index):
        index += 1
        return whitespace(index)
    if isNull(index):
        return index
    return -1

def letDigStr(index):
    if index >= len(curr_message):
        return -1
    if isLetterDigit(index):
        index += 1
        return letDigStr(index)
    return index

def name(index):
    if isLetter(index):
        index += 1
        letDigIndex = letDigStr(index)
        if letDigIndex > index:
            return letDigIndex
        else:
            print("Error -- let-dig-string")
    else:
        print("Error -- name")
    return -1

def element(index):
    letterIndex = index
    if isLetter(index):
        letterIndex += 1

    if letterIndex == index:
        print("Error -- element")
        return -1

    nameIndex = name(index)
    
    if nameIndex > letterIndex:
        return nameIndex
    else:
        return letterIndex

def domain(index):
    elementIndex = element(index);
    if elementIndex > index:
        if elementIndex < len(curr_message) and curr_message[elementIndex] == '.':
            domainIndex = domain(elementIndex + 1)
            if domainIndex > elementIndex + 1:
                return domainIndex
            else:
                return -1
        return elementIndex
    return -1

def indexString(index):
    if index >= len(curr_message):
        return -1
    if isChar(index):
        index += 1
        return indexString(index)
    return index

def localPart(index):
    stringIndex = indexString(index)
    if stringIndex > index:
        return stringIndex
    else:
        print("Error -- string")
    return -1

def mailbox(index):
    localIndex = localPart(index)
    if localIndex > index:
        if localIndex < len(curr_message) and curr_message[localIndex] == '@':
            domainIndex = domain(localIndex + 1)
            if domainIndex > localIndex + 1:
                return domainIndex
            else:
                return -1
        else:
            print("Error -- mailbox")
    return -1

def path(index):
    if curr_message[index] == '<':
        index += 1
        mailIndex = mailbox(index)
        if mailIndex > index:
            if curr_message[mailIndex] == '>':
                return mailIndex + 1
            else:
                print("Error -- path")
    else:
        print("Error -- path")
    return -1

def reversePath(index):
    pathIndex = path(index)
    if pathIndex > index:
        return pathIndex
    else:
        return index

def isMailFromCMD():
    index = 0
    mailArray = ['M', 'A', 'I', 'L']
    fromArray = ['F', 'R', 'O', 'M', ':']

    for character in mailArray:
        if curr_message[index] == character:
            index += 1
    if index == 4:
        if index >= len(curr_message):
            print("Error -- whitespace")
            return False
        whitespaceIndex = whitespace(index)
        if whitespaceIndex > index:
            index = whitespaceIndex
        else:
            print("Error -- whitespace")
            return False
        for character in fromArray:
            if curr_message[index] == character:
                index += 1
        if index - whitespaceIndex != 5:
            print("Error -- mail-from-cmd")
            return False
    else:
        print("Error -- mail-from-cmd")
        return False

    nullIndex = isNullspace(index)
    if nullIndex >= index:
        index = nullIndex
        reverseIndex = reversePath(index)
        if reverseIndex > index:
            index = reverseIndex
        else:
            return False
    else:
        print("Error -- mail-from-cmd")
        return False

    nullIndex = isNullspace(index)
    if nullIndex >= index:
        index = nullIndex
    else:
        print("Error -- nullspace")
        return False
    
    if isCRLF():
        return True
    else:
        print("Error -- mail-from-cmd")
        return False

def main():
    global curr_message
    for line in sys.stdin:
        curr_message = line
        print(curr_message[:len(curr_message)-1])
        if isMailFromCMD():
            print("Sender ok")

main()
