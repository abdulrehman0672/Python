import random

def guess_game():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 10.")
    print("You have 4 attempts to guess the number correctly.")
    print("Let's see if you can guess it!")

    
    number_to_guess = random.randint(1, 10)
    attempts = 0
    max_attempts = 4

    while attempts < max_attempts:
        try:
            secret_number = int(input("Take a guess: "))
            attempts += 1

            if secret_number < 1 or secret_number > 10:
                print("Please guess a number between 1 and 10.")
                continue

            if secret_number < number_to_guess:
                print("Your guess is too low.")

            elif secret_number > number_to_guess:
                print("Your guess is too high.")
            else:
                print(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")
                break
        except ValueError:
            print("That's not a valid number. Please enter an integer between 1 and 10.")

    else:
        print(f"Sorry, you've used all your attempts. The number was {number_to_guess}.")
    print("Thanks for playing!")


guess_game()