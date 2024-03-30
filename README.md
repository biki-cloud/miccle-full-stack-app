# フルスタック FastAPI テンプレート

<a href="https://github.com/biki-cloud/miccle-full-stack-app/actions?query=workflow%3ATest" target="_blank"><img src="https://github.com/biki-cloud/miccle-full-stack-app/workflows/Test/badge.svg" alt="Test"></a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/full-stack-fastapi-template" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/full-stack-fastapi-template.svg" alt="Coverage"></a>

## 技術スタックと機能

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com)：Python バックエンド API。
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com)：Python SQL データベースインタラクション（ORM）。
    - 🔍 FastAPI が使用するデータの検証と設定管理のための [Pydantic](https://docs.pydantic.dev)。
    - 💾 [PostgreSQL](https://www.postgresql.org)：SQL データベース。
- 🚀 フロントエンドには [React](https://react.dev) を使用。
    - 💃 TypeScript、hooks、Vite など、モダンなフロントエンドスタックの一部を使用。
    - 🎨 フロントエンドコンポーネントには [Chakra UI](https://chakra-ui.com) を使用。
    - 🤖 自動生成されたフロントエンドクライアント。
    - 🦇 ダークモードのサポート。
- 🐋 開発および本番環境用の Docker Compose。
- 🔒 デフォルトでセキュアなパスワードハッシング。
- 🔑 JWT トークン認証。
- 📫 メールベースのパスワードリカバリー。
- ✅ [Pytest](https://pytest.org) を使用したテスト。
- 📞 リバースプロキシ/ロードバランサーとしての [Traefik](https://traefik.io)。
- 🚢 Docker Compose を使用したデプロイ手順、自動 HTTPS 証明書を処理するフロントエンド Traefik プロキシの設定方法。
- 🏭 GitHub Actions に基づく CI（継続的インテグレーション）および CD（継続的デプロイメント）。

### ダッシュボード ログイン

[![API docs](img/login.png)](https://github.com/biki-cloud/miccle-full-stack-app)

### ダッシュボード - 管理者

[![API docs](img/dashboard.png)](https://github.com/biki-cloud/miccle-full-stack-app)

### ダッシュボード - ユーザー作成

[![API docs](img/dashboard-create.png)](https://github.com/biki-cloud/miccle-full-stack-app)

### ダッシュボード - アイテム

[![API docs](img/dashboard-items.png)](https://github.com/biki-cloud/miccle-full-stack-app)

### ダッシュボード - ユーザー設定

[![API docs](img/dashboard-user-settings.png)](https://github.com/biki-cloud/miccle-full-stack-app)

### ダッシュボード - ダークモード

[![API docs](img/dashboard-dark.png)](https://github.com/biki-cloud/miccle-full-stack-app)

### インタラクティブ API ドキュメント

[![API docs](img/docs.png)](https://github.com/biki-cloud/miccle-full-stack-app)

## 使い方

このリポジトリをフォークまたはクローンして、そのまま使用できます。

✨ それだけで機能します。 ✨

### 設定

次に、`.env` ファイルの設定を更新して、独自の設定をカスタマイズできます。

デプロイする前に、少なくとも以下の値を変更してください：

- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`
- `POSTGRES_PASSWORD`

### シークレットキーの生成

`.env` ファイル内のいくつかの環境変数にはデフォルトで `changethis` という値が設定されています。

これらをシークレットキーに変更するには、次のコマンドを実行してシークレットキーを生成します：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## バックエンド開発

バックエンドのドキュメント: [backend/README.md](./backend/README.md)。

## フロントエンド開発

フロントエンドのドキュメント: [frontend/README.md](./frontend/README.md)。

## デプロイ

デプロイのドキュメント: [deployment.md](./deployment.md)。

## 開発

一般的な開発のドキュメント: [development.md](./development.md)。

これには、Docker Compose、カスタムローカルドメイン、`.env` の設定などが含まれます。

## リリースノート

ファイル [release-notes.md](./release-notes.md) をチェックしてください。

## ライセンス

Full Stack FastAPI Template は MIT ライセンスのもとで提供されています。