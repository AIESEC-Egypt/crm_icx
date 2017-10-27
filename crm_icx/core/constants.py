APPLICATION_REQUEST = 'Applications Request'
APPLICATION_REQUEST_ID = 1

OPPORTUNITIES_REQUEST = "Opportunities Request"
OPPORTUNITIES_REQUEST_ID = 2

API_REQUESTS_CHOICES = (
    (1, 'Applications'),
    (2, 'Opportunities'),
    (9, 'None')
)

OPPORTUNITIES_STATUSES = (
    (1, 'DRAFT'),
    (2, 'OPEN'),
    (3, 'TO PROCESS'),
    (4, 'ACCEPTED'),
    (5, 'APPROVED'),
    (6, 'UNMATCHED'),
    (7, 'REALIZED'),
    (8, 'COMPLETED'),
    (9, 'REMOVED')
)

APPLICATIONS_STATUSES = (
    (1, 'OPEN'),
    (2, 'ACCEPTED'),
    (3, 'IN PROGRESS'),
    (4, 'APPROVED'),
    (5, 'REALIZED'),
    (6, 'COMPLETED'),
    (7, 'WITHDRAWN'),
    (8, 'REJECTED'),
    (9, 'DECLINED')
)
