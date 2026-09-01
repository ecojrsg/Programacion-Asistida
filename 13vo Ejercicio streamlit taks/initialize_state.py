# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-09-01 11:24:20
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-09-01 11:27:02
import streamlit as st


def initialize_state() -> None:
    """Initialize the session counter used to identify tasks."""
    if "todo_count" not in st.session_state:
        st.session_state["todo_count"] = 0
