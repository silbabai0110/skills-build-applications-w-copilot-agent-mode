from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users (super heroes)
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "marvel"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Create teams
        teams = [
            {"name": "marvel", "members": [u["email"] for u in users if u["team"] == "marvel"]},
            {"name": "dc", "members": [u["email"] for u in users if u["team"] == "dc"]},
        ]
        db.teams.insert_many(teams)

        # Create activities
        activities = [
            {"user_email": "ironman@marvel.com", "activity": "Running", "duration": 30},
            {"user_email": "batman@dc.com", "activity": "Cycling", "duration": 45},
            {"user_email": "superman@dc.com", "activity": "Swimming", "duration": 60},
        ]
        db.activities.insert_many(activities)

        # Create leaderboard
        leaderboard = [
            {"team": "marvel", "points": 120},
            {"team": "dc", "points": 150},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Create workouts
        workouts = [
            {"name": "Morning Cardio", "type": "Cardio", "duration": 30},
            {"name": "Strength Training", "type": "Strength", "duration": 45},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data'))
