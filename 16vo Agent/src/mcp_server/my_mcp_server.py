#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local MCP server for retrieving country information.
"""

import json
from functools import lru_cache
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from fastmcp import FastMCP

DATA_URL = (
    "https://raw.githubusercontent.com/mledoze/countries/master/"
    "countries.json"
)
REQUEST_TIMEOUT = 10

mcp = FastMCP("CountryGuide")


@lru_cache(maxsize=1)
def _fetch_countries() -> list[dict[str, Any]]:
    """Fetch the country dataset once per server session."""
    request = Request(
        DATA_URL,
        headers={"User-Agent": "CountryGuide-MCP/1.0"},
    )

    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        countries = json.loads(response.read().decode("utf-8"))

    return countries if isinstance(countries, list) else []


def _get_country(country_name: str) -> dict[str, Any] | None:
    """Find one country by its common or official name."""
    try:
        countries = _fetch_countries()
    except (URLError, TimeoutError, ValueError):
        return None

    search_name = country_name.strip().casefold()
    for country in countries:
        names = country.get("name", {})
        candidates = [names.get("common", ""), names.get("official", "")]
        candidates.extend(country.get("altSpellings", []))
        native_names = names.get("native", {})
        for native_name in native_names.values():
            candidates.append(native_name.get("common", ""))
        if any(search_name == candidate.casefold() for candidate in candidates):
            return country

    return None


def _get_country_by_code(country_code: str) -> dict[str, Any] | None:
    """Find one country by its ISO alpha-3 code."""
    try:
        countries = _fetch_countries()
    except (URLError, TimeoutError, ValueError):
        return None

    for country in countries:
        if country.get("cca3") == country_code:
            return country
    return None


def _country_label(country: dict[str, Any]) -> str:
    """Return the common country name."""
    name = country.get("name", {})
    return name.get("common", "Nombre no disponible")


def _languages(country: dict[str, Any]) -> list[str]:
    """Return the languages spoken in a country."""
    languages = country.get("languages", {})
    return list(languages.values()) if isinstance(languages, dict) else []


def _currencies(country: dict[str, Any]) -> list[str]:
    """Return the currencies used in a country."""
    currencies = country.get("currencies", {})
    if not isinstance(currencies, dict):
        return []

    return [
        f"{data.get('name', code)} ({data.get('symbol', '')})".strip()
        for code, data in currencies.items()
        if isinstance(data, dict)
    ]


def _format_country(country: dict[str, Any]) -> dict[str, Any]:
    """Format API data for the user."""
    capitals = country.get("capital", [])

    capital = "No disponible"
    if capitals and isinstance(capitals[0], dict):
        capital = capitals[0].get("name", "No disponible")
    elif capitals:
        capital = capitals[0]

    flag_value = country.get("flag", "No disponible")

    return {
        "nombre": _country_label(country),
        "capital": capital,
        "poblacion": country.get("population", "No disponible"),
        "region": country.get("region", "No disponible"),
        "subregion": country.get("subregion", "No disponible"),
        "idiomas": _languages(country),
        "monedas": _currencies(country),
        "zonas_horarias": country.get("timezones", []),
        "bandera": flag_value,
    }


def _missing_value_message(*field_names: str) -> dict[str, str]:
    """Build a Spanish message for missing values."""
    fields = ", ".join(field_names)
    return {"error": f"Faltan los siguientes datos: {fields}."}


@mcp.tool
def get_country_info(country_name: str) -> dict[str, Any]:
    """Return basic information for a country.

    Args:
        country_name: Country name.
    """
    if not country_name.strip():
        return _missing_value_message("nombre del país")

    country = _get_country(country_name)
    if country is None:
        return {"error": f"No se encontró el país '{country_name}'."}

    return _format_country(country)


@mcp.tool
def compare_countries(
    first_country: str,
    second_country: str,
) -> dict[str, Any]:
    """Compare basic information for two countries.

    Args:
        first_country: First country name.
        second_country: Second country name.
    """
    missing = []
    if not first_country.strip():
        missing.append("primer país")
    if not second_country.strip():
        missing.append("segundo país")
    if missing:
        return _missing_value_message(*missing)

    first = _get_country(first_country)
    second = _get_country(second_country)
    if first is None or second is None:
        missing_countries = []
        if first is None:
            missing_countries.append(first_country)
        if second is None:
            missing_countries.append(second_country)
        names = ", ".join(missing_countries)
        return {"error": f"No se encontró: {names}."}

    return {
        "primer_pais": _format_country(first),
        "segundo_pais": _format_country(second),
    }


@mcp.tool
def list_countries_by_region(region: str) -> dict[str, Any]:
    """List countries from a geographic region.

    Args:
        region: Region name in English.
    """
    if not region.strip():
        return _missing_value_message("región")

    valid_regions = {"africa", "americas", "asia", "europe", "oceania"}
    normalized_region = region.strip().lower()
    if normalized_region not in valid_regions:
        valid = ", ".join(sorted(valid_regions))
        return {"error": f"Región inválida. Usa una de estas: {valid}."}

    try:
        countries = [
            country
            for country in _fetch_countries()
            if country.get("region", "").casefold() == normalized_region
        ]
    except (URLError, TimeoutError, ValueError):
        return {"error": "No fue posible consultar la API de países."}

    result = []
    for country in countries:
        capitals = country.get("capital", [])
        capital = "No disponible"
        if capitals and isinstance(capitals[0], dict):
            capital = capitals[0].get("name", "No disponible")
        result.append(
            {
                "nombre": _country_label(country),
                "capital": capital,
                "poblacion": country.get("population", "No disponible"),
            }
        )

    return {"region": region, "cantidad": len(result), "paises": result}


@mcp.tool
def get_country_neighbors(country_name: str) -> dict[str, Any]:
    """Return the land neighbors of a country.

    Args:
        country_name: Country name.
    """
    if not country_name.strip():
        return _missing_value_message("nombre del país")

    country = _get_country(country_name)
    if country is None:
        return {"error": f"No se encontró el país '{country_name}'."}

    borders = country.get("borders", [])
    if not borders:
        return {
            "pais": _country_label(country),
            "cantidad": 0,
            "vecinos": [],
            "mensaje": "El país no tiene fronteras terrestres.",
        }

    names = []
    for border in borders:
        neighbor = _get_country_by_code(border)
        if neighbor is not None:
            names.append(_country_label(neighbor))

    return {
        "pais": _country_label(country),
        "cantidad": len(names),
        "vecinos": sorted(names),
    }


@mcp.tool
def create_tourist_profile(country_name: str) -> dict[str, Any]:
    """Create a short tourist profile for a country.

    Args:
        country_name: Country name.
    """
    if not country_name.strip():
        return _missing_value_message("nombre del país")

    country_info = get_country_info(country_name)
    if "error" in country_info:
        return country_info

    neighbors = get_country_neighbors(country_name)
    return {
        "perfil_turistico": country_info,
        "paises_vecinos": neighbors.get("vecinos", []),
        "recomendacion": (
            "Consulta la capital, los idiomas, la moneda y las zonas horarias "
            "antes de planificar tu viaje."
        ),
    }


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=4000)
