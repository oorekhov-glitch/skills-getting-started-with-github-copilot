"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest


class TestSignupForActivity:
    """Tests for activity signup functionality"""

    def test_signup_valid_email_successful(self, client):
        """
        Test successful signup with valid activity name and email.
        AAA Pattern:
        - Arrange: Prepare valid activity name and new email
        - Act: POST to signup endpoint
        - Assert: Verify 200 status and participant added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_multiple_emails_all_added(self, client):
        """
        Test that multiple different emails can successfully sign up.
        AAA Pattern:
        - Arrange: Prepare multiple email addresses
        - Act: Sign up each email for the same activity
        - Assert: Verify all participants added and response messages correct
        """
        # Arrange
        activity_name = "Programming Class"
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]

        # Act & Assert for each signup
        for email in emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200
            assert email in response.json()["message"]

        # Verify all participants were added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        for email in emails:
            assert email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Test that signup to a non-existent activity returns 404 error.
        AAA Pattern:
        - Arrange: Prepare invalid activity name and valid email
        - Act: POST to signup endpoint with invalid activity
        - Assert: Verify 404 status and "Activity not found" error message
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert "Activity not found" in response_data["detail"]

    def test_signup_duplicate_email_returns_400(self, client):
        """
        Test that signing up with duplicate email returns 400 error.
        AAA Pattern:
        - Arrange: Get an already-registered email from an activity
        - Act: Try to sign up that email again for the same activity
        - Assert: Verify 400 status and appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        # michael@mergington.edu is already in Chess Club
        email = "michael@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert "already signed up" in response_data["detail"]

    def test_signup_same_email_different_activities_allowed(self, client):
        """
        Test that the same email can sign up for different activities.
        AAA Pattern:
        - Arrange: Prepare email and two different activities
        - Act: Sign up email for both activities
        - Assert: Verify both signups successful and email appears in both activities
        """
        # Arrange
        email = "multi@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Art Club"

        # Act
        response1 = client.post(f"/activities/{activity1}/signup?email={email}")
        response2 = client.post(f"/activities/{activity2}/signup?email={email}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_signup_missing_email_parameter_returns_error(self, client):
        """
        Test that signup without email parameter returns error.
        AAA Pattern:
        - Arrange: Prepare activity but no email parameter
        - Act: POST to signup endpoint without email query parameter
        - Assert: Verify error (422 Unprocessable Entity for missing required param)
        """
        # Arrange
        activity_name = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity_name}/signup")

        # Assert
        assert response.status_code == 422  # FastAPI returns 422 for missing required params
        response_data = response.json()
        assert "detail" in response_data

    def test_signup_whitespace_email_treated_as_different(self, client):
        """
        Test that emails with different whitespace are treated as different.
        AAA Pattern:
        - Arrange: Prepare two similar emails (one with space)
        - Act: Sign up both emails for same activity
        - Assert: Verify both signups succeed (treated as different)
        """
        # Arrange
        activity_name = "Programming Class"
        email1 = "student@mergington.edu"
        email2 = " student@mergington.edu"  # Leading space

        # Act
        response1 = client.post(f"/activities/{activity_name}/signup?email={email1}")
        response2 = client.post(f"/activities/{activity_name}/signup?email={email2}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
