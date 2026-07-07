# Dataset Storage

The raw dataset is tracked by DVC at:

```text
data/raw/student_performance.csv.dvc
```

The preferred storage backend is Google Drive.

## Google Drive DVC Remote

1. Create a folder in Google Drive, for example `eduscore-dvc`.
2. Copy the folder ID from the URL.

For a URL like:

```text
https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWxYz
```

the folder ID is:

```text
1AbCdEfGhIjKlMnOpQrStUvWxYz
```

3. Configure the DVC remote:

```powershell
scripts\setup_gdrive_remote.cmd <folder-id>
```

4. Upload the local DVC-tracked data:

```powershell
scripts\dvc.cmd push
```

5. Restore data on another machine:

```powershell
scripts\dvc.cmd pull
```

The first `push` or `pull` opens a browser for Google authentication.

### If Google Blocks the DVC App

If Google shows "This app is blocked", use your own Google Cloud OAuth client:

1. Open Google Cloud Console.
2. Create or select a project.
3. Enable the Google Drive API.
4. Configure the OAuth consent screen.
5. If the app is in `Testing` mode, add your Google account under `Audience` > `Test users`.
   Otherwise Google returns `Error 403: access_denied` and says the app can only be accessed by developer-approved testers.
6. Create OAuth credentials with application type `Desktop app`.
7. Copy the client ID and client secret.
8. Configure the DVC remote with those credentials:

```powershell
scripts\setup_gdrive_oauth.cmd <folder-id> <client-id> <client-secret>
scripts\dvc.cmd push
```

The client ID and secret are written to `.dvc/config.local`, which is ignored by Git.

For CI/CD or non-interactive automation, use a Google service account instead of browser OAuth. Share the Google Drive folder with the service account email and configure:

```powershell
scripts\dvc.cmd remote modify gdrive gdrive_use_service_account true
scripts\dvc.cmd remote modify --local gdrive gdrive_service_account_json_file_path path\to\service-account.json
```

## Manual Kaggle Fallback

Use this only when the data is not available in the DVC remote.

## Manual Option

1. Open the dataset page:
   <https://www.kaggle.com/datasets/nabeelqureshitiii/student-performance-dataset>
2. Download the CSV file.
3. Rename it to:

```text
student_performance.csv
```

4. Place it in:

```text
data/raw/student_performance.csv
```

## Kaggle CLI Fallback

Install Kaggle CLI and configure your token:

```bash
pip install kaggle
mkdir -p ~/.kaggle
# put kaggle.json in ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

Download:

```bash
kaggle datasets download -d nabeelqureshitiii/student-performance-dataset -p data/raw --unzip
```

If the downloaded filename is different, rename the CSV to `student_performance.csv`.
