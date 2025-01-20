# backend/attack.py
import itertools
import string
import time
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from password_manager import is_strong_password

# Function to perform brute force attack
def brute_force_attack(target_password):
    characters = string.ascii_letters + string.digits + string.punctuation
    attempts = 0
    start_time = time.time()
    
    for length in range(1, 5):  # Limiting to passwords of length 4 for demonstration
        for guess in itertools.product(characters, repeat=length):
            attempts += 1
            guess = ''.join(guess)
            if guess == target_password:
                end_time = time.time()
                print(f"Password found: {guess}")
                print(f"Attempts: {attempts}")
                print(f"Time taken: {end_time - start_time} seconds")
                return
    print("Password not found within the given length limit.")

# Function to perform dictionary attack
def dictionary_attack(target_password, dictionary_file):
    attempts = 0
    start_time = time.time()
    
    with open(dictionary_file, 'r') as file:
        for line in file:
            attempts += 1
            guess = line.strip()
            if guess == target_password:
                end_time = time.time()
                print(f"Password found: {guess}")
                print(f"Attempts: {attempts}")
                print(f"Time taken: {end_time - start_time} seconds")
                return
    print("Password not found in the dictionary.")

if __name__ == "__main__":
    target_password = "Pass!"  # Replace with the password you want to test
    print("Starting brute force attack...")
    brute_force_attack(target_password)
    
    print("\nStarting dictionary attack...")
    dictionary_file = "backend/dictionary.txt"  # Replace with the path to your dictionary file
    dictionary_attack(target_password, dictionary_file)