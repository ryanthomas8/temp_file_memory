# Download files from S3 into RAM-backed storage to pass to Binary

```bash
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
docker compose up -d
python upload_to_localstack.py
python download_and_read.py
```
