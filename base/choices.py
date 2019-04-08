# from enum import Enum
#
# from base.exceptions import ChoicesError
#
#
# class CharChoices(Enum):
#     @staticmethod
#     def clean_name(name):
#         name = name.replace('_', ' ')
#         name = name.title()
#         return name
#
#     @classmethod
#     def _get_choice_map(cls, choice_list=None):
#         if not choice_list:
#             return cls.__members__
#         return {name: cls.__members__[name] for name in choice_list}
#
#     @classmethod
#     def choices(cls, choice_list=None):
#         status_map = ()
#         duplicates = []
#
#         choice_map = cls._get_choice_map(choice_list)
#
#         for name, member in choice_map.items():
#             if name != member.name:
#                 duplicates.append((name, member.name))
#
#             status_map += ((member.value, Choices.clean_name(name)),)
#
#         if duplicates:
#             duplicate_details = ', '.join(
#                 ['%s -> %s' % (alias, name) for (alias, name) in duplicates])
#             raise ChoicesError(
#                 'duplicate values found in %s: %s' % (duplicate_details,
#                                                       cls.__name__))
#
#         return status_map
#
#     @classmethod
#     def get_name(cls, value, choice_list=None):
#         choice_map = cls._get_choice_map(choice_list)
#         for name, member in choice_map.items():
#             if value == member.value:
#                 return cls.clean_name(name)
#
#         raise ChoicesError(
#             'Invalid value {} passed for {}'.format(value, cls.__name__))
#
#     @classmethod
#     def find_member(cls, name, choice_list=None):
#         choice_map = cls._get_choice_map(choice_list)
#         for member in choice_map.values():
#             if cls.clean_name(member.name) == name:
#                 return member
#
#         return None
#
#     @classmethod
#     def has_attr(cls, name, choice_list=None):
#         return bool(cls.find_member(name, choice_list))
#
#     @classmethod
#     def get_val(cls, name, choice_list=None):
#         member = cls.find_member(name, choice_list)
#
#         if member is None:
#             raise ChoicesError('%s not found in %s' % (name, cls.__name__))
#
#         return member.value
#
#
# class Choices(int, CharChoices):
#     pass
