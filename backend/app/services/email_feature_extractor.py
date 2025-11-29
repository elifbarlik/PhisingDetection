"""
Advanced Email Feature Extractor
Çıkarılan features: 30+
- Sender analysis
- Header analysis
- Subject line analysis
- Body text analysis (NLP)
"""

import re
import email
from email.parser import HeaderParser
from textblob import TextBlob
from typing import Dict, List, Tuple
import validators
from app.constants import (
    URGENCY_KEYWORDS, THREAT_KEYWORDS, ACTION_KEYWORDS,
    SUSPICIOUS_DOMAIN_PATTERNS, TRUSTED_DOMAINS, PHISHING_KEYWORDS_TR,
    FEAR_INDICATORS, GREED_INDICATORS, URGENCY_INDICATORS
)


class EmailFeatureExtractor:
    """
    Email'den 30+ feature çıkart

    Features kategorileri:
    1. Sender Features (6)
    2. Header Features (5)
    3. Subject Features (5)
    4. Body Features (10+)
    5. URL Features (4)
    """

    def __init__(self):
        self.urgency_keywords = URGENCY_KEYWORDS
        self.threat_keywords = THREAT_KEYWORDS
        self.action_keywords = ACTION_KEYWORDS
        self.suspicious_patterns = SUSPICIOUS_DOMAIN_PATTERNS
        self.trusted_domains = TRUSTED_DOMAINS
        self.fear_indicators = FEAR_INDICATORS
        self.greed_indicators = GREED_INDICATORS


    def extract_features(self, email_data: dict) -> dict:
        """
        Email'den tüm features çıkart

        Args:
            email_data: {
                'raw_email': str (MIME format),
                'sender': str,
                'subject': str,
                'body': str,
                'headers': dict (optional)
            }

        Returns:
            dict: 30+ feature
        """

        # Parse email
        sender = email_data.get("sender", "").lower()
        subject = email_data.get("subject", "")
        body = email_data.get("body", "")
        headers = email_data.get("headers", {})
        raw_email = email_data.get("raw_email", "")

        features = {}

        sender_features = self._extract_sender_features(sender, headers)
        features.update(sender_features)

        header_features = self._extract_header_features(headers)
        features.update(header_features)

        subject_features = self._extract_subject_features(subject)
        features.update(subject_features)

        body_features = self._extract_body_features(body)
        features.update(body_features)

        url_features = self._extract_url_features(body)
        features.update(url_features)

        return features


    def _extract_sender_features(self, sender: str, headers: dict) -> dict:
        """
        Sender analizi: Domain güvenliği, reputation

        Features:
        - sender_domain_trusted
        - sender_domain_length
        - sender_has_suspicious_pattern
        - sender_is_no_reply
        - sender_domain_suspicious_tld
        - return_path_matches_sender
        """
        features = {}

        # Domain çıkart
        domain = sender.split("@")[-1] if "@" in sender else ""

        # 1. Domain trusted mi?
        features["sender_domain_trusted"] = 1 if domain in self.trusted_domains else 0

        # 2. Domain uzunluğu
        features["sender_domain_length"] = len(domain)

        # 3. Suspicious pattern (paypal, verify, confirm vs)
        suspicious_count = sum(1 for pattern in self.suspicious_patterns if pattern in domain)
        features["sender_has_suspicious_pattern"] = min(suspicious_count, 3)

        # 4. noreply/no-reply/donotreply
        features["sender_is_no_reply"] = 1 if any(x in sender for x in ["noreply", "no-reply", "donotreply"]) else 0

        # 5. Suspicious TLD
        tld = domain.split(".")[-1] if "." in domain else ""
        suspicious_tlds = ["tk", "ml", "ga", "cf", "xyz"]
        features["sender_has_suspicious_tld"] = 1 if tld in suspicious_tlds else 0

        # 6. Return-Path vs From consistency
        return_path = headers.get("return_path", "").lower()
        features["return_path_matches_sender"] = 1 if return_path and return_path in sender else 0

        return features

    def _extract_header_features(self, headers: dict) -> dict:
        """
        Email headers analizi: SPF, DKIM, DMARC, consistency

        Features:
        - spf_valid
        - dkim_valid
        - dmarc_valid
        - header_consistency_score
        - suspicious_received_count
        """
        features = {}

        # 1. SPF kontrolü
        auth_results = headers.get("authentication_results", "")
        features["spf_valid"] = 1 if "spf=pass" in auth_results.lower() else 0

        # 2. DKIM kontrolü
        features["dkim_valid"] = 1 if "dkim=pass" in auth_results.lower() else 0

        # 3. DMARC kontrolü
        features["dmarc_valid"] = 1 if "dmarc=pass" in auth_results.lower() else 0

        # 4. Header consistency (From, Reply-To, Return-Path)
        from_addr = headers.get("from", "").lower()
        reply_to = headers.get("reply_to", "").lower()
        return_path = headers.get("return_path", "").lower()

        consistency = 0
        if from_addr and reply_to and from_addr.split("@")[-1] == reply_to.split("@")[-1]:
            consistency += 1
        if from_addr and return_path and from_addr.split("@")[-1] == return_path.split("@")[-1]:
            consistency += 1

        features["header_consistency_score"] = consistency / 2.0

        # 5. Suspicious received headers sayısı
        received = headers.get("received", [])
        if isinstance(received, list):
            suspicious_count = sum(1 for r in received if any(x in r.lower() for x in ["smtp", "mail"]))
            features["suspicious_received_count"] = min(suspicious_count, 5)
        else:
            features["suspicious_received_count"] = 0

        return features

    def _extract_subject_features(self, subject: str) -> dict:
        """
        Subject line analizi: Uzunluk, karakterler, keywordler

        Features:
        - subject_length
        - subject_has_urgent_keywords
        - subject_capitalization_ratio
        - subject_special_char_ratio
        - subject_has_suspicious_links
        """
        features = {}

        # 1. Uzunluk
        features["subject_length"] = len(subject)

        # 2. Urgent keyword sayısı
        urgent_count = self._count_keyword_matches(subject, self.urgency_keywords)
        features["subject_has_urgent_keywords"] = min(urgent_count, 3)

        # 3. Büyük harf oranı
        if len(subject) > 0:
            capital_ratio = sum(1 for c in subject if c.isupper()) / len(subject)
            features["subject_capitalization_ratio"] = round(capital_ratio, 2)
        else:
            features["subject_capitalization_ratio"] = 0.0

        # 4. Özel karakter oranı
        special_chars = sum(1 for c in subject if not c.isalnum() and c != " ")
        features["subject_special_char_ratio"] = round(special_chars / len(subject) if subject else 0, 2)

        # 5. Subject'te link var mı?
        has_link = 1 if re.search(r'http[s]?://\S+', subject) else 0
        features["subject_has_suspicious_links"] = has_link

        return features

    def _extract_body_features(self, body: str) -> dict:
        """
        Email body analizi: NLP, sentiment, grammar, patterns

        Features:
        - body_length
        - body_urgency_score
        - body_threat_score
        - body_action_score
        - body_sentiment_score
        - body_fear_indicators_count
        - body_greed_indicators_count
        - body_typo_ratio
        - body_has_html_tags
        - body_domain_mentions
        """
        features = {}

        if not body:
            return {
                "body_length": 0,
                "body_urgency_score": 0.0,
                "body_threat_score": 0.0,
                "body_action_score": 0.0,
                "body_sentiment_score": 0.0,
                "body_fear_indicators_count": 0,
                "body_greed_indicators_count": 0,
                "body_typo_ratio": 0.0,
                "body_has_html_tags": 0,
                "body_domain_mentions": 0
            }

        # 1. Body uzunluğu
        features["body_length"] = len(body)

        # 2. Urgency, Threat, Action scores
        features["body_urgency_score"] = round(
            self._calculate_keyword_score(body, self.urgency_keywords), 2
        )
        features["body_threat_score"] = round(
            self._calculate_keyword_score(body, self.threat_keywords), 2
        )
        features["body_action_score"] = round(
            self._calculate_keyword_score(body, self.action_keywords), 2
        )

        # 3. Sentiment analysis (TextBlob)
        try:
            blob = TextBlob(body)
            polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
            features["body_sentiment_score"] = round(polarity, 2)
        except:
            features["body_sentiment_score"] = 0.0

        # 4. Fear indicators (korku dili)
        fear_count = self._count_keyword_matches(body, self.fear_indicators)
        features["body_fear_indicators_count"] = min(fear_count, 5)

        # 5. Greed indicators (açgözlülük dili)
        greed_count = self._count_keyword_matches(body, self.greed_indicators)
        features["body_greed_indicators_count"] = min(greed_count, 5)

        # 6. Typo oranı (büyük harf hatası, garip karakterler)
        typo_count = self._count_typos(body)
        features["body_typo_ratio"] = round(typo_count / len(body) if body else 0, 3)

        # 7. HTML tags var mı?
        features["body_has_html_tags"] = 1 if re.search(r'<[^>]+>', body) else 0

        # 8. Domain mentions (paypal.com, amazon.com mentions)
        domain_count = sum(1 for domain in self.trusted_domains if domain in body.lower())
        features["body_domain_mentions"] = min(domain_count, 5)

        return features

    def _extract_url_features(self, body: str) -> dict:
        """
        Email'deki URLs analizi

        Features:
        - url_count
        - url_domain_mismatch
        - url_ip_address
        - url_shortest_domain
        """
        features = {}

        # URL'leri çıkart
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)

        # 1. URL sayısı
        features["url_count"] = len(urls)

        if not urls:
            return {
                "url_count": 0,
                "url_domain_mismatch": 0,
                "url_ip_address": 0,
                "url_shortest_domain": 100
            }

        # 2. Domain mismatch (gözüken vs gerçek domain farklı)
        mismatch_count = 0
        for url in urls:
            # Basit kontrol: URL'de @ varsa (credential harvesting)
            if "@" in url:
                mismatch_count += 1
        features["url_domain_mismatch"] = min(mismatch_count, 3)

        # 3. IP address kullanan URL var mı?
        ip_urls = sum(1 for url in urls if re.search(r'\d+\.\d+\.\d+\.\d+', url))
        features["url_ip_address"] = 1 if ip_urls > 0 else 0

        # 4. En kısa domain adı
        domains = [re.search(r'://([^/]+)', url).group(1) if re.search(r'://([^/]+)', url) else "" for url in urls]
        shortest = min([len(d) for d in domains if d]) if domains else 100
        features["url_shortest_domain"] = shortest

        return features

    def _count_keyword_matches(self, text: str, keywords: List[str]) -> int:
        """Metinde keyword kaç kez geçiyor?"""
        if not text or not keywords:
            return 0

        text_lower = text.lower()
        count = 0
        for keyword in keywords:
            matches = re.findall(r'\b' + re.escape(keyword) + r'\b', text_lower)
            count += len(matches)
        return count

    def _calculate_keyword_score(self, text: str, keywords: List[str]) -> float:
        """
        Keyword score hesapla (0-1)
        Kaç keyword bulundu / toplam kelime sayısı
        """
        if not text or not keywords:
            return 0.0

        words = text.lower().split()
        matched = self._count_keyword_matches(text, keywords)
        score = matched / len(words) if len(words) > 0 else 0.0
        return min(score, 1.0)

    def _count_typos(self, text: str) -> int:
        """
        Yazım hatası sayısı (basit metrik)
        - Yan yana 3+ aynı karakter
        - Garip karakter kombinasyonları
        """
        typo_count = 0

        # Yan yana 3+ aynı karakter
        for char in set(text):
            if char.isalpha():
                pattern = char * 3
                typo_count += len(re.findall(pattern, text))

        return typo_count

    def get_feature_names(self) -> List[str]:
        """Tüm feature isimleri döndür"""
        return [
            # Sender (6)
            "sender_domain_trusted",
            "sender_domain_length",
            "sender_has_suspicious_pattern",
            "sender_is_no_reply",
            "sender_has_suspicious_tld",
            "return_path_matches_sender",
            # Header (5)
            "spf_valid",
            "dkim_valid",
            "dmarc_valid",
            "header_consistency_score",
            "suspicious_received_count",
            # Subject (5)
            "subject_length",
            "subject_has_urgent_keywords",
            "subject_capitalization_ratio",
            "subject_special_char_ratio",
            "subject_has_suspicious_links",
            # Body (10)
            "body_length",
            "body_urgency_score",
            "body_threat_score",
            "body_action_score",
            "body_sentiment_score",
            "body_fear_indicators_count",
            "body_greed_indicators_count",
            "body_typo_ratio",
            "body_has_html_tags",
            "body_domain_mentions",
            # URL (4)
            "url_count",
            "url_domain_mismatch",
            "url_ip_address",
            "url_shortest_domain",
        ]


# Test
if __name__ == "__main__":
    extractor = EmailFeatureExtractor()

    test_email = {
        "sender": "noreply@suspicious-bank.com",
        "subject": "URGENT: Verify Your Account NOW!!!",
        "body": """
        Dear valued customer,

        We detected unusual activity on your account. 
        Click here to verify: http://suspicious-bank.com/verify@real-bank.com

        Regards,
        Security Team
        """,
        "headers": {
            "from": "noreply@suspicious-bank.com",
            "reply_to": "support@other-domain.com",
            "return_path": "bounce@suspicious-bank.com",
            "authentication_results": "spf=fail; dkim=fail; dmarc=fail"
        }
    }

    features = extractor.extract_features(test_email)

    print("📊 Çıkarılan Features:")
    print("=" * 50)
    for key, value in sorted(features.items()):
        print(f"{key:40} = {value}")

    print(f"\n✅ Toplam {len(features)} feature çıkarıldı")
    print(f"📋 Feature listesi: {extractor.get_feature_names()}")