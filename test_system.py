#!/usr/bin/env python3
"""
VoiceCoach AI - Quick Test Script
Verify all components are working correctly
"""

import requests
import json
import sys

# Test configuration
BACKEND_URL = "http://localhost:8000"
TEST_ROLE = "Software Engineer"
TEST_QUESTION = "Tell me about yourself and why you want this role."
TEST_ANSWER = """
So, I'm a software engineer with 8 years of experience in full-stack development.
I've worked at several companies where I led teams and shipped products that impacted millions of users.
What excites me about this role is the opportunity to work on challenging problems with smart people.
I believe my background in scalable systems and team leadership would be a great fit.
"""

def test_health():
    """Test if backend is running"""
    print("\n🏥 Testing Backend Health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running: {data['service']}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_session_creation():
    """Test session creation"""
    print("\n📋 Testing Session Creation...")
    try:
        payload = {
            "role": TEST_ROLE,
            "user_id": "test-user"
        }
        response = requests.post(f"{BACKEND_URL}/session/create", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Session created: {data['session_id'][:8]}...")
            print(f"   Role: {data['role']}")
            print(f"   Questions: {len(data['questions'])}")
            return data['session_id'], data['questions'][0]
        else:
            print(f"❌ Failed to create session: {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        return None, None

def test_text_analysis(question):
    """Test text analysis"""
    print("\n🔍 Testing Text Analysis...")
    try:
        payload = {
            "transcript": TEST_ANSWER,
            "question": question,
            "role": TEST_ROLE,
            "session_id": "test"
        }
        response = requests.post(f"{BACKEND_URL}/analysis/text", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis completed")
            
            if 'scores' in data:
                print("\n   📊 Scores:")
                for metric, score in data['scores'].items():
                    print(f"      {metric.title()}: {score}/10")
            
            if 'overall' in data:
                print(f"\n   ⭐ Overall: {data['overall']}/10")
            
            if 'tip' in data:
                print(f"\n   💡 Tip: {data['tip']}")
            
            return True
        else:
            print(f"❌ Analysis failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("VoiceCoach AI - System Check")
    print("="*50)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Backend is not running. Please start it with:")
        print("   cd backend && python main.py")
        sys.exit(1)
    
    # Test 2: Session creation
    session_id, question = test_session_creation()
    if not session_id:
        print("\n❌ Session creation failed")
        sys.exit(1)
    
    # Test 3: Text analysis
    if not test_text_analysis(question):
        print("\n❌ Analysis failed")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("✅ All Tests Passed! System is Ready")
    print("="*50)
    print("\nFrontend: http://localhost:3000")
    print("Backend API: http://localhost:8000")
    print("\nStart your session and begin practicing! 🎤✨\n")

if __name__ == "__main__":
    main()
