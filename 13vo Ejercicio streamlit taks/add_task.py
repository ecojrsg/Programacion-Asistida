# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-09-01 11:24:20
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-09-01 11:27:06
import streamlit as st


def add_task(task_text: str) -> None:
    """Store a non-empty task in the current session state."""
    cleaned_task = task_text.strip()

    if not cleaned_task:
        return

    todo_id = st.session_state["todo_count"]
    st.session_state[f"todo_{todo_id}"] = cleaned_task
    st.session_state["todo_count"] += 1
