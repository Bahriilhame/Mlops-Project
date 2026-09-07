from pathlib import Path
import pandas as pd


DATA_DIR = Path("data/raw/oulad")

FILES = [
    "studentInfo.csv",
    "studentAssessment.csv",
    "studentVle.csv",
    "studentRegistration.csv",
    "assessments.csv",
    "courses.csv",
    "vle.csv",
]


def main():
    print("=" * 70)
    print("OULAD DATASET INSPECTION")
    print("=" * 70)

    for filename in FILES:
        path = DATA_DIR / filename

        if not path.exists():
            print(f"[ERROR] Missing: {filename}")
            continue

        df = pd.read_csv(path)

        print(f"\n{filename}")
        print(f"  Rows    : {len(df):,}")
        print(f"  Columns : {len(df.columns)}")
        print(f"  Shape   : {df.shape}")

        print("  Columns:")
        print(f"    {list(df.columns)}")


if __name__ == "__main__":
    main()