DUMMY_CONTACTS = [
    {
        "color": "#9327FF",
        "name": "Max Mustermann",
        "email": "max.mustermann@test",
        "phone": "0123456789",
    },
    {
        "color": "#29ABE2",
        "name": "Erika Musterfrau",
        "email": "erika.musterfrau@test",
        "phone": "0123456788",
    },
    {
        "color": "#02CF2F",
        "name": "John Doe",
        "email": "john.doe@test",
        "phone": "0123456799",
    },
    {
        "color": "#1ABC9C",
        "name": "Sophie Schneider",
        "email": "sophie.schneider@test",
        "phone": "0123456444",
    },
    {
        "color": "#E67E22",
        "name": "Ben Krause",
        "email": "ben.krause@test",
        "phone": "0123456555",
    },
]

DUMMY_CATEGORIES = [
    {"name": "Developing", "color": "#0000FF"},
    {"name": "HR", "color": "#FF0000"},
    {"name": "Marketing", "color": "#FFA500"},
    {"name": "Sales", "color": "#008000"},
]

DUMMY_TASKS = [
    {
        "title": "Develop new feature",
        "description": "Implement a new feature in the software",
        "category": "Developing",
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
        "category": "HR",
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
        "category": "Marketing",
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
        "category": "Sales",
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
        "category": "HR",
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
        "category": "Sales",
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
