"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

import pytest


class TestRemoveParticipant:
    """Tests for removing participants from activities"""

    def test_remove_existing_participant_successful(self, client):
        """
        Test successful removal of an existing participant.
        AAA Pattern:
        - Arrange: Get existing participant email from an activity
        - Act: DELETE request to remove participant
        - Assert: Verify 200 status and participant removed from activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == f"Unregistered {email} from {activity_name}"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_remove_multiple_participants_from_same_activity(self, client):
        """
        Test removing multiple different participants from the same activity.
        AAA Pattern:
        - Arrange: Identify multiple participants in an activity
        - Act: Remove each participant sequentially
        - Assert: Verify each removal successful and count decreases
        """
        # Arrange
        activity_name = "Chess Club"
        emails_to_remove = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        activities_before = client.get("/activities").json()
        initial_count = len(activities_before[activity_name]["participants"])

        # Act & Assert
        for i, email in enumerate(emails_to_remove):
            response = client.delete(f"/activities/{activity_name}/participants/{email}")
            assert response.status_code == 200
            
            # Verify count decreased
            activities_after = client.get("/activities").json()
            current_count = len(activities_after[activity_name]["participants"])
            assert current_count == initial_count - (i + 1)

    def test_remove_nonexistent_activity_returns_404(self, client):
        """
        Test that removing from a non-existent activity returns 404.
        AAA Pattern:
        - Arrange: Prepare invalid activity name and email
        - Act: DELETE request with invalid activity
        - Assert: Verify 404 status and error message
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert "Activity not found" in response_data["detail"]

    def test_remove_participant_not_in_activity_returns_400(self, client):
        """
        Test that removing a non-participant returns 400 error.
        AAA Pattern:
        - Arrange: Prepare email not in activity and activity name
        - Act: DELETE request for non-participant
        - Assert: Verify 400 status and "not signed up" error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notstudent@mergington.edu"  # Not in Chess Club

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert "not signed up" in response_data["detail"]

    def test_remove_participant_add_back_separately(self, client):
        """
        Test that a participant can be removed and then added back.
        AAA Pattern:
        - Arrange: Get existing participant
        - Act: Remove participant, then sign them up again
        - Assert: Verify removal and re-addition both successful
        """
        # Arrange
        activity_name = "Programming Class"
        email = "student@example.com"
        
        # Sign up first
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200

        # Act - Remove
        remove_response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert remove_response.status_code == 200

        # Assert - Verify removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]

        # Act - Add back
        signup_again_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_again_response.status_code == 200

        # Assert - Verify added back
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_remove_does_not_affect_other_activities(self, client):
        """
        Test that removing from one activity doesn't affect other activities.
        AAA Pattern:
        - Arrange: Add same email to two activities, then remove from one
        - Act: Remove from first activity
        - Assert: Verify removed from first but still in second
        """
        # Arrange
        activity1 = "Drama Club"
        activity2 = "Science Club"
        email = "drama_science@mergington.edu"
        
        # Add to both activities
        client.post(f"/activities/{activity1}/signup?email={email}")
        client.post(f"/activities/{activity2}/signup?email={email}")

        # Act - Remove from first activity
        response = client.delete(f"/activities/{activity1}/participants/{email}")

        # Assert
        assert response.status_code == 200
        activities = client.get("/activities").json()
        assert email not in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_remove_same_participant_twice_returns_400(self, client):
        """
        Test that removing the same participant twice returns error on second attempt.
        AAA Pattern:
        - Arrange: Get a participant to remove
        - Act: Remove them once, then try again
        - Assert: First removal succeeds, second returns 400
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "noah@mergington.edu"

        # Act - First removal
        response1 = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert - First removal succeeds
        assert response1.status_code == 200

        # Act - Second removal attempt
        response2 = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert - Second removal fails
        assert response2.status_code == 400
        response_data = response2.json()
        assert "not signed up" in response_data["detail"]
