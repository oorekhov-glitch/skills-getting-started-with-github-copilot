"""Tests for GET /activities endpoint"""

import pytest


class TestGetActivities:
    """Tests for retrieving all activities"""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities.
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: Make GET request to /activities endpoint
        - Assert: Verify status code 200 and all 9 activities present
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Club",
            "Drama Club",
            "Science Club",
            "Academic Debate"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == 9
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_response_structure(self, client):
        """
        Test that each activity in the response has the correct structure.
        AAA Pattern:
        - Arrange: Define expected keys for an activity
        - Act: Make GET request and examine response structure
        - Assert: Verify each activity has required fields
        """
        # Arrange
        expected_keys = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            assert set(activity_data.keys()) == expected_keys
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
            # All participants should be strings (email addresses)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)

    def test_get_activities_initial_participants(self, client):
        """
        Test that activities have the correct initial participants.
        AAA Pattern:
        - Arrange: Define expected initial state
        - Act: Fetch activities and check specific activity participants
        - Assert: Verify each activity has expected starting participants
        """
        # Arrange
        # Chess Club should have 2 participants initially
        # Programming Class should have 2 participants initially
        expected_initial_state = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2,
            "Basketball Team": 1,
            "Tennis Club": 2,
            "Art Club": 1,
            "Drama Club": 2,
            "Science Club": 1,
            "Academic Debate": 2
        }

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, expected_count in expected_initial_state.items():
            actual_count = len(activities[activity_name]["participants"])
            assert actual_count == expected_count, \
                f"{activity_name} expected {expected_count} participants, got {actual_count}"
