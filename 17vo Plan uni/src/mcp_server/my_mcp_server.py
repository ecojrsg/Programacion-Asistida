#!/usr/bin/env python3
"""MCP tools for the university schedule planner."""

from typing import Any

from fastmcp import FastMCP

from src.schedule_planner import (
    add_course_to_schedule as plan_add_course,
    get_course as plan_get_course,
    get_current_schedule as plan_get_current_schedule,
    list_courses as plan_list_courses,
)


mcp = FastMCP("UniversitySchedulePlanner")


@mcp.tool()
def list_courses(
    day: str | None = None,
    credits: int | None = None,
    name: str | None = None,
) -> dict[str, Any]:
    """List courses using optional day, credit, and name filters.

    Use this tool to inspect available courses before selecting one.
    """
    return plan_list_courses(day=day, credits=credits, name=name)


@mcp.tool()
def get_course(course_name: str) -> dict[str, Any]:
    """Return the details of one course by code or name.

    Use this tool when detailed information about a course is needed.
    """
    return plan_get_course(course_name)


@mcp.tool()
def add_course_to_schedule(course_name: str) -> dict[str, Any]:
    """Add a course after applying all schedule rules.

    Use this tool to enroll a course and persist the updated state.
    """
    return plan_add_course(course_name)


@mcp.tool()
def get_current_schedule() -> dict[str, Any]:
    """Return the saved schedule and its total credits.

    Use this tool to review the student's current schedule.
    """
    return plan_get_current_schedule()


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=4000)
