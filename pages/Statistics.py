import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Statistics", layout="centered")
st.title("📊 Game Stats")
st.sidebar.success("Select a page above to play or view stats.")

stats = st.session_state["stats"]
games_played = stats["games_played"]
guesses_per_game = stats["guesses_per_game"]

if games_played > 0:
    st.write(f"**Games Played:** {games_played}")
    st.write(f"**Average Guesses Per Game:** {sum(guesses_per_game) / games_played:.2f}")

    # Bar chart
    df = pd.DataFrame({"Game": range(1, games_played + 1), "Guesses": guesses_per_game})
    fig, ax = plt.subplots()
    df.plot(kind="bar", x="Game", y="Guesses", ax=ax, legend=False)
    ax.set_title("Number of Guesses per Game")
    ax.set_xlabel("Game")
    ax.set_ylabel("Guesses")
    st.pyplot(fig)
else:
    st.write("No games played yet!")
