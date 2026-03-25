from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


# ===== LLM呼び出し関数 =====
def get_llm_response(user_input, expert_type):
    # 専門家ごとのシステムメッセージ
    if expert_type == "ITエンジニア":
        system_prompt = "あなたは優秀なITエンジニアです。技術的に正確で分かりやすく回答してください。"
    elif expert_type == "マーケター":
        system_prompt = "あなたは優秀なマーケターです。ビジネス視点で分かりやすく回答してください。"
    else:
        system_prompt = "あなたは親切なアシスタントです。"

    # LangChainでLLM設定
    llm = ChatOpenAI(
        temperature=0.7,
        model_name="gpt-4o-mini"
    )

    # メッセージ作成
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    # LLM実行
    response = llm.invoke(messages)

    return response.content


# ===== 画面UI =====
st.title("💬 LangChain LLMアプリ")

st.write("""
このアプリでは、入力したテキストをLLMに送信し、回答を表示します。  
また、ラジオボタンで専門家の種類を選択すると、その専門家として回答します。

【使い方】
1. 専門家タイプを選択
2. テキストを入力
3. 実行ボタンを押す
""")

# ラジオボタン
expert_type = st.radio(
    "専門家の種類を選択してください",
    ["ITエンジニア", "マーケター"]
)

# 入力フォーム
user_input = st.text_input("質問を入力してください")

# 実行ボタン
if st.button("実行"):
    if user_input:
        result = get_llm_response(user_input, expert_type)
        st.write("### 回答")
        st.write(result)
    else:
        st.warning("テキストを入力してください")