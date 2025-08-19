# Tooling Strategy (MCP Integration Plan)

This document outlines the external tools required for each agent in the Claude Code Runners team. These tools will be provided via a Model Context Protocol (MCP) server.

## Agent Tooling Requirements

### 1. `researcher`
- **Tool:** `google_search(query: str) -> list[dict]`
  - **Purpose:** To search the web for market data, competitor information, and user forum discussions.
  - **Returns:** A list of search result objects, each with a title, URL, and snippet.
- **Tool:** `view_text_website(url: str) -> str`
  - **Purpose:** To read the content of a specific webpage found during research.

### 2. `product-manager`
- **Tool:** `jira_create_ticket(title: str, description: str, issue_type: str) -> str`
  - **Purpose:** To create new user stories or tasks in Jira directly from the PRD.
  - **Returns:** The ID of the newly created Jira ticket (e.g., "PROJ-123").

### 3. `ux-designer` & `ui-designer`
- **Tool:** `figma_get_component(name: str) -> dict`
  - **Purpose:** To fetch existing design system components from a Figma library.
- **Tool:** `figma_upload_wireframe(name: str, description: str) -> str`
  - **Purpose:** To upload a new wireframe or mockup description to Figma.
  - **Returns:** The URL of the new Figma frame.

### 4. `senior-engineer`
- **Tool:** `linter_check(file_path: str) -> bool`
  - **Purpose:** To run a project-specific linter against a file.
  - **Returns:** `True` if the check passes, `False` otherwise, along with the linter output.

### 5. `dev-ops`
- **Tool:** `aws_s3_upload(file_path: str, bucket: str) -> str`
  - **Purpose:** To upload build artifacts to an S3 bucket.
- **Tool:** `github_create_pr(title: str, body: str, branch: str) -> str`
  - **Purpose:** To create a pull request on GitHub after a feature is complete.

## Next Steps
1. Implement a mock MCP server that provides these tools.
2. Update agent prompts to use these tools.
