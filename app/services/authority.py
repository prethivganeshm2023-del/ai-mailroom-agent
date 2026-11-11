
import os


def check_authority(sender):

    trusted_senders = {
        item.strip().lower()
        for item in os.getenv(
            "TRUSTED_SENDERS", ""
        ).split(",")
        if item.strip()
    }

    authorized = sender.strip().lower() in trusted_senders

    return {
        "authorized": authorized,
        "reason": (
            "Sender is in the trusted list"
            if authorized
            else "Sender is not authorized"
        )
    }
