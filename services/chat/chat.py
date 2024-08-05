import logging
from typing import Optional

import google.generativeai as genai

import config
import streamlit as st
from services.chat.history import Message, add_message, Author
from services.youtube.snippet import fetch_snippet, YoutubeSnippet
from services.youtube.transcript import transcribe

logger = logging.getLogger(__name__)


def answer(message: Message):
    """
    ユーザーの入力に対して回答を作成する。
    :param message: ユーザーの入力
    """
    video_id = message.video_id
    text = message.message
    if len(video_id) == 0:
        with st.chat_message("assistant"):
            st.write("YouTubeのURLが記載されていないようです。確認してみてください。")
    else:
        with st.chat_message("assistant"):
            with st.status("動画データを取得しています..."):
                st.write("文字起こしデータを取得しています...")
                languages = config.TRANSCRIPT_LANGUAGES
                transcription = transcribe(video_id, languages)
                st.write(transcription)

                snippet = None
                # st.write("動画スニペットを取得しています...")
                # snippet = fetch_snippet(video_id, config.YOUTUBE_API_KEY)

                st.write("回答を取得しています...")
                summary = answer_by_gemini(message=text, transcription=transcription, snippet=snippet, )
            answer_message = "こちらが回答になります。"
            add_message(
                answer_message,
                author=Author.Assistant,
                code=summary,
            )
            st.write(answer_message)
            st.code(summary)


def answer_by_gemini(message: str, transcription: str, snippet: Optional[YoutubeSnippet] = None) -> str:
    """
    Geminiを使いユーザーの要望に回答する。
    :param message:
    :param transcription:
    :param snippet:
    :return:
    """
    query = [f"""
YouTube動画に関する要望に答えましょう。必要に応じて動画情報や文字起こし結果を使いましょう。

# 要望

{message}
""".strip()]
    if snippet is not None:
        query += [f"""
# 動画情報

## 動画タイトル

{snippet.title}

## 動画概要

{snippet.description}
""".strip()]

    query = [f"""
# 文字起こし結果

${transcription}
""".strip()]
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    query = "\n\n".join(query)
    logger.info(f"{query=}")
    response = model.generate_content(query)
    return response.text or ""
