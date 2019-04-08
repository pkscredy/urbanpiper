class StatesStatus:
    STATUS_NOT_SET = 0
    NEW = 1
    ACCEPTED = 2
    COMPLETED = 3
    DECLINED = 4
    CANCELLED = 5
    CLOSED = 6


STATE_STATUS_CHOICES = (
    (StatesStatus.STATUS_NOT_SET, 'Status Not Set'),
    (StatesStatus.NEW, 'New'),
    (StatesStatus.ACCEPTED, 'Accepted'),
    (StatesStatus.COMPLETED, 'Completed'),
    (StatesStatus.DECLINED, 'Decline'),
    (StatesStatus.CANCELLED, 'Cancelled'),
    (StatesStatus.CLOSED, 'Closed')
)


class PriorityStatus:
    STATUS_NOT_SET = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


PRIORITY_CHOICES = (
    (PriorityStatus.STATUS_NOT_SET, 'Status Not Set'),
    (PriorityStatus.HIGH, 'High'),
    (PriorityStatus.MEDIUM, 'Medium'),
    (PriorityStatus.LOW, 'Low')
)
