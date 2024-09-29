from modeltranslation import translator

from . import models


@translator.register(models.SomeModel)
class SomeModelOptions(translator.TranslationOptions):
    fields = ("name",)


@translator.register(models.MonkeypatchedModel)
class FlavoredModelOptions(translator.TranslationOptions):
    fields = ("name",)


@translator.register(models.DeclaredModel)
class DeclaredModelOptions(translator.TranslationOptions):
    fields = ("name",)
