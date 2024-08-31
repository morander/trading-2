from app import create_app, db
from app.models import Task

def insert_test_data():
    app = create_app()
    with app.app_context():
        # Create some test tasks
        task1 = Task(title="Complete project proposal", description="Write up the proposal for the new project")
        task2 = Task(title="Buy groceries", description="Milk, eggs, bread, and vegetables")
        task3 = Task(title="Learn Flask", description="Complete the Flask tutorial and build a sample app")

        # Add tasks to the session and commit
        db.session.add_all([task1, task2, task3])
        db.session.commit()

        print("Test data inserted successfully!")

if __name__ == "__main__":
    insert_test_data()