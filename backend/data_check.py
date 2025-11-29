import pandas as pd
import os

# data/raw klasöründeki CSV dosyalarını listele
raw_data_path = "data/raw"
csv_files = [f for f in os.listdir(raw_data_path) if f.endswith('.csv')]

print("📊 Bulunan CSV Dosyaları:\n")

for csv_file in csv_files:
    file_path = os.path.join(raw_data_path, csv_file)
    df = pd.read_csv(file_path)

    print(f"📄 {csv_file}")
    print(f"   Satır: {len(df)} | Sütun: {len(df.columns)}")
    print(f"   Sütunlar: {df.columns.tolist()}")
    print(f"   Boş veri: {df.isnull().sum().sum()}")
    print()