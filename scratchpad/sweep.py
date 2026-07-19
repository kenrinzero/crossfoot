import sys
import glob
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from reconcile import check

def main():
    files = sorted(glob.glob(str(root / "tables/**/*.cells.json"), recursive=True))
    print(f"Checking {len(files)} files...")
    errors = 0
    for f in files:
        rel_path = Path(f).relative_to(root)
        try:
            violations, warnings = check(f)
            if violations:
                print(f"RED   {rel_path}: {violations}")
                errors += 1
            else:
                # print(f"GREEN {rel_path}")
                pass
        except Exception as e:
            print(f"ERROR {rel_path}: {e}")
            errors += 1
    if errors:
        print(f"Sweep failed with {errors} errors.")
        sys.exit(1)
    print("ALL GREEN!")

if __name__ == "__main__":
    main()
