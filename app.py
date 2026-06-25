import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from feature_extraction import (
    classify_theme, classify_emotion,
    classify_difficulty, classify_audience, classify_title_type
)

df = pd.read_csv("youtube_videos_features.csv", encoding="utf-8-sig")

st.set_page_config(page_title="タイトル分析ツール", page_icon="🎙️", layout="centered")

st.markdown("""
<style>
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 {
        color: #e94560;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    .hero p {
        color: #a8b2d8;
        font-size: 1rem;
        margin: 0;
    }
    .stTextInput > div > div > input {
        border: 2px solid #0f3460;
        border-radius: 10px;
        font-size: 1.1rem;
        padding: 0.7rem 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #e94560;
        box-shadow: 0 0 0 2px rgba(233,69,96,0.2);
    }
    .example-label {
        color: #888;
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
    }
</style>
<div class="hero">
    <h1>🎙️ ゆる言語学ラジオ<br>タイトル分析ツール</h1>
    <p>488本の動画データをもとに、タイトル案の傾向と改善案を分析します</p>
</div>
""", unsafe_allow_html=True)

def suggest_titles(title, title_type, theme):
    # タイトルの核を抽出（よくある語尾を除去）
    core = title
    for pattern in ['について', 'とは何か', 'とは', 'の話', 'を解説', 'を語る',
                    'の世界', 'の秘密', 'のこと', 'に関して', 'をまとめ']:
        core = core.replace(pattern, '')
    core = core.strip('　 。！？')

    suggestions = []

    # クイズ型
    if title_type != "クイズ型":
        suggestions.append(("クイズ型", f"{core}、どっちが正しい？【クイズ】"))
        suggestions.append(("クイズ型", f"【エウレーカクイズ】{core}できる人いる？"))

    # 驚き型
    suggestions.append(("驚き型", f"実は意外！{core}の真実"))
    suggestions.append(("驚き型", f"{core}が想像と全然違った"))

    # 質問型
    if title_type != "質問型":
        suggestions.append(("質問型", f"なぜ{core}なのか？"))

    # ランキング型
    if theme in ["語源・語彙", "文字・漢字", "歴史・文化"]:
        suggestions.append(("ランキング型", f"知って得する{core}うんちくランキング"))

    return suggestions

theme_median = df.groupby("theme")["views"].median().round(0)
title_type_median = df.groupby("title_type")["views"].median().round(0)
overall_median = df["views"].median()

st.markdown('<p class="example-label">💡 例：「日本語の助詞が消える日」「語源クイズ！この言葉の意味は？」</p>', unsafe_allow_html=True)
title = st.text_input("", placeholder="タイトル案を入力してください...")

