# Claude Code Runners: An Agentic Software Development Team

This project implements a team of specialized AI agents that work together to automate the software development lifecycle, from initial research to deployment. It is built using the agentic features of **Claude Code**, including Subagents, Hooks, and Model Context Protocol (MCP) for custom tooling.

## Features

- **Multi-Agent System:** A team of 9 specialized agents, each with a distinct role (planning, research, product management, UX/UI design, architecture, engineering, QA, and DevOps).
- **Automated Orchestration:** A Python-based orchestrator (`orchestrator.py`) reads a project plan (`plan.yml`) and runs the agents in the correct order based on dependencies.
- **Spec-Driven Development:** The workflow is kicked off by a `project-planner` agent that creates a detailed plan, ensuring a structured and predictable development process.
- **Extensible Tooling:** Includes a mock Model Context Protocol (MCP) server (`mcp_server/`) to demonstrate how to provide custom tools (like Jira or Figma integration) to the agents.

## Architecture Overview

1.  **Project Planner:** The user provides a high-level goal to the `project-planner` agent. It generates a `plan.yml` file, which defines all the tasks, dependencies, and the responsible agent for each task.
2.  **Orchestrator:** The `orchestrator.py` script is run. It reads `plan.yml` and executes the tasks sequentially, respecting the dependency graph.
3.  **Agent Execution:** The orchestrator invokes the appropriate agent for each task using the `claude` command-line tool.
4.  **Tool Usage (MCP):** When an agent needs to perform an action not built into Claude Code (e.g., search the web, create a Jira ticket), it calls a tool provided by the running MCP server.
5.  **Output as Input:** The output of one agent's task (e.g., the path to a PRD file) becomes the input for the next agent in the chain.

## The Agent Team

-   `project-planner`: The team lead. Takes a high-level request and creates the master `plan.yml`.
-   `researcher`: Conducts market and competitor research.
-   `product-manager`: Creates the Product Requirements Document (PRD).
-   `ux-designer`: Designs the user flow and wireframes.
-   `ui-designer`: Creates a detailed UI Kit and design system.
-   `software-architect`: Creates the Technical Design Document (TDD).
-   `senior-engineer`: Implements the feature by writing code.
-   `qa-tester`: Writes and runs automated tests.
-   `dev-ops`: Handles deployment and infrastructure.

## Getting Started

### 1. Prerequisites
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) installed.
- Python 3.x installed.

### 2. Installation
Install the Python dependencies for the orchestrator and the mock server:
```bash
pip install -r requirements.txt
pip install -r mcp_server/requirements.txt
```

### 3. Running the System

1.  **Start the Mock Tool Server:**
    Open a terminal and run the MCP server in the background.
    ```bash
    python3 mcp_server/server.py &
    ```

2.  **Configure Claude Code:**
    This project is designed to work with Claude Code's project-level settings. When you run `claude` from within the `claude-code-runners` directory, it should automatically pick up the MCP server configuration from `.claude/settings.json`.

3.  **Generate the Project Plan:**
    Kick off a new project by invoking the `project-planner` agent.
    ```bash
    claude -p "Use the project-planner agent. The task is: Plan the development of a 'social login' feature."
    ```
    This will create a `plan.yml` file in the current directory.

4.  **Run the Orchestrator:**
    Execute the plan using the orchestrator script.
    ```bash
    python3 orchestrator.py
    ```
    The orchestrator will now run through the tasks in `plan.yml`, executing each agent in turn (in simulation mode).

## Next Steps

-   Implement the "real" agent execution calls in `orchestrator.py` (uncomment the `subprocess.run` line).
-   Build out the mock MCP server with more tools.
-   Create a simple CLI to wrap these setup and execution steps into a single command.
