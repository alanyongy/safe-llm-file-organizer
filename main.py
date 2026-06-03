from planner import generate_plan
from validator import validate_plan
from actions import list_files, move_item, create_folder


def execute_plan(plan):
    """
    Executes a plan using deterministic filesystem tools.
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
    Main orchestration loop for the LLM File Organizer system.
    """

    # Step 1: user inputs
    root_dir = r"E:\\Projects\\LLM File Organizer\\TestSample:"
    #root_dir = input("Enter root directory (e.g. E:\\Downloads): ").strip()
    default_goal = "Categorize and place the following folders and files into new folders at the root directory."
    goal = goal("Enter goal (leave empty for default: " + default_goal + ")").strip()

    if goal == "":
        goal = default_goal

    # Step 2: scan files
    files = list_files(root_dir)

    print("\nDetected files:")
    for f in files:
        print(" -", f)

    # Step 3: generate plan
    plan = generate_plan(files, root_dir, goal)

    print("\nGenerated Plan:")
    for action in plan:
        print(action)

    # Step 4: validate plan
    validated_plan = validate_plan(plan, root_dir)

    # Step 5: confirm execution (IMPORTANT UX + SAFETY STEP)
    confirm = input("\nExecute this plan? (y/n): ").strip().lower()

    if confirm != "y":
        print("Aborted.")
        return

    print("\nExecuting Plan...\n")

    execute_plan(validated_plan)

    print("\nDone.")


if __name__ == "__main__":
    main()