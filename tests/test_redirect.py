"""Tests for GET / redirect endpoint"""

import pytest


class TestRedirectEndpoint:
    """Tests for root endpoint redirect functionality"""

    def test_root_endpoint_returns_redirect_status(self, client):
        """
        Test that GET / returns a redirect response.
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: Make GET request to root endpoint with follow_redirects=False
        - Assert: Verify redirect status code (307 or 302)
        """
        # Arrange
        # (client already prepared by fixture)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        # FastAPI RedirectResponse returns 307 (Temporary Redirect)
        assert response.status_code == 307

    def test_root_endpoint_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html.
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: Make GET request to root with follow_redirects=True to get final destination
        - Assert: Verify Location header points to /static/index.html
        """
        # Arrange
        # (client already prepared by fixture)

        # Act
        response_no_follow = client.get("/", follow_redirects=False)

        # Assert
        assert "location" in response_no_follow.headers
        assert response_no_follow.headers["location"] == "/static/index.html"

    def test_root_endpoint_redirect_location_header(self, client):
        """
        Test that Location header is properly set on redirect.
        AAA Pattern:
        - Arrange: Define expected redirect destination
        - Act: GET /, capture headers
        - Assert: Verify Location header matches expected value
        """
        # Arrange
        expected_location = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers.get("location") == expected_location

    def test_root_endpoint_no_content_in_redirect(self, client):
        """
        Test that redirect response has no content body.
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: GET / with follow_redirects=False
        - Assert: Verify response has no body content
        """
        # Arrange
        # (client already prepared by fixture)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        # Redirect responses typically have empty body
        assert len(response.content) == 0 or response.json() == {}
