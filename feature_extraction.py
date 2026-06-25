import pandas as pd
import re

THEME_OPTIONS = [
    "語源・語彙", "日本語文法", "音声・音韻", "意味・論理", "文字・漢字",
    "方言・地域語", "心理・認知", "コミュニケーション", "歴史・文化",
    "科学・自然", "クイズ・ゲーム", "読書・学習", "雑談・ライブ", "その他"
]
EMOTION_OPTIONS = ["驚き", "疑問", "共感", "知識欲", "笑い", "違和感", "議論", "実用", "その他"]
DIFFICULTY_OPTIONS = ["初級", "中級", "上級"]
AUDIENCE_OPTIONS = ["一般", "言語好き", "学生", "ビジネス層", "読書好き", "雑学好き", "その他"]
TITLE_TYPE_OPTIONS = [
    "質問型", "断定型", "謎解き型", "検証型", "解説型",
    "クイズ型", "ランキング型", "雑談型", "ライブ型", "その他"
]

if __name__ == "__main__":
    df = pd.read_csv("youtube_videos_categorized.csv", encoding="utf-8-sig")
    print(f"データ読み込み完了: {len(df)} 件")


def classify_theme(title, category):
    t = title

    if re.search(r'ライブ|生放送|後夜祭|全国ツアー', t):
        return '雑談・ライブ'
    if re.search(r'温泉旅館|旅館で|寝落ち用|ダラダラ喋る|布団で', t):
        return '雑談・ライブ'
    if '雑談回' in t or ('雑談' in t and '言語学的に正しい雑談' not in t and '雑談の話題' not in t):
        return '雑談・ライブ'

    if re.search(r'クイズ|エウレーカ|しりとり|罵ろう|集めろ', t):
        return 'クイズ・ゲーム'

    if re.search(r'方言|関西弁|讃岐弁|鹿児島方言|エセ関西弁|手話', t):
        return '方言・地域語'

    if re.search(r'漢字|ひらがな|カタカナ|五十音|竹冠|方言漢字', t):
        return '文字・漢字'

    if re.search(r'意味論|語用論|真理値|サピア|ウォーフ|言語哲学', t):
        return '意味・論理'

    if re.search(r'文法|助詞|係り結び|「はい」と「うん」|関係詞', t):
        return '日本語文法'
    if re.search(r'「ます」|「っす」|タメ語|乱れているのか|死にかけている', t):
        return '日本語文法'

    if re.search(r'心理|認知|スキーマ|視覚思考|プロジェクション|努力中毒|自己肯定感|自己評価', t):
        return '心理・認知'
    if re.search(r'ミステイクアワード|スケールエラー|脳内を見せ|キモいのか', t):
        return '心理・認知'
    if category == '心理学・認知':
        return '心理・認知'

    if re.search(r'歴史|古語|江戸|平安|明治|古代|漂流|黒歴史|今と昔|花言葉|下ネタ古文|校正者', t):
        return '歴史・文化'
    if re.search(r'名古屋は.*作られた|オリンピックの輪', t):
        return '歴史・文化'
    if category == '歴史・文化':
        return '歴史・文化'

    if re.search(r'音声|発音|アクセント|音韻|母音|子音|響き|オノマトペ', t):
        return '音声・音韻'

    if re.search(r'遺伝子|農薬|甘味料|生態|FOXP2|アル中|植物|ペンギン', t):
        return '科学・自然'
    if re.search(r'世界中の色|色を調べ|記憶力.*筋力|図鑑', t):
        return '科学・自然'
    if category == '科学・自然':
        return '科学・自然'

    if re.search(r'コミュニケーション|よろしくお願い|言葉のすれ違い|徹底討論|炎上した|嫌われるのか|暴力になりうる', t):
        return 'コミュニケーション'
    if re.search(r'言語学的に正しい雑談|不毛な対立|「論理的」.*地域|バズ|LINE.*返せない', t):
        return 'コミュニケーション'
    if re.search(r'「推し」|気象庁.*Webサイト|歯医者.*言うのか|結論から喋る', t):
        return 'コミュニケーション'
    if category == 'コミュニケーション':
        return 'コミュニケーション'
    if category == '社会・時事':
        return 'コミュニケーション'

    if re.search(r'辞書|教科書|ベスト本|名著|国語辞典|文献学|本大賞|品切れ|予約開始', t):
        return '読書・学習'
    if re.search(r'読書|本を読む|良い本|本.*語る|書いた本', t):
        return '読書・学習'

    if re.search(r'語源|由来|外来語|単語を集め|語彙|うんちく', t):
        return '語源・語彙'
    if re.search(r'account|right.*「右」|懐石料理|コスプレ界隈|ルー大柴|「彼女」|「弁」|まだ労働', t):
        return '語源・語彙'
    if re.search(r'意味多すぎ|意味が意外|どう訳す|共通点を見つけ', t):
        return '語源・語彙'

    if category == '語源・語彙':
        return '語源・語彙'
    if category == '文字・漢字':
        return '文字・漢字'
    if category == '言語学':
        return '語源・語彙'

    return 'その他'


