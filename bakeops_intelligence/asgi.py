"""
ASGI config for BakeOps Intelligence.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "bakeops_intelligence.settings.production",
)

application = get_asgi_application()