"""
Constants for phishing detection
Suspicious keywords, patterns, and trusted domains
"""

# ==================== URGENCY KEYWORDS (25) ====================
# Words that create time pressure and urgency
URGENCY_KEYWORDS = [
    "urgent",
    "immediately",
    "asap",
    "now",
    "act now",
    "verify",
    "confirm",
    "validate",
    "update",
    "click here",
    "right away",
    "do not delay",
    "limited time",
    "expires",
    "expires soon",
    "deadline",
    "action required",
    "must confirm",
    "immediate action",
    "time sensitive",
    "don't delay",
    "hurry",
    "quick action",
    "before it's too late",
    "final notice"
]

# ==================== THREAT KEYWORDS (25) ====================
# Words indicating account/payment threats
THREAT_KEYWORDS = [
    "account suspended",
    "account locked",
    "confirm identity",
    "unusual activity",
    "unauthorized access",
    "suspicious activity",
    "update payment",
    "verify credentials",
    "verify account",
    "confirm password",
    "reset password",
    "security alert",
    "security issue",
    "compromised account",
    "fraudulent activity",
    "restricted account",
    "limited access",
    "abnormal behavior",
    "unauthorized transaction",
    "payment failed",
    "billing problem",
    "card declined",
    "identity theft",
    "breach detected",
    "re-authenticate"
]

# ==================== ACTION KEYWORDS (25) ====================
# Words urging user to take action (click, download, etc)
ACTION_KEYWORDS = [
    "click",
    "click here",
    "download",
    "open",
    "confirm",
    "verify",
    "validate",
    "authenticate",
    "login",
    "sign in",
    "sign up",
    "update",
    "upgrade",
    "activate",
    "enable",
    "submit",
    "complete",
    "confirm now",
    "proceed",
    "continue",
    "access",
    "install",
    "accept",
    "agree",
    "approve"
]

# ==================== SUSPICIOUS DOMAIN PATTERNS (25) ====================
# Domain keywords that might indicate fake/phishing domains
SUSPICIOUS_DOMAIN_PATTERNS = [
    "verify",
    "confirm",
    "validate",
    "update",
    "secure",
    "login",
    "account",
    "password",
    "reset",
    "recovery",
    "help",
    "support",
    "service",
    "paypal",
    "apple",
    "amazon",
    "microsoft",
    "google",
    "facebook",
    "bank",
    "banking",
    "security",
    "verify-account",
    "confirm-identity",
    "update-payment"
]

# ==================== TRUSTED DOMAINS (WHITELIST) ====================
# Legitimate domains - no suspicion
TRUSTED_DOMAINS = [
    "paypal.com",
    "apple.com",
    "amazon.com",
    "microsoft.com",
    "google.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "linkedin.com",
    "github.com",
    "gmail.com",
    "outlook.com",
    "yahoo.com",
    "dropbox.com",
    "slack.com"
]

# ==================== SUSPICIOUS TLDS ====================
# Top-level domains commonly used in phishing
SUSPICIOUS_TLDS = [
    "tk",      # Tokelau - free domain provider
    "ml",      # Mali - free domain provider
    "ga",      # Gabon - free domain provider
    "cf",      # Central African Republic - free domain provider
    "click",   # Generic - often used for phishing
    "download",
    "online",
    "space",
    "xyz",
    "top",
    "win",
    "date",
    "racing",
    "review",
    "gdn",
    "work"
]

# ==================== ATTACHMENT SUSPICIOUS EXTENSIONS ====================
# File extensions commonly used in phishing attachments
SUSPICIOUS_EXTENSIONS = [
    ".exe",
    ".bat",
    ".cmd",
    ".com",
    ".msi",
    ".scr",
    ".vbs",
    ".js",
    ".jar",
    ".zip",
    ".rar",
    ".7z",
    ".docm",    # Macro-enabled Word
    ".xlsm",    # Macro-enabled Excel
    ".pptm",    # Macro-enabled PowerPoint
    ".potm",
    ".ppam",
    ".pslm",
    ".sldm",
    ".app",
    ".deb",
    ".rpm"
]

# ==================== FEATURE THRESHOLDS ====================
# Thresholds for determining risk levels
FEATURE_THRESHOLDS = {
    "urgency_keywords_threshold": 2,      # 2+ urgency words = suspicious
    "threat_keywords_threshold": 1,       # 1+ threat words = suspicious
    "action_keywords_threshold": 2,       # 2+ action words = suspicious
    "suspicious_domain_pattern_threshold": 1,  # 1+ pattern match = suspicious
    "url_count_threshold": 3,             # 3+ URLs = suspicious
    "suspicious_url_ratio": 0.5,          # 50%+ suspicious URLs = high risk
    "short_domain_length": 3,             # Domain < 3 chars = suspicious
    "very_long_url_length": 200,          # URL > 200 chars = suspicious
    "high_capital_ratio": 0.3,            # >30% capital letters = suspicious
}

# ==================== PHISHING KEYWORDS IN DIFFERENT LANGUAGES ====================
# Turkish phishing keywords
PHISHING_KEYWORDS_TR = [
    "acil",
    "hemen",
    "derhal",
    "şimdi",
    "doğrulama",
    "doğrula",
    "onay",
    "onayla",
    "güncelleme",
    "güncelle",
    "hesap askıya",
    "şüpheli faaliyet",
    "yetkisiz erişim",
    "parola sıfırla",
    "kimlik doğrula",
    "acil bildirim",
    "tehlike",
    "uyarı",
    "sınırlandırılmış erişim",
    "işlem başarısız"
]

# ==================== URL SUSPICIOUS PATTERNS ====================
# Regex patterns and indicators for suspicious URLs
URL_SUSPICIOUS_INDICATORS = [
    "@",                # URL with @ symbol (credential harvesting)
    "-",                # Hyphen in domain
    "paypal",
    "apple",
    "amazon",
    "microsoft",
    "google",
    "facebook",
    "bank",
    "secure",
    "verify",
    "login",
    "account",
    "password",
    "reset",
]

# ==================== EMAIL HEADER SUSPICIOUS PATTERNS ====================
# Patterns in email headers that indicate phishing
HEADER_SUSPICIOUS_PATTERNS = {
    "spoofed_sender": ["noreply@", "no-reply@", "donotreply@"],
    "suspicious_return_path": ["bounce@", "return@", "mailer-daemon"],
    "missing_headers": ["DKIM-Signature", "SPF-Record"],
    "suspicious_received": ["smtp.gmail.com", "mail.outlook.com"],  # Compromised account
}

# ==================== SENTIMENT ANALYSIS INDICATORS ====================
# Words indicating phishing sentiment (fear, urgency, greed)
FEAR_INDICATORS = [
    "danger",
    "threat",
    "risk",
    "dangerous",
    "unsafe",
    "vulnerable",
    "compromised",
    "breach",
    "attack"
]

GREED_INDICATORS = [
    "free",
    "prize",
    "winner",
    "congratulations",
    "claim",
    "bonus",
    "reward",
    "money",
    "cash",
    "inheritance"
]

URGENCY_INDICATORS = [
    "urgent",
    "immediately",
    "asap",
    "now",
    "deadline",
    "limited",
    "expires",
    "hurry",
    "quick"
]