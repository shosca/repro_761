from django.utils.translation import gettext_lazy as _

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.admin",
    "modeltranslation",
    "app",
]


LANGUAGES = (("en-us", _("American English")), ("es", _("Spanish")))
