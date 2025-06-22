"""
Unified entry point for workflow documentation generator.
Supports both Azure DevOps (devops) and generic JSON conversion (convert) subcommands.
"""
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: workflow-doc-gen <devops|convert> [args...]")
        sys.exit(1)
    cmd = sys.argv[1]
    sys.argv = [sys.argv[0]] + sys.argv[2:]  # Remove the subcommand from args

    if cmd == "azure_devops":
        from hungovercoders_workflow_doc_gen.azure_devops_cli import main as azure_devops_main
        azure_devops_main()
    elif cmd == "json":
        from hungovercoders_workflow_doc_gen.json_cli import main as json_main
        json_main()
    else:
        print(f"Unknown subcommand: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
