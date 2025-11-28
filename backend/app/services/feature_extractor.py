from app.constants import URGENCY_KEYWORDS, THREAT_KEYWORDS, ACTION_KEYWORDS
import re

class EmailFeatureExtractor:
    """Extract features from email for phishing detection"""
    def __init__(self):
        self.urgency_keywords = URGENCY_KEYWORDS
        self.threat_keywords = THREAT_KEYWORDS
        self.action_keywords = ACTION_KEYWORDS

    def extract_features(self, email_data: dict) -> dict:
        sender = email_data.get("sender", "").lower()
        subject = email_data.get("subject", "")
        body = email_data.get("body", "")

        full_text = f"{subject} {body}"

        urgency_score = self.calculate_keyword_score(full_text, self.urgency_keywords)
        threat_score = self.calculate_keyword_score(full_text, self.threat_keywords)
        action_score = self.calculate_keyword_score(full_text, self.action_keywords)

        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
        url_count = len(urls)

        has_attachment = email_data.get("has_attachment", False)

        return {
            "urgency_score": round(urgency_score, 2),
            "threat_score": round(threat_score, 2),
            "action_score": round(action_score, 2),
            "url_count": url_count,
            "has_attachment": has_attachment
        }

    def count_keyword_matches(self, text: str, keywords: list)->int:
        if not text or not keywords:
            return 0
        text_lower = text.lower()
        count=0
        for keyword in keywords:
            matches = re.findall(r'\b'+ re.escape(keyword) + r'\b', text_lower)
            count += len(matches)
        return count

    def calculate_keyword_score(self, text: str, keywords: list)->float:
        if not text or not keywords:
            return 0.0
        words = text.lower().split()
        matched = self.count_keyword_matches(text, keywords)
        score = matched/len(words) if len(words) >0 else 0.0
        return min(score, 1.0)

