# FastAPIプロジェクト - デプロイ

このプロジェクトは、Docker Composeを使用してリモートサーバーにデプロイできます。

このプロジェクトでは、外部世界との通信とHTTPS証明書を処理するTraefikプロキシが必要です。

CI/CD（継続的インテグレーションと継続的デプロイメント）システムを使用して自動的にデプロイできます。GitHub Actionsを使用してこれを行うための設定がすでにあります。

ただし、最初にいくつかの設定を行う必要があります。🤓

## 準備

* リモートサーバーを準備し、利用可能にします。
* ドメインのDNSレコードを、作成したサーバーのIPに指すように設定します。
* ドメインのワイルドカードサブドメインを設定します。これにより、`*.fastapi-project.example.com`のような異なるサービスのための複数のサブドメインを持つことができます。これは、`traefik.fastapi-project.example.com`、`adminer.fastapi-project.example.com`などの異なるコンポーネントにアクセスするため、また`staging`のために、`staging.fastapi-project.example.com`、`staging.adminer.fastapi-project.example.com`などにアクセスするために便利です。
* リモートサーバーに[Docker](https://docs.docker.com/engine/install/)をインストールし、設定します（Docker Engine、Docker Desktopではありません）。

## パブリックTraefik

受信接続とHTTPS証明書を処理するTraefikプロキシが必要です。

次の手順は一度だけ行う必要があります。

### Traefik Docker Compose

* Traefik Docker Composeファイルを保存するためのリモートディレクトリを作成します：

```bash
mkdir -p /root/code/traefik-public/
```

Traefik Docker Composeファイルをサーバーにコピーします。これは、ローカルのターミナルで`rsync`コマンドを実行することで行うことができます：

```bash
rsync -a docker-compose.traefik.yml root@your-server.example.com:/root/code/traefik-public/
```

# Traefik Public Network

このTraefikは、`traefik-public`という名前のDocker "public network"を通じてスタックと通信することを期待しています。

このようにすると、外部世界との通信（HTTPとHTTPS）を処理する単一の公開Traefikプロキシが存在し、その背後には、同一の単一サーバー上でも、異なるドメインを持つ1つ以上のスタックが存在することができます。

リモートサーバーで以下のコマンドを実行して、`traefik-public`という名前のDocker "public network"を作成します：

```bash
docker network create traefik-public
```

### Traefikの環境変数

Traefik Docker Composeファイルは、それを開始する前にターミナルでいくつかの環境変数が設定されていることを期待しています。これは、リモートサーバーで以下のコマンドを実行することで行うことができます。

* HTTP Basic Authのユーザー名を作成します。例えば：

```bash
export USERNAME=admin
```

* HTTP Basic Authのパスワードを環境変数に作成します。例えば：

```bash
export PASSWORD=changethis
```

* opensslを使用してHTTP Basic Authのパスワードの"ハッシュ化"バージョンを生成し、それを環境変数に保存します：

```bash
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)
```

ハッシュ化されたパスワードが正しいことを確認するために、それを印刷することができます：

```bash
echo $HASHED_PASSWORD
```

* サーバーのドメイン名を環境変数に作成します。例えば：

```bash
export DOMAIN=fastapi-project.example.com
```

* Let's Encryptのメールを環境変数に作成します。例えば：

```bash
export EMAIL=admin@example.com
```

**注意**：異なるメールを設定する必要があります。`@example.com`のメールは機能しません。

### Traefik Docker Composeの開始

リモートサーバーでTraefik Docker Composeファイルをコピーしたディレクトリに移動します：

```bash
cd /root/code/traefik-public/
```

これで、環境変数が設定され、`docker-compose.traefik.yml`が配置されているので、次のコマンドを実行してTraefik Docker Composeを開始できます：

```bash
docker compose -f docker-compose.traefik.yml up -d
```

## FastAPIプロジェクトのデプロイ

Traefikが配置されているので、Docker Composeを使用してFastAPIプロジェクトをデプロイできます。

**注意**：GitHub Actionsを使用した継続的デプロイのセクションに進むことをお勧めします。

## 環境変数

まず、いくつかの環境変数を設定する必要があります。

`ENVIRONMENT`を設定します。デフォルトは`local`（開発用）ですが、サーバーにデプロイする場合は`staging`や`production`などを設定します：

```bash
export ENVIRONMENT=production
```

`DOMAIN`を設定します。デフォルトは`localhost`（開発用）ですが、デプロイする場合は自分のドメインを使用します。例えば：

```bash
export DOMAIN=fastapi-project.example.com
```

以下のようないくつかの変数を設定できます：

* `BACKEND_CORS_ORIGINS`：カンマで区切られた許可されるCORSオリジンのリスト。
* `SECRET_KEY`：FastAPIプロジェクトの秘密鍵。トークンの署名に使用されます。
* `FIRST_SUPERUSER`：最初のスーパーユーザーのメール。このスーパーユーザーは新しいユーザーを作成できるユーザーになります。
* `FIRST_SUPERUSER_PASSWORD`：最初のスーパーユーザーのパスワード。
* `USERS_OPEN_REGISTRATION`：新しいユーザーのオープン登録を許可するかどうか。
* `SMTP_HOST`：メールを送信するためのSMTPサーバーホスト。これはあなたのメールプロバイダーから来ます（例：Mailgun、Sparkpost、Sendgridなど）。
* `SMTP_USER`：メールを送信するためのSMTPサーバーユーザー。
* `SMTP_PASSWORD`：メールを送信するためのSMTPサーバーパスワード。
* `EMAILS_FROM_EMAIL`：メールを送信するメールアカウント。
* `POSTGRES_SERVER`：PostgreSQLサーバーのホスト名。同じDocker Composeが提供するデフォルトの`db`をそのまま使用できます。通常、サードパーティのプロバイダーを使用している場合を除き、これを変更する必要はありません。
* `POSTGRES_PORT`：PostgreSQLサーバーのポート。デフォルトのままで良いです。通常、サードパーティのプロバイダーを使用している場合を除き、これを変更する必要はありません。
* `POSTGRES_PASSWORD`：Postgresのパスワード。
* `POSTGRES_USER`：Postgresのユーザー。デフォルトのままで良いです。
* `POSTGRES_DB`：このアプリケーションで使用するデータベース名。デフォルトの`app`をそのまま使用できます。
* `SENTRY_DSN`：SentryのDSN。使用している場合。

### 秘密鍵の生成

`.env`ファイルのいくつかの環境変数は、デフォルト値が`changethis`になっています。

これらを秘密鍵で置き換える必要があります。秘密鍵を生成するには、次のコマンドを実行します：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

内容をコピーしてパスワード/秘密鍵として使用します。そして、再度安全なキーを生成するためにそれを実行します。

### Docker Composeでのデプロイ

環境変数が設定されている場合、Docker Composeを使用してデプロイできます：

```bash
docker compose -f docker-compose.yml up -d
```

本番環境では、`docker-compose.override.yml`のオーバーライドを使用したくないため、使用するファイルとして明示的に`docker-compose.yml`を指定しています。

## 継続的デプロイメント（CD）

GitHub Actionsを使用してプロジェクトを自動的にデプロイできます。😎

複数の環境デプロイメントを持つことができます。

すでに`staging`と`production`の2つの環境が設定されています。🚀

### GitHub Actions Runnerのインストール

* リモートサーバーで、`root`ユーザーとして実行している場合は、GitHub Actions用のユーザーを作成します：

```bash
adduser github
```

* `github`ユーザーにDockerの権限を追加します：

```bash
usermod -aG docker github
```

* 一時的に`github`ユーザーに切り替えます：

```bash
su - github
```

* `github`ユーザーのホームディレクトリに移動します：

```bash
cd
```

* [公式ガイドに従ってGitHub Actionの自己ホスト型ランナーをインストールします](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners#adding-a-self-hosted-runner-to-a-repository)。

* ラベルについて尋ねられたら、環境のラベルを追加します。例えば、`production`など。後からラベルを追加することもできます。

インストール後、ガイドではランナーを開始するためのコマンドを実行するよう指示されます。しかし、そのプロセスを終了したり、サーバーへのローカル接続が失われたりすると、ランナーは停止します。

起動時に実行され、継続的に実行されるようにするために、サービスとしてインストールすることができます。それを行うためには、`github`ユーザーを終了し、`root`ユーザーに戻ります：

```bash
exit
```

これを行うと、再度`root`ユーザーになります。そして、`root`ユーザーの前のディレクトリに戻ります。

* `github`ユーザーのホームディレクトリ内の`actions-runner`ディレクトリに移動します：

```bash
cd /home/github/actions-runner
```

* `github`ユーザーで自己ホスト型ランナーをサービスとしてインストールします：

```bash
./svc.sh install github
```

* サービスを開始します：

```bash
./svc.sh start
```

* サービスのステータスを確認します：

```bash
./svc.sh status
```

詳細については、公式ガイドの[自己ホスト型ランナーアプリケーションをサービスとして設定する](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/configuring-the-self-hosted-runner-application-as-a-service)を参照してください。

### シークレットの設定

あなたのリポジトリで、必要な環境変数のシークレットを設定します。これには、上記の`SECRET_KEY`などが含まれます。リポジトリのシークレットを設定するための[公式GitHubガイド](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)に従ってください。

現在のGithub Actionsワークフローは、以下のシークレットを期待しています：

* `DOMAIN_PRODUCTION`
* `DOMAIN_STAGING`
* `EMAILS_FROM_EMAIL`
* `FIRST_SUPERUSER`
* `FIRST_SUPERUSER_PASSWORD`
* `POSTGRES_PASSWORD`
* `SECRET_KEY`

## GitHub Actionデプロイメントワークフロー

`.github/workflows`ディレクトリには、環境（GitHub Actionsランナーのラベル）にデプロイするためのGitHub Actionワークフローがすでに設定されています：

* `staging`：`master`ブランチにプッシュ（またはマージ）した後。
* `production`：リリースを公開した後。

追加の環境が必要な場合は、これらを出発点として使用できます。

## URLs

`fastapi-project.example.com`をあなたのドメインに置き換えてください。

### Main Traefik Dashboard

Traefik UI: `https://traefik.fastapi-project.example.com`

### Production

Frontend: `https://fastapi-project.example.com`

Backend API docs: `https://fastapi-project.example.com/docs`

Backend API base URL: `https://fastapi-project.example.com/api/`

Adminer: `https://adminer.fastapi-project.example.com`

### Staging

Frontend: `https://staging.fastapi-project.example.com`

Backend API docs: `https://staging.fastapi-project.example.com/docs`

Backend API base URL: `https://staging.fastapi-project.example.com/api/`

Adminer: `https://staging.adminer.fastapi-project.example.com`