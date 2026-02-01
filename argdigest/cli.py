import argparse
import importlib
import inspect
import sys
from typing import Any

def audit_module(module_name: str):
    """
    Imports a module and prints the digestion plan for all decorated functions.
    """
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        print(f"Error: Could not import module '{module_name}': {e}")
        return

    print(f"\nAudit Report for module: {module_name}")
    print("=" * (22 + len(module_name)))

    found = False
    for name, obj in inspect.getmembers(module):
        if hasattr(obj, "digestion_plan"):
            found = True
            plan = obj.digestion_plan
            print(f"\nFunction: {name}")
            print(f"  Strictness: {plan.strictness}")
            print(f"  Skip Param: {plan.skip_param}")
            print(f"  Profiling:  {plan.profiling}")
            
            if plan.digesters:
                print(f"  Argument Digesters: {list(plan.digesters.keys())}")
            
            if plan.pipeline_targets:
                print(f"  Pipeline Targets:")
                for arg, cfg in plan.pipeline_targets.items():
                    kind = cfg.get("kind")
                    rules = cfg.get("rules", [])
                    print(f"    - {arg}: kind='{kind}', rules={rules}")

    if not found:
        print("\nNo functions with @digest found in this module.")

def main():
    parser = argparse.ArgumentParser(prog="argdigest", description="ArgDigest CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Audit validation rules in a module")
    audit_parser.add_argument("module", help="Module or package name to audit (e.g. mylib.api)")

    args = parser.parse_args()

    if args.command == "audit":
        audit_module(args.module)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
