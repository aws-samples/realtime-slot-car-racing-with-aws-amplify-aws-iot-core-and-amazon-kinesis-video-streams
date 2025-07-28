"""
Run all test suites
"""
import sys
sys.path.append('..')

import asyncio
from test_byte_helper import run_all_tests as test_byte_helper
from test_models import run_all_tests as test_models
from test_race_controller import run_all_tests as test_race_controller
from test_security import run_all_tests as test_security

async def main():
    """Run all test suites"""
    print("🧪 Running MicroPython Race Controller Test Suite")
    print("=" * 50)
    
    results = []
    
    # Run synchronous tests
    print("\n1. ByteHelper Tests")
    results.append(test_byte_helper())
    
    print("\n2. Models Tests")
    results.append(test_models())
    
    # Run asynchronous tests
    print("\n3. RaceController Tests")
    results.append(await test_race_controller())
    
    print("\n4. Security Tests")
    results.append(test_security())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    test_names = ["ByteHelper", "Models", "RaceController", "Security"]
    passed = sum(results)
    total = len(results)
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed! Code is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)