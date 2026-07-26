# note アフィ日次自動化

## できること / できないこと

| 工程 | 自動化 | 備考 |
|------|--------|------|
| MD素材を読んで記事下書き | ✅ | ローカル生成（APIキー不要のテンプレ回転） |
| xAI APIで文章生成 | △ | `XAI_API_KEY` があるときのみ |
| grok.com の **Project に投げて書かせる** | ❌ 公式APIなし | プロジェクトの指示文を `config/project_prompt.md` にコピーして同等運用 |
| 画像プロンプト生成 | ✅ | 本文の `<!-- IMG: ... -->` から |
| 画像ファイル生成 | △ | 別途 Imagine/API。なければプレースホルダ＋プロンプト |
| サムネ指定 | ✅ | `thumbnail_prompt.txt` + 任意PNG |
| note へ投稿 | △ 半自動 | Playwright。初回ログイン必須。非公式で壊れやすい |
| 完全無人で毎日投稿 | △ | タスクスケジューラ＋認証維持が必要 |

**結論:**  
「素材 → 記事 → 画像指示 → 投稿用フォルダ」は日次自動できる。  
「grok.com プロジェクトUI操作」と「note完全無人投稿」は公式導線が無いため **半自動** が現実解。

---

## 最短の使い方

```powershell
cd C:\Users\ys734\fanza_affiliate_kit
python automation\run_daily.py
```

出力:

```
automation/out/YYYY-MM-DD_slug/
  article.md          … note本文
  meta.json           … タイトル・タグ・ハブURL
  images/
    01_prompt.txt     … 挿入画像プロンプト
    02_prompt.txt
    thumb_prompt.txt  … サムネプロンプト
  PUBLISH.md          … 手投稿チェックリスト
```

### 任意: note 半自動投稿

```powershell
pip install playwright
playwright install chromium
python automation\note_publish.py --package automation\out\最新フォルダ --headed
```

初回はブラウザで note にログイン。以後は保存プロファイルを再利用（保証なし）。

---

## 設定

- `config/settings.json` … ハブURL・af・1日1本の回転
- `config/project_prompt.md` … grokプロジェクト相当の執筆指示（**ここにプロジェクトのルールを貼る**）
- `config/series.json` … 連載ネタキュー

---

## 日次スケジュール

### A. PC電源オフでも動かす（推奨）→ クラウド

詳細: [`CLOUD_DAILY.md`](CLOUD_DAILY.md)

- GitHub に push すると **GitHub Actions** が毎日パッケージ生成
- PCが落ちていてもOK
- 成果物は `automation/latest/` と Actions の Artifact

```powershell
# 初回: git 準備
powershell -ExecutionPolicy Bypass -File automation\setup_git_for_cloud.ps1
# その後 GitHub に remote を付けて push（CLOUD_DAILY.md 参照）
```

### B. PCが起動しているときだけ（非推奨・オフでは動かない）

```
program: python
args:    C:\Users\ys734\fanza_affiliate_kit\automation\run_daily.py
start in: C:\Users\ys734\fanza_affiliate_kit
```

または `register_windows_task.ps1`（電源OFFでは実行されない）。

投稿まで自動化する場合は `note_publish.py`（ヘッドレスは非推奨・ログイン切れやすい）。
