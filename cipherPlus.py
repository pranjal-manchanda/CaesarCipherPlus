"""
    Program that can cipher/de-cipher messages by receiving input directly
    from the user or by reading the accompanying story.txt file
    Can decipher messages without receiving a shift key as an input
"""

import string

def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'
valid_words = load_words(WORDLIST_FILENAME)

class Message(object):

    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has one attribute:
            self.message_text (string, determined by input text)
        '''
        self.message_text = text
        
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text


    def get_valid_words(self):
        '''
        Used to safely access a copy of valid_words outside of the class
        
        Returns: a COPY of valid_words
        '''
        return valid_words[:]
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        shift_dict = {}
        
        for letter in string.ascii_lowercase:
            shift_dict[letter] = chr(((((ord(letter) + shift) % 97) % 26) + 97))
    
        for letter in string.ascii_uppercase:
            shift_dict[letter] = chr(((((ord(letter) + shift) % 65) % 26) + 65))
            
        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        text = self.get_message_text()
        
        cypher_dict = self.build_shift_dict(shift)
        cypher = ""
        
        for letter in text:
            if letter in string.ascii_letters:
                cypher += cypher_dict[letter]
            else:
                cypher += letter
        
        return cypher

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has four attributes:
            self.message_text (string, determined by input text)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less 
        code is repeated
        '''
        Message.__init__(self, text)
        self.message_text = Message.get_message_text(self)
        self.shift = shift
        self.encrypting_dict = Message.build_shift_dict(self, self.shift)
        self.message_text_encrypted = Message.apply_shift(self, self.shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        '''
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encrypting_dict = Message.build_shift_dict(self, self.shift)
        self.message_text_encrypted = Message.apply_shift(self, self.shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has one attribute:
            self.message_text (string, determined by input text)
        '''
        Message.__init__(self, text)
        self.message_text = text

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.
  
        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        bestShift = ()
        maxCount = 0
        
        for i in range(26):
            count = 0
            decryptedMessage = self.apply_shift(i)
            decryptedList = decryptedMessage.split(' ')
            
            for word in decryptedList:
                if is_word(valid_words, word):
                    count += 1
                    
            if count > maxCount:
                maxCount = count
                bestShift = (i, decryptedMessage)
                
        return bestShift
    
    def decrypt_story():
        decryptedStory = CiphertextMessage(get_story_string())
        return decryptedStory.decrypt_message()

#Run Program
#PlaintextMessage
plaintext = PlaintextMessage('Random Phrase', 2)
print('\nPlainText Input: ' + plaintext.get_message_text())
print('\nCipher Output:', plaintext.get_message_text_encrypted())

print('\n------')
print('------')

#CiphertextMessage
ciphertext = CiphertextMessage(get_story_string())
print('\nCipher Input: ' + ciphertext.get_message_text())
print('\nPlainText Output:', ciphertext.decrypt_message())
