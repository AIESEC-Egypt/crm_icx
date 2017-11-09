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
    (None, 'all'),
    ('open', 'open'),
    ('accepted', 'accepted'),
    ('matched', 'matched'),
    ('approved', 'approved'),
    ('realized', 'realized'),
    ('completed', 'completed'),
    ('withdrawn', 'withdrawn'),
    ('rejected', 'rejected'),
    ('declined', 'declined')
)
