import json
import os
from groq import Groq
from openmetadata import OpenMetadataClient
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY", "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"))

def call_tool(name: str, args: dict, om_client: OpenMetadataClient):
    if name == "search_tables":
        return om_client.search_tables(args.get("query", ""))
    elif name == "get_table_details":
        return om_client.get_table_details(args.get("table_fqn", ""))
    elif name == "get_table_owner":
        return om_client.get_table_owner(args.get("table_fqn", ""))
    elif name == "get_lineage":
        return om_client.get_lineage(args.get("table_fqn", ""))
    elif name == "list_recently_updated":
        return om_client.list_recently_updated()
    return {"error": f"Unknown tool: {name}"}


def run_agent(user_question: str, om_client: OpenMetadataClient, chat_history: list = None) -> str:
    try:
        # Step 1 — Figure out what data to fetch using simple prompt
        plan_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are a data catalog assistant. 
Based on the user question, respond with ONLY a JSON object like this:
{"tool": "search_tables", "args": {"query": "customer"}}

Available tools:
- search_tables: {"query": "keyword"} — search tables by keyword
- get_table_details: {"table_fqn": "name"} — get columns and details
- get_table_owner: {"table_fqn": "name"} — get owner of table
- get_lineage: {"table_fqn": "name"} — get lineage of table
- list_recently_updated: {} — list recently updated tables

Respond ONLY with valid JSON. No explanation."""
                },
                {"role": "user", "content": user_question}
            ],
            max_tokens=200,
        )

        plan_text = plan_response.choices[0].message.content.strip()

        # Clean JSON if wrapped in code block
        if "```" in plan_text:
            plan_text = plan_text.split("```")[1].replace("json", "").strip()

        plan = json.loads(plan_text)
        tool_name = plan.get("tool", "search_tables")
        tool_args = plan.get("args", {})

        print(f"[Agent] Tool: {tool_name}, Args: {tool_args}")

        # Step 2 — Call the tool
        tool_result = call_tool(tool_name, tool_args, om_client)
        print(f"[Agent] Result: {tool_result}")

        # Step 3 — Generate final answer
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are MetaBot, a friendly data catalog assistant. "
                        "Answer the user's question using the data provided. "
                        "Be concise and use emojis. Format nicely."
                    )
                },
                {"role": "user", "content": user_question},
                {
                    "role": "assistant",
                    "content": f"I found this data: {json.dumps(tool_result, default=str)}"
                },
                {
                    "role": "user",
                    "content": "Now give me a clean, friendly answer based on that data."
                }
            ],
            max_tokens=1024,
        )

        return final_response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
