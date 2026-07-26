# PCが電源オフでも毎日回す（クラウド）

## なぜPCタスクでは足りないか

| 方式 | PCオフ |
|------|--------|
| Windows タスクスケジューラ | ❌ 電源OFFだと動かない（スリープ復帰も不安定） |
| **GitHub Actions（推奨）** | ✅ クラウドで毎日実行 |
| 自前VPS | ✅ 月額・メンテが必要 |

画像生成や note 本投稿まで完全無人にするには、さらにAPI鍵・noteログインが必要で壊れやすい。  
まずは **「毎日、投稿用パッケージをクラウドで生成」** を確実にする。

---

## セットアップ（初回だけ・15分）

### 1. GitHub でリポジトリを作る

1. https://github.com/new  
2. 名前例: `fanza-affiliate-kit`（Private 推奨）  
3. Create

### 2. このフォルダを push

**このキット用アカウント/リポジトリ（確定）**

- GitHub ユーザー: `fanza-affiliate-kit`
- リポジトリ名: `fanza-affiliate-kit`
- URL: https://github.com/fanza-affiliate-kit/fanza-affiliate-kit

先に https://github.com/new で **そのアカウントにログインした状態で** 空の Private リポジトリ `fanza-affiliate-kit` を作る（README なし）。

PowerShell:

```powershell
cd C:\Users\ys734\fanza_affiliate_kit
git remote remove origin 2>$null
git remote add origin https://github.com/fanza-affiliate-kit/fanza-affiliate-kit.git
git branch -M main
git push -u origin main
```

または:

```powershell
powershell -ExecutionPolicy Bypass -File automation\push_github.ps1 -GitHubUser fanza-affiliate-kit
```

認証を聞かれたら、その GitHub アカウントのパスワードではなく **Personal Access Token** を使う（Settings → Developer settings → Tokens）。

GitHub CLI がある場合:

```powershell
cd C:\Users\ys734\fanza_affiliate_kit
git init
git add .
git commit -m "feat: affiliate kit + daily cloud automation"
gh repo create fanza-affiliate-kit --private --source=. --remote=origin --push
```

### 3. Actions を有効化

1. GitHub のリポジトリ → **Actions**  
2. ワークフローが出ない場合は一度手動:  
   **Daily note package** → **Run workflow**  
3. 成功すると:
   - **Artifacts** に `note-package`（14日保存）
   - リポジトリの `automation/latest/` に最新記事  
   - `automation/state.json` で連載キューが進む

### 4. 任意: 文章をGrok API品質にする

1. リポジトリ → Settings → Secrets and variables → Actions  
2. Secret 名: `XAI_API_KEY`  
3. 値: xAI の API キー  

未設定でも **テンプレ回転で毎日生成** されます。

### 5. 時刻を変えたい

`.github/workflows/daily_note_package.yml` の cron:

```yaml
- cron: "15 0 * * *"   # 00:15 UTC ≒ 09:15 日本時間
```

日本時間 21:00 にしたい例: `0 12 * * *`（UTC 12:00）

---

## 毎日のあなたの作業（PCオフでも生成は済んでいる）

1. スマホでも可: GitHub → リポジトリ → `automation/latest/article.md`  
2. 内容を note にコピペ  
3. `images/*_prompt.txt` で画像・サムネ作成して添付  
4. 公開  

Artifacts からZIPダウンロードでも可。

---

## note完全自動投稿について

GitHub Actions から note にログイン投稿するのは:

- 公式APIなし  
- 利用規約・アカウントロックリスク  
- ログインCookieのクラウド保存が危険  

**推奨しない。** 生成まで自動化し、投稿は1日1回コピペが安全。

---

## 動作確認（ローカル）

```powershell
cd C:\Users\ys734\fanza_affiliate_kit
python automation\run_daily.py --dry-run
```

ワークフロー構文チェック:

```powershell
python automation\check_workflow.py
```
