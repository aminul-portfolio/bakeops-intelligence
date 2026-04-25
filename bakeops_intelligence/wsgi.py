"""
WSGI config for BakeOps Intelligence.
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "bakeops_intelligence.settings.production",
)

application = get_wsgi_application()