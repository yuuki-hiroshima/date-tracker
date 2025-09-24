
# ========== 完成イメージ（登録機能を追加） ==========

# 入力：
#     ・コマンド引数で受け取る
#     ・名前と日付は必須（前後の空白は削除）
#     ・欠けている or 日付形式が違うなら、エラーメッセージを表示し終了

# 処理：
#     ・JSONを読み込む（無ければ空）（理由：読み取りは1つに絞ると単純化、保存は両方で互換を保つ）
#     ・入力を検証する
#     ・辞書に上書き登録
#     ・JSONとCSVの両方へ保存

# 出力：
#     ・「登録：<名前>=<日付>」のように1行で確定結果を表示

# エラー対応：
#     ・処理を中断しメッセージを表示（終了コードは気にしなくてOK：将来sys.exit(1)にする余地あり）

# 補足：
#     前後だけ削除（strip()）にするか、中の空白も全削除にするか（"".join(s.split())）はお好み。

# ========== 擬似コード（登録機能を追加） ==========

# パスの固定：
#     json_path = "data/event_log.json" / csv_path = "data/event_log.csv"

# 入力：
#   コマンド引数を解析する（--add <NAME> <DATE>）。
# 	NAME = NAME.strip() / DATE = DATE.strip()。
# 	NAME が空なら「名前を指定してください」とエラー終了。
# 	DATE が "YYYY-MM-DD" かを is_iso_date(DATE) で確認。NGなら「日付は YYYY-MM-DD 形式で」とエラー終了。

# 処理：
#     records = load_json(json_path)（無ければ {} が返る）。
#     records[NAME] = DATE（上書き登録）。
#     save_json(records, json_path) と save_csv(records, csv_path) を呼ぶ。

# 出力：
#     登録：<NAME> = <DATE> と1行表示。


# ========== Pythonコード（登録機能を追加） ==========

# import argparse  # コマンドライン引数を解析する標準ライブラリ
# # コア関数は tracker_core から再利用（CLIとロジックを分離）
# from tracker_core import is_iso_date, load_json, save_json, save_csv

# JSON_PATH = "data/event_log.json"  # JSONの保存先パス（固定）
# CSV_PATH  = "data/event_log.csv"   # CSVの保存先パス（固定）

# def main():  # プログラムの入口
#     parser = argparse.ArgumentParser(  # 引数パーサを1つ作る
#         description="date-tracker フェーズ1: 追加（--add NAME DATE）のみ対応"
#     )
#     parser.add_argument(               # --add を定義
#         "--add",
#         nargs=2,                       # ← 変更点：2個の値（NAME, DATE）を受け取る
#         metavar=("NAME", "DATE"),      # ヘルプ表示用の見出し
#         help="1件登録: NAME と YYYY-MM-DD を指定"
#     )
#     args = parser.parse_args()         # 実行時の引数を解析

#     if not args.add:                   # --add が無ければ使い方を表示して終了
#         parser.print_help()
#         return

#     name, date = args.add              # ["電池交換", "2025-10-01"] → 2変数に展開
#     name = name.strip()                # 前後の空白除去（入力ゆらぎ対策）
#     date = date.strip()                # 同上

#     if not name:                       # 名前が空 → エラー表示して終了
#         print("エラー: 名前を指定してください。")
#         return

#     if not is_iso_date(date):          # 日付が YYYY-MM-DD 形式でない → エラー表示して終了
#         print("エラー: 日付は YYYY-MM-DD の形式で入力してください。処理を中止します。")
#         return

#     records = load_json(JSON_PATH)     # 既存データを読み込む（無ければ {} が返る設計）
#     records[name] = date               # 上書き登録（同名があれば更新）
#     save_json(records, JSON_PATH)      # JSONへ保存（フォルダ作成は save_* 内で実施済み）
#     save_csv(records, CSV_PATH)        # CSVへ保存（並び順固定）

#     print(f"登録：{name} = {date}")    # 結果を1行表示

# if __name__ == "__main__":             # スクリプト直実行時のみ main() を走らせる
#     main()

# ========== 完成イメージ（経過日の表示を追加） ==========

# 起動方法
# 	•	python3 app.py --elapsed <NAME> --on <YYYY-MM-DD>

# 入力
# 	•	<NAME> と <DATE> は必須。いずれも .strip()。
# 	•	<DATE> は YYYY-MM-DD 形式であること（不正ならエラー終了）。

# 処理
# 	1.	records = load_json(JSON_PATH)（無ければ {}）
# 	2.	record_date = records.get(NAME)
# 	•	取得できなければ："<NAME>" の登録が見つかりません。 と表示して終了
# 	3.	d = days_between(record_date, DATE)（指定日 − 登録日）

# 出力（3パターン）
# 	•	d > 0：データ内の日付から、{d}日が経過しました。
# 	•	d == 0：今日はデータ内の日付（当日）です。
# 	•	d < 0：データ内の日付まで、あと{abs(d)}日です。

# エラー対応
# 	•	引数不足：ヘルプ表示
# 	•	日付形式エラー：エラー: 日付は YYYY-MM-DD 形式で入力してください。
# 	•	NAME 未登録："<NAME>" の登録が見つかりません。

# 保存
# 	•	なし（フェーズ2は表示のみ。データは変更しない）

# 例（動作イメージ）
# 	•	python3 app.py --elapsed 電池交換 --on 2025-10-11
# → データ内の日付から、10日が経過しました。
# 	•	python3 app.py --elapsed 電池交換 --on 2025-10-01
# → 今日はデータ内の日付（当日）です。
# 	•	python3 app.py --elapsed 電池交換 --on 2025-09-25
# → データ内の日付まで、あと6日です。
# 	•	python3 app.py --elapsed フィルター清掃 --on 2025-10-01
# → "フィルター清掃" の登録が見つかりません。

