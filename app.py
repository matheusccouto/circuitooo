"""circuit.ooo app"""

import datetime
import os
import random

import streamlit as st
import pyperclip
import yaml

THIS_DIR = os.path.dirname(__file__)
FLAG = "\U0001F3C1"
CROSS = "\u274C"
BUG = "https://github.com/matheusccouto/circuitooo/issues/new"
ABOUT = "Inspirado em estadi.ooo\n\nColabore em github.com/matheusccouto/circuitooo"
stop = False

st.set_page_config(
    page_title="circuit.ooo",
    page_icon=":checkered_flag:",
    menu_items={"Get help": None, "Report a Bug": BUG, "About": ABOUT},
)

HIDE_STREAMLIT_STYLE = """
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: visible;}
"""
st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

# Load YAML file with data.
with open(os.path.join(THIS_DIR, "data", "data.yml"), encoding="utf-8") as file:
    data = yaml.load(file, yaml.CLoader)

# Get all tracks and select one for the day.
all_tracks = list(sorted(data.keys()))
random.seed(int(datetime.datetime.today().date().strftime("%Y%m%d")))
track = random.choice(all_tracks)

# Initialize session variables.
if "n_trials" not in st.session_state:
    st.session_state.n_trials = 5
if "n_mistakes" not in st.session_state:
    st.session_state.n_mistakes = 0

# App widgets.
st.title("circuit.ooo")
st.image(data[track]["image"])
trials = st.empty()
tips = [st.empty() for _ in data[track]["tips"]]
droplist = st.empty()

# User input.
guess = droplist.selectbox(
    label="Que circuito é esse?",
    options=[""] + all_tracks,
    disabled=stop,
)

# If the user gor it wrong, record a mistake.
if guess and guess != track:
    st.session_state.n_mistakes += 1
    st.session_state.n_trials -= 1

# Update the number of chances left for the user.
mistake_emojis = CROSS * st.session_state.n_mistakes
tries_emojis = FLAG * st.session_state.n_trials
trials.subheader(mistake_emojis + tries_emojis)

# Update tips
random.shuffle(data[track]["tips"])
for i in range(st.session_state.n_mistakes + 1):
    if i <= len(tips) - 1:
        tips[i].write(data[track]["tips"][i])

if st.session_state.n_trials == 0 or guess == track:
    stop = True

if stop:

    droplist.empty()
    trials.empty()
    for tip in tips:
        tip.empty()

    st.header(track)
    st.caption(data[track]["location"])

    msg = (
        "Já joguei circuit.ooo hoje, e tu? "
        f"Consegue acertar o autódromo? {mistake_emojis + tries_emojis}"
    )
    st.write(msg)
    if st.button("Copiar"):
        pyperclip.copy(msg)
