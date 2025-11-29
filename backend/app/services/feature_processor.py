"""
Feature Processor - FINAL VERSION
Email + URL features'ı birleştirip işle

İşlem adımları:
1. Veriyi load et (CSV'den)
2. Email features çıkart
3. URL features çıkart
4. Features'ı birleştir
5. Normalizasyon (scaling)
6. Outlier detection
7. CSV'ye kaydet
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import re
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest
import warnings

warnings.filterwarnings('ignore')

from app.services.email_feature_extractor import EmailFeatureExtractor
from app.services.url_feature_extractor import URLFeatureExtractor


class FeatureProcessor:
    """
    Email + URL features'ı işle ve kaydet

    Adımlar:
    1. Load data
    2. Features çıkart (email + url)
    3. Normalize
    4. Outlier detection
    5. Save
    """

    def __init__(self, data_dir: str = "data"):
        """
        Initialize processor

        Args:
            data_dir: Data klasörü (data/splits vb)
        """
        self.data_dir = Path(data_dir)
        self.email_extractor = EmailFeatureExtractor()
        self.url_extractor = URLFeatureExtractor()

        # Scaler
        self.scaler_minmax = MinMaxScaler()

        # Processed veriyi tutacak
        self.processed_data = None

    # ================== MAIN PIPELINE ==================

    def process_all_splits(self):
        """
        Tüm split'leri (train, val, test) işle

        Adımlar:
        1. URLs train/val/test process et
        2. Emails train/val/test process et
        3. Features'ı birleştir
        4. Normalize et
        5. Save et
        """

        print("📊 Feature Processing Pipeline başlıyor...")
        print("=" * 70)

        # ===== URLS PROCESS =====
        print("\n1️⃣ URL features processing...")
        urls_train = self._process_urls_split("urls_train.csv")
        urls_val = self._process_urls_split("urls_val.csv")
        urls_test = self._process_urls_split("urls_test.csv")

        print(f"   ✅ URLs: train={len(urls_train)}, val={len(urls_val)}, test={len(urls_test)}")

        # ===== EMAILS PROCESS =====
        print("\n2️⃣ Email features processing...")
        emails_train = self._process_emails_split("emails_train.csv")
        emails_val = self._process_emails_split("emails_val.csv")
        emails_test = self._process_emails_split("emails_test.csv")

        print(f"   ✅ Emails: train={len(emails_train)}, val={len(emails_val)}, test={len(emails_test)}")

        # ===== COMBINE FEATURES =====
        print("\n3️⃣ Features birleştiriliyor...")
        train_combined = self._combine_features(emails_train, urls_train, split="train")
        val_combined = self._combine_features(emails_val, urls_val, split="val")
        test_combined = self._combine_features(emails_test, urls_test, split="test")

        print(f"   ✅ Combined: train={len(train_combined)}, val={len(val_combined)}, test={len(test_combined)}")

        # ===== NORMALIZATION =====
        print("\n4️⃣ Normalizasyon yapılıyor...")
        train_normalized, scaler_info = self._normalize_features(
            train_combined,
            fit=True
        )
        val_normalized, _ = self._normalize_features(val_combined, fit=False)
        test_normalized, _ = self._normalize_features(test_combined, fit=False)

        print(f"   ✅ Normalized: train={len(train_normalized)}, val={len(val_normalized)}, test={len(test_normalized)}")

        # ===== OUTLIER DETECTION =====
        print("\n5️⃣ Outlier detection yapılıyor...")
        train_cleaned, outliers_removed = self._detect_outliers(train_normalized)

        print(f"   ✅ Outliers removed: {outliers_removed}")
        print(f"   ✅ Clean data: {len(train_cleaned)}")

        # ===== SAVE =====
        print("\n6️⃣ CSV'ye kaydediliyor...")
        self._save_processed_data(train_cleaned, "features_train_processed.csv")
        self._save_processed_data(val_normalized, "features_val_processed.csv")
        self._save_processed_data(test_normalized, "features_test_processed.csv")

        print("   ✅ CSV dosyaları kaydedildi:")
        print("      - features_train_processed.csv")
        print("      - features_val_processed.csv")
        print("      - features_test_processed.csv")

        # ===== STATISTICS =====
        print("\n7️⃣ İstatistikler hesaplanıyor...")
        self._print_statistics(train_cleaned, val_normalized, test_normalized)

        print("\n" + "=" * 70)
        print("✅ Feature Processing Pipeline tamamlandı!")

        return {
            "train": train_cleaned,
            "val": val_normalized,
            "test": test_normalized,
            "scaler_info": scaler_info
        }

    # ================== STEP 1: LOAD URL SPLIT ==================

    def _process_urls_split(self, filename: str) -> pd.DataFrame:
        """
        URL split CSV'sini load et ve features çıkart

        Input CSV formatı:
        url,label
        https://paypal.com,0
        https://malicious.tk,1
        """

        filepath = self.data_dir / "splits" / filename

        if not filepath.exists():
            print(f"   ⚠️ {filename} bulunamadı")
            return pd.DataFrame()

        # CSV load et
        df = pd.read_csv(filepath)

        # Her URL için features çıkart
        features_list = []

        for idx, row in df.iterrows():
            url = row.get("URL", "")
            label = row.get("Label", 0)

            # Features çıkart
            features = self.url_extractor.extract_features(url)
            features["label"] = label

            features_list.append(features)

        # DataFrame'e dönüştür
        features_df = pd.DataFrame(features_list)

        return features_df

    # ================== STEP 2: LOAD EMAIL SPLIT ==================

    def _process_emails_split(self, filename: str) -> pd.DataFrame:
        """
        Email split CSV'sini load et ve features çıkart

        Input CSV formatı:
        sender,subject,body,label
        noreply@bank.com,Verify Account,Click here,1
        """

        filepath = self.data_dir / "splits" / filename

        if not filepath.exists():
            print(f"   ⚠️ {filename} bulunamadı")
            return pd.DataFrame()

        # CSV load et
        df = pd.read_csv(filepath)

        # Her email için features çıkart
        features_list = []

        for idx, row in df.iterrows():
            email_data = {
                "sender": row.get("sender", ""),
                "subject": row.get("subject", ""),
                "body": row.get("body", ""),
                "headers": {}
            }

            label = row.get("label", 0)

            # Features çıkart
            features = self.email_extractor.extract_features(email_data)
            features["label"] = label

            features_list.append(features)

        # DataFrame'e dönüştür
        features_df = pd.DataFrame(features_list)

        return features_df

    # ================== STEP 3: COMBINE FEATURES ==================

    def _combine_features(self, emails_df: pd.DataFrame, urls_df: pd.DataFrame, split: str) -> pd.DataFrame:
        """
        Email + URL features'ı birleştir

        Her satırda:
        - 30 email feature
        - 20 URL feature
        - 1 label
        = 51 feature
        """

        # Eğer boş ise boş DataFrame döndür
        if emails_df.empty or urls_df.empty:
            return pd.DataFrame()

        # EMAIL FEATURES - label'ı ayır
        email_cols = [col for col in emails_df.columns if col != "label"]
        emails_features = emails_df[email_cols].copy()
        emails_features.columns = [f"email_{col}" for col in email_cols]

        # URL FEATURES - label'ı ayır
        url_cols = [col for col in urls_df.columns if col != "label"]
        urls_features = urls_df[url_cols].copy()
        urls_features.columns = [f"url_{col}" for col in url_cols]

        # Birleştir (features sadece)
        combined = pd.concat([
            emails_features.reset_index(drop=True),
            urls_features.reset_index(drop=True)
        ], axis=1)

        # Label'ı EN SONDA ekle (duplicate olmasın diye)
        # emails_df ve urls_df'nin label'ları aynı olmalı
        if "label" in emails_df.columns:
            combined["label"] = emails_df["label"].values

        return combined

    # ================== STEP 4: NORMALIZATION ==================

    def _normalize_features(self, df: pd.DataFrame, fit: bool = False) -> tuple:
        """
        Features'ı normalize et (0-1 aralığına)

        ✅ FIX:
        1. Sadece NUMERIC kolonları normalize et
        2. Label'ı HARIC tut
        3. Shape mismatch hatası olmayacak

        Yöntem: MinMaxScaler (0-1)
        """

        if df.empty:
            return df, None

        # Label'ı ayır (normalize etmeyelim)
        label = df["label"].copy() if "label" in df.columns else None

        # ✅ SADECE NUMERIC KOLONLARI AL (label HARIC!)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Label'ı çıkar (eğer numeric ise)
        if "label" in numeric_cols:
            numeric_cols.remove("label")

        if not numeric_cols:
            print(f"   ⚠️ Numeric kolon bulunamadı!")
            return df, None

        print(f"   ℹ️ Normalizing {len(numeric_cols)} numeric features...")

        # ✅ SADECE numeric_cols'ı normalize et
        X_numeric = df[numeric_cols].values  # numpy array

        # Normalize et
        if fit:
            # Training seti için fit et
            scaled = self.scaler_minmax.fit_transform(X_numeric)
            scaler_info = {
                "min": self.scaler_minmax.data_min_,
                "max": self.scaler_minmax.data_max_,
                "feature_names": numeric_cols
            }
        else:
            # Val/test için fit edilmiş scaler kullan
            scaled = self.scaler_minmax.transform(X_numeric)
            scaler_info = None

        # ✅ DataFrame'e dönüştür (shape match olacak!)
        # scaled shape: (200, 48)
        # numeric_cols length: 48
        normalized_df = pd.DataFrame(scaled, columns=numeric_cols)

        # Label'ı geri ekle (eğer varsa)
        if label is not None:
            normalized_df["label"] = label.values

        print(f"   ✅ Shape: {normalized_df.shape}")

        return normalized_df, scaler_info

    # ================== STEP 5: OUTLIER DETECTION ==================

    def _detect_outliers(self, df: pd.DataFrame) -> tuple:
        """
        Outlier'ları tespit et ve kaldır

        Yöntem: Isolation Forest
        - Anomali tespiti için machine learning algoritması
        - Outlier'ları otomatik tespit eder

        contamination: %5 outlier var diyoruz
        """

        if df.empty:
            return df, 0

        # Label'ı ayır
        label = df["label"].copy() if "label" in df.columns else None
        feature_cols = [col for col in df.columns if col != "label"]

        if not feature_cols:
            return df, 0

        # Isolation Forest
        iso_forest = IsolationForest(
            contamination=0.05,  # %5 outlier
            random_state=42,
            n_estimators=100
        )

        # Outlier tahmini yap (-1 = outlier, 1 = normal)
        outlier_predictions = iso_forest.fit_predict(df[feature_cols])

        # Outlier'ları kaldır
        clean_df = df[outlier_predictions == 1].copy()
        outliers_count = len(df) - len(clean_df)

        return clean_df, outliers_count

    # ================== STEP 6: SAVE ==================

    def _save_processed_data(self, df: pd.DataFrame, filename: str):
        """
        İşlenmiş veriyi CSV'ye kaydet
        """

        output_path = self.data_dir / "processed" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_path, index=False)

        print(f"      ✅ {filename} saved ({len(df)} rows, {len(df.columns)} features)")

    # ================== STEP 7: STATISTICS ==================

    def _print_statistics(self, train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame):
        """
        İstatistikleri yazdır
        """

        print("\n   📈 Dataset İstatistikleri:")
        print("   " + "-" * 60)

        # Boyut
        print(f"   Train: {len(train_df)} samples, {len(train_df.columns)} features")
        print(f"   Val:   {len(val_df)} samples, {len(val_df.columns)} features")
        print(f"   Test:  {len(test_df)} samples, {len(test_df.columns)} features")

        # Label dağılımı
        print("\n   🏷️ Label Dağılımı:")
        if "label" in train_df.columns:
            train_labels = train_df["label"].value_counts()
            print(f"   Train - Phishing: {train_labels.get(1, 0)}, Legitimate: {train_labels.get(0, 0)}")

            if len(val_df) > 0 and "label" in val_df.columns:
                val_labels = val_df["label"].value_counts()
                print(f"   Val   - Phishing: {val_labels.get(1, 0)}, Legitimate: {val_labels.get(0, 0)}")

            if len(test_df) > 0 and "label" in test_df.columns:
                test_labels = test_df["label"].value_counts()
                print(f"   Test  - Phishing: {test_labels.get(1, 0)}, Legitimate: {test_labels.get(0, 0)}")

        # Feature istatistikleri
        print("\n   📊 Feature İstatistikleri (Train):")
        numeric_cols = train_df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) > 0:
            print(f"   Min: {train_df[numeric_cols].min().min():.4f}")
            print(f"   Max: {train_df[numeric_cols].max().max():.4f}")
            print(f"   Mean: {train_df[numeric_cols].mean().mean():.4f}")
            print(f"   Std: {train_df[numeric_cols].std().mean():.4f}")

        # Eksik veri
        print("\n   ✓ Eksik Veri (Train):")
        missing = train_df.isnull().sum()
        if missing.sum() == 0:
            print("   ✅ Eksik veri yok!")
        else:
            print(f"   ⚠️ {missing.sum()} eksik veri bulundu")
