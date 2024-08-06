import streamlit as st
from services.chat.chat import answer
from services.chat.history import add_message, get_history, Author, show_message
from services.youtube.video_id import extract_video_id


# ユーザーの入力部分
with st.chat_message("assistant"):
    st.write("こんにちは。YouTube動画に関してお役に立てることはありますか？？")

text = st.chat_input("入力してください。")

if text:
    video_id = extract_video_id(text)
    add_message(text, video_id=video_id)

# 履歴の表示
messages = get_history()
for message in messages:
    show_message(message)

if len(messages) > 0 and messages[-1].author == Author.User:
    # ユーザーの入力に対して回答作成
    answer(messages[-1])
