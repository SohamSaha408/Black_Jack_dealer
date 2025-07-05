!pip install gtts



import streamlit as st
import requests
import random
import os
from gtts import gTTS
from pathlib import Path

# === Blackjack Card Setup ===
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def card_value(card):
    rank, _ = card
    if rank in ['jack', 'queen', 'king']:
        return 10
    elif rank == 'ace':
        return 11
    return int(rank)

def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if card[0] == 'ace')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def card_to_image_filename(card):
    rank, suit = card
    return f"cards/{rank.lower()}_of_{suit.lower()}.png"

# === TTS: Convert text to voice ===
def speak(text, filename="dealer_voice.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# === Game state ===
if 'deck' not in st.session_state:
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)

if 'player_hand' not in st.session_state:
    st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]

if 'dealer_hand' not in st.session_state:
    st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]

if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# === UI ===
st.set_page_config(page_title="Blackjack with AI Dealer")
st.title("🃏 Blackjack AI Dealer with Voice")

# === Display Hands ===
st.markdown("### 🧑 Your Cards:")
for card in st.session_state.player_hand:
    st.image(card_to_image_filename(card), width=100)

st.markdown(f"**Total:** {hand_value(st.session_state.player_hand)}")

if st.session_state.game_over:
    st.markdown("### 🧑 Dealer's Cards:")
    for card in st.session_state.dealer_hand:
        st.image(card_to_image_filename(card), width=100)
    st.markdown(f"**Dealer Total:** {hand_value(st.session_state.dealer_hand)}")

# === Game Actions ===
if not st.session_state.game_over:
    col1, col2 = st.columns(2)

    if col1.button("Hit"):
        st.session_state.player_hand.append(st.session_state.deck.pop())
        if hand_value(st.session_state.player_hand) > 21:
            st.session_state.game_over = True

    if col2.button("Stand"):
        while hand_value(st.session_state.dealer_hand) < 17:
            st.session_state.dealer_hand.append(st.session_state.deck.pop())
        st.session_state.game_over = True

# === Voice Narration ===
msg = ""
if st.session_state.game_over:
    player_score = hand_value(st.session_state.player_hand)
    dealer_score = hand_value(st.session_state.dealer_hand)

    if player_score > 21:
        msg = f"You busted with {player_score}. Dealer wins."
    elif dealer_score > 21:
        msg = f"Dealer busted with {dealer_score}. You win!"
    elif player_score > dealer_score:
        msg = f"You win with {player_score} against dealer's {dealer_score}!"
    elif player_score < dealer_score:
        msg = f"Dealer wins with {dealer_score} against your {player_score}."
    else:
        msg = "It's a tie!"

    st.markdown(f"### 🎙️ Dealer Says: {msg}")
    mp3_path = speak(msg)
    st.audio(mp3_path)

# === Reset Button ===
if st.button("Restart Game"):
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.game_over = False
    if os.path.exists("dealer_voice.mp3"):
        os.remove("dealer_voice.mp3")
import os

# Create the 'cards' directory if it doesn't exist
if not os.path.exists('cards'):
    os.makedirs('cards')
    print("Created 'cards' directory. Please upload your card image files into this directory.")
else:
    print("'cards' directory already exists.")
