from django.apps import apps
from django.contrib import admin
from django.test import TestCase


class BakeOpsAdminRegistrationTests(TestCase):
    def test_all_bakeops_models_are_registered_in_admin(self):
        models = list(apps.get_app_config("bakeops").get_models())

        missing = [
            model.__name__
            for model in models
            if model not in admin.site._registry
        ]

        self.assertEqual(missing, [])
        self.assertEqual(len(models), 25)