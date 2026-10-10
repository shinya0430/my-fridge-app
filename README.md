# わが家の冷蔵庫 — ブラウザ公開版 v1.2

スマホとPCのブラウザで動く、個人用冷蔵庫管理アプリです。

## 機能
- 食材の追加・編集・削除、残量、保存場所、賞味期限・消費期限の管理
- 期限3日以内・期限切れのアプリ内アラート
- 写真からの食材候補推定（無料・試験機能。環境によって利用できない場合があります）
- JSON形式のバックアップと復元
- インストール不要でURLから利用可能

## Cloudflare Pagesで無料公開する（GitHub連携）
1. GitHub (https://github.com/) にログインし、`fridge-pwa` という新しいリポジトリを作成します。公開/非公開は選択可能です。
2. ZIPを解凍し、`fridge-pwa` フォルダ**内のファイル一式**（`index.html`, `src.jsx`, `style.css`, `package.json`, `sw.js`, `icon.svg`, `manifest.webmanifest`, `_headers`）をリポジトリ直下へアップロードしてコミットします。`node_modules` は不要です。
3. Cloudflare (https://dash.cloudflare.com/) にログインし、Workers & Pages → Create → Pages → Gitリポジトリを接続します（表示名は変更される場合があります）。
4. 作成したGitHubリポジトリを選択し、以下を設定します。
   - Framework preset: `Vite`（選択できなければ None でも可）
   - Build command: `npm run build`
   - Build output directory: `dist`
   - Root directory: リポジトリのルート（`/`）
   - Node.js: 20以上を推奨
5. Deploy を実行し、ビルドが成功したら発行された `https://...pages.dev` のURLをスマホで開きます。

**重要**: まだCloudflareへのデプロイは実施していません。実際のURLはユーザー自身のCloudflareアカウントで公開が完了すると発行されます。

## PCでローカル起動する場合
Node.js 20以上をインストールしてから：

```bash
npm install
npm run dev
```

## 注意
- データはブラウザの `localStorage` に保存されます。別の端末やブラウザには同期されません。履歴・サイトデータを消去すると在庫が消えることがあるため、設定からJSONバックアップしてください。
- 写真AIは画像全体から候補を推定する実験機能です。複数食材の正確な個別検出、数量・賞味期限の自動読み取りはできません。モデルは外部から初回ダウンロードします。
- 期限の警告はアプリを開いたときに確認できます。通知テストは即時通知であり、ブラウザを閉じた状態の定時通知は未実装です。
- 本番公開前のビルド・ブラウザ実機テストは未実施です。