def classify_emotion(title):
    t = title

    if re.search(r'炎上|論争|徹底討論|本当に正しいのか|乱れているのか|怒らせた|嫌われるのか|不毛な対立', t):
        return '議論'

    if re.search(r'死にかけている|消える日|暴力になりうる|失礼じゃない|キモいのか', t):
        return '違和感'

    if re.search(r'使えばいい|どっちを優先|学べ！|コツ|おすすめ|ベスト|どう訳す', t):
        return '実用'

    if re.search(r'衝撃|驚き|意外すぎ|強すぎた|すごすぎ|！！！！！|なんと|まさか|真逆', t):
        return '驚き'

    if re.search(r'おもしろ|面白|インテリ悪口|ウケる', t):
        return '笑い'

    if re.search(r'悲劇|感動が生まれた|申し訳ありません|あるある|苦節|泣いちゃった', t):
        return '共感'

    if '？' in t:
        return '疑問'
    if re.search(r'なぜ|どうして|どうやって|なんで|どういうこと', t):
        return '疑問'

    return '知識欲'


def classify_difficulty(title, category):
    t = title

    upper_terms = [
        '意味論', '語用論', '言語哲学', 'サピア=ウォーフ', 'FOXP2', '歴史言語学',
        '真理値', '記述言語学', '言語類型論', '認知言語学', '音韻論', '形態論', '統語論',
        '係り結び', 'ちょいガチ', '文献学', '意味論勉強会', '言語学オリンピック'
    ]
    if any(k in t for k in upper_terms):
        return '上級'

    beginner_terms = ['クイズ', 'しりとり', 'ライブ', '入門', '初心者', '雑談', '寝落ち']
    if any(k in t for k in beginner_terms):
        return '初級'

    return '中級'


def classify_audience(title, category):
    t = title

    if re.search(r'辞書|ベスト本|名著|国語辞典|文献学|読書|本を読む|良い本|本大賞|著者は|校正者|泣いちゃった話', t):
        return '読書好き'

    if re.search(r'教科書|テスト|受験|入試|英語オンチ', t):
        return '学生'

    if re.search(r'ビジネス|バーガーキング|広告|四季報|バズ', t):
        return 'ビジネス層'

    if re.search(r'うんちく|衝撃|意外すぎ|トリビア|おもしろ響き|ヘンな.*クイズ|キショ', t):
        return '雑学好き'

    if category in ['言語学', '語源・語彙', '文字・漢字', 'コミュニケーション', '心理学・認知']:
        return '言語好き'
    if re.search(r'言語学|語源|音韻|文法|方言|漢字|音声|翻訳|辞書|意味論|語用論', t):
        return '言語好き'

    if category in ['科学・自然', '歴史・文化', '社会・時事']:
        return '一般'
    if re.search(r'心理|認知|自己肯定感|自己評価|LINEをすぐ', t):
        return '一般'

    return '言語好き'


def classify_title_type(title):
    t = title

    if re.search(r'ライブ|生放送|後夜祭', t):
        return 'ライブ型'

    if re.search(r'クイズ|エウレーカ', t):
        return 'クイズ型'

    if re.search(r'ランキング|ベスト本.*語り|第.*位|年間ベスト', t):
        return 'ランキング型'

    if re.search(r'検証|やってみ|試してみ|を調べたら|実態をお伝え|解説してもらったら|対決|集めてみた', t):
        return '検証型'
    if 'しりとり' in t:
        return '検証型'

    if re.search(r'雑談回|旅館で|温泉旅館|寝落ち|ダラダラ|に出た話|語るよ', t):
        return '雑談型'

    if re.search(r'正体|謎|黒歴史|真実が明らか|の内情|暴露|秘密', t):
        return '謎解き型'

    if '？' in t:
        return '質問型'
    if re.search(r'なぜ|どうして|どうやって|なんで|どういうこと', t):
        return '質問型'

    if re.search(r'とは|について|を語り尽くす|を厳選しました|を集めました|を全部言います|徹底解説|の世界|◯◯', t):
        return '解説型'
    if re.search(r'を紹介|教えます|教えてくれ|堪能しよう|語り尽くす', t):
        return '解説型'

    return '断定型'


if __name__ == "__main__":
    # ===== メイン処理 =====
    features = []
    for _, row in df.iterrows():
        title = row['title']
        category = row['category']
        features.append({
            'theme': classify_theme(title, category),
            'emotion': classify_emotion(title),
            'difficulty': classify_difficulty(title, category),
            'audience': classify_audience(title, category),
            'title_type': classify_title_type(title),
        })

    features_df = pd.DataFrame(features)
    for col in features_df.columns:
        df[col] = features_df[col]

    output_path = "youtube_videos_features.csv"
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n保存完了: {output_path}")
    print(f"列: {list(df.columns)}")

    print("\n" + "=" * 50)
    for col in ["theme", "emotion", "difficulty", "audience", "title_type"]:
        print(f"\n【{col}】")
        print(df[col].value_counts().to_string())
    print("=" * 50)
