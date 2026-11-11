
import re


SUSPICIOUS_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"send\s+(all\s+)?passwords",
    r"reveal\s+confidential\s+information",
    r"bypass\s+security",
    r"ignore\s+all\s+rules",
    r"disable\s+security"
]


def inspect_email(body):

    text = body.lower()

    for pattern in SUSPICIOUS_PATTERNS:

        if re.search(pattern, text):
            return {
                "suspicious": True,
                "reason": "Potential prompt injection detected"
            }

    return {
        "suspicious": False,
        "reason": "No known suspicious pattern detected"
    }
