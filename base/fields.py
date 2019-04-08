# """Custom Django Field to store Choices."""
# from django.db import models
#
#
# class ChoicesMixin:
#     """Provides functionality to store Choices."""
#
#     def __init__(self, choice_class=None, *args, **kwargs):
#         """Add choice_class while initialization."""
#         self.choice_class = choice_class
#         if choice_class:
#             kwargs['choices'] = choice_class.choices()
#         super().__init__(*args, **kwargs)
#
#     def deconstruct(self):
#         """Remove choices while deconstructing."""
#         name, path, args, kwargs = super().deconstruct()
#         del kwargs['choices']
#         if self.choice_class:
#             kwargs['choice_class'] = self.choice_class
#         return name, path, args, kwargs
#
#
# class IntChoicesMixin(ChoicesMixin):
#     """For Integer Choices."""
#
#     def get_prep_value(self, value):
#         """Convert value to integer before storing."""
#         return super().get_prep_value(int(value))
#
#
# class ChoicesField(IntChoicesMixin, models.PositiveSmallIntegerField):
#     """Integer choice field."""
#
#     pass
#
#
# class CharChoicesField(ChoicesMixin, models.CharField):
#     """Char choice field."""
#
#     pass
