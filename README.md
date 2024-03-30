# フルスタック FastAPI テンプレート

<a href="https://github.com/tiangolo/full-stack-fastapi-template/actions?query=workflow%3ATest" target="_blank"><img src="https://github.com/tiangolo/full-stack-fastapi-template/workflows/Test/badge.svg" alt="Test"></a>
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

[![API docs](img/login.png)](https://github.com/tiangolo/full-stack-fastapi-template)

### ダッシュボード - 管理者

[![API docs](img/dashboard.png)](https://github.com/tiangolo/full-stack-fastapi-template)

### ダッシュボード - ユーザー作成

[![API docs](img/dashboard-create.png)](https://github.com/tiangolo/full-stack-fastapi-template)

### ダッシュボード - アイテム

[![API docs](img/dashboard-items.png)](https://github.com/tiangolo/full-stack-fastapi-template)

### ダッシュボード - ユーザー設定

[![API docs](img/dashboard-user-settings.png)](https://github.com/tiangolo/full-stack-fastapi-template)

### ダッシュボード - ダークモード

[![API docs](img/dashboard-dark.png)](https://github.com/tiangolo/full-stack-fastapi-template)

### インタラクティブ API ドキュメント

[![API docs](img/docs.png)](https://github.com/tiangolo/full-stack-fastapi-template)

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

コンテンツをコピーして、パスワード/シークレットキーとして使用します。そして、再度実行して別のセキュアキーを生成します。

## 使い方 - Copier を使った代替方法

このリポジトリは [Copier](https://copier.readthedocs.io) を使用して新しいプロジェクトを生成することもサポートしています。

Copier を使用すると、すべてのファイルがコピーされ、設定の質問が表示され、`.env` ファイルが回答に応じて更新されます。

### Copier のインストール

Copier を以下のコマンドでインストールできます：

```bash
pip install copier
```

または、[`pipx`](https://pipx.pypa.io/) を使用している場合は、次のように実行できます：

```bash
pipx install copier
```

**注意**: `pipx` をお持ちの場合、copier のインストールは任意です。直接実行することもできます。

### Copier を使ってプロジェクトを生成する

新しいプロジェクトのディレクトリ名を決めて、以下の手順を実行します。例えば、`my-awesome-project` とします。

プロジェクトの親ディレクトリに移動し、プロジェクト名を指定して以下のコマンドを実行します：

```bash
copier copy https://github.com/tiangolo/full-stack-fastapi-template my-awesome-project --trust
```

`pipx` をインストールしていて、`copier` をインストールしていない場合は、直接実行することができます：
```bash
pipx run copier copy https://github.com/tiangolo/full-stack-fastapi-template my-awesome-project --trust
```

**注記**: `.env` ファイルを更新する [post-creation script](https://github.com/tiangolo/full-stack-fastapi-template/blob/master/.copier/update_dotenv.py) を実行するために `--trust` オプションが必要です。

### 入力変数

Copier はいくつかのデータを要求しますが、プロジェクトを生成する前に手元に用意しておくことができます。

しかし心配する必要はありません、生成後に `.env` ファイルを更新することができます。

入力変数とそのデフォルト値（一部は自動生成）は次のとおりです：

- `project_name`: (デフォルト: `"FastAPI Project"`) API ユーザーに表示されるプロジェクト名（.env内）。
- `stack_name`: (デフォルト: `"fastapi-project"`) Docker Compose ラベルに使用されるスタックの名前（スペースなし）（.env内）。
- `secret_key`: (デフォルト: `"changethis"`) プロジェクトのセキュリティに使用されるシークレットキー（.env内）。上記の方法で生成できます。
- `first_superuser`: (デフォルト: `"admin@example.com"`) 最初のスーパーユーザーのメールアドレス（.env内）。
- `first_superuser_password`: (デフォルト: `"changethis"`) 最初のスーパーユーザーのパスワード（.env内）。
- `smtp_host`: (デフォルト: "") メールを送信するための SMTP サーバーホスト（.env内で後で設定できます）。
- `smtp_user`: (デフォルト: "") メールを送信するための SMTP サーバーユーザー（.env内で後で設定できます）。
- `smtp_password`: (デフォルト: "") メールを送信するための SMTP サーバーパスワード（.env内で後で設定できます）。
- `emails_from_email`: (デフォルト: `"info@example.com"`) メールを送信するためのアカウントのメールアドレス（.env内で後で設定できます）。
- `postgres_password`: (デフォルト: `"changethis"`) PostgreSQL データベースのパスワード（.env内）。上記の方法で生成できます。
- `sentry_dsn`: (デフォルト: "") 使用している場合の Sentry の DSN（.env内で後で設定できます）。

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