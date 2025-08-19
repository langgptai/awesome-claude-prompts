from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for mock data
mock_jira_tickets = []
mock_figma_files = []

@app.route('/')
def index():
    return "Mock MCP Server is running."

@app.route('/tools', methods=['GET'])
def get_tools():
    """
    Exposes the list of available tools to Claude Code.
    """
    tools = [
        {
            "name": "google_search",
            "description": "Searches the web for a given query.",
            "parameters": [{"name": "query", "type": "string", "description": "The search query."}]
        },
        {
            "name": "jira_create_ticket",
            "description": "Creates a new ticket in Jira.",
            "parameters": [
                {"name": "title", "type": "string", "description": "The title of the ticket."},
                {"name": "description", "type": "string", "description": "The description of the ticket."},
                {"name": "issue_type", "type": "string", "description": "The type of the issue (e.g., Story, Bug, Task)."}
            ]
        }
        # Add other tools from TOOLING_STRATEGY.md here
    ]
    return jsonify(tools)

@app.route('/execute_tool', methods=['POST'])
def execute_tool():
    """
    Executes a tool call from Claude Code.
    """
    data = request.json
    tool_name = data.get('tool_name')
    parameters = data.get('parameters', {})

    print(f"Received tool call for '{tool_name}' with parameters: {parameters}")

    if tool_name == 'google_search':
        query = parameters.get('query', '')
        # Mock implementation
        mock_results = [
            {"title": f"Result 1 for {query}", "url": f"https://example.com/search?q={query}&n=1", "snippet": "This is the first mock result."},
            {"title": f"Result 2 for {query}", "url": f"https://example.com/search?q={query}&n=2", "snippet": "This is the second mock result."}
        ]
        return jsonify({"status": "success", "result": mock_results})

    elif tool_name == 'jira_create_ticket':
        title = parameters.get('title', 'No Title')
        ticket_id = f"PROJ-{len(mock_jira_tickets) + 1}"
        mock_jira_tickets.append({"id": ticket_id, "title": title, "description": parameters.get('description')})
        print(f"Created Jira ticket: {ticket_id}")
        return jsonify({"status": "success", "result": {"ticket_id": ticket_id}})

    else:
        return jsonify({"status": "error", "message": "Tool not found."}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
