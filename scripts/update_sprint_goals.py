#!/usr/bin/env python3
"""Update sprint goals for Sprints 32-36 (Coupon Roadmap).

Uses JiraAPI._request() to call the Agile REST API:
  PUT /rest/agile/1.0/sprint/{sprintId}
  Body: {"goal": "new goal text"}
"""

import sys
from pathlib import Path

# Add atlassian-scripts to path so we can import the library
scripts_dir = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "atlassian-scripts"
sys.path.insert(0, str(scripts_dir))

from lib.auth import create_ssl_context, load_credentials, get_auth_header
from lib.jira_api import JiraAPI, derive_jira_url

# Sprint goals to update
SPRINT_GOALS = [
    {
        "id": 640,
        "name": "Sprint 32",
        "goal": "VS1 Walking Skeleton + VS-Enabler + VS2 Credit Coupon E2E (BE+FE) + Admin CRUD จบบน Staging",
    },
    {
        "id": 673,
        "name": "Sprint 33",
        "goal": "VS3 Discount Coupon E2E + Non-coupon cleanup (hotfix, phone auth, usage history bugs)",
    },
    {
        "id": 706,
        "name": "Sprint 34",
        "goal": "VS4 Cashback E2E + VS5 History Tab + VS6 Popup + Ad Integration + Production Ready",
    },
    {
        "id": 707,
        "name": "Sprint 35",
        "goal": "Integration Testing + Performance Optimization + Feature Flag Rollout",
    },
    {
        "id": 708,
        "name": "Sprint 36",
        "goal": "Production Launch + Monitoring + Post-launch Stabilization",
    },
]


def main():
    # Load credentials and create API client
    creds = load_credentials()
    jira_url = derive_jira_url(creds["CONFLUENCE_URL"])
    api = JiraAPI(
        base_url=jira_url,
        auth_header=get_auth_header(creds["CONFLUENCE_USERNAME"], creds["CONFLUENCE_API_TOKEN"]),
        ssl_context=create_ssl_context(),
    )

    print(f"Jira URL: {jira_url}")
    print(f"Updating {len(SPRINT_GOALS)} sprint goals...\n")

    success_count = 0
    for sprint in SPRINT_GOALS:
        sprint_id = sprint["id"]
        sprint_label = sprint["name"]
        goal = sprint["goal"]

        print(f"  [{sprint_label}] (ID: {sprint_id})")
        print(f"    New Goal: {goal}")

        try:
            # Step 1: GET the sprint to retrieve its actual name (required by PUT)
            current = api._request("GET", f"/rest/agile/1.0/sprint/{sprint_id}")
            actual_name = current["name"]
            print(f"    Actual name: {actual_name}")

            # Step 2: PUT with name + state (both required) + goal
            actual_state = current["state"]
            print(f"    State: {actual_state}")
            result = api._request(
                "PUT",
                f"/rest/agile/1.0/sprint/{sprint_id}",
                {"name": actual_name, "state": actual_state, "goal": goal},
            )
            status = result.get("_status", 200)
            # Agile API returns the sprint object on success (200)
            if "id" in result or status in (200, 204):
                print(f"    -> OK")
                success_count += 1
            else:
                print(f"    -> Unexpected response: {result}")
        except Exception as e:
            print(f"    -> FAILED: {e}")

        print()

    print(f"Done: {success_count}/{len(SPRINT_GOALS)} sprints updated successfully.")
    return 0 if success_count == len(SPRINT_GOALS) else 1


if __name__ == "__main__":
    sys.exit(main())
