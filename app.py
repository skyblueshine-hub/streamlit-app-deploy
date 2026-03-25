from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


# ===== LLM呼び出し関数 =====
def get_llm_response(user_input, expert_type):
    if expert_type == "ITエンジニア":
        system_prompt = "あなたは優秀なITエンジニアです。技術的に正確で分かりやすく回答してください。"
    elif expert_type == "マーケター":
        system_prompt = "あなたは優秀なマーケターです。ビジネス視点で分かりやすく回答してください。"
    else:
        system_prompt = "あなたは親切なアシスタントです。"

    api_key = st.secrets["OPENAI_API_KEY"]

    llm = ChatOpenAI(
        temperature=0.7,
        model="gpt-4o-mini",
        api_key=api_key
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    response = llm.invoke(messages)
    return response.content


# ===== 画面UI =====
st.set_page_config(page_title="LangChain LLMアプリ", page_icon="💬")
st.title("💬 LangChain LLMアプリ")

st.write("""
このアプリでは、入力したテキストをLLMに送信し、回答を表示します。  
また、ラジオボタンで専門家の種類を選択すると、その専門家として回答します。

【使い方】
1. 専門家タイプを選択
2. テキストを入力
3. 実行ボタンを押す
""")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY が Streamlit Secrets に設定されていません。")
    st.stop()

expert_type = st.radio(
    "専門家の種類を選択してください",
    ["ITエンジニア", "マーケター"]
)

user_input = st.text_input("質問を入力してください")

if st.button("実行"):
    if user_input.strip():
        try:
            with st.spinner("回答を生成中です..."):
                result = get_llm_response(user_input, expert_type)
            st.write("### 回答")
            st.write(result)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("テキストを入力してください")
