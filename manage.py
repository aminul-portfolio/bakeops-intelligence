#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "bakeops_intelligence.settings.local",
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure your virtual environment is "
            "activated and dependencies are installed from requirements.txt."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()