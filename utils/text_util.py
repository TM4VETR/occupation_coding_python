def replace_umlauts(text: str) -> str:
    """
    Replace German umlauts and ß with ASCII equivalents.

    Args:
        text (str): Input text.

    Returns:
        str: Normalized text (e.g., "Bürokauffrau" -> "Buerokauffrau").
    """
    replacements = {
        "ä": "ae", "ö": "oe", "ü": "ue",
        "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
        "ß": "ss",
    }

    for orig, repl in replacements.items():
        text = text.replace(orig, repl)

    return text
