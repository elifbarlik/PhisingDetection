"""
Bu script Kaggle verilerini işler:
1. Dosyaları kontrol eder
2. Feature Processor'ı çalıştırır
3. CSV'ye kaydeder
4. İstatistik raporunu yazdırır
"""

import sys
import pandas as pd
from pathlib import Path
from typing import Dict
from app.services.feature_processor import FeatureProcessor

DATA_DIR = Path("data")

REQUIRED_FILES = [
    "splits/emails_train.csv",
    "splits/emails_val.csv",
    "splits/emails_test.csv",
    "splits/urls_train.csv",
    "splits/urls_val.csv",
    "splits/urls_test.csv",
]


def check_files() -> bool:
    """Gerekli dosyaları kontrol et"""
    print("=" * 80)
    print("🔍 DOSYA KONTROLÜ")
    print("=" * 80)

    if not DATA_DIR.exists():
        print(f"❌ HATA: {DATA_DIR} bulunamadı!")
        print(f"   Lütfen şundan çalıştır: C:\\Users\\elifb\\Desktop\\PhisingDetection\\backend")
        return False

    print(f"✅ Data klasörü: {DATA_DIR}")

    missing = []
    for file in REQUIRED_FILES:
        path = DATA_DIR / file
        if path.exists():
            size = path.stat().st_size / (1024 * 1024)
            print(f"  ✅ {file} ({size:.2f} MB)")
        else:
            print(f"  ❌ {file} BULUNAMADI")
            missing.append(file)

    if missing:
        print(f"\n❌ HATA: Şu dosyalar bulunamadı:")
        for f in missing:
            print(f"   • {f}")
        return False

    return True


def process_features() -> Dict:
    """Feature Processor'ı çalıştır"""
    print("\n" + "=" * 80)
    print("🚀 FEATURE PROCESSOR BAŞLIYOR")
    print("=" * 80)

    try:
        processor = FeatureProcessor(data_dir=str(DATA_DIR))
    except ImportError:
        print("❌ HATA: FeatureProcessor bulunamadı!")
        print("   Kontrol et: app/services/feature_processor.py var mı?")
        sys.exit(1)

    print("\n📊 Pipeline başlıyor...")
    print("  1. URLs yükleniyor...")
    print("  2. Emails yükleniyor...")
    print("  3. Features çıkarılıyor...")
    print("  4. Normalizasyon yapılıyor...")
    print("  5. Outlier detection yapılıyor...")
    print("  6. CSV'ye kaydediliyor...\n")

    try:
        results = processor.process_all_splits()
    except Exception as e:
        print(f"\n❌ Feature Processor hatası: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("✅ Feature processing tamamlandı!")

    return results


def show_results(results: Dict):
    """Sonuçları göster"""
    print("\n" + "=" * 80)
    print("📊 SONUÇLAR")
    print("=" * 80)

    for split in ["train", "val", "test"]:
        if split in results:
            df = results[split]
            print(f"\n{split.upper()}:")
            print(f"  Shape: {df.shape}")
            print(f"  Rows: {len(df):,}")
            print(f"  Columns: {len(df.columns)}")
            print(f"  Memory: {df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")

            # Label dağılımı
            if "label" in df.columns:
                label_counts = df["label"].value_counts().sort_index()
                print(f"  Label Distribution:")
                for label, count in label_counts.items():
                    label_name = "Legitimate" if label == 0 else "Phishing"
                    pct = 100 * count / len(df)
                    print(f"    {label_name} ({label}): {count:,} ({pct:.1f}%)")


def save_results(results: Dict):
    """Sonuçları CSV'ye kaydet"""
    print("\n" + "=" * 80)
    print("💾 CSV'YE KAYDETME")
    print("=" * 80)

    for split in ["train", "val", "test"]:
        if split in results:
            df = results[split]
            path = DATA_DIR / "processed" / f"features_{split}_processed.csv"
            path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(path, index=False)
            print(f"✅ {path}")


def main():
    """Main function"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "🚀 FEATURE PROCESSOR - GERÇEK KAGGLE VERİSİ İŞLEMESİ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    # 1. Dosyaları kontrol et
    if not check_files():
        print("\n❌ Dosya kontrolü başarısız!")
        sys.exit(1)

    # 2. Feature processing
    try:
        results = process_features()
    except Exception as e:
        print(f"\n❌ Işlem hatası: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 3. Sonuçları göster
    show_results(results)

    # 4. CSV'ye kaydet
    try:
        save_results(results)
    except Exception as e:
        print(f"\n❌ CSV kaydetme hatası: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 5. Tamamlandı mesajı
    print("\n" + "=" * 80)
    print("✅ TAMAMLANDI!")
    print("=" * 80)
    print(f"\n📁 Processed files:")
    print(f"   ✅ data/processed/features_train_processed.csv")
    print(f"   ✅ data/processed/features_val_processed.csv")
    print(f"   ✅ data/processed/features_test_processed.csv")

    print(f"\n🔜 SONRAKI ADIM: XGBoost Model Training başla!")

    print(f"""
════════════════════════════════════════════════════════════════════════════════

Model Training örneği:

from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd

# Veri yükle
X_train = pd.read_csv("data/processed/features_train_processed.csv")
y_train = X_train.pop("label")

X_val = pd.read_csv("data/processed/features_val_processed.csv")
y_val = X_val.pop("label")

X_test = pd.read_csv("data/processed/features_test_processed.csv")
y_test = X_test.pop("label")

# Model eğit
model = XGBClassifier(
    n_estimators=100,
    max_depth=10,
    learning_rate=0.1,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Evaluate
y_pred_val = model.predict(X_val)
y_pred_test = model.predict(X_test)

print(f"Val Accuracy: {{accuracy_score(y_val, y_pred_val):.4f}}")
print(f"Test Accuracy: {{accuracy_score(y_test, y_pred_test):.4f}}")
print(f"Test Precision: {{precision_score(y_test, y_pred_test):.4f}}")
print(f"Test Recall: {{recall_score(y_test, y_pred_test):.4f}}")
print(f"Test F1-Score: {{f1_score(y_test, y_pred_test):.4f}}")

════════════════════════════════════════════════════════════════════════════════
    """)

    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ İşlem kullanıcı tarafından iptal edildi!")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ BEKLENMEYEN HATA: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)