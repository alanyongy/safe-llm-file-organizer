"""
Main orchestration entrypoint for the LLM File Organizer system.

Coordinates the full organization workflow:
- Collect user inputs
- Scan the target directory
- Generate an organization plan using the LLM
- Validate the generated plan
- Execute approved filesystem operations
"""

from planner import generate_plan
from validator import validate_plan
from actions import list_files, move_item, create_folder

def execute_plan(plan):
    """
    Executes a validated filesystem plan.

    Each action is mapped to a deterministic filesystem
    operation exposed by the actions module.

    Args:
        plan: List of validated action dictionaries.
    """

    for action in plan:
        action_type = action["action"]

        if action_type == "move_item":
            move_item(
                action["source"],
                action["destination_folder"]
            )

        elif action_type == "create_folder":
            create_folder(action["path"])

def main():
    """
    Runs the interactive file organization workflow.

    Prompts the user for:
    - A root directory to organize
    - An organization goal

    The directory contents are scanned, an execution plan is
    generated and validated, then the user is asked to approve
    execution before any filesystem modifications occur.
    """

    # User inputs
    root_dir = input("Enter directory to organize (e.g. C:\\Downloads):\n").strip()

    default_goal = "Categorize and place the following folders and files into new folders at the root directory."
    goal = input(f"Enter goal: (Leave empty for default: \"{default_goal}\")\n").strip()

    if goal == "":
        goal = default_goal

    # Scan files
    files = list_files(root_dir)

    print("\nDetected files:")
    for f in files:
        print(" -", f)

    # Generate plan
    print("\nAwaiting LLM response...")
    plan = generate_plan(files, root_dir, goal)

    print("\nGenerated Plan:")
    for action in plan:
        print(action)

    # Validate plan
    validated_plan = validate_plan(plan, root_dir)

    # Confirm execution
    confirm = input("\nExecute this plan? (y/n): ").strip().lower()

    if confirm != "y":
        print("Aborted.")
        return

    print("\nExecuting Plan...")

    execute_plan(validated_plan)

    print("\nDone.")


if __name__ == "__main__":
    main()