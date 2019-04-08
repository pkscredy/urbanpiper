from abc import ABCMeta, abstractmethod

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from base.constants import DBConstants
from base.exceptions import ModelOperationError


class AbstractBaseDbIO(object):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError('missing model for DbIO!')

    def _iterate_fields(self, kwargs):
        fields = [f.name for f in self.model._meta.get_fields()]
        for k, v in kwargs.items():
            if k in fields or k.split('__')[0] in fields:
                yield k, v

    def _clean_save_object(self, obj):
        obj.full_clean()
        obj.save()
        return obj

    def _get_clean_data(self, kwargs):
        clean_data = {}
        for k, v in self._iterate_fields(kwargs):
            clean_data[k] = v

        if not clean_data:
            raise ModelOperationError(
                DBConstants.INVALID_QUERY_PARAMS.format(
                    self.model.__name__))
        return clean_data

    def create_obj(self, kwargs, **extra):
        try:
            clean_data = {}
            for k, v in self._iterate_fields(kwargs):
                clean_data[k] = v
            obj = self.model(**clean_data)
            return self._clean_save_object(obj)
        except IntegrityError:
            msg = DBConstants.FAILED_OPERATION.format('save', obj=self)
            self._raise_exception(msg, **extra)

    def update_obj(self, obj, kwargs, **extra):
        try:
            for k, v in self._iterate_fields(kwargs):
                setattr(obj, k, v)
            return self._clean_save_object(obj)
        except (TypeError, ValueError, ValidationError):
            msg = DBConstants.FAILED_OPERATION.format('update', obj=self)
            self._raise_exception(msg, **extra)

    def get_object(self, kwargs, attrs=(), **extra):
        clean_data = self._get_clean_data(kwargs)
        try:
            return self.model.objects.only(*attrs).get(**clean_data)
        except self.model.DoesNotExist:
            msg = DBConstants.OBJECT_NOT_FOUND.format(obj=self)
            self._raise_exception(msg, **extra)

    def filter_objects(self, kwargs, attrs=()):
        clean_data = self._get_clean_data(kwargs)
        return self.model.objects.only(*attrs).filter(**clean_data)

    @staticmethod
    def _raise_exception(msg, **kwargs):
        if not kwargs.get('fail_silently', False):
            raise ModelOperationError(msg)
