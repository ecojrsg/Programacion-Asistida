"""Business logic for the university schedule planner."""

import json
from pathlib import Path
from typing import Any


MAX_CREDITS = 24
STATE_FILE = Path(__file__).parent / "data" / "schedule_state.json"


def _load_state() -> dict[str, Any]:
    """Load the course catalogue and schedule from the JSON state file."""
    with STATE_FILE.open("r", encoding="utf-8") as state_file:
        return json.load(state_file)


def _save_state(state: dict[str, Any]) -> None:
    """Save the current course catalogue and schedule to the JSON file."""
    with STATE_FILE.open("w", encoding="utf-8") as state_file:
        json.dump(state, state_file, ensure_ascii=False, indent=2)
        state_file.write("\n")


def _find_course(
    courses: dict[str, dict[str, Any]], course_name: str
) -> tuple[str, dict[str, Any]] | None:
    """Find a course by code or exact name without case-sensitive matching."""
    search_value = course_name.strip().casefold()

    for course_code, course in courses.items():
        if (
            course_code.casefold() == search_value
            or course["nombre"].casefold() == search_value
        ):
            return course_code, course

    return None


def _has_time_overlap(
    courses: dict[str, dict[str, Any]], schedule: list[str], course_code: str
) -> bool:
    """Return whether a course overlaps an item already in the schedule."""
    course = courses[course_code]

    for scheduled_code in schedule:
        scheduled_course = courses[scheduled_code]
        same_day = course["dia"] == scheduled_course["dia"]
        starts_before_end = course["hora_inicio"] < scheduled_course["hora_fin"]
        ends_after_start = course["hora_fin"] > scheduled_course["hora_inicio"]

        if same_day and starts_before_end and ends_after_start:
            return True

    return False


def list_courses(
    day: str | None = None,
    credits: int | None = None,
    name: str | None = None,
) -> dict[str, Any]:
    """List courses filtered by day, credits, or a partial name.

    Use this function to inspect the catalogue before selecting a course.
    """
    state = _load_state()
    normalized_day = day.strip().casefold() if day else None
    normalized_name = name.strip().casefold() if name else None
    courses = []

    for course_code, course in state["courses"].items():
        matches_day = (
            normalized_day is None
            or course["dia"].casefold() == normalized_day
        )
        matches_credits = credits is None or course["creditos"] == credits
        matches_name = (
            normalized_name is None
            or normalized_name in course["nombre"].casefold()
        )

        if matches_day and matches_credits and matches_name:
            courses.append({"codigo": course_code, **course})

    return {"courses": courses, "count": len(courses)}


def get_course(course_name: str) -> dict[str, Any]:
    """Return one course by code or exact name.

    Use this function when detailed information is needed before scheduling.
    """
    state = _load_state()
    result = _find_course(state["courses"], course_name)

    if result is None:
        return {"success": False, "error": "Course not found."}

    course_code, course = result
    return {"success": True, "course": {"codigo": course_code, **course}}


def add_course_to_schedule(course_name: str) -> dict[str, Any]:
    """Add a course after validating seats, credits, and schedule conflicts.

    Use this function to enroll a course and persist the updated state.
    """
    state = _load_state()
    courses = state["courses"]
    schedule = state["current_schedule"]
    result = _find_course(courses, course_name)

    if result is None:
        return {"success": False, "error": "Course not found."}

    course_code, course = result

    if course["cupos"] == 0:
        return {"success": False, "error": "The course is full."}

    if course_code in schedule:
        return {"success": False, "error": "The course is already scheduled."}

    total_credits = sum(courses[code]["creditos"] for code in schedule)
    if total_credits + course["creditos"] > state["max_credits"]:
        return {
            "success": False,
            "error": (
                f"The schedule cannot exceed {state['max_credits']} credits."
            ),
        }

    if _has_time_overlap(courses, schedule, course_code):
        return {"success": False, "error": "The course overlaps the schedule."}

    schedule.append(course_code)
    course["cupos"] -= 1
    _save_state(state)

    return {
        "success": True,
        "message": "Course added to the schedule.",
        "course": {"codigo": course_code, **course},
        "total_credits": total_credits + course["creditos"],
    }


def get_current_schedule() -> dict[str, Any]:
    """Return the persisted schedule and its total credit count.

    Use this function to review the student's current schedule.
    """
    state = _load_state()
    courses = [
        {"codigo": code, **state["courses"][code]}
        for code in state["current_schedule"]
    ]
    total_credits = sum(course["creditos"] for course in courses)

    return {
        "courses": courses,
        "count": len(courses),
        "total_credits": total_credits,
        "max_credits": state["max_credits"],
    }
