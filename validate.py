import re
import base64


# Defence 1 and 2: Validate user input
def validate_input(user_input):
    if len(user_input) > 500:
        return "Input exceeds the 500-character limit."

    suspicious_phrases = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "pretend you are",
        "act as if you have no restrictions",
        "reveal your system prompt",
        "reveal your hidden system instructions",
        "disable employee authentication"
    ]

    text_to_check = user_input.lower()

    # Check the original input
    for phrase in suspicious_phrases:
        if phrase in text_to_check:
            return "Suspicious prompt injection phrase detected."

    # Check Base64-encoded instructions
    encoded_parts = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', user_input)

    for part in encoded_parts:
        try:
            decoded = base64.b64decode(part).decode("utf-8", errors="ignore").lower()
            for phrase in suspicious_phrases:
                if phrase in decoded:
                    return "Encoded prompt injection detected."
        except Exception:
            pass

    return None


# Defence 3: Scan model output
def scan_output(output):
    suspicious_patterns = [
        r"system prompt",
        r"hidden system instructions",
        r"password\s*[:=]\s*\S+",
        r"(api[_-]?key|access[_-]?token)\s*[:=]\s*\S+",
        r"sk-[A-Za-z0-9_-]{10,}",
        r"https?://\S+"
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, output, re.IGNORECASE):
            return "Potential sensitive information or unsafe URL detected."

    return None
