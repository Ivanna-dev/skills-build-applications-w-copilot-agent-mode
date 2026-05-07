from django.core.management.base import BaseCommand
from django.conf import settings

from django.db import connections

# Sample data for superheroes, teams, activities, leaderboard, and workouts
def get_sample_data():
    users = [
        {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
        {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
        {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
        {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
        {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
        {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
    ]
    teams = [
        {"name": "Marvel", "members": ["ironman@marvel.com", "cap@marvel.com", "widow@marvel.com"]},
        {"name": "DC", "members": ["superman@dc.com", "batman@dc.com", "wonderwoman@dc.com"]},
    ]
    activities = [
        {"user_email": "superman@dc.com", "activity": "Flying", "duration": 60},
        {"user_email": "batman@dc.com", "activity": "Martial Arts", "duration": 45},
        {"user_email": "ironman@marvel.com", "activity": "Flight Suit Training", "duration": 50},
    ]
    leaderboard = [
        {"user_email": "superman@dc.com", "points": 100},
        {"user_email": "ironman@marvel.com", "points": 90},
        {"user_email": "batman@dc.com", "points": 80},
    ]
    workouts = [
        {"name": "Strength Training", "suggested_for": ["superman@dc.com", "cap@marvel.com"]},
        {"name": "Agility Drills", "suggested_for": ["batman@dc.com", "widow@marvel.com"]},
    ]
    return users, teams, activities, leaderboard, workouts

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Ensure the database connection is established
        conn = connections['default']
        conn.ensure_connection()
        db = conn.connection.client['octofit_db']
        users, teams, activities, leaderboard, workouts = get_sample_data()

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert data
        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        # Create unique index on email for users
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
