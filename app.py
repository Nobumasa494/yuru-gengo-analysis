import streamlit as st
import pandas as pd
from feature_extraction import (
    classify_theme, classify_emotion,
    classify_difficulty, classify_audience, classify_title_type
)

df = pd.read_csv("youtube_videos_features.csv", encoding="utf-8-sig")

theme_median = df.groupby("theme")["views"].median().round(0)
title_type_median = df.groupby("title_type")["views"].median().round(0)
overall_median = df["views"].median()

st.title("ゆる言語学ラジオ タイトル分析ツール")
title = st.text_input("タイトル案を入力してください")

if title:
    theme = classify_theme(title, "")
    emotion = classify_emotion(title)
    difficulty = classify_difficulty(title, "")
    audience = classify_audience(title, "")
    title_type = classify_title_type(title)

    st.subheader("分類結果")
    col1, col2 = st.columns(2)
    col1.metric("テーマ", theme)
    col2.metric("タイトル型", title_type)
    col1.metric("難易度", difficulty)
    col2.metric("ターゲット", audience)

    st.subheader("統計的な傾向")
    t_med = int(theme_median.get(theme, 0))
    tt_med = int(title_type_median.get(title_type, 0))
    col1, col2 = st.columns(2)
    col1.metric("このテーマの中央値再生数", f"{t_med:,}回",
                delta=f"{int(t_med - overall_median):+,}回 (全体比)")
    col2.metric("このタイトル型の中央値再生数", f"{tt_med:,}回",
                delta=f"{int(tt_med - overall_median):+,}回 (全体比)")

    st.subheader("改善案")
    tips = []
    if title_type not in ["クイズ型", "ランキング型"]:
        tips.append("「クイズ型」タイトルは統計的に再生数が高い傾向あり（例：〇〇はどっち？）")
    if theme not in ["クイズ・ゲーム", "科学・自然", "コミュニケーション"]:
        tips.append(f"現在のテーマ「{theme}」より「クイズ・ゲーム」系の方が再生数が高い傾向あり")
    if not tips:
        tips.append("このテーマ・タイトル型は統計的に伸びやすい組み合わせです")
    for tip in tips:
        st.info(tip)