if title:
    theme = classify_theme(title, "")
    emotion = classify_emotion(title)
    difficulty = classify_difficulty(title, "")
    audience = classify_audience(title, "")
    title_type = classify_title_type(title)

    # 分類結果
    st.subheader("分類結果")
    col1, col2, col3 = st.columns(3)
    col1.metric("テーマ", theme)
    col2.metric("タイトル型", title_type)
    col3.metric("難易度", difficulty)
    col1.metric("ターゲット", audience)
    col2.metric("感情", emotion)

    # 統計的傾向
    st.subheader("統計的な傾向")
    t_med = int(theme_median.get(theme, 0))
    tt_med = int(title_type_median.get(title_type, 0))
    col1, col2, col3 = st.columns(3)
    col1.metric("このテーマの中央値", f"{t_med:,}回",
                delta=f"{int(t_med - overall_median):+,}回")
    col2.metric("このタイトル型の中央値", f"{tt_med:,}回",
                delta=f"{int(tt_med - overall_median):+,}回")
    col3.metric("全体中央値", f"{int(overall_median):,}回")

    # テーマ別再生数グラフ（現在位置をハイライト）
    st.subheader("テーマ別 中央値再生数（赤 = 入力タイトルのテーマ）")
    theme_sorted = theme_median.sort_values(ascending=True)
    colors = ["#e74c3c" if t == theme else "#3498db" for t in theme_sorted.index]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(theme_sorted.index, theme_sorted.values, color=colors)
    ax.set_xlabel("中央値再生数")
    ax.axvline(overall_median, color="gray", linestyle="--", label="全体中央値")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # 類似した過去の高再生数動画
    st.subheader("同テーマ・同タイトル型の高再生数動画 TOP5")
    similar = df[(df["theme"] == theme) & (df["title_type"] == title_type)]
    if len(similar) == 0:
        similar = df[df["theme"] == theme]
    top5 = similar.sort_values("views", ascending=False).head(5)[["title", "views"]].reset_index(drop=True)
    top5.index += 1
    top5.columns = ["タイトル", "再生数"]
    top5["再生数"] = top5["再生数"].apply(lambda x: f"{x:,}回")
    st.table(top5)

    # 改善案
    st.subheader("改善案")
    tips = []

    if title_type == "断定型":
        tips.append("📌 断定型は本数が多く埋もれやすい。「〇〇はどっち？」などクイズ型に変えると再生数が高まる傾向あり")
    elif title_type == "解説型":
        tips.append("📌 解説型は再生数が低め。具体的な問いかけ（質問型）や驚き要素を加えると良い")
    elif title_type == "質問型":
        tips.append("📌 質問型は中位。「クイズ・エウレーカ」などゲーム要素を加えるとさらに伸びやすい")
    elif title_type in ["クイズ型", "ランキング型"]:
        tips.append("✅ クイズ型・ランキング型は統計的に再生数が高い。この方向性は正解")
    elif title_type == "謎解き型":
        tips.append("📌 謎解き型は中位。「正体」「真実」などの言葉は興味を引くが、クイズ型ほど再生数は高くない")
    elif title_type == "検証型":
        tips.append("📌 検証型は中位。結果をタイトルに入れるとさらに効果的")
    elif title_type in ["雑談型", "ライブ型"]:
        tips.append("📌 雑談・ライブ型は固定ファン向け。新規視聴者へのリーチは限られる傾向あり")

    if theme == "その他":
        tips.append("📌 「その他」は最も再生数が低いカテゴリ。テーマを明確に示すキーワードを入れると良い")
    elif theme in ["日本語文法", "音声・音韻", "方言・地域語"]:
        tips.append(f"📌 「{theme}」は再生数が低め。クイズ要素や身近な例を加えると広がりやすい")
    elif theme in ["クイズ・ゲーム", "科学・自然", "コミュニケーション"]:
        tips.append(f"✅ 「{theme}」は再生数が高いテーマ。この方向性は統計的に有利")
    elif theme in ["語源・語彙", "意味・論理"]:
        tips.append(f"📌 「{theme}」は中位。「意外な語源」「実は〇〇だった」など驚き要素を加えると伸びやすい")
    elif theme in ["文字・漢字", "歴史・文化"]:
        tips.append(f"📌 「{theme}」は中位。クイズ形式にすると参加型になり伸びやすい")
    elif theme == "心理・認知":
        tips.append("✅ 「心理・認知」は再生数が高め。身近な体験と結びつけるとさらに効果的")
    elif theme == "読書・学習":
        tips.append("📌 「読書・学習」は読書好き層に刺さるが、一般層へのリーチは限られる")
    elif theme == "雑談・ライブ":
        tips.append("📌 「雑談・ライブ」は固定ファン向け。新規獲得には向いていないが、コミュニティ維持には有効")

    if difficulty == "上級":
        tips.append("📌 上級コンテンツは再生数が低め。「入門」「初めて学ぶ」などを加えると間口が広がる")
    elif difficulty == "初級":
        tips.append("✅ 初級コンテンツは再生数が高い傾向あり")
    elif difficulty == "中級":
        tips.append("📌 中級は再生数が最も低いゾーン。初級寄りの表現にするか、上級として専門性を前面に出す方が差別化しやすい")

    if audience == "言語好き":
        tips.append("📌 言語好き向けは再生数が低め。「うんちく」「雑学」など一般向けの表現にすると広がりやすい")
    elif audience == "雑学好き":
        tips.append("✅ 雑学好き向けは再生数が高い傾向あり")
    elif audience == "読書好き":
        tips.append("📌 読書好き向けは再生数が低め。「言語的な発見」に焦点を当てると広がりやすい")
    elif audience == "学生":
        tips.append("📌 学生向けは再生数が中位。「テスト」「受験」より「知的好奇心」に訴えると層が広がる")
    elif audience == "一般":
        tips.append("✅ 一般向けコンテンツは広い層にリーチしやすい")

    if emotion == "驚き":
        tips.append("✅ 驚き要素はクリック率を高める傾向あり。「意外」「実は」などの言葉が効果的")
    elif emotion == "議論":
        tips.append("📌 議論・炎上系は注目を集めるがリスクも高い。統計的には中位の再生数")
    elif emotion == "実用":
        tips.append("📌 実用系は検索流入には強いが、このチャンネルでは知的好奇心系の方が伸びる傾向あり")

    if not tips:
        tips.append("✅ このテーマ・タイトル型は統計的に伸びやすい組み合わせです")

    for tip in tips:
        st.info(tip)

    # タイトル改善案
    st.subheader("タイトル改善案（統計的に伸びやすい型に変換）")
    alt_titles = suggest_titles(title, title_type, theme)
    for typ, alt in alt_titles:
        t_med_alt = int(title_type_median.get(
            "クイズ型" if "クイズ" in typ else
            "質問型" if "質問" in typ else
            "ランキング型" if "ランキング" in typ else title_type, 0))
        st.success(f"**【{typ}】** {alt}　　→　中央値 {t_med_alt:,}回")
