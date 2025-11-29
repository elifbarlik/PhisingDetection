import pandas as pd
import os

# 1. URL VERİSİ YÜKLE
print("🔗 URL Verisi Yükleniyor...")
url_df = pd.read_csv('data/raw/phishing_site_urls.csv')
print(f"   Orjinal: {len(url_df)} satır")

# Boş satırları çıkar
url_df = url_df.dropna()
print(f"   Temizleme sonrası: {len(url_df)} satır")

# Label'ları standardize et (0: Good, 1: Bad) - küçük harf kontrol et
url_df['label'] = (url_df['Label'].str.lower() == 'bad').astype(int)
url_df = url_df[['URL', 'label']]
print(f"   Label dağılımı: {url_df['label'].value_counts().to_dict()}")
print()

# 2. EMAIL VERİSİ YÜKLE
print("📧 Email Verisi Yükleniyor...")
phishing_email = pd.read_csv('data/raw/phishing_email.csv')
print(f"   Phishing emails: {len(phishing_email)} satır")
print(f"   Sütunlar: {phishing_email.columns.tolist()}")

spam_data = pd.read_csv('data/raw/combined_data.csv')
print(f"   Spam/Ham data: {len(spam_data)} satır")
print(f"   Sütunlar: {spam_data.columns.tolist()}")

# Merge emails
emails = pd.concat([phishing_email, spam_data], ignore_index=True)
print(f"   Toplam: {len(emails)} satır")
print()

# 3. PROCESSED KLASÖRÜ OLUŞTUR VE KAYDET
os.makedirs('data/processed', exist_ok=True)

url_df.to_csv('data/processed/urls_cleaned.csv', index=False)
emails.to_csv('data/processed/emails_raw.csv', index=False)

print("✅ Temizlenmiş veriler kaydedildi:")
print("   - data/processed/urls_cleaned.csv")
print("   - data/processed/emails_raw.csv")