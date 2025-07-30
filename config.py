# Supported file extensions
ESTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff'}

# Regex rules: name -> pattern
RULES = {
    "iban": r"\bIT\d{2}[A-Z0-9]{1,30}\b",
    "fiscal_code": r"\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b",
    "secret_word": r"\bsecret\b",
    "secret_word2": r"\bdelta\b",
}