DUMMY_CONTACTS = [
    {
        "id": 1,
        "name": "Max Mustermann",
        "first_name": "Max",
        "last_name": "Mustermann",
        "email": "max.mustermann@test.de",
        "phone_number": "0123456789",
        "color": "#9327ff",
    },
    {
        "id": 2,
        "name": "Erika Musterfrau",
        "first_name": "Erika",
        "last_name": "Musterfrau",
        "email": "erika.musterfrau@test.de",
        "phone_number": "0123456788",
        "color": "#29abe2",
    },
    {
        "id": 3,
        "name": "John Doe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.de",
        "phone_number": "0123456799",
        "color": "#02cf2f",
    },
    {
        "id": 4,
        "name": "Sophie Schneider",
        "first_name": "Sophie",
        "last_name": "Schneider",
        "email": "sophie.schneider@test.de",
        "phone_number": "0123456444",
        "color": "#1abc9c",
    },
    {
        "id": 5,
        "name": "Ben Krause",
        "first_name": "Ben",
        "last_name": "Krause",
        "email": "ben.krause@test.de",
        "phone_number": "0123456555",
        "color": "#e67e22",
    },
    {
        "id": 6,
        "name": "Anna Müller",
        "first_name": "Anna",
        "last_name": "Müller",
        "email": "anna.mueller@test.de",
        "phone_number": "0123456777",
        "color": "#f39c12",
    },
]

DUMMY_CATEGORIES = [
    {"id": 1, "name": "Developing", "color": "#0000ff"},
    {"id": 2, "name": "HR", "color": "#ff0000"},
    {"id": 3, "name": "Marketing", "color": "#ffa500"},
    {"id": 4, "name": "Sales", "color": "#008000"},
]




DUMMY_TASKS = [
    {
        "title": "Develop new feature",
        "description": "Implement a new feature in the software",
        "category": 1,
        "contacts": [1, 3, 4, 5],
        "due_date": "2025-07-05",
        "priority": "medium",
        "process_step": "inProgress",
        "subtasks": [
            {"name": "Write code for the feature", "status": True},
            {"name": "Test the feature for bugs", "status": False},
        ],
    },
    {
        "title": "Conduct performance review",
        "description": "Schedule and conduct performance reviews for employees",
        "category": 2,
        "contacts": [2, 4],
        "due_date": "2024-01-07",
        "priority": "urgent",
        "process_step": "done",
        "subtasks": [
            {"name": "Prepare evaluation forms", "status": True},
            {"name": "Schedule meetings with employees", "status": True},
        ],
    },
    {
        "title": "Launch new marketing campaign",
        "description": "Plan and execute a new marketing campaign",
        "category": 3,
        "contacts": [5],
        "due_date": "2025-07-10",
        "priority": "medium",
        "process_step": "todo",
        "subtasks": [
            {"name": "Create campaign strategy", "status": False},
            {"name": "Design marketing materials", "status": False},
        ],
    },
    {
        "title": "Follow up with potential leads",
        "description": "Contact potential leads and follow up on sales inquiries",
        "category": 4,
        "contacts": [6, 2, 3],
        "due_date": "2024-07-12",
        "priority": "low",
        "process_step": "awaitingFeedback",
        "subtasks": [
            {"name": "Send follow-up emails", "status": True},
            {"name": "Make phone calls to leads", "status": False},
        ],
    },
    {
        "title": "Organize training session",
        "description": "Coordinate and plan a training session for employees",
        "category": 2,
        "contacts": [1, 3],
        "due_date": "2024-07-15",
        "priority": "medium",
        "process_step": "todo",
        "subtasks": [
            {"name": "Choose training topics", "status": False},
            {"name": "Arrange training logistics", "status": False},
        ],
    },
    {
        "title": "Create sales presentation",
        "description": "Develop a sales presentation for a client meeting",
        "category": 4,
        "contacts": [4, 5, 6],
        "due_date": "2023-07-20",
        "priority": "urgent",
        "process_step": "done",
        "subtasks": [
            {"name": "Research client's needs", "status": True},
            {"name": "Design presentation slides", "status": True},
        ],
    },
]
