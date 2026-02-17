"""Utility functions for string manipulation, such as slugification."""

import re
import unicodedata

# Pre-compile regex for performance
_SLUG_PATTERN = re.compile(r'[^a-z0-9]+')


def slugify(text: str) -> str:
    """Normalizes a string to a slug format (lowercase, no accents, snake_case).

    Example:
        "Patrimônio Líquido" -> "patrimonio_liquido"
        "Ativo Total" -> "ativo_total"
        " Disponibilidades (a) " -> "disponibilidades_a"

    Args:
        text (str): The input string.

    Returns:
        str: The normalized slug string.
    """

    # Normalize unicode characters (deose accents)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    # Convert to lowercase
    text = text.lower()

    # Replace non-alphanumeric characters with underscores.
    text = _SLUG_PATTERN.sub('_', text)

    # Remove leading/trailing underscores
    text = text.strip('_')

    return text
