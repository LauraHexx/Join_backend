from django.utils.timezone import now

from tasks_app.models import Task


def get_next_due_date(user):
    """
    Returns the next due date for the user or None if no tasks are due.
    """
    return (
        Task.objects.filter(created_by=user, due_date__gte=now())
        .order_by("due_date")
        .values_list("due_date", flat=True)
        .first()
    )


def format_due_date(due_date):
    """
    Formats a due date into a readable string ("Month day, year") or returns None if no date.
    """
    if due_date:
        return due_date.strftime("%B %d, %Y")
    return None
