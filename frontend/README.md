# FastAPIプロジェクト - フロントエンド

フロントエンドは、[Vite](https://vitejs.dev/)、[React](https://reactjs.org/)、[TypeScript](https://www.typescriptlang.org/)、[TanStack Query](https://tanstack.com/query)、[TanStack Router](https://tanstack.com/router)、および[Chakra UI](https://chakra-ui.com/)を使用して構築されています。

## フロントエンドの開発

開始する前に、Node Version Manager（nvm）またはFast Node Manager（fnm）のいずれかがシステムにインストールされていることを確認してください。

* fnmをインストールするには、[公式のfnmガイド](https://github.com/Schniz/fnm#installation)に従ってください。nvmを好む場合は、[公式のnvmガイド](https://github.com/nvm-sh/nvm#installing-and-updating)を使用してインストールできます。

* nvmまたはfnmのいずれかをインストールしたら、`frontend`ディレクトリに進みます：

```bash
cd frontend
```
* `.nvmrc` ファイルに指定された Node.js のバージョンがシステムにインストールされていない場合は、適切なコマンドを使用してインストールできます：

```bash
# fnmを使用する場合
fnm install

# nvmを使用する場合
nvm install
```

* インストールが完了したら、インストールしたバージョンに切り替えます：

```bash
# fnmを使用する場合
fnm use 

# nvmを使用する場合
nvm use
```

* `frontend` ディレクトリ内で、必要なNPMパッケージをインストールします：

```bash
npm install
```

* そして、以下の `npm` スクリプトでライブサーバーを起動します：

```bash
npm run dev
```

* その後、ブラウザを http://localhost:5173/ で開きます。

このライブサーバーはDocker内で動作していないことに注意してください。これはローカル開発用で、推奨されるワークフローです。フロントエンドに満足したら、フロントエンドのDockerイメージをビルドして起動し、本番環境に近い環境でテストすることができます。しかし、変更のたびにイメージをビルドすると、ライブリロード付きのローカル開発サーバーを実行するよりも生産性が低下します。

他の利用可能なオプションについては、`package.json` ファイルを確認してください。

### フロントエンドの削除

APIのみのアプリを開発していて、フロントエンドを削除したい場合は、簡単に行うことができます：

* `./frontend` ディレクトリを削除します。

* `docker-compose.yml` ファイルから、`frontend` の全サービス/セクションを削除します。

* `docker-compose.override.yml` ファイルから、`frontend` の全サービス/セクションを削除します。

これで、フロントエンドのない（APIのみの）アプリが完成しました。🤓

---

もしよろしければ、以下から `FRONTEND` 環境変数も削除できます：

* `.env`
* `./scripts/*.sh`

ただし、これはそれらをクリーンアップするためだけで、残しておいても特に影響はありません。

## クライアントの生成

* Docker Compose スタックを起動します。

* `http://localhost/api/v1/openapi.json` からOpenAPI JSONファイルをダウンロードし、それを `frontend` ディレクトリのルートに新しいファイル `openapi.json` としてコピーします。

* 生成されたフロントエンドクライアントコードの名前を簡略化するために、以下のスクリプトを実行して `openapi.json` ファイルを修正します：

```bash
node modify-openapi-operationids.js
```

* フロントエンドクライアントを生成するには、以下を実行します：

```bash
npm run generate-client
```

* 変更をコミットします。

バックエンドが変更されるたびに（OpenAPIスキーマを変更する）、フロントエンドクライアントを更新するためにこれらの手順を再度実行する必要があることに注意してください。

## リモートAPIの使用

リモートAPIを使用したい場合は、環境変数 `VITE_API_URL` をリモートAPIのURLに設定できます。例えば、`frontend/.env` ファイルで設定できます：

```env
VITE_API_URL=https://my-remote-api.example.com
```

その後、フロントエンドを実行すると、そのURLがAPIのベースURLとして使用されます。

## コード構造

フロントエンドのコードは以下のように構成されています：

* `frontend/src` - メインのフロントエンドコード。
* `frontend/src/assets` - 静的アセット。
* `frontend/src/client` - 生成されたOpenAPIクライアント。
* `frontend/src/components` - フロントエンドのさまざまなコンポーネント。
* `frontend/src/hooks` - カスタムフック。
* `frontend/src/routes` - ページを含むフロントエンドのさまざまなルート。
* `theme.tsx` - Chakra UIのカスタムテーマ。