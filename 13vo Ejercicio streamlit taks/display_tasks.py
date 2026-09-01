# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-09-01 11:24:20
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-09-01 11:26:51
import streamlit as st


def display_tasks() -> None:
    """Display every task stored in the current session state."""
    st.subheader("Tasks")

    if st.session_state["todo_count"] == 0:
        st.info("No tasks added yet.")
        return

    for todo_id in range(st.session_state["todo_count"]):
        task_text = st.session_state[f"todo_{todo_id}"]
        st.write(f"{todo_id + 1}. {task_text}")
