import streamlit as st
from openai import OpenAI
import random


# Initialize session state
if "stats" not in st.session_state:
    st.session_state["stats"] = {"games_played": 0, "guesses_per_game": []}
if "current_game" not in st.session_state:
    st.session_state["current_game"] = {"target_word": "", "guess_count": 0, "guessed_correctly": False}

st.set_page_config(page_title="Guessing Game", layout="centered")
st.sidebar.success("Select a page above to play or view stats.")
st.title("🎮 Play the Guessing Game")
st.markdown("Try to guess the secret word!\nCompare the guess with the target word and return hints.\n- '🟩': Letter is in the correct position.\n- '🟨': Letter is in the target word but in the wrong position.\n- '⬜': Letter is not in the target word.")


client = OpenAI(api_key="key here")
model = "gpt-4o-mini"


def generate_hint(guess, target):
    """
    Compare the guess with the target word and return hints.

    - '🟩': Letter is in the correct position.
    - '🟨': Letter is in the target word but in the wrong position.
    - '⬜': Letter is not in the target word.
    """
    hints = []
    target_checked = [False] * len(target)  # Tracks used letters in target for '🟨'

    # First pass: Check for correct letters in correct positions
    for i in range(len(guess)):
        if i < len(target) and guess[i] == target[i]:
            hints.append('🟩')
            target_checked[i] = True
        else:
            hints.append(None)  

    # Second pass: Check for correct letters in wrong positions
    for i in range(len(guess)):
        if hints[i] is None:  # Only check remaining letters
            if guess[i] in target and not target_checked[target.index(guess[i])]:
                hints[i] = '🟨'
                target_checked[target.index(guess[i])] = True
            else:
                hints[i] = '⬜'

    return ''.join(hints), target



def reset_game():
    """Reset the game state for a new game."""
    st.session_state["current_game"] = {
        "target_word": random.choice(["apple", "banana", "grape", "cherry", "mango"]),  # Example target words
        "guess_count": 0,
        "guessed_correctly": False
    }


# Initialize a new game if needed
if not st.session_state["current_game"]["target_word"]:
    reset_game()




def ai(user_guess):
    question = "I am playing a word guessing game. Shortly and only give me hints to the corrects word:" + str(user_guess)

    chat_completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": question},
    ],
)
    return chat_completion.choices[0].message.content






# Get current game state
game = st.session_state["current_game"]

# Display chat for guessing
if not game["guessed_correctly"]:
    user_guess = st.chat_input("Enter your guess:")
    if user_guess:
        game["guess_count"] += 1
        if user_guess.lower() == game["target_word"]:
            st.chat_message("assistant").write("🎉 Correct! You found the word!")
            st.session_state["stats"]["games_played"] += 1
            st.session_state["stats"]["guesses_per_game"].append(game["guess_count"])
            game["guessed_correctly"] = True
        else:
            hint = generate_hint(game["target_word"], user_guess)
            st.chat_message("assistant").write(f"❌ Not quite! Hint: {hint}")
            so = ai(user_guess)
            st.chat_message("assistant").write(f"Hint: {so}")

            
            
            

else:
    st.write("You've already guessed correctly! Start a new game.")

# Button to reset the game
if st.button("Start New Game"):
    reset_game()

