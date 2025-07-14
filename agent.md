このリポジトリでは、Python ソースを `function_source.zip` にまとめて GCS にアップロードし、Terraform から Cloud Functions をデプロイします。

### 手順メモ
1. リポジトリ直下で ZIP を作成する
   ```bash
   zip function_source.zip *.py requirements.txt
   ```
2. `terraform` ディレクトリで `terraform apply` を実行する
   ```bash
   cd terraform
   terraform init
   terraform apply -var project=<GCP_PROJECT_ID> -var sheet_id=<GOOGLE_SHEET_ID>
   ```
   実行すると Cloud Storage バケットに ZIP が配置され、Cloud Function と Scheduler が作成されます。

