import os
import subprocess
import sys
PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
MODULES = {
    "1": (
        "Registry Information Collection",
        "registry_collection.py"
    ),
    "2": (
        "Registry Baseline Creation",
        "registry_baseline.py"
    ),
    "3": (
        "Registry Change Detection",
        "registry_detection.py"
    ),
    "4": (
        "Registry Baseline Comparison",
        "registry_comparison.py"
    ),
    "5": (
        "Unauthorized Modification Detection",
        "unauthorized_detection.py"
    ),
    "6": (
        "Registry Alert Generation",
        "registry_alert.py"
    ),
    "7": (
        "Registry Log and Report Generation",
        "registry_report.py"
    )
}
def execute_module(filename):
    file_path = os.path.join(SRC_DIR, filename)
    if not os.path.isfile(file_path):
        print("Error: Module file not found:", filename)
        return
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            cwd=PROJECT_DIR,
            check=False
        )
        if result.returncode == 0:
            print("Module execution completed.")
        else:
            print(
                "Module exited with code:",
                result.returncode
            )
    except OSError as error:
        print("Module execution error:", error)
def display_menu():
    print("\n" + "=" * 48)
    print("WINDOWS REGISTRY CHANGE MONITORING SYSTEM")
    print("=" * 48)
    for option, (title, filename) in MODULES.items():
        print(f"{option}. {title}")
    print("8. Run Monitoring Modules")
    print("0. Exit")
def run_monitoring():
    # Baseline creation is a separate initial setup step.
    # Do not recreate the baseline during routine checks.
    for option in ("1", "3", "4", "5", "6", "7"):
        title, filename = MODULES[option]
        print(f"\nExecuting: {title}")
        execute_module(filename)
def main():
    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip()
        if choice == "0":
            print("Exiting Registry Monitoring System.")
            break
        elif choice == "8":
            run_monitoring()
        elif choice in MODULES:
            title, filename = MODULES[choice]
            print(f"\nExecuting: {title}")
            execute_module(filename)
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
