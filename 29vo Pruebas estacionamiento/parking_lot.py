#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: .
Creation Date: 2026-10-26.
Description: Parking lot excercise.
"""

import math


def calculate_toll(minutes: float, type: str = "auto", weekend: bool = False) -> int:
    if minutes < 0:
        raise ValueError("Minutes cannot be negative")
    if minutes <= 15:
        return 0

    hours = math.ceil(minutes / 60)
    if type == "auto":
        toll = 20
    elif type == "moto":
        toll = 10
    elif type == "pension":
        return 0
    else:
        raise ValueError("Invalid vehicle type.")
    total = hours * toll
    if weekend:
        total *= 1.5
    return min(total, 200)
