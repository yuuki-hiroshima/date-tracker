
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

# import os                                   # フォルダ/ファイル操作に使う
# import csv                                  # CSVの読み書きに使う
# import json                                 # JSONの読み書きに使う
# from datetime import datetime, date         # 日付文字列→日付型の変換や今日の日付取得に使う

# data_dir = "data"                           # 変数名の理由: データ用ディレクトリ（*_dir は“フォルダ”の合図）
# os.makedirs(data_dir, exist_ok=True)        # 既にあってもエラーにしない安全な作成

# csv_path = os.path.join(data_dir, "event_log.csv")   # 変数名の理由: CSVの“道”（*_path は“ファイルパス”の合図）
# json_path = os.path.join(data_dir, "event_log.json") # JSON保存先パス

# # ---------- CSVが無ければヘッダーで新規作成 ----------
# if not os.path.exists(csv_path):                                        # 初回起動などファイルが無いとき
#     with open(csv_path, "w", encoding="utf-8", newline="") as f:        # "w": 新規/上書き, newline="": 余計な空行防止
#         writer = csv.writer(f)                                          # CSVの“書き手”
#         writer.writerow(["name", "date_iso"])                           # 変更: 今回は name/date_iso の2列
#         print("event_log.csv を新規作成しました（ヘッダーのみ）。")        # 状況メッセージ

# # ---------- 読み込み（CSV → 辞書） ----------
# records = {}                                                            # 役割: {イベント名: "YYYY-MM-DD"} の対応表
# with open(csv_path, "r", encoding="utf-8", newline="") as f:           # 読み込みモードで開く
#     reader = csv.DictReader(f)                                          # 1行→辞書 {"name": "...", "date_iso": "..."}
#     for row in reader:                                                  # 行ごとに処理
#         name = str(row.get("name", "")).strip()                         # 追記: 欠損に強い取り方 + 前後空白除去
#         if name == "":                                                  # 空名はスキップ
#             continue
#         date_iso = str(row.get("date_iso", "")).strip()                 # 追記: 日付は文字列のまま（"YYYY-MM-DD"）
#         # 形式ざっくりチェック（厳密にやりたければ try でパース）
#         if len(date_iso) != 10 or "-" not in date_iso:                  # 例: "2025-09-10" の長さ想定
#             continue
#         records[name] = date_iso                                        # 登録/上書き

# # ---------- ユーティリティ（よく使う処理を関数化） ----------
# def parse_ymd(s: str) -> date:                                          # 役割: "YYYY-MM-DD" → date型 にする
#     """YYYY-MM-DD を date 型に変換（不正なら ValueError）"""
#     return datetime.strptime(s, "%Y-%m-%d").date()                      # 変更: フォーマットを明示

# def format_jp(iso: str) -> str:                                         # 役割: ISO文字列を「YYYY年M月D日」に整形して表示用に
#     y, m, d = map(int, iso.split("-"))                                  # 追記: ゼロ埋めを外して日本語日付に
#     return f"{y}年{m}月{d}日"

# def save_to_csv(records: dict[str, str], csv_path: str) -> None:        # 役割: 全件をCSVにヘッダー付きで保存
#     with open(csv_path, "w", encoding="utf-8", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["name", "date_iso"])                           # 変更: 正しいヘッダー
#         for name in sorted(records.keys()):                             # 並びを固定（テストしやすい）
#             writer.writerow([name, records[name]])                      # 1行ずつ出力

# def save_to_json(records: dict[str, str], json_path: str) -> None:      # 役割: 全件をJSONに保存（見やすく整形）
#     rows = []                                                           # JSONは [{"name":..., "date_iso":...}, ...] の形に
#     for name in sorted(records.keys()):                                 # 並びを固定
#         rows.append({"name": name, "date_iso": records[name]})          # 1件ぶんの辞書を追加
#     with open(json_path, "w", encoding="utf-8") as f:
#         json.dump(rows, f, ensure_ascii=False, indent=2)                # 日本語OK/インデントで見やすく

# # ---------- メニュー（追加 / 確認 / 保存して終了） ----------
# while True:                                                             # 終了まで繰り返す
#     print("\n1) 追加  2) 確認  3) 保存して終了")                         # 選択肢の表示
#     choice = input("番号を入力してください（空で終了）：").strip()           # 入力値の取得（前後空白除去）

#     if choice == "":                                                    # 空でメニュー終了（任意）
#         print("終了します。")
#         break

