import streamlit as st
import pandas as pd
import os

# ページ設定
st.set_page_config(page_title="Frontale Manager", layout="centered")

# --- 👑 画面をフロンターレカラーにする魔法 (安全なスタイル設定) ---
st.markdown("""
    <style>
    /* 勝ち点などの数字を水色にする */
    [data-testid="stMetricValue"] { color: #00A3E0 !important; }
    /* サブヘッダーの線の下の色 */
    h2 { border-bottom: 2px solid #00A3E0; }
    </style>
    """, unsafe_allow_html=True)

CSV_FILE = "results.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["節", "相手", "結果", "得点", "失点", "順位"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

def calc_points(res):
    if res == "勝": return 3
    if res == "PK勝": return 2
    if res == "PK負": return 1
    return 0

# アプリのメイン表示
st.title("🐬 フロンターレ戦績 & 順位管理")

df = load_data()

# --- 1. 入力フォーム（サイドバー） ---
with st.sidebar:
    st.header("📝 試合結果の入力")
    with st.form("input_form", clear_on_submit=True):
        sect = st.number_input("節", min_value=1, step=1)
        opponent = st.text_input("対戦相手")
        result = st.selectbox("結果", ["勝", "PK勝", "PK負", "負"])
        score_get = st.number_input("得点", min_value=0, step=1)
        score_lost = st.number_input("失点", min_value=0, step=1)
        rank = st.number_input("試合終了後の順位", min_value=1, step=1)
        
        submitted = st.form_submit_button("記録を保存")
        if submitted:
            new_data = pd.DataFrame([[sect, opponent, result, score_get, score_lost, rank]], 
                                    columns=["節", "相手", "結果", "得点", "失点", "順位"])
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success(f"第{sect}節の結果を保存しました！")

# --- 2. 勝ち点と戦績内訳の計算 ---
df["勝ち点"] = df["結果"].apply(calc_points)
total_points = df["勝ち点"].sum()

v_90 = len(df[df["結果"] == "勝"])
v_pk = len(df[df["結果"] == "PK勝"])
l_pk = len(df[df["結果"] == "PK負"])
l_90 = len(df[df["結果"] == "負"])

# --- 3. 画面表示 ---
m1, m2, m3 = st.columns(3)
m1.metric("総勝ち点", f"{total_points} pts")
# 最新順位の表示（データがない場合はハイフン）
current_rank = f"{df.iloc[-1]['順位']} 位" if len(df) > 0 else "-"
m2.metric("最新順位", current_rank)
m3.metric("試合数", f"{len(df)}")

st.subheader("📊 戦績内訳")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"**90分勝** \n# {v_90}")
c2.markdown(f"**PK勝** \n# {v_pk}")
c3.markdown(f"**PK負** \n# {l_pk}")
c4.markdown(f"**90分負** \n# {l_90}")

st.subheader("📋 リーグ戦記録一覧")
# データフレームの表示（配置はライブラリにお任せ）
st.dataframe(df.drop(columns=["勝ち点"]), use_container_width=True, hide_index=True)

if st.button("直近の記録を消去"):
    if len(df) > 0:
        df = df[:-1]
        save_data(df)
        st.rerun()