# ========== 擬似コード（経過日の表示を追加） ==========

# 入力：
#     ・--elapsed NAME --on DATE を受け取る（どちらも必須／strip()）
# 	・NAME = (--elapsed の値).strip()
# 	・DATE = (--on の値).strip()
# 	・どちらか欠けていれば ヘルプを表示して終了。
#     ・DATE は strip 後 に is_iso_date(DATE) で検証（NGならエラー表示→終了）。

# 処理：
#     ・DATE は is_iso_date(DATE) で検証（NGなら終了）
#     ・records = load_json(JSON_PATH) → record_date = records.get(NAME) をまず取り出し、未登録なら終了。
#     ・見つからなければメッセージ→終了／見つかれば d = days_between(record_date, DATE)

# 出力：
# 	・	【変更】3パターンをこの順で分岐
# 	1.	d > 0：データ内の日付から、{d}日が経過しました。
# 	2.	d == 0：今日はデータ内の日付（当日）です。
# 	3.	d < 0：データ内の日付まで、あと{abs(d)}日です。

# エラー対応：
#     ・引数不足：ヘルプ表示→終了（戻り値は意識しなくてOK）
#     ・日付形式エラー：エラー: 日付は YYYY-MM-DD 形式で入力してください。
#     ・NAME 未登録："<NAME>" の登録が見つかりません。



# ========== Pythonコード（経過日の表示を追加） ==========

# import argparse
# from tracker_core import is_iso_date, load_json, days_between

# JSON_PATH = "data/event_log.json"

# def main():
#     parser = argparse.ArgumentParser(
#         description="フェーズ2: 経過日の表示（--elapsed NAME --on YYYY-MM-DD）"
#         )
    
#     parser.add_argument("--elapsed", metavar="NAME", help="登録名")
#     parser.add_argument("--on", metavar="DATE", help="基準日（YYYY-MM-DD）")

#     args = parser.parse_args()
#     name = (args.elapsed or "").strip()
#     date = (args.on or "").strip()

#     if not name or not date:
#         parser.print_help()
#         return
    
#     if not is_iso_date(date):
#         print("エラー: 日付は YYYY-MM-DD 形式で入力してください。処理を中止します。")
#         return

#     records = load_json(JSON_PATH)
#     records_date = records.get(name)

#     if not records_date:
#         print(f'"{name}" の登録が見つかりません。')
#         return
    
#     d = days_between(records_date,date)

#     if d > 0:
#         print(f"データ内の日付から、{d}日が経過しました。")
#     elif d == 0:
#         print("今日はデータ内の日付（当日）です。")
#     elif d < 0:
#         print(f"データ内の日付まで、あと{abs(d)}日です。")

# if __name__ == "__main__":
#     main()



# ========== 完成イメージ（一覧表示） ==========

# 目標
# 	python3 app.py --list で「名前: YYYY-MM-DD」を名前順に表示

# 入力
# 	--list（引数なし）を受け付ける
#   --list が指定されていないときは ヘルプを表示して終了（他のオプションとの同時指定も今回は非対応にして終了でOK）。

# 処理
#   records = load_json(JSON_PATH)で読み込み
#   load_json(JSON_PATH) はファイル無し／壊れたJSONなら 空辞書 {} を返す設計になっている
#   空なら「登録はありません。」と表示
#   sortedを使って名前順（昇順）に並び替え

# 出力
#   0件 → 「登録はありません。」
#   1件以上 → for name in sorted(records): print(f"{name}: {records[name]}")


# ========== 擬似コード（一覧表示） ==========

# 入力
#     python3 app.py --list
#     parser.add_argument("--list", action="store_true", help="登録一覧を表示")
#     if not args.list: parser.print_help(); return（他オプションと同時指定を避けるなら、先に if args.list: ...; return の早期終了でもOK）

# 処理
#     records = load_json(JSON_PATH)
#     if not records: print("登録はありません。");
#     return 終了

# 出力
#     print("=== 登録一覧 ===")
#     for name in sorted(records): で 名前昇順に print(f"{name}: {records[name]}")
#     print(f"合計 {len(records)} 件")

# ========== Pythonコード（一覧表示） ==========

import argparse                     # コマンド引数を扱う標準ライブラリを読み込む
from tracker_core import load_json   # JSON読み込み関数（壊れていても空{}を返す設計）

JSON_PATH = "data/event_log.json"    # データの保存場所（相対パス）

def main():                          # CLIの入口となる関数
    parser = argparse.ArgumentParser(    # 引数パーサを1つ作成
        description="--list で登録一覧を表示します"
    )
    parser.add_argument(                 # --list は値を持たないフラグ
        "--list",
        action="store_true",
        help="登録一覧を表示"
    )
    args = parser.parse_args()           # 実行時引数を解析

    if not args.list:                    # --list が指定されていない場合
        parser.print_help()              # 使い方を表示して
        return                           # 終了（CLIなのでループはしない）

    records = load_json(JSON_PATH)       # データを読み込む（無ければ {}）

    if not records:                      # 0件ならメッセージを出して終了
        print("登録はありません。")
        return

    print("=== 登録一覧 ===")            # 見出し
    for name in sorted(records):         # 名前の昇順で並べて
        print(f"{name}: {records[name]}")# 1行ずつ「名前: 日付」を表示

    print(f"合計 {len(records)} 件")     # ループの外で合計件数を1回だけ表示

if __name__ == "__main__":               # スクリプト直実行時のみ
    main()                               # main() を起動

# Cursorから追記

# ==========  ==========

# ==========  ==========

# ==========  ==========

# ==========  ==========
