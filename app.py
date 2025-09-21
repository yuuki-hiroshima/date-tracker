
# ========== 完成イメージ ==========

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

# ========== 擬似コード ==========

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


# ========== Pythonコード ==========

import argparse  # コマンドライン引数を解析する標準ライブラリ
# コア関数は tracker_core から再利用（CLIとロジックを分離）
from tracker_core import is_iso_date, load_json, save_json, save_csv

JSON_PATH = "data/event_log.json"  # JSONの保存先パス（固定）
CSV_PATH  = "data/event_log.csv"   # CSVの保存先パス（固定）

def main():  # プログラムの入口
    parser = argparse.ArgumentParser(  # 引数パーサを1つ作る
        description="date-tracker フェーズ1: 追加（--add NAME DATE）のみ対応"
    )
    parser.add_argument(               # --add を定義
        "--add",
        nargs=2,                       # ← 変更点：2個の値（NAME, DATE）を受け取る
        metavar=("NAME", "DATE"),      # ヘルプ表示用の見出し
        help="1件登録: NAME と YYYY-MM-DD を指定"
    )
    args = parser.parse_args()         # 実行時の引数を解析

    if not args.add:                   # --add が無ければ使い方を表示して終了
        parser.print_help()
        return

    name, date = args.add              # ["電池交換", "2025-10-01"] → 2変数に展開
    name = name.strip()                # 前後の空白除去（入力ゆらぎ対策）
    date = date.strip()                # 同上

    if not name:                       # 名前が空 → エラー表示して終了
        print("エラー: 名前を指定してください。")
        return

    if not is_iso_date(date):          # 日付が YYYY-MM-DD 形式でない → エラー表示して終了
        print("エラー: 日付は YYYY-MM-DD の形式で入力してください。処理を中止します。")
        return

    records = load_json(JSON_PATH)     # 既存データを読み込む（無ければ {} が返る設計）
    records[name] = date               # 上書き登録（同名があれば更新）
    save_json(records, JSON_PATH)      # JSONへ保存（フォルダ作成は save_* 内で実施済み）
    save_csv(records, CSV_PATH)        # CSVへ保存（並び順固定）

    print(f"登録：{name} = {date}")    # 結果を1行表示

if __name__ == "__main__":             # スクリプト直実行時のみ main() を走らせる
    main()

# ==========  ==========

# ==========  ==========



