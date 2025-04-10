from django.db import IntegrityError
from tasks_app.models import Contact, Category, Task, Subtask
from contacts_app.models import Contact as ContactModel
from dummy_data_app.api.data import DUMMY_CONTACTS, DUMMY_CATEGORIES, DUMMY_TASKS
from django.db import IntegrityError
from tasks_app.models import Contact, Category, Task, Subtask
from contacts_app.models import Contact as ContactModel
from dummy_data_app.api.data import DUMMY_CONTACTS, DUMMY_CATEGORIES, DUMMY_TASKS


class ItemNotFoundError(Exception):
    """
    Custom exception for when an item cannot be found by its ID.
    """

    pass


def find_item_by_id(data_list, item_id):
    """
    Finds an item in a list of dictionaries by its 'id'.
    """
    item_data = next((item for item in data_list if item["id"] == item_id), None)

    if not item_data:
        raise ItemNotFoundError(f"Item with ID {item_id} in {data_list} not found.")

    return item_data


def create_contact(contact_data, user):
    """
    Creates a contact in the database.
    """
    Contact.objects.create(
        name=contact_data["name"],
        first_name=contact_data["first_name"],
        last_name=contact_data["last_name"],
        email=contact_data["email"],
        phone_number=contact_data["phone_number"],
        color=contact_data["color"],
        created_by=user,
    )


def create_category(category_data, user):
    """
    Creates a category in the database.
    """
    Category.objects.create(
        name=category_data["name"],
        color=category_data["color"],
        created_by=user,
    )


def get_category_details(task_data, user):
    """
    Extracts the category from the task data, finds it by ID, and creates it.
    """
    category_data = find_item_by_id(DUMMY_CATEGORIES, task_data["category"])

    return Category.objects.get(
        name=category_data["name"], color=category_data["color"], created_by=user
    )


def create_task(task_data, user):
    """
    Creates a task and sets the related contacts and subtasks.
    """
    category = get_category_details(task_data, user)

    task = Task.objects.create(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
        priority=task_data["priority"],
        process_step=task_data["process_step"],
        category=category,
        created_by=user,
    )

    set_contacts_for_task(task_data["contacts"], user, task)
    create_subtasks(task_data["subtasks"], task)
    task.save()


def set_contacts_for_task(contact_ids, user, task):
    """
    Sets the contacts for the task based on contact IDs.
    """
    contacts = []
    for contact_id in contact_ids:
        contact_data = find_item_by_id(DUMMY_CONTACTS, contact_id)
        contact = Contact.objects.get(email=contact_data["email"], created_by=user)
        contacts.append(contact)

    task.contacts.set(contacts)


def create_subtasks(subtask_data, task):
    """
    Creates the subtasks for a task.
    """
    for subtask in subtask_data:
        Subtask.objects.create(task=task, **subtask)


def create_dummy_data(user):
    """
    Creates all dummy data: contacts, categories, and tasks.
    """
    try:
        for contact_data in DUMMY_CONTACTS:
            create_contact(contact_data, user)

        for category_data in DUMMY_CATEGORIES:
            create_category(category_data, user)

        for task_data in DUMMY_TASKS:
            create_task(task_data, user)

    except IntegrityError as e:
        print(f"Error during the creation of dummy data: {e}")
