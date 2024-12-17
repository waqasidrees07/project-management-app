from django.test import TestCase
from django.utils import timezone
from user.models import User
from .models import Project, Task
from datetime import timedelta


class ProjectTaskTests(TestCase):

    def setUp(self):
        """
        Set up initial data for tests.
        """
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password123"
        )
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="password123"
        )

        self.project = Project.objects.create(
            user=self.user1,
            title="Project Alpha",
            description="This is a test project.",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=10)
        )
        self.project.team_members.add(self.user2, self.user3)

    def test_user_email_field(self):
        """
        Test that the email field is set correctly for users.
        """
        self.assertEqual(self.user1.email, "user1@example.com")
        self.assertEqual(self.user2.email, "user2@example.com")
        self.assertEqual(self.user3.email, "user3@example.com")

    def test_add_task_with_assigned_user_email(self):
        """
        Test adding a task and checking the assigned user's email.
        """
        task = Task.objects.create(
            user=self.user1,
            title="Task with Email",
            description="Task assigned to user2 with email.",
            priority="High",
            due_date=timezone.now().date() + timedelta(days=5),
            status="backlog",
            project=self.project,
            assigned_to=self.user2
        )

        self.assertEqual(task.assigned_to.email, "user2@example.com")
        self.assertEqual(task.assigned_to.username, "user2")

    def test_project_team_member_emails(self):
        """
        Test that team members' emails are accessible in the project.
        """
        team_emails = list(self.project.team_members.values_list("email", flat=True))
        self.assertIn("user2@example.com", team_emails)
        self.assertIn("user3@example.com", team_emails)

    def test_task_dependencies_with_emails(self):
        """
        Test task dependencies and verify user emails for dependent tasks.
        """
        task1 = Task.objects.create(
            user=self.user1,
            title="Task 1",
            description="First task",
            priority="Medium",
            due_date=timezone.now().date() + timedelta(days=3),
            status="backlog",
            project=self.project
        )
        task2 = Task.objects.create(
            user=self.user1,
            title="Task 2",
            description="Second task dependent on Task 1",
            priority="High",
            due_date=timezone.now().date() + timedelta(days=7),
            status="backlog",
            project=self.project,
            assigned_to=self.user3
        )

        task2.dependencies.add(task1)

        self.assertEqual(task2.dependencies.count(), 1)
        self.assertIn(task1, task2.dependencies.all())
        self.assertEqual(task2.assigned_to.email, "user3@example.com")
