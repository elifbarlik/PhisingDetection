import pandas as pd
from sklearn.model_selection import train_test_split
import os

# URLS
print("🔗 URL Split İşlemi...")
urls = pd.read_csv('data/processed/urls_cleaned.csv')

# Train/Test Split (70/30)
train_urls, test_urls = train_test_split(urls, test_size=0.3, random_state=42, stratify=urls['label'])

# Test'i Validation/Test'e böl (15/15)
val_urls, test_urls = train_test_split(test_urls, test_size=0.5, random_state=42, stratify=test_urls['label'])

print(f"   Train: {len(train_urls)} ({len(train_urls)/len(urls)*100:.1f}%)")
print(f"   Val:   {len(val_urls)} ({len(val_urls)/len(urls)*100:.1f}%)")
print(f"   Test:  {len(test_urls)} ({len(test_urls)/len(urls)*100:.1f}%)")
print()

# EMAILS
print("📧 Email Split İşlemi...")
emails = pd.read_csv('data/processed/emails_raw.csv')

# Train/Test Split
train_emails, test_emails = train_test_split(emails, test_size=0.3, random_state=42, stratify=emails['label'])

# Test'i Validation/Test'e böl
val_emails, test_emails = train_test_split(test_emails, test_size=0.5, random_state=42, stratify=test_emails['label'])

print(f"   Train: {len(train_emails)} ({len(train_emails)/len(emails)*100:.1f}%)")
print(f"   Val:   {len(val_emails)} ({len(val_emails)/len(emails)*100:.1f}%)")
print(f"   Test:  {len(test_emails)} ({len(test_emails)/len(emails)*100:.1f}%)")
print()

# KAYDET
os.makedirs('data/splits', exist_ok=True)

# URLs
train_urls.to_csv('data/splits/urls_train.csv', index=False)
val_urls.to_csv('data/splits/urls_val.csv', index=False)
test_urls.to_csv('data/splits/urls_test.csv', index=False)

# Emails
train_emails.to_csv('data/splits/emails_train.csv', index=False)
val_emails.to_csv('data/splits/emails_val.csv', index=False)
test_emails.to_csv('data/splits/emails_test.csv', index=False)

print("✅ Split veriler kaydedildi:")
print("   URLs: train/val/test")
print("   Emails: train/val/test")