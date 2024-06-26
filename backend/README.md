# FastAPIプロジェクト - バックエンド

## 必要条件

* [Docker](https://www.docker.com/).
* Pythonパッケージと環境管理のための[Poetry](https://python-poetry.org/)。

## ローカル開発

* Docker Composeでスタックを起動します：

```bash
docker compose up -d
```

* これでブラウザを開き、以下のURLで操作できます：

フロントエンド、Dockerで構築され、パスに基づいてルートが処理されます：http://localhost

OpenAPIに基づいたJSONベースのWeb APIバックエンド：http://localhost/api/

Swagger UI（OpenAPIバックエンドから）による自動インタラクティブドキュメンテーション：http://localhost/docs

データベースのWeb管理、Adminer：http://localhost:8080

プロキシによってルートがどのように処理されているかを確認するためのTraefik UI：http://localhost:8090

**注**：スタックを初めて起動するときは、準備が整うまでに1分ほどかかることがあります。バックエンドがデータベースの準備が整うのを待って、すべてを設定しています。ログを確認して監視することができます。

ログを確認するには、次のコマンドを実行します：

```bash
docker compose logs
```

特定のサービスのログを確認するには、サービス名を追加します。例えば：

```bash
docker compose logs backend
```

## バックエンドのローカル開発、追加の詳細

### 一般的なワークフロー

デフォルトでは、依存関係は[Poetry](https://python-poetry.org/)で管理されています。そこに行ってインストールしてください。

`./backend/`から、すべての依存関係を以下のようにインストールできます：

```console
$ poetry install
```

次に、新しい環境でシェルセッションを開始できます：

```console
$ poetry shell
```

エディタが正しいPython仮想環境を使用していることを確認してください。

`./backend/app/models.py`でSQLModelモデルを変更または追加してデータとSQLテーブルを作成し、`./backend/app/api/`でAPIエンドポイントを変更または追加し、`./backend/app/crud.py`でCRUD（Create, Read, Update, Delete）ユーティリティを変更または追加します。

### VS Code

VS Codeのデバッガーを通じてバックエンドを実行するための設定がすでに存在しているため、ブレークポイントを使用したり、変数を一時停止して調査したりすることができます。

VS CodeのPythonテストタブを通じてテストを実行するための設定もすでに構成されています。

### Docker Composeのオーバーライド

開発中は、`docker-compose.override.yml`ファイルでDocker Composeの設定を変更し、ローカル開発環境のみに影響を与えることができます。

そのファイルへの変更はローカル開発環境のみに影響を与え、本番環境には影響を与えません。したがって、開発ワークフローを支援する"一時的な"変更を追加することができます。

例えば、バックエンドのコードがあるディレクトリは、Dockerの"ホストボリューム"としてマウントされ、リアルタイムで変更したコードをコンテナ内のディレクトリにマッピングします。これにより、Dockerイメージを再度ビルドすることなく、変更をすぐにテストすることができます。これは開発中にのみ行うべきで、本番環境では、バックエンドのコードの最新バージョンを含むDockerイメージをビルドするべきです。しかし、開発中は非常に高速に反復することができます。

また、デフォルトの`/start.sh`（ベースイメージに含まれている）の代わりに`/start-reload.sh`（ベースイメージに含まれている）を実行するコマンドオーバーライドもあります。これは単一のサーバープロセスを起動し（本番環境では複数）、コードの変更を検出するとプロセスをリロードします。Pythonファイルに構文エラーがあり、それを保存すると、エラーが発生し、終了し、コンテナが停止します。その後、エラーを修正して再度実行すると、コンテナを再起動できます：

```console
$ docker compose up -d
```

### バックエンドのテスト

バックエンドをテストするには、以下を実行します：

```console
$ bash ./scripts/test.sh
```

テストはPytestで実行されます。`./backend/app/tests/`にテストを変更または追加します。

GitHub Actionsを使用している場合、テストは自動的に実行されます。

#### テスト実行スタック

スタックがすでに起動していて、テストだけを実行したい場合は、以下を使用できます：

```bash
docker compose exec backend bash /app/tests-start.sh
```

その`/app/tests-start.sh`スクリプトは、スタックの残りが実行中であることを確認した後に`pytest`を呼び出します。`pytest`に追加の引数を渡す必要がある場合は、そのコマンドに引数を渡すことができ、それらは転送されます。

例えば、最初のエラーで停止するには：

```bash
docker compose exec backend bash /app/tests-start.sh -x
```

#### テストカバレッジ

テストを実行すると、`htmlcov/index.html`ファイルが生成されます。これをブラウザで開くと、テストのカバレッジを確認できます。

### マイグレーション

ローカル開発中は、アプリのディレクトリがコンテナ内のボリュームとしてマウントされているため、コンテナ内で`alembic`コマンドを実行してマイグレーションを実行することもできます。その結果、マイグレーションコードはアプリのディレクトリ内に存在します（コンテナ内だけでなく）。そのため、gitリポジトリに追加することができます。

モデルを変更するたびに（例えば、列を追加するなど）、モデルの"リビジョン"を作成し、そのリビジョンでデータベースを"アップグレード"することを忘れないでください。これにより、データベースのテーブルが更新されます。そうしないと、アプリケーションにエラーが発生します。

* バックエンドコンテナで対話式セッションを開始します：

```console
$ docker compose exec backend bash
```

* Alembicはすでに`./backend/app/models.py`からSQLModelモデルをインポートするように設定されています。

* モデルを変更した後（例えば、列を追加した後）、コンテナ内でリビジョンを作成します。例えば：

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* alembicディレクトリ内で生成されたファイルをgitリポジトリにコミットします。

* リビジョンを作成した後、データベースでマイグレーションを実行します（これが実際にデータベースを変更するものです）：

```console
$ alembic upgrade head
```

もしマイグレーションを全く使用したくない場合は、`./backend/app/core/db.py`ファイル内の以下の行をコメントアウトします：

```python
SQLModel.metadata.create_all(engine)
```

そして、以下の内容を含む`prestart.sh`ファイル内の行をコメントアウトします：

```console
$ alembic upgrade head
```

もしデフォルトのモデルを使用したくなく、最初からそれらを削除/変更したい場合、`./backend/app/alembic/versions/`の下のリビジョンファイル（`.py` Pythonファイル）を削除できます。そして、上記のように最初のマイグレーションを作成します。