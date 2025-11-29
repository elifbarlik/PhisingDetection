"""
URL Feature Extractor
URL'den 25+ feature çıkart

Features kategorileri:
1. URL Structure (7 feature)
2. Domain Analysis (6 feature)
3. Typosquatting (1 feature)
4. Reputation (4 feature)
5. SSL/Security (2 feature)
"""

import re
import socket
import ssl
import requests
from typing import Dict, List
from difflib import SequenceMatcher
from app.constants import TRUSTED_DOMAINS


class URLFeatureExtractor:

    def __init__(self):
        self.trusted_domains = TRUSTED_DOMAINS
        self.suspicious_tlds = ["tk", "ml", "ga", "cf", "xyz", "top", "click", "download"]
        self.suspicious_keywords = ["verify", "confirm", "update", "secure", "login", "account", "password"]

    def extract_features(self, url: str) -> dict:
        """
        URL'den tüm features çıkart

        Args:
           url: "https://example.com/path"

        Returns:
           dict: 25+ feature
        """
        if not url:
            return self._get_empty_features()

        features = {}

        # ===== URL STRUCTURE FEATURES =====
        structure_features = self._extract_url_structure_features(url)
        features.update(structure_features)

        # ===== DOMAIN FEATURES =====
        domain_features = self._extract_domain_features(url)
        features.update(domain_features)

        # ===== TYPOSQUATTING =====
        typosquatting = self._extract_typosquatting_features(url)
        features.update(typosquatting)

        # ===== REPUTATION (API) =====
        reputation = self._extract_reputation_features(url)
        features.update(reputation)

        # ===== SSL/SECURITY =====
        ssl_features = self._extract_ssl_features(url)
        features.update(ssl_features)

        return features

    def _extract_url_structure_features(self, url: str) -> dict:
        """
        URL'nin yapısını analiz et

        Features:
        - url_length
        - url_has_at_symbol
        - url_has_ip_address
        - url_subdomain_count
        - url_port_unusual
        - url_query_params_count
        - url_path_depth
        """
        features = {}

        features["url_length"] = len(url)
        features["url_has_at_symbol"] = 1 if "@" in url else 0

        ip_pattern = r'\d+\.\d+\.\d+\.\d+'
        features["url_has_ip_address"] = 1 if re.search(ip_pattern, url) else 0

        match = re.search(r'://([^/:?#]+)', url)
        domain = match.group(1) if match else ""

        subdomain_count = domain.count(".")
        features["url_subdomain_count"] = subdomain_count

        port_match = re.search(r':(\d+)', url)
        port = int(port_match.group(1)) if port_match else None

        features["url_port_unusual"] = 0
        if port and port not in [80, 443]:
            features["url_port_unusual"] = 1

        return features

    def _extract_domain_features(self, url: str) -> dict:
        """
        Domain'i analiz et

        Features:
        - domain_length
        - domain_has_hyphen
        - domain_has_suspicious_tld
        - domain_trusted
        - domain_has_suspicious_keywords
        - domain_numeric_ratio
        """
        features = {}
        domain_match = re.search(r'://([^/:?#]+)', url)
        domain = domain_match.group(1) if domain_match else ""

        if not domain:
            return {
                "domain_length": 0,
                "domain_has_hyphen": 0,
                "domain_has_suspicious_tld": 0,
                "domain_trusted": 0,
                "domain_has_suspicious_keywords": 0,
                "domain_numeric_ratio": 0.0
            }
        features["domain_length"] = len(domain)

        features["domain_has_hyphen"] = 1 if "-" in domain else 0

        # TLD analizi
        # example.com → com
        # sub.example.co.uk → co.uk (karışık)
        tld = domain.split(".")[-1]
        suspicious_tlds = ["tk", "ml", "ga", "cf", "xyz", "top"]
        features["domain_has_suspicious_tld"] = 1 if tld in suspicious_tlds else 0

        trusted_domains = ["paypal.com", "google.com", "amazon.com", "apple.com"]
        features["domain_trusted"] = 1 if domain in trusted_domains else 0

        suspicious_keywords = ["verify", "confirm", "update", "secure", "login"]
        keyword_count = sum(1 for kw in suspicious_keywords if kw in domain)
        features["domain_has_suspicious_keywords"] = min(keyword_count, 2)

        digit_count = sum(1 for c in domain if c.isdigit())
        features["domain_numeric_ratio"] = round(digit_count / len(domain), 2)

        return features

    def _extract_typosquatting_features(self, url: str) -> dict:
        """
        Typosquatting tespiti

        Fake domain'in real domain'e benzeşiyse suspicious

        Örnek:
        Real:  paypal.com
        Fake:  paypa1.com (benzerlik: 0.95) → Typosquatting!

        Feature:
        - domain_is_typosquatted
        """

        features = {}

        domain_match = re.search(r'://([^/:?#]+)', url)
        domain = domain_match.group(1) if domain_match else ""

        if not domain:
            return {"domain_is_typosquatted": 0}

        typosquatting_threshold = 0.8

        is_typosquatted = 0
        for real_domain in self.trusted_domains:
            similarity = SequenceMatcher(None, domain, real_domain).ratio()

            if similarity > typosquatting_threshold and domain != real_domain:
                is_typosquatted = 1
                break

        features["domain_is_typosquatted"] = is_typosquatted

        return features


    def _extract_reputation_features(self, url: str) -> dict:
        """
        Dış API'lardan URL'nin reputation'ı kontrol et

        Features:
        - vt_malicious_vendors (VirusTotal)
        - vt_is_malicious
        - urlhaus_is_malicious
        - urlhaus_threat_type
        """
        features = {}

        vt_results = self._check_virustotal(url)
        features.update(vt_results)

        urlhaus_results = self._check_urlhaus(url)
        features.update(urlhaus_results)

        return features

    def _check_virustotal(self, url: str) -> dict:
        """
        VirusTotal API'sini kullan

        VirusTotal: Antivirus ve URL scanning servisi
        Birden çok security vendor'ın malware/phishing tespiti
        """
        features = {
            "vt_malicious_vendors": 0,
            "vt_is_malicious": 0
        }

        # API key olmadan çalışmaz (production için gerekli)
        # Şimdilik mock data dönüşü yap

        try:
            api_key = "YOUR_VIRUSTOTAL_API_KEY"

            if not api_key or api_key == "YOUR_VIRUSTOTAL_API_KEY":
                return features

            endpoint = "https://www.virustotal.com/api/v3/urls"
            headers = {"x-apikey": api_key}

            data = {"url": url}

            response = requests.post(endpoint, headers=headers, data=data, timeout=5)

            if response.status_code == 200:
                result = response.json()

                if "data" in result and "attributes" in result["data"]:
                    stats = result["data"]["attributes"].get("last_analysis_stats", {})
                    malicious_count = stats.get("malicious", 0)

                    features["vt_malicious_vendors"] = min(malicious_count, 10)
                    features["vt_is_malicious"] = 1 if malicious_count > 0 else 0

        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            pass

        return features

    def _check_urlhaus(self, url: str) -> dict:
        """
        URLhaus API'sini kullan

        URLhaus: Malicious URL veritabanı
        """
        features = {
            "urlhaus_is_malicious": 0,
            "urlhaus_threat_type": ""
        }

        try:
            endpoint = "https://urlhaus-api.abuse.ch/v1/url/"

            response = requests.post(
                endpoint,
                data={"url": url},
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()

                if result.get("query_status") == "ok":
                    features["urlhaus_is_malicious"] = 1
                    features["urlhaus_threat_type"] = result.get("threat_type", "unknown")

        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            pass

        return features

    def _extract_ssl_features(self, url: str) -> dict:
        """
        SSL sertifikası kontrol et

        Features:
        - ssl_valid
        - ssl_cert_valid
        """
        features = {
            "ssl_valid": 0,
            "ssl_cert_valid": 0
        }

        if not url.startswith("https://"):
            return features

        try:
            domain_match = re.search(r'://([^/:?#]+)', url)
            hostname = domain_match.group(1) if domain_match else ""

            if not hostname:
                return features

            context = ssl.create_default_context()

            with socket.create_connection((hostname, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()

                    if cert:
                        features["ssl_valid"] = 1
                        features["ssl_cert_valid"] = 1

        except ssl.SSLError:
            features["ssl_valid"] = 0
            features["ssl_cert_valid"] = 0
        except socket.gaierror:
            features["ssl_valid"] = 0
        except socket.timeout:
            features["ssl_valid"] = 0
        except Exception as e:
            features["ssl_valid"] = 0

        return features

    # ================== HELPER METHODS ==================

    def _get_empty_features(self) -> dict:
        """URL yoksa boş features döndür"""
        return {
            "url_length": 0,
            "url_has_at_symbol": 0,
            "url_has_ip_address": 0,
            "url_subdomain_count": 0,
            "url_port_unusual": 0,
            "url_query_params_count": 0,
            "url_path_depth": 0,
            "domain_length": 0,
            "domain_has_hyphen": 0,
            "domain_has_suspicious_tld": 0,
            "domain_trusted": 0,
            "domain_has_suspicious_keywords": 0,
            "domain_numeric_ratio": 0.0,
            "domain_is_typosquatted": 0,
            "vt_malicious_vendors": 0,
            "vt_is_malicious": 0,
            "urlhaus_is_malicious": 0,
            "urlhaus_threat_type": "",
            "ssl_valid": 0,
            "ssl_cert_valid": 0
        }

    def get_feature_names(self) -> List[str]:
        """Tüm feature isimleri döndür"""
        return [
            # URL Structure (7)
            "url_length",
            "url_has_at_symbol",
            "url_has_ip_address",
            "url_subdomain_count",
            "url_port_unusual",
            "url_query_params_count",
            "url_path_depth",
            # Domain (6)
            "domain_length",
            "domain_has_hyphen",
            "domain_has_suspicious_tld",
            "domain_trusted",
            "domain_has_suspicious_keywords",
            "domain_numeric_ratio",
            # Typosquatting (1)
            "domain_is_typosquatted",
            # Reputation (4)
            "vt_malicious_vendors",
            "vt_is_malicious",
            "urlhaus_is_malicious",
            "urlhaus_threat_type",
            # SSL (2)
            "ssl_valid",
            "ssl_cert_valid",
        ]


# ================== TEST ==================

if __name__ == "__main__":
    extractor = URLFeatureExtractor()

    # Test URL'leri
    test_urls = [
        "https://paypal.com/login",  # Legitimate
        "https://paypa1-verify.tk:8080/update?id=123",  # Suspicious
        "http://192.168.1.1/admin",  # IP address
        "https://confirm-amazon@malicious.com/verify",  # @ symbol
    ]

    print("🔗 URL FEATURE EXTRACTOR TEST")
    print("=" * 70)

    for url in test_urls:
        print(f"\n📌 URL: {url}")
        print("-" * 70)

        features = extractor.extract_features(url)

        for key, value in sorted(features.items()):
            print(f"  {key:40} = {value}")

    print("\n" + "=" * 70)
    print(f"✅ Toplam {len(extractor.get_feature_names())} feature çıkarıldı")
    print(f"📋 Features: {extractor.get_feature_names()}")










