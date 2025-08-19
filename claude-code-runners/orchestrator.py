import yaml
import subprocess
import sys
import os

PLAN_FILE = 'plan.yml'

class Orchestrator:
    def __init__(self, plan_file):
        self.plan_file = plan_file
        if not os.path.exists(self.plan_file):
            print(f"Error: Plan file '{self.plan_file}' not found.")
            sys.exit(1)
        self.plan = self.load_plan()

    def load_plan(self):
        """Loads the YAML plan file."""
        with open(self.plan_file, 'r') as f:
            return yaml.safe_load(f)

    def save_plan(self):
        """Saves the current state of the plan back to the YAML file."""
        with open(self.plan_file, 'w') as f:
            yaml.dump(self.plan, f, sort_keys=False)

    def _dependencies_met(self, task):
        """Checks if a task's dependencies are all complete."""
        for dep_id in task.get('dependencies', []):
            # Find the dependency task in the plan
            dep_task = next((t for t in self.plan['tasks'] if t['task_id'] == dep_id), None)
            if not dep_task or dep_task.get('status') != 'completed':
                return False
        return True

    def run(self):
        """Runs the orchestration loop until all tasks are complete or no progress can be made."""
        print("Starting orchestration...")

        while True:
            tasks_executed_in_pass = False
            # Find the next task to run
            next_task_to_run = None
            for task in self.plan.get('tasks', []):
                if task.get('status') == 'pending' and self._dependencies_met(task):
                    next_task_to_run = task
                    break

            if next_task_to_run:
                self.execute_task(next_task_to_run)
                tasks_executed_in_pass = True

            # If we went through a whole pass without executing any tasks, we're done or stuck.
            if not tasks_executed_in_pass:
                break

        # Final status check
        pending_tasks = [t['task_id'] for t in self.plan['tasks'] if t['status'] == 'pending']
        failed_tasks = [t['task_id'] for t in self.plan['tasks'] if t['status'] == 'failed']

        if not pending_tasks and not failed_tasks:
            print("Orchestration complete. All tasks finished successfully.")
        else:
            print("Orchestration stopped.")
            if pending_tasks:
                print(f"The following tasks are still pending: {', '.join(pending_tasks)}")
                print("This may be due to circular dependencies.")
            if failed_tasks:
                print(f"The following tasks failed: {', '.join(failed_tasks)}")

    def execute_task(self, task):
        """Executes a single task."""
        task_id = task.get('task_id')
        agent = task.get('agent')
        description = task.get('description')

        print(f"Executing task: {task_id} with agent: {agent}")
        print(f"Description: {description}")

        # Update status to in_progress
        task['status'] = 'in_progress'
        self.save_plan()

        # Construct the actual command to call the Claude agent
        # We will use the non-interactive mode with a prompt.
        prompt = f"Use the {agent} agent. The task is: {description}."

        # In a real scenario, we would also pass input file paths from dependencies.
        # This will be implemented in a future step.

        command = f"claude -p \"{prompt}\""

        print(f"Constructed command: {command}")

        try:
            # We will use subprocess.run to call the claude CLI.
            # For now, we will continue to simulate the run to avoid making real,
            # time-consuming, and potentially costly LLM calls during development.
            # In a real run, the following line would be uncommented.
            # result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            # print("Agent output:", result.stdout)

            print(f"Task {task_id} completed successfully (simulation of command execution).")
            task['status'] = 'completed'
        except subprocess.CalledProcessError as e:
            print(f"Error executing task {task_id}: {e}")
            print(f"Stderr: {e.stderr}")
            task['status'] = 'failed'

        self.save_plan()


if __name__ == '__main__':
    # We need a sample plan.yml to test this.
    # The project-planner agent will create this in a real run.
    if not os.path.exists(PLAN_FILE):
        print(f"Creating a sample '{PLAN_FILE}' for testing purposes.")
        sample_plan = {
            'project_name': 'Comprehensive Test Project',
            'request': 'Build a social login feature with Google and GitHub.',
            'tasks': [
                {'task_id': 'market_research', 'agent': 'researcher', 'description': 'Research social login features', 'status': 'pending', 'dependencies': [], 'outputs': ['research_report_file']},
                {'task_id': 'create_prd', 'agent': 'product-manager', 'description': 'Create PRD for social login', 'status': 'pending', 'dependencies': ['market_research'], 'inputs': ['research_report_file'], 'outputs': ['prd_file']},
                {'task_id': 'create_ux_spec', 'agent': 'ux-designer', 'description': 'Create UX spec', 'status': 'pending', 'dependencies': ['create_prd'], 'inputs': ['prd_file'], 'outputs': ['ux_spec_file']},
                {'task_id': 'create_ui_spec', 'agent': 'ui-designer', 'description': 'Create UI spec', 'status': 'pending', 'dependencies': ['create_ux_spec'], 'inputs': ['ux_spec_file'], 'outputs': ['ui_spec_file']},
                {'task_id': 'create_tdd', 'agent': 'software-architect', 'description': 'Create TDD for social login', 'status': 'pending', 'dependencies': ['create_prd', 'create_ui_spec'], 'inputs': ['prd_file', 'ui_spec_file'], 'outputs': ['tdd_file']},
                {'task_id': 'implement_feature', 'agent': 'senior-engineer', 'description': 'Implement the social login feature', 'status': 'pending', 'dependencies': ['create_tdd'], 'inputs': ['tdd_file', 'ui_spec_file'], 'outputs': ['source_code_files']},
                {'task_id': 'run_qa', 'agent': 'qa-tester', 'description': 'Run QA and tests', 'status': 'pending', 'dependencies': ['implement_feature'], 'inputs': ['source_code_files'], 'outputs': ['qa_report_file']},
                {'task_id': 'deploy_staging', 'agent': 'dev-ops', 'description': 'Deploy to staging', 'status': 'pending', 'dependencies': ['run_qa'], 'inputs': ['qa_report_file'], 'outputs': ['deployment_status']}
            ]
        }
        with open(PLAN_FILE, 'w') as f:
            yaml.dump(sample_plan, f, sort_keys=False)

    orchestrator = Orchestrator(PLAN_FILE)
    orchestrator.run()
