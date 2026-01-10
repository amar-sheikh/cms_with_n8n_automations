def sidebar_context(request):
    nav_links = [
        ('home', 'Dashboard', 'bi bi-speedometer2'),
        ('courses', 'Courses', 'bi bi-journal-richtext'),
        ('batches', 'Batches', 'bi bi-journal-richtext'),
        ('instructors', 'Instructors', 'bi bi-people'),
        ('parents', 'Parents', 'bi bi-people'),
        ('students', 'Students', 'bi bi-people')
    ]

    return { 'nav_links': nav_links }