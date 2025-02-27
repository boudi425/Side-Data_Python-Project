#This will properly have the functions which i don't need in the main input because i don't like how it looks if it's like this
#Might not even used it
import string
from random import shuffle
import hashlib
s1 = list(string.ascii_lowercase)
s2 = list(string.ascii_uppercase)
s3 = list(string.punctuation)
s4 = list(string.digits)

number_of_characters = 10

shuffle(s1)
shuffle(s2)
shuffle(s3)
shuffle(s4)

part1 = round(number_of_characters * (30/100))
part2 = round(number_of_characters * (20/100))

def Strong_passkey(Number_of_characters=10):
    password = []
    for i in range(part1):
        password.append(s1[i])
        password.append(s2[i])
    for i in range(part2):
        password.append(s3[i])
        password.append(s4[i])
    shuffle(password)
    password = "".join(password[0:])
    return password

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Hash the password

def verify_password(input_password, stored_hash):
    return hash_password(input_password) == stored_hash  # Compare hashes

        