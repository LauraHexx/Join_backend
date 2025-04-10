import random
import re
from django.core.exceptions import ValidationError


def generate_random_color():
    """
    Generates a random hex color code in the format #RRGGBB.
    """
    return "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)])


def validate_hex_color(value):
    """
    Validates if the provided color value is a valid hex color code (#RRGGBB).
    """
    if not re.match(r"^#[0-9A-Fa-f]{6}$", value):
        raise ValidationError("Color must be a valid hex code in the format #RRGGBB.")
