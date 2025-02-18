from data_app.models import Contact, Category, Task, Subtask

# Contact.objects.create(user_id=1, color="#9327FF", name="Max Mustermann", email="max.mustermann@test", phone="0123456789")
# Contact.objects.create(user_id=1, color="#29ABE2", name="Erika Musterfrau", email="erika.musterfrau@test", phone="0123456788")
# Contact.objects.create(user_id=1, color="#02CF2F", name="John Doe", email="john.doe@test", phone="0123456799")
# Contact.objects.create(user_id=1, color="#AF1616", name="Johny Depp", email="johny.depp@test", phone="0123456777")
# Contact.objects.create(user_id=1, color="#462F8A", name="Lena Residenz", email="lena.residenz@test", phone="0123456766")
# Contact.objects.create(user_id=1, color="#FFC700", name="Hannah Müller", email="hannah.mueller@test", phone="01234566789")


# Category.objects.create(user_id=1, color="blue", name="Developing")
# Category.objects.create(user_id=1, color="red", name="HR")
# Category.objects.create(user_id=1, color="orange", name="Marketing")
# Category.objects.create(user_id=1, color="green", name="Sales")

# dev_category, _ = Category.objects.get_or_create(user_id=1, name="Developing", defaults={"color": "blue"})
# hr_category, _ = Category.objects.get_or_create(user_id=1, name="HR", defaults={"color": "red"})
# marketing_category, _ = Category.objects.get_or_create(user_id=1, name="Marketing", defaults={"color": "green"})
# sales_category, _ = Category.objects.get_or_create(user_id=1, name="Sales", defaults={"color": "orange"})
#
#
# task1 = Task.objects.create(user_id=1, title="Develop new feature", description="Implement a new feature in the software", category=dev_category, due_date="2025-07-05", priority="medium", process_step="inProgress")
# task2 = Task.objects.create(user_id=1, title="Conduct performance review", description="Schedule and conduct performance reviews for employees", category=hr_category, due_date="2024-01-07", priority="urgent", process_step="done")
# task3 = Task.objects.create(user_id=1, title="Launch new marketing campaign", description="Plan and execute a new marketing campaign", category=marketing_category, due_date="2025-07-10", priority="medium", process_step="todo")
# task4 = Task.objects.create(user_id=1, title="Follow up with potential leads", description="Contact potential leads and follow up on sales inquiries", category=sales_category, due_date="2024-07-12", priority="low", process_step="awaitingFeedback")
# task5 = Task.objects.create(user_id=1, title="Organize training session", description="Coordinate and plan a training session for employees", category=hr_category, due_date="2024-07-15", priority="medium", process_step="todo")
# task6 = Task.objects.create(user_id=1, title="Create sales presentation", description="Develop a sales presentation for a client meeting", category=sales_category, due_date="2023-07-20", priority="urgent", process_step="done")
#
#
# Subtask.objects.create(task=task1, name="Write code for the feature", status=True)
# Subtask.objects.create(task=task1, name="Test the feature for bugs", status=False)
# Subtask.objects.create(task=task2, name="Prepare evaluation forms", status=True)
# Subtask.objects.create(task=task2, name="Schedule meetings with employees", status=True)
# Subtask.objects.create(task=task3, name="Create campaign strategy", status=False)
# Subtask.objects.create(task=task3, name="Design marketing materials", status=False)
# Subtask.objects.create(task=task4, name="Send follow-up emails", status=True)
# Subtask.objects.create(task=task4, name="Make phone calls to leads", status=False)
# Subtask.objects.create(task=task5, name="Choose training topics", status=False)
# Subtask.objects.create(task=task5, name="Arrange training logistics", status=False)
# Subtask.objects.create(task=task6, name="Research client's needs", status=True)
# Subtask.objects.create(task=task6, name="Design presentation slides", status=True)
#
#
# task1.contacts.set([1, 3, 4, 5])
# task2.contacts.set([2, 4])
# task3.contacts.set([5])
# task4.contacts.set([6, 2, 3])
# task5.contacts.set([1, 3])
# task6.contacts.set([4, 5, 6])
