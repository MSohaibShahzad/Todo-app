#!/usr/bin/env python3
"""
Test Better-Auth endpoints

This script tests the authentication endpoints by making HTTP requests
to the Better-Auth server and validating responses.

Usage:
    python test_auth.py --base-url http://localhost:3001
    python test_auth.py --base-url https://your-auth-service.com --email test@example.com
"""

import argparse
import requests
import json
from typing import Dict, Optional

class AuthTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.cookies: Dict[str, str] = {}

    def test_health(self) -> bool:
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False

    def test_signup(self, email: str, password: str, name: str, custom_data: Optional[Dict] = None) -> bool:
        """Test user signup"""
        try:
            payload = {
                "email": email,
                "password": password,
                "name": name,
            }

            if custom_data:
                payload.update(custom_data)

            response = self.session.post(
                f"{self.base_url}/api/auth/sign-up/email",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                print(f"✅ Signup successful")
                print(f"   User ID: {data.get('user', {}).get('id', 'N/A')}")
                print(f"   Email: {data.get('user', {}).get('email', 'N/A')}")

                # Save cookies for subsequent requests
                self.cookies = dict(response.cookies)
                return True
            else:
                print(f"❌ Signup failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Signup error: {e}")
            return False

    def test_signin(self, email: str, password: str) -> bool:
        """Test user signin"""
        try:
            payload = {
                "email": email,
                "password": password,
            }

            response = self.session.post(
                f"{self.base_url}/api/auth/sign-in/email",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Signin successful")
                print(f"   User ID: {data.get('user', {}).get('id', 'N/A')}")
                print(f"   Email: {data.get('user', {}).get('email', 'N/A')}")

                # Save cookies
                self.cookies = dict(response.cookies)
                return True
            else:
                print(f"❌ Signin failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Signin error: {e}")
            return False

    def test_get_session(self) -> bool:
        """Test getting current session"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/auth/session",
                cookies=self.cookies
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Session retrieved")
                print(f"   User: {data.get('user', {}).get('email', 'N/A')}")
                print(f"   Session ID: {data.get('session', {}).get('id', 'N/A')}")
                return True
            else:
                print(f"❌ Get session failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Get session error: {e}")
            return False

    def test_jwt_generation(self) -> Optional[str]:
        """Test JWT token generation"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/auth/jwt",
                cookies=self.cookies
            )

            if response.status_code == 200:
                data = response.json()
                token = data.get('token')
                print(f"✅ JWT generated successfully")
                print(f"   Token: {token[:50]}...")
                return token
            else:
                print(f"❌ JWT generation failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ JWT generation error: {e}")
            return None

    def test_signout(self) -> bool:
        """Test user signout"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/sign-out",
                cookies=self.cookies
            )

            if response.status_code == 200:
                print(f"✅ Signout successful")
                self.cookies = {}
                return True
            else:
                print(f"❌ Signout failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Signout error: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Test Better-Auth endpoints")
    parser.add_argument("--base-url", default="http://localhost:3001", help="Base URL of auth service")
    parser.add_argument("--email", default="test@example.com", help="Test email")
    parser.add_argument("--password", default="TestPassword123!", help="Test password")
    parser.add_argument("--name", default="Test User", help="Test user name")
    parser.add_argument("--custom-fields", default="", help="Custom fields as JSON")

    args = parser.parse_args()

    # Parse custom fields
    custom_data = None
    if args.custom_fields:
        try:
            custom_data = json.loads(args.custom_fields)
        except json.JSONDecodeError:
            print("❌ Invalid JSON for custom fields")
            return

    tester = AuthTester(args.base_url)

    print(f"🧪 Testing Better-Auth at {args.base_url}\n")
    print("=" * 60)

    # Run tests
    print("\n1. Testing health endpoint...")
    if not tester.test_health():
        print("\n❌ Health check failed. Is the server running?")
        return

    print("\n2. Testing signup...")
    if not tester.test_signup(args.email, args.password, args.name, custom_data):
        print("\n⚠️  Signup failed (user might already exist). Trying signin...")
        print("\n3. Testing signin...")
        if not tester.test_signin(args.email, args.password):
            print("\n❌ Both signup and signin failed. Stopping tests.")
            return
    else:
        print("\n   Note: Signup auto-signs in, skipping separate signin test")

    print("\n4. Testing session retrieval...")
    tester.test_get_session()

    print("\n5. Testing JWT generation...")
    tester.test_jwt_generation()

    print("\n6. Testing signout...")
    tester.test_signout()

    print("\n" + "=" * 60)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()
