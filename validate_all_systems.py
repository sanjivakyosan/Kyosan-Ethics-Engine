#!/usr/bin/env python3
"""
Kyosan Ethics Engine - System Validation Script
Verifies that all systems are active, implemented, and run in the pipeline at level "detailed".

©sanjivakyosan
Created by Sanjiva Kyosan

Run from project root: python validate_all_systems.py
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    errors = []
    print("=" * 60)
    print("Kyosan Ethics Engine - All Systems Validation")
    print("=" * 60)

    # 1. Load integrator
    try:
        from EthicalSystemIntegrator import EthicalSystemIntegrator
        integrator = EthicalSystemIntegrator()
    except Exception as e:
        print(f"FAIL: Could not initialize EthicalSystemIntegrator: {e}")
        return 1

    status = integrator.get_system_status()
    systems_dict = integrator.systems
    expected_count = len(systems_dict)

    # 2. Verify no system has import/init error
    failed = [name for name, s in status.items() if s not in ("active", "available")]
    if failed:
        for name in failed:
            errors.append(f"System {name}: status = {status[name]}")
        print(f"\nFAIL: {len(failed)} system(s) did not load correctly:")
        for e in errors:
            print(f"  - {e}")
    else:
        print(f"\n✓ All {expected_count} systems loaded (active or available)")

    # 3. Run pipeline at "detailed" and verify all systems appear in active_systems
    result = integrator.process_input("What is ethics?", {}, "detailed")
    active = result.get("active_systems", [])
    print(f"\n  Pipeline result status: {result.get('status')}; active_systems count: {len(active)}")

    # At detailed: PrincipleBasedEthicalProcessor + all integrator systems
    expected_set = set(systems_dict.keys()) | {"PrincipleBasedEthicalProcessor"}
    missing = expected_set - set(active)
    if missing:
        errors.append(f"Pipeline at 'detailed' missing from active_systems: {sorted(missing)}")
        print(f"\nFAIL: At processing_level='detailed', {len(missing)} system(s) not in active_systems:")
        for m in sorted(missing):
            print(f"  - {m}")
    else:
        print(f"✓ Pipeline at 'detailed': all {len(active)} systems active (43 = 42 integrator + PrincipleBasedEthicalProcessor)")

    if result.get("status") not in ("complete", "processed", "approved"):
        print(f"  Note: processing status = {result.get('status')}")

    # 4. Summary
    print("\n" + "-" * 60)
    if errors:
        print("VALIDATION: FAILED")
        print(f"  {len(errors)} issue(s) found.")
        return 1
    print("VALIDATION: PASSED")
    print(f"  - {expected_count} systems in integrator: all loaded")
    print(f"  - At processing_level='detailed': {len(active)} systems active in pipeline")
    print("-" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
