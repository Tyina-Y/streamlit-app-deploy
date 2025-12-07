from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Check if OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ and "OPENAI_API_KEY" not in st.secrets:
    st.error("⚠️ OpenAI APIキーが設定されていません。Streamlit Cloudの場合は、'Manage app' → 'Settings' → 'Secrets'で設定してください。")
    st.stop()

st.title("カウンセターアプリ")
input_message = st.text_input(label="質問領域ボタンを選択して、質問を入力してください。")
text_count = len(input_message)

def result_chain(param, system_template):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{input}")
    ])
    chain = prompt | llm
    result = chain.invoke({"input": param})
    return result.content

def get_childcare_stress_advice(param):
    system_template = """
    あなたは親の育児ストレスを軽減するための専門家です。
    育児疲れやストレス管理に関する実践的なアドバイスを提供します。
    親自身の心身の健康を保つための方法を教えます。
    """
    result = result_chain(param, system_template)
    return result

def get_childcare_nutrition_advice(param):
    system_template = """
    あなたは子どもの栄養に詳しいアドバイザーです。
    子どもの健康な発育を支える食事や栄養バランスについてアドバイスを提供します。
    食事の習慣や偏食に関する質問にも丁寧に答えます。
    """
    result = result_chain(param, system_template)
    return result

if st.button("育児ストレスについて質問する"):
    if text_count > 0:
        try:
            with st.spinner("回答を生成中..."):
                result = get_childcare_stress_advice(input_message)
            st.write(f"回答: **{result}**")
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.warning("質問を入力してください。")

if st.button("子どもの栄養について質問する"):
    if text_count > 0:
        try:
            with st.spinner("回答を生成中..."):
                result = get_childcare_nutrition_advice(input_message)
            st.write(f"回答: **{result}**")
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.warning("質問を入力してください。")