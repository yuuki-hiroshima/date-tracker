
# ========== 目的 ==========

# 題名：date-tracker をブラウザ操作できる最小Flask版

# 目的

# 既存の tracker_core.py をそのまま活かし、ブラウザから
# 	•	登録（CLIの --add）
# 	•	一覧（--list）
# 	•	経過日表示（--elapsed）
# を操作できるUIを作る。

# ========== 完成イメージ（オリジナル） ==========

# ページの遷移先
#     「登録」「一覧」「経過日」
#     add の送信が完了したらトップページで結果を表示

# 画面項目
#     トップページ → 「登録」「一覧」「経過日」へのボタン
#     登録 → 名前と日付の入力フォーム・登録ボタン・戻るボタン
#     一覧 → 一覧表示・戻るボタン
#     経過日 → タイトルと比較したい日付の入力フォーム・検索ボタン・戻るボタン

# エラーメッセージ
#     登録で名前が空白 → 「名前を入力してください」
#     登録で日付の形式に問題がある → 「"YYYY-MM-DD" の形式で入力してください」
#     一覧でデータが存在しない → 「表示できるデータがありません」
#     経過日で名前が見つからない → 「一致するイベントはありません」
#     経過日で日付の形式に問題がある → 「"YYYY-MM-DD" の形式で入力してください」

# 成功時のメッセージ
#     登録に成功した場合 → 「タイトルの登録に成功しました。」
#     経過日（日付 > 0） → 「タイトルから、〇〇日が経過しました」
#     経過日（日付 == 0） → 「今日はデータ内の日付（当日）です」
#     経過日（日付 < 0） → 「タイトルまで、あと〇〇日です」

# ========== 完成イメージ（ChatGPT） ==========

# ページ遷移
# 	•	GET / … メニュー（登録・一覧・経過日のボタン）＋フラッシュ表示枠
# 	•	GET /add … フォーム（name, date_iso）
# 	•	POST /add … 入力検証 → 成功なら flash("「{name}」の登録に成功しました。", "success") → Redirect /
# 	•	GET /list … 名前昇順テーブル＋「合計 N 件」／空なら「表示できるデータがありません」
# 	•	GET /elapsed … フォーム（name, on_date）
# 	•	POST /elapsed … 入力検証 → days_between 計算 → 結果表示ページ（または同ページ内に結果表示でもOK）

# 画面項目
# 	•	トップ：3ボタン（登録 / 一覧 / 経過日）
# 	•	登録：名前, 日付(YYYY-MM-DD)、登録、トップへ
# 	•	一覧：テーブル（名前 / 日付）、合計件数、トップへ
# 	•	経過日：名前, 比較日(YYYY-MM-DD)、計算、トップへ

# エラー文言（フラッシュ error）
# 	•	登録：名前が空です。 / "YYYY-MM-DD" の形式で入力してください。
# 	•	一覧：表示できるデータがありません。
# 	•	経過日：一致するイベントはありません。 / "YYYY-MM-DD" の形式で入力してください。

# 成功・結果文言
# 	•	登録成功：「{name}」の登録に成功しました。（トップで success）
# 	•	経過日：
# 	•	d > 0：{name} から、{d}日が経過しました。
# 	•	d == 0：今日はデータ内の日付（当日）です。
# 	•	d < 0：{name} まで、あと {abs(d)} 日です。


# ========== 擬似コード ==========

# •	sanitize_name(text)
# 	•	入力文字列の前後空白を除去
# 	•	空文字なら エラー扱い（呼び出し側でフラッシュ）
# •	validate_iso(date_text)
# 	•	tracker_core.is_iso_date(date_text) を呼ぶ
# 	•	True/False を返すだけ（詳細メッセージは呼び出し側で決める）
# •	load_records()
# 	•	tracker_core.load_json(JSON_PATH) を呼び dict[str, str] を受け取る
# 	•	例外は tracker_core に任せる（壊れていれば空にして返る設計）
# •	save_records(records)
# 	•	tracker_core.save_json(records, JSON_PATH)
# 	•	tracker_core.save_csv(records, CSV_PATH)
# 	•	どちらも成功した前提で呼び出し（失敗時は例外→エラーフラッシュ）
# •	メッセージ文言（固定）
# 	•	空name："名前が空です。"
# 	•	形式NG："\"YYYY-MM-DD\" の形式で入力してください。"
# 	•	未登録name（経過日）："一致するイベントはありません。"
# 	•	登録成功："「{name}」の登録に成功しました。"