#     if choice == "1":                                                   # 追加モード
#         while True:                                                     # 複数件を連続登録できるようループ
#             event = input("イベント名（空で追加終了）：").strip()             # イベント名を受け取る
#             if event == "":                                            # 空なら追加モード終了
#                 break
#             date_str = input("期日を入力（YYYY-MM-DD）：").strip()          # 期日を文字列で受け取る
#             try:
#                 dt = parse_ymd(date_str)                                # 変更: 正しいフォーマットか検証（不正なら except）
#             except ValueError:
#                 print("YYYY-MM-DD の形式で入力してください。")
#                 continue
#             records[event] = dt.isoformat()                             # 変更: 内部表現は常に ISO 文字列に統一
#             print(f"登録しました：{event}, {format_jp(records[event])}")    # 見やすい日本語日付でフィードバック

#     elif choice == "2":                                                 # 確認モード（経過日を出す）
#         while True:
#             check_event = input("調べたいイベント名（空で確認終了）：").strip()  # 調べたい名前
#             if check_event == "":
#                 break
#             if check_event not in records:                              # 変更: 存在チェックの正しい書き方
#                 print("一致するイベントはありません。")
#                 continue
#             # 参照日（入力日）を受け取る：空なら今日
#             ref_str = input("基準日（YYYY-MM-DD、空なら今日）：").strip()     # 追記: 入力が空なら今日にする
#             if ref_str == "":
#                 ref_date = date.today()                                 # 今日の日付（date型）
#             else:
#                 try:
#                     ref_date = parse_ymd(ref_str)                        # 指定された基準日をパース
#                 except ValueError:
#                     print("YYYY-MM-DD の形式で入力してください。")
#                     continue
#             base_iso = records[check_event]                              # 記録してある ISO 文字列を取得
#             base_date = parse_ymd(base_iso)                              # 計算のため date型へ
#             elapsed = (ref_date - base_date).days                        # 経過日数を整数で取得（マイナスなら未来）
#             # 出力（例に合わせた情報量）
#             print(f"登録内容：{check_event}, {format_jp(base_iso)}")       # 登録済みの期日（日本語表記）
#             print(f"入力日：{format_jp(ref_date.isoformat())}")           # 基準日（日本語表記）
#             print(f"経過日：{elapsed}日")                                 # 日数（負なら「-◯日」）

#     elif choice == "3":                                                 # 保存して終了
#         save_to_csv(records, csv_path)                                  # CSVに保存
#         save_to_json(records, json_path)                                # JSONにも保存
#         print("CSV と JSON に保存しました。終了します。")
#         break

#     else:
#         print("1 / 2 / 3 のいずれかを入力してください。")                    # 入力ミスへの案内


# # ========== 型の練習1 ===========

# import os
# import csv
# import json
# from datetime import datetime, date

# def load_csv(path: str) -> dict[str, str]:
#     out: dict[str, str] = {}
#     with open(path, "r", encoding="utf-8", newline="") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             name = (row.get("name") or "").strip()
#             iso = (row.get("date_iso") or "").strip()
#             if name and iso:
#                 out[name] = iso
#     return out

# def save_csv(records: dict[str, str], path: str) -> None:
#     with open(path, "w", encoding="utf-8", newline="") as f:
#         w = csv.writer(f)
#         w.writerow(["name", "date_iso"])
#         for name in sorted(records):
#             w.writerow([name, records[name]])

# def save_json(records: dict[str, str], path: str) -> None:
#     rows = [{"name": n, "date_iso": records[n]} for n in sorted(records)]
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(rows, f, ensure_ascii=False, indent=2)

# def days_between(iso_a: str, iso_b: str) -> int:
#     a = datetime.strptime(iso_a, "%Y-%m-%d").date()
#     b = datetime.strptime(iso_b, "%Y-%m-%d").date()
#     return (b - a).days


# # ========== 型の練習2 ===========

# import os
# import csv
# import json
# from datetime import datetime, date

# def load_csv(path: str) -> dict[str, str]:
#     out: dict[str, str] = {}
#     with open(path, "r", encoding="utf-8", newline="") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             name = (row.get("name") or "").strip()
#             iso = (row.get("date_iso") or "").strip()
#             if name and iso:
#                 out[name] = iso
#     return out

# def save_csv(records: dict[str, str], path: str) -> None:
#     with open(path, "w", encoding="utf-8", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["name", "date_iso"])
#         for name in sorted(records):
#             writer.writerow([name, records[name]])

