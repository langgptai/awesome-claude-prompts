import anyio
import yaml
import sys
import os
from pathlib import Path

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, ResultMessage

PLAN_FILE = 'plan.yml'
AGENTS_DIR = 'agents'

class Orchestrator:
    def __init__(self, plan_file):
        self.plan_file = Path(plan_file)
        # The base directory is the directory where this script is located.
        self.base_dir = Path(__file__).parent
        if not self.plan_file.exists():
            print(f"Error: Plan file '{self.plan_file}' not found.")
            sys.exit(1)
        self.plan = self.load_plan()
        self.task_outputs = {} # To store outputs from completed tasks

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
            dep_task = next((t for t in self.plan['tasks'] if t['task_id'] == dep_id), None)
            if not dep_task or dep_task.get('status') != 'completed':
                return False
        return True

    async def run(self):
        """Runs the orchestration loop until all tasks are complete or no progress can be made."""
        print("Starting orchestration with Claude Code SDK...")

        while True:
            runnable_task = None
            for task in self.plan.get('tasks', []):
                if task.get('status') == 'pending' and self._dependencies_met(task):
                    runnable_task = task
                    break

            if runnable_task:
                await self.execute_task(runnable_task)
            else:
                # No more runnable tasks
                break

        # Final status check
        pending_tasks = [t['task_id'] for t in self.plan['tasks'] if t['status'] == 'pending']
        if not pending_tasks:
            print("Orchestration complete. All tasks finished.")
        else:
            print(f"Orchestration stopped. The following tasks are still pending: {', '.join(pending_tasks)}")

    async def execute_task(self, task):
        """Executes a single task using the Claude Code SDK."""
        task_id = task.get('task_id')
        agent_name = task.get('agent')
        description = task.get('description')

        print(f"\n--- Executing task: {task_id} with agent: {agent_name} ---")

        task['status'] = 'in_progress'
        self.save_plan()

        try:
            # 1. Read the agent's system prompt from its definition file
            agent_file = self.base_dir / AGENTS_DIR / f"{agent_name}.md"
            if not agent_file.exists():
                raise FileNotFoundError(f"Agent definition file not found: {agent_file}")

            # The content of the .md file is the system prompt
            system_prompt = agent_file.read_text()

            # 2. Construct the user prompt for the agent
            prompt = f"The task is: {description}."

            # Add inputs from dependencies to the prompt
            input_files = []
            for input_key in task.get('inputs', []):
                if input_key in self.task_outputs:
                    input_files.append(self.task_outputs[input_key])

            if input_files:
                prompt += f" Please use the following input file(s): {', '.join(input_files)}"

            print(f"System Prompt loaded from: {agent_file}")
            print(f"User Prompt: {prompt}")

            # 3. Configure and run the agent via the SDK
            options = ClaudeCodeOptions(system_prompt=system_prompt)
            final_result = ""

            # For now, we will continue to simulate to avoid real LLM calls
            print("Simulating SDK call...")
            # In a real run, the following block would be used:
            # async with ClaudeSDKClient(options=options) as client:
            #     await client.query(prompt)
            #     async for message in client.receive_response():
            #         if isinstance(message, ResultMessage):
            #             final_result = message.result
            #             break

            # Mocked result for simulation
            output_key = task.get('outputs', [None])[0]
            if output_key:
                 # Create a dummy output file
                mock_output_filename = f"{self.base_dir}/mock_output_{task_id}.md"
                with open(mock_output_filename, "w") as f:
                    f.write(f"This is the mock output for task {task_id}.")
                final_result = mock_output_filename
                self.task_outputs[output_key] = final_result
                print(f"Simulated output stored: {output_key} = {final_result}")

            print(f"Agent '{agent_name}' finished.")
            print(f"Result: {final_result}")

            task['status'] = 'completed'

        except Exception as e:
            print(f"Error executing task {task_id}: {e}", file=sys.stderr)
            task['status'] = 'failed'

        self.save_plan()


async def main():
    # We need a sample plan.yml to test this.
    if not os.path.exists(PLAN_FILE):
        print(f"Creating a sample '{PLAN_FILE}' for testing purposes.")
        sample_plan = {
            'project_name': 'SDK Test Project',
            'request': 'Test the SDK orchestrator.',
            'tasks': [
                {'task_id': 'create_prd', 'agent': 'product-manager', 'status': 'pending', 'dependencies': [], 'outputs': ['prd_file'], 'description': "Create a PRD for 'New Login Flow'"},
                {'task_id': 'create_tdd', 'agent': 'software-architect', 'status': 'pending', 'dependencies': ['create_prd'], 'inputs': ['prd_file'], 'outputs': ['tdd_file'], 'description': "Create a TDD for the PRD"}
            ]
        }
        with open(PLAN_FILE, 'w') as f:
            yaml.dump(sample_plan, f, sort_keys=False)

    orchestrator = Orchestrator(PLAN_FILE)
    await orchestrator.run()

if __name__ == '__main__':
    anyio.run(main)
