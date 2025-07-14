# freee_to_sheets

このリポジトリは、勤怠管理サービス **freee** のデータを Google Sheets へ同期する Cloud Functions のコードと Terraform 定義を含みます。

## デプロイ手順

1. Python ファイルを ZIP 化し、リポジトリ直下に `function_source.zip` として配置します。
   ```bash
   zip function_source.zip *.py requirements.txt
   ```
2. Terraform を実行して GCP リソースを作成します。
   ```bash
   cd terraform
   terraform init
   terraform apply -var project=<GCP_PROJECT_ID> -var sheet_id=<GOOGLE_SHEET_ID>
   ```
   `region` 変数には既定値 `asia-northeast1` が設定されています。必要に応じて上書きしてください。

`terraform apply` 実行時に、作成した ZIP が GCS バケットへアップロードされ、Cloud Function と Pub/Sub、Cloud Scheduler が設定されます。Scheduler は毎日 JST 03:00 に実行されます。

## 環境変数

`env.example` を参考に freee API 用の Secret Manager 名や対象従業員 ID などを設定してください。