# def save_json(records: dict[str, str], path: str) -> None:
#     rows = [{"name": n, "date_iso": records[n]} for n in sorted(records)]
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(rows, f, ensure_ascii=False, indent=2)

# def days_between(iso_a: str, iso_b: str) -> int:
#     a = datetime.strptime(iso_a, "%Y-%m-%d").date()
#     b = datetime.strptime(iso_b, "%Y-%m-%d").date()
#     return (b - a).days



# # ========== 型の練習3 ===========

# import os
# import csv
# import json
# from datetime import datetime, date

def load_csv(path: str) -> dict[str, str]:                              # 役割: CSV(列: name,date_iso)を読み、{name: date_iso} の辞書で返す
    out: dict[str, str] = {}                                            # 返却用の空辞書を用意（変数名 out: “出力結果”の意味で覚えやすい）
    with open(path, "r", encoding="utf-8", newline="") as f:            # ファイルを読み込みモードで開く（UTF-8/改行崩れ防止）
        reader = csv.DictReader(f)                                      # 1行を {"name": "...", "date_iso": "..."} の辞書として受け取れる“読み手”
        for row in reader:                                              # CSVの各行を1件ずつ処理
            name = (row.get("name") or "").strip()                      # 列nameを安全に取得（欠損は""に）→前後空白除去（入力ブレ対策）
            iso = (row.get("date_iso") or "").strip()                   # 列date_isoも同様に取得→空白除去（常に文字列で扱うのがポイント）
            if name and iso:                                            # どちらも空でなければ有効データとみなす
                out[name] = iso                                         # 結果辞書へ登録（同じnameがあれば後勝ち＝上書き仕様）
    return out                                                          # 取り込み完了。内部表現は {name: "YYYY-MM-DD"} で統一（保存・計算が安定）

def save_csv(records: dict[str, str], path: str) -> None:               # 役割: {name: date_iso} をCSVへヘッダー付きで保存
    with open(path, "r", encoding="utf-8", newline="") as f:            # 書き込みモード（既存があれば上書き）
        writer = csv.writer(f)                                          # リストを1行として書き出す“書き手”を用意
        writer.writerow(["name", "date_iso"])                           # 1行目に列名（ヘッダー）を書いて形式を明示
        for name in sorted(records):                                    # 並び順を固定（Gitの差分が安定／テストしやすい）
            writer.writerow([name, records[name]])                      # 1行分を書き込む（値は文字列のまま保存される）

def save_json(records: dict[str, str], path: str) -> None:                  # 役割: {name: date_iso} をJSONへ保存（人が読める整形）
    rows = [{"name": n, "date_iso": records[n]} for n in sorted(records)]   # JSONの素: 辞書の配列へ変換（順序固定）
    with open(path, "w", encoding="utf-8") as f:                            # JSONはテキストなので newline="" は不要
        json.dump(rows, f, ensure_ascii=False, indent=2)                    # ensure_ascii=False: 日本語そのまま／indent=2: 見やすく整形

def days_between(iso_a: str, iso_b: str) -> int:                            # 役割: 2つの日付文字列の差（b - a）の“日数”を整数で返す
    a = datetime.strptime(iso_a, "%Y-%m-%d").date()                         # 文字列→日付型に変換（%Y-%m-%d を明示して入力ミスを検出）
    b = datetime.strptime(iso_b, "%Y-%m-%d").date()                         # 同上。date() で時刻情報を切り落として“日”単位にそろえる
    return (b - a).days                                                     # datetime.date 同士の差分は timedelta。daysで“日数”だけ取り出す（負値なら“未来までの残り日数”）


# # ========== 型の練習4 ===========

# import os
# import csv
# import json
# from datetime import datetime, date

# def load_csv(path: str) -> dict[str, str]:
#     out: dict[str, str] = {}
#     with open(path, "r", encoding="utf-8", newline="") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             name = (row.get("name") or "").strip()
#             iso = (row.get("date_iso") or "").strip()
#             if name and iso:
#                 out[name] = iso
#     return out

# def save_csv(records: dict[str, str], path: str) -> None:
#     with open(path, "w", encoding="utf-8", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["name", "date_iso"])
#         for name in sorted(records):
#             writer.writerow([name, records[name]])

# def sava_json(records: dict[str, str], path: str) -> None:
#     rows = [{"name": n, "date_iso": records[n]} for n in sorted(records)]
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(path, f, ensure_ascii=False, indent=2)

# def days_between(iso_a: str, iso_b: str) -> int:
#     a = datetime.strptime(iso_a, "%Y-%m-%d").date()
#     b = datetime.strptime(iso_b, "%Y-%m-%d").date()
#     return (b - a).days


# # ========== 型の練習5 ===========

# import csv
# import json
# from datetime import datetime, date

# def load_csv(path: str) -> dict[str, str]:
#     out: dict[str, str] = {}
#     with open(path, "r", encoding="utf-8", newline="") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             name = (row.get("name") or "").strip()
#             iso = (row.get("date_iso") or "").strip()
#             if name and iso:
#                 out[name] = iso
#     return out

# def save_csv(records: dict[str, str], path: str) -> None:
#     with open(path, "w", encoding="utf-8", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["name", "date_sio"])
#         for name in sorted(records):
#             writer.writerow([name, records[name]])

# def save_json(records: dict[str, str], path: str) -> None:
#     rows = [{"name": n, "date_iso": records[n]} for n in sorted(records)]
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(rows, f, ensure_ascii=False, indent=2)

# def days_between(iso_a: str, iso_b: str) -> int:
#     a = datetime.strptime(iso_a, "%Y-%m-%d").date()
#     b = datetime.strptime(iso_b, "%Y-%m-%d").date()
#     return (b - a).days

# ========== 型の練習6 → 改良と拡張 ===========

import csv
import json
from datetime import datetime, date

def load_csv(path: str) -> dict[str, str]:
    out: dict[str, str] = {}
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or "").strip()
            iso = (row.get("date_iso") or "").strip()
            if name and iso:
                out[name] = iso
            print("ROW:", row)
    return out

def load_json(path: str) -> dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    out: dict[str, str] = {}
    for row in data:
        title = (row.get("title") or row.get("name") or "").strip()
        iso = (row.get("created_at") or row.get("date_iso") or "").strip()

        if not (title and iso):
            continue

        try:
            datetime.strptime(iso, "%Y-%m-%d")
        except ValueError:
            continue

        out[title] = iso
    return out

def save_csv(records: dict[str, str], path: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "date_iso"])
        for name in sorted(records):
            writer.writerow([name, records[name]])

def save_json(records: dict[str, str], path: str) -> None:
    rows = [{"name": n, "date_iso": records[n]} for n in sorted(records)]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

def days_between(iso_a: str, iso_b: str) -> int:
    a = datetime.strptime(iso_a, "%Y-%m-%d").date()
    b = datetime.strptime(iso_b, "%Y-%m-%d").date()
    return (b - a).days

records = {"電池交換": "2025-09-10", "フィルター清掃": "2025-08-01"}

# 1) 保存 → 2) 読み戻し → 3) 一致確認
records = {"フィルター清掃": "2025-08-01", "電池交換": "2025-09-10"}
save_json(records, "data/test.json")
loaded = load_json("data/test.json")
assert loaded == records, "JSONの往復で内容が変わっていないこと"

# 2) CSV保存→読込
save_csv(records, "data/test.csv")
loaded = load_csv("data/test.csv")
assert loaded == records

# 3) 日数
assert days_between("2025-09-10", "2025-09-20") == 10

assert days_between("2025-01-01","2025-01-01")==0
assert days_between("2025-12-31","2026-01-01")==1

# 4) ついでに日数テスト（自己テスト）
assert days_between("2025-09-10", "2025-09-20") == 10
assert days_between("2025-09-20", "2025-09-10") == -10

# ========== 実験・改造 ===========

# import csv
# import json
# from datetime import datetime, date

# def load_csv(path: str) -> dict[str, str]:
#     out: dict[str, str] = {}
#     with open(path, "r", encoding="utf-8", newline="") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             name = (row.get("title") or "").strip()
#             iso = (row.get("created_at") or "").strip()
#             if name and iso:
#                 out[name] = iso
#     return out

# def save_csv(records: dict[str, str], path: str) -> None:
#     with open(path, "w", encoding="utf-8", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["title", "created_at"])
#         for title in sorted(records):
#             writer.writerow([title, records[title]])

# def save_json(records: dict[str, str], path: str) -> None:
#     rows = [{"title": t, "created_at": records[t]} for t in sorted(records)]
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(rows, f, ensure_ascii=False, indent=2)

# def days_between(iso_a: str, iso_b: str) -> int:
#     a = datetime.strptime(iso_a, "%Y-%m-%d").date()
#     b = datetime.strptime(iso_b, "%Y-%m-%d").date()
#     return (b - a).days