# ========== Pythonコード ==========

# app_web.py
# ---------------------------------------
# 役割：Flaskで date-tracker をWeb操作できる最小アプリ
# 依存：tracker_core.py（既存の入出力・検証・日付差）
# ---------------------------------------

from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for, flash
from tracker_core import load_json, save_json, save_csv
import os
import tracker_core as core

APP_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(APP_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = os.environ.get("FLASK_SEACRET_KEY", "dev-secret")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
JSON_PATH = os.path.join(DATA_DIR, "event_log.json")
CSV_PATH = os.path.join(DATA_DIR, "event_log.csv")

def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

def sanitize_name(text: str) -> str:
    return text.strip()

def validate_iso(date_text: str) -> bool:
    return core.is_iso_date(date_text)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    
    ensure_data_dir()
    name_raw = request.form.get("name", "")
    date_iso = request.form.get("date_iso", "")
    name = sanitize_name(name_raw)

    if not name:
        flash("名前が空です。", "error")
        return redirect(url_for("add"))
    
    if not validate_iso(date_iso):
        flash("\"YYYY-MM-DD\" の形式で入力してください。", "error")
        return redirect(url_for("add"))
    
    try:
        records: dict[str, str] = core.load_json(JSON_PATH)
        records[name] = date_iso
        core.save_json(records, JSON_PATH)
        core.save_csv(records, CSV_PATH)
    except Exception:
        flash("保存に失敗しました。もう一度お試しください。", "error")
        return redirect(url_for("add"))
    
    flash(f"「{name}」の登録に成功しました。", "success")
    return redirect(url_for("index"))

@app.route("/list")
def list_view():
    records: dict[str, str] = core.load_json(JSON_PATH)
    count = len(records)
    if count == 0:
        return render_template("list.html", records=None, count=0)
    
    sorted_names = sorted(records.keys())
    rows = [(n, records[n]) for n in sorted_names]
    return render_template("list.html", records=rows, count=count)

@app.post("/delete/<name>")
def delete_entry(name: str):
    name = name.strip()
    if not name:
        flash("削除対象の名前がからです。", "error")
        return redirect(url_for("list_view"))
    
    records = load_json(JSON_PATH)
    if name not in records:
        flash(f"「{name}」は見つかりません。", "error")
        return redirect(url_for("list_view"))
    
    del records[name]
    save_json(records, JSON_PATH)
    save_csv(records, CSV_PATH)

    flash(f"「{name}」を削除しました。", "success")
    return redirect(url_for("list_view"))


@app.route("/elapsed", methods=["GET", "POST"])
def elapsed():
    if request.method == "GET":
        return render_template("elapsed.html", result=None)
    
    name_raw = request.form.get("name", "")
    on_date = request.form.get("on_date", "")
    name = sanitize_name(name_raw)

    if not name:
        flash("名前が空です。", "error")
        return redirect(url_for("elapsed"))
    
    if not validate_iso(on_date):
        flash("\"YYYY-MM-DD\" の形式で入力してください。", "error")
        return redirect(url_for("elapsed"))
    
    records: dict[str, str] = core.load_json(JSON_PATH)
    if name not in records:
        flash("一致するイベントはありません。", "error")
        return redirect(url_for("elapsed"))
    
    reg_date = records[name]
    d = core.days_between(reg_date, on_date)
    if d > 0:
        result = f"{name} から、{d}日が経過しました。"
    elif d == 0:
        result = "今日はデータ内の日付（当日）です。"
    else:
        result = f"{name} まで、あと{abs(d)}日です。"

    return render_template("elapsed.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)



# ==========  ==========

# ==========  ==========

# ==========  ==========

# ==========  ==========

# ==========  ==========

# ==========  ==========

# ==========  ==========