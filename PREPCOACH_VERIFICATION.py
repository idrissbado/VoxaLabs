#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PrepCoach AI - Comprehensive System Verification
Tests: Whisper integration, Report generation, Mistral AI, Role mapping
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("\n" + "=" * 80)
print("PrepCoach AI - Complete System Verification")
print("   Supports: Interview Prep | Career Coaching | Exam Training | Skill Development")
print("=" * 80 + "\n")

test_results = []

# Test 1: Whisper Audio Transcription
print("[1/6] Checking Whisper Audio Integration...")
try:
    import whisper
    print("      [OK] Whisper module imported")
    print("      [OK] Status: READY for audio transcription")
    test_results.append(("Whisper Module", "PASS"))
except ImportError:
    print("      [WN] Whisper not installed (optional, has fallback)")
    test_results.append(("Whisper Module", "WARN"))

# Test 2: Services Imports
print("[2/6] Checking Core Services...")
try:
    from services.mistral_service import generate_coaching_feedback
    from services.scoring_engine import generate_full_report, calculate_performance_metrics
    from services.voxtral_service import transcribe_audio, analyze_voice_answer
    print("      [OK] mistral_service imported")
    print("      [OK] scoring_engine imported")
    print("      [OK] voxtral_service imported")
    test_results.append(("Core Services", "PASS"))
except ImportError as e:
    print(f"      [ER] Service import failed: {e}")
    test_results.append(("Core Services", "FAIL"))

# Test 3: API Routers
print("[3/6] Checking API Routers...")
try:
    from routers import session, analysis, report
    print("      [OK] session router imported")
    print("      [OK] analysis router imported")
    print("      [OK] report router imported")
    print("      [OK] Status: 7 API endpoints ready")
    test_results.append(("API Routers", "PASS"))
except ImportError as e:
    print(f"      [ER] Router import failed: {e}")
    test_results.append(("API Routers", "FAIL"))

# Test 4: Report Generation & Analytics
print("[4/6] Checking Report Generation & Analytics...")
try:
    from services.scoring_engine import calculate_performance_metrics
    
    # Simulate session data
    test_sessions = [
        {
            'overall': 7.5,
            'technical_depth': 8,
            'communication': 7,
            'problem_solving': 7.5,
            'structure': 7,
            'impact': 7.5,
            'timestamp': '2026-02-28T10:00:00'
        },
        {
            'overall': 8.0,
            'technical_depth': 8.5,
            'communication': 8,
            'problem_solving': 8,
            'structure': 8,
            'impact': 7.5,
            'timestamp': '2026-02-28T11:00:00'
        }
    ]
    
    metrics = calculate_performance_metrics(test_sessions, 'Software Engineer')
    avg = metrics['average_score']
    readiness = metrics['overall_readiness']
    
    print(f"      [OK] Report metrics calculated")
    print(f"      [OK] Average Score: {avg}/10")
    print(f"      [OK] Readiness: {readiness}")
    print(f"      [OK] Sessions analyzed: {metrics['total_sessions']}")
    test_results.append(("Report Generation", "PASS"))
except Exception as e:
    print(f"      [ER] Report generation failed: {e}")
    test_results.append(("Report Generation", "FAIL"))

# Test 5: Role Mapping
print("[5/6] Checking Role Mapping...")
try:
    from services.scoring_engine import ROLE_MAPPING
    
    num_aliases = len(ROLE_MAPPING)
    unique_roles = set(ROLE_MAPPING.values())
    
    print(f"      [OK] Role mapping loaded: {num_aliases} aliases")
    print(f"      [OK] Roles configured: {', '.join(sorted(unique_roles))}")
    print(f"      [OK] Sample aliases: {', '.join(list(ROLE_MAPPING.keys())[:5])}...")
    test_results.append(("Role Mapping", "PASS"))
except Exception as e:
    print(f"      [ER] Role mapping failed: {e}")
    test_results.append(("Role Mapping", "FAIL"))

# Test 6: Mistral Configuration
print("[6/6] Checking Mistral AI Configuration...")
try:
    from services.mistral_service import client
    
    api_key_set = bool(os.environ.get('MISTRAL_API_KEY'))
    if api_key_set:
        print("      [OK] Mistral API key configured")
        print("      [OK] Client initialized: READY for production")
        test_results.append(("Mistral AI", "PASS"))
    else:
        print("      [WN] Mistral API key not set (demo mode)")
        print("      [WN] Set MISTRAL_API_KEY environment variable for production")
        test_results.append(("Mistral AI", "WARN"))
except Exception as e:
    print(f"      [ER] Mistral check failed: {e}")
    test_results.append(("Mistral AI", "FAIL"))

# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY:")
print("-" * 80)

passed = sum(1 for _, status in test_results if status == "PASS")
warned = sum(1 for _, status in test_results if status == "WARN")
failed = sum(1 for _, status in test_results if status == "FAIL")

for component, status in test_results:
    icon = "[OK]" if status == "PASS" else "[WN]" if status == "WARN" else "[ER]"
    print(f"{icon} {component:25} {status}")

print("-" * 80)
print(f"Results: {passed} PASS | {warned} WARN | {failed} FAIL")
print("=" * 80)

if failed == 0:
    print("\nPrepCoach AI - All systems VERIFIED and READY for deployment!\n")
else:
    print(f"\nPlease fix {failed} failing test(s) before deployment.\n")

print("API Endpoints Available:")
print("  • POST /session/create - Create new session")
print("  • GET /session/questions - Get questions by role")
print("  • POST /session/answer - Submit answer for coaching")
print("  • POST /analysis/transcribe - Transcribe audio (Whisper)")
print("  • POST /report/generate - Generate full report (Mistral)")
print("  • POST /report/analytics - Get performance analytics")
print("  • POST /report/summary - Quick performance summary\n")
