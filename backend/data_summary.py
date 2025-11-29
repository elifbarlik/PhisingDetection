import pandas as pd
import os

print("=" * 60)
print("📊 DATASET ÖZET")
print("=" * 60)

# 1. URLs
print("\n🔗 URL DATASET")
for split in ['train', 'val', 'test']:
    df = pd.read_csv(f'data/splits/urls_{split}.csv')
    bad_count = (df['label'] == 1).sum()
    good_count = (df['label'] == 0).sum()
    print(f"\n{split.upper()}:")
    print(f"  Good URLs: {good_count:,} ({good_count/len(df)*100:.1f}%)")
    print(f"  Bad URLs:  {bad_count:,} ({bad_count/len(df)*100:.1f}%)")
    print(f"  Total:     {len(df):,}")

# 2. Emails
print("\n\n📧 EMAIL DATASET")
for split in ['train', 'val', 'test']:
    df = pd.read_csv(f'data/splits/emails_{split}.csv')
    label_counts = df['label'].value_counts()
    print(f"\n{split.upper()}:")
    for label, count in label_counts.items():
        print(f"  Label {label}: {count:,} ({count/len(df)*100:.1f}%)")
    print(f"  Total:    {len(df):,}")

# 3. Klasör Yapısı
print("\n\n📁 KLASÖR YAPISI")
print("\ndata/")
for root, dirs, files in os.walk('data'):
    level = root.replace('data', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in sorted(files)[:10]:  # İlk 10 dosya
        print(f'{subindent}{file}')
    if len(files) > 10:
        print(f'{subindent}... ve {len(files) - 10} dosya daha')

print("\n" + "=" * 60)
print("✅ HAZIR: Feature Engineering'e başlayabiliriz!")
print("=" * 60)