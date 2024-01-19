import random

user_action = input("Enter a choice (rock, paper, scissors): ")
possible_actions = ["rock", "paper", "scissors"]
computer_action = random.choice(possible_actions)
print(f"\nYou chose {user_action}, computer chose {computer_action}.\n")

if user_action == computer_action:
    print("It's a draw!")
elif (
        (user_action == "rock" and computer_action == "scissors") or
        (user_action == "paper" and computer_action == "rock") or
        (user_action == "scissors" and computer_action == "paper")
):
    print(f"You win! {user_action} beats {computer_action}.")
else:
    print(f"You lose! {computer_action} beats {user_action}.")


