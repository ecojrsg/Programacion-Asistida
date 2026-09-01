# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-09-01 11:20:00
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-09-01 11:20:31

import streamlit as st

from add_task import add_task
from display_tasks import display_tasks
from initialize_state import initialize_state


def main() -> None:
    """Render the to-do list application."""
    st.title("To-Do List")
    initialize_state()

    task_text = st.text_input("Enter a task")

    if st.button("Add task"):
        add_task(task_text)

    display_tasks()


if __name__ == "__main__":
    main()
