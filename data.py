from data_app.models import Contact, Category, Task, Subtask


contacts = [
    {
        "user_id": 1,
        "color": "#9327FF",
        "name": "Max Mustermann",
        "email": "max.mustermann@test",
        "phone": "0123456789",
    },
    {
        "user_id": 1,
        "color": "#29ABE2",
        "name": "Erika Musterfrau",
        "email": "erika.musterfrau@test",
        "phone": "0123456788",
    },
    {
        "user_id": 1,
        "color": "#02CF2F",
        "name": "John Doe",
        "email": "john.doe@test",
        "phone": "0123456799",
    },
    {
        "user_id": 1,
        "color": "#AF1616",
        "name": "Johny Depp",
        "email": "johny.depp@test",
        "phone": "0123456777",
    },
    {
        "user_id": 1,
        "color": "#462F8A",
        "name": "Lena Residenz",
        "email": "lena.residenz@test",
        "phone": "0123456766",
    },
    {
        "user_id": 1,
        "color": "#FFC700",
        "name": "Hannah Müller",
        "email": "hannah.mueller@test",
        "phone": "01234566789",
    },
]

for contact in contacts:
    Contact.objects.create(**contact)
