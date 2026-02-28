#!/usr/bin/env python3
"""PrepCoach AI - Backend Verification Script"""

import os
import sys

print("\n" + "=" * 70)
print("🎓 PrepCoach AI - System Verification (Interview/Career/Exam Prep)")
print("=" * 70 + "\n")

# Test 1: Check Whisper integration
print("[1] Checking Whisper Integration...")
try:
    import whisper
    print("    ✓ Whisper module imported successfully")
except ImportError as e:
    print(f"    ✗ Whisper import failed: {e}")

# Test 2: Check services imports
print("[2] Checking Services Imports...")
try:
    from services.mistral_service import analyze_interview_answer
    from services.scoring_engine import generate_full_report, calculate_performance_metrics
    from services.voxtral_service import transcribe_audio
    print("    ✓ All services imported successfully")
except ImportError as e:
    print(f"    ✗ Service import failed: {e}")

# Test 3: Check routers
print("[3] Checking Routers...")
try:
    from routers import session, analysis, report
    print("    ✓ All routers imported successfully")
except ImportError as e:
    print(f"    ✗ Router import failed: {e}")

# Test 4: Check report functionality
print("[4] Checking Report Generation Functions...")
try:
    from services.scoring_engine import calculate_performance_metrics
    test_sessions = [
        {
            'overall': 7.5,
            'technical_depth': 8,
            'communication': 7,
            'problem_solving': 7.5,
            'structure': 7,
            'impact': 7.5
        }
    ]
    metrics = calculate_performance_metrics(test_sessions, 'Software Engineer')
    avg_score = metrics['average_score']
    readiness = metrics['overall_readiness']
    print(f"    ✓ Report metrics: avg_score={avg_score}, readiness={readiness}")
except Exception as e:
    print(f"    ✗ Report calculation failed: {e}")

# Test 5: Check role mapping
print("[5] Checking Role Mapping...")
try:
    from services.scoring_engine import ROLE_MAPPING
    num_roles = len(ROLE_MAPPING)
    unique_roles = set(ROLE_MAPPING.values())
    print(f"    ✓ Role mapping loaded: {num_roles} aliases configured")
    print(f"    Roles: {', '.join(sorted(unique_roles))}")
except Exception as e:
    print(f"    ✗ Role mapping failed: {e}")

# Test 6: Check Mistral client
print("[6] Checking Mistral Configuration...")
try:
    from services.mistral_service import client
    api_key_set = bool(os.environ.get('MISTRAL_API_KEY'))
    if api_key_set:
        print("    ✓ Mistral API key is configured")
    else:
        print("    ⚠ Mistral API key not set (demo mode)")
except Exception as e:
    print(f"    ✗ Mistral check failed: {e}")

print("\n" + "=" * 70)
print("✅ VoiceCoach AI - Backend Verification Complete")
print("=" * 70 + "\n")
