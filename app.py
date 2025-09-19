
# ========== 自作コード ===========

# import os
# import csv
# import json
# from datetime import datetime

# data_dir = "data"
# os.makedirs(data_dir, exist_ok=True)

# csv_path = os.path.join(data_dir, "event_log.csv")
# json_path = os.path.join(data_dir, "event_log.json")

# if not os.path.exists(csv_path):
#     with open(csv_path, "w", encoding="utf-8", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["name", "date_iso"])
#         print("event_log.csv を新規作成しました。")

# records = {}

# with open(csv_path, "r", encoding="utf-8", newline="") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         name = row["name"].strip()
#         if name == "":
#             continue
#         records[name] = date_iso

# def save_to_csv(records, csv_path):
#     with open(csv_path, "w", encoding="utf-8", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["name", "date_iso"])

# def save_to_json(records, json_path):
#     rows = []
#     with open(json_path, "w", encoding="utf-8") as f:
#         json.dump(rows, f, ensure_ascii=False, indent=2)

# while True:
#     print("1) 追加  2) 確認 3) 保存して終了")
#     choice = input("番号を入力してください（空入力で終了）：").strip()

#     if choice == "1":
#         while True:
#             event = input("イベント名を入力してください：").strip()
#             if event == "":
#                 break
#             date_str = input("日時を入力してください（YYYY-MM-DD）：").strip()
#             try:
#                 date = datetime.strptime(date_str, "%Y-%m-%d")
#             except ValueError:
#                 print("日時（YYYY-MM-DD）を入力してください。")
#                 continue
#             records[event] = date

#     elif choice == "2": # 記述すべきコードがわからない
#         while True:
#             check_event = input("イベント名を入力してください（空入力で終了）：").strip()
#             if check_event == "":
#                 break
#             elif check_event not in records:
#                 print("一致するイベントはありません。")
#                 continue
#             else:
#                 elapsed = (入力日 - 記録日).days  # 記述すべきコードがわからない
#                 print(f"{elapsed}日が経ちました。")
    
#     elif choice == "3":
#         save_to_csv(records, csv_path)
#         save_to_json(records, json_path)
#         print("CSV と JSON に保存しました。")
#         break

#     else:
#         print("1 / 2 / 3 のいずれかを入力してください。")


# ========== ChatGPTの修正バージョン ===========

import os                                   # フォルダ/ファイル操作に使う
import csv                                  # CSVの読み書きに使う
import json                                 # JSONの読み書きに使う
from datetime import datetime, date         # 日付文字列→日付型の変換や今日の日付取得に使う

data_dir = "data"                           # 変数名の理由: データ用ディレクトリ（*_dir は“フォルダ”の合図）
os.makedirs(data_dir, exist_ok=True)        # 既にあってもエラーにしない安全な作成

csv_path = os.path.join(data_dir, "event_log.csv")   # 変数名の理由: CSVの“道”（*_path は“ファイルパス”の合図）
json_path = os.path.join(data_dir, "event_log.json") # JSON保存先パス

# ---------- CSVが無ければヘッダーで新規作成 ----------
if not os.path.exists(csv_path):                                        # 初回起動などファイルが無いとき
    with open(csv_path, "w", encoding="utf-8", newline="") as f:        # "w": 新規/上書き, newline="": 余計な空行防止
        writer = csv.writer(f)                                          # CSVの“書き手”
        writer.writerow(["name", "date_iso"])                           # 変更: 今回は name/date_iso の2列
        print("event_log.csv を新規作成しました（ヘッダーのみ）。")        # 状況メッセージ

# ---------- 読み込み（CSV → 辞書） ----------
records = {}                                                            # 役割: {イベント名: "YYYY-MM-DD"} の対応表
with open(csv_path, "r", encoding="utf-8", newline="") as f:           # 読み込みモードで開く
    reader = csv.DictReader(f)                                          # 1行→辞書 {"name": "...", "date_iso": "..."}
    for row in reader:                                                  # 行ごとに処理
        name = str(row.get("name", "")).strip()                         # 追記: 欠損に強い取り方 + 前後空白除去
        if name == "":                                                  # 空名はスキップ
            continue
        date_iso = str(row.get("date_iso", "")).strip()                 # 追記: 日付は文字列のまま（"YYYY-MM-DD"）
        # 形式ざっくりチェック（厳密にやりたければ try でパース）
        if len(date_iso) != 10 or "-" not in date_iso:                  # 例: "2025-09-10" の長さ想定
            continue
        records[name] = date_iso                                        # 登録/上書き

