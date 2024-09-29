from __future__ import annotations

from typing import TypeVar

from django.db import models
from model_utils.managers import SoftDeletableManager
from model_utils.models import SoftDeletableModel
from modeltranslation.manager import MultilingualManager

_T = TypeVar("_T", bound=models.Model, covariant=True)


# TypeError: __class__ assignment: 'NewMultilingualManager' object layout differs from 'SoftDeletableManager'
# declaring the manager to avoid monkeypatching
# error: Definition of "get_queryset" in base class "SoftDeletableManagerMixin" is incompatible with definition in base class "MultilingualManager"  [misc]
# error: Definition of "get_queryset" in base class "SoftDeletableManagerMixin" is incompatible with definition in base class "MultilingualQuerysetManager"  [misc]
# MultilingualManager.get_queryset() -> Queryset[_T] fixes error
class SomeModelManager(SoftDeletableManager[_T], MultilingualManager[_T]):
    pass


class SomeModel(SoftDeletableModel):
    name = models.CharField(max_length=200)

    objects = SomeModelManager()
    available_objects = SomeModelManager()


class SoftDeleteQuerySet(models.QuerySet):
    pass


class SoftDeleteManager(models.Manager[_T]):
    _queryset_class = SoftDeleteQuerySet

    def get_queryset(self) -> models.QuerySet[_T]:
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class MonkeypatchedManager(SoftDeleteManager[_T]):
    pass


class MonkeypatchedModel(SoftDeleteModel):
    name = models.CharField(max_length=200)

    # when modeltranslation patches the manager, mypy_django_plugin cannot figure out the type
    # error: Could not resolve manager type for "app.models.MonkeypatchedModel.objects"  [django-manager-missing]
    objects = MonkeypatchedManager()

    # declaring type works
    objects_: MonkeypatchedManager[MonkeypatchedModel] = MonkeypatchedManager()
    other_objects = MultilingualManager()
    all_objects = models.Manager()

    class Meta:
        default_manager_name = "all_objects"


# cannot declare the manager to make mypy_django_plugin happy because of get_queryset overload
# error: Definition of "get_queryset" in base class "SoftDeleteManager" is incompatible with definition in base class "MultilingualManager"  [misc]
# error: Definition of "get_queryset" in base class "SoftDeleteManager" is incompatible with definition in base class "MultilingualQuerysetManager"  [misc]
# MultilingualManager.get_queryset() -> Queryset[_T] fixes error
class DeclaredModelManager(SoftDeleteManager[_T], MultilingualManager[_T]):
    pass


class DeclaredModel(SoftDeleteModel):
    name = models.CharField(max_length=200)

    objects = DeclaredModelManager()
    all_objects = models.Manager()
    lang_objects = MultilingualManager()

    class Meta:
        default_manager_name = "all_objects"
