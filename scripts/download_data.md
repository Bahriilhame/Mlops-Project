# Download Dataset

The Kaggle dataset cannot always be downloaded without a Kaggle token.

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

## Kaggle CLI Option

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