# ---------- ユーティリティ（よく使う処理を関数化） ----------
def parse_ymd(s: str) -> date:                                          # 役割: "YYYY-MM-DD" → date型 にする
    """YYYY-MM-DD を date 型に変換（不正なら ValueError）"""
    return datetime.strptime(s, "%Y-%m-%d").date()                      # 変更: フォーマットを明示

def format_jp(iso: str) -> str:                                         # 役割: ISO文字列を「YYYY年M月D日」に整形して表示用に
    y, m, d = map(int, iso.split("-"))                                  # 追記: ゼロ埋めを外して日本語日付に
    return f"{y}年{m}月{d}日"

def save_to_csv(records: dict[str, str], csv_path: str) -> None:        # 役割: 全件をCSVにヘッダー付きで保存
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "date_iso"])                           # 変更: 正しいヘッダー
        for name in sorted(records.keys()):                             # 並びを固定（テストしやすい）
            writer.writerow([name, records[name]])                      # 1行ずつ出力

def save_to_json(records: dict[str, str], json_path: str) -> None:      # 役割: 全件をJSONに保存（見やすく整形）
    rows = []                                                           # JSONは [{"name":..., "date_iso":...}, ...] の形に
    for name in sorted(records.keys()):                                 # 並びを固定
        rows.append({"name": name, "date_iso": records[name]})          # 1件ぶんの辞書を追加
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)                # 日本語OK/インデントで見やすく

# ---------- メニュー（追加 / 確認 / 保存して終了） ----------
while True:                                                             # 終了まで繰り返す
    print("\n1) 追加  2) 確認  3) 保存して終了")                         # 選択肢の表示
    choice = input("番号を入力してください（空で終了）：").strip()           # 入力値の取得（前後空白除去）

    if choice == "":                                                    # 空でメニュー終了（任意）
        print("終了します。")
        break

    if choice == "1":                                                   # 追加モード
        while True:                                                     # 複数件を連続登録できるようループ
            event = input("イベント名（空で追加終了）：").strip()             # イベント名を受け取る
            if event == "":                                            # 空なら追加モード終了
                break
            date_str = input("期日を入力（YYYY-MM-DD）：").strip()          # 期日を文字列で受け取る
            try:
                dt = parse_ymd(date_str)                                # 変更: 正しいフォーマットか検証（不正なら except）
            except ValueError:
                print("YYYY-MM-DD の形式で入力してください。")
                continue
            records[event] = dt.isoformat()                             # 変更: 内部表現は常に ISO 文字列に統一
            print(f"登録しました：{event}, {format_jp(records[event])}")    # 見やすい日本語日付でフィードバック

    elif choice == "2":                                                 # 確認モード（経過日を出す）
        while True:
            check_event = input("調べたいイベント名（空で確認終了）：").strip()  # 調べたい名前
            if check_event == "":
                break
            if check_event not in records:                              # 変更: 存在チェックの正しい書き方
                print("一致するイベントはありません。")
                continue
            # 参照日（入力日）を受け取る：空なら今日
            ref_str = input("基準日（YYYY-MM-DD、空なら今日）：").strip()     # 追記: 入力が空なら今日にする
            if ref_str == "":
                ref_date = date.today()                                 # 今日の日付（date型）
            else:
                try:
                    ref_date = parse_ymd(ref_str)                        # 指定された基準日をパース
                except ValueError:
                    print("YYYY-MM-DD の形式で入力してください。")
                    continue
            base_iso = records[check_event]                              # 記録してある ISO 文字列を取得
            base_date = parse_ymd(base_iso)                              # 計算のため date型へ
            elapsed = (ref_date - base_date).days                        # 経過日数を整数で取得（マイナスなら未来）
            # 出力（例に合わせた情報量）
            print(f"登録内容：{check_event}, {format_jp(base_iso)}")       # 登録済みの期日（日本語表記）
            print(f"入力日：{format_jp(ref_date.isoformat())}")           # 基準日（日本語表記）
            print(f"経過日：{elapsed}日")                                 # 日数（負なら「-◯日」）

    elif choice == "3":                                                 # 保存して終了
        save_to_csv(records, csv_path)                                  # CSVに保存
        save_to_json(records, json_path)                                # JSONにも保存
        print("CSV と JSON に保存しました。終了します。")
        break

    else:
        print("1 / 2 / 3 のいずれかを入力してください。")                    # 入力ミスへの案内


# ==========  ===========





# ==========  ===========



# ==========  ===========