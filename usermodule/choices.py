class Gender:
    STATUS_NOT_SET = 0
    MALE = 1
    FEMALE = 2


GENDER_CHOICES = (
    (Gender.STATUS_NOT_SET, 'Status Not Set'),
    (Gender.MALE, 'Male'),
    (Gender.FEMALE, 'Female')
)


class UserType:
    STATUS_NOT_SET = 0
    MANAGER = 1
    DELIVERY = 2


USERTYPE_CHOICES = (
    (UserType.STATUS_NOT_SET, 'Status Not Set'),
    (UserType.MANAGER, 'Manager'),
    (UserType.DELIVERY, 'Delivery')
)
