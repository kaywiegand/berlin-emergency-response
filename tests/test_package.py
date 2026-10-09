"""Smoke test for the project package used by notebooks."""

from berlin_emergency_response.config import PATHS, PROJECT_NAME


def test_paths_point_into_the_project():
    assert PATHS["dbt"].joinpath("dbt_project.yml").exists()
    assert PATHS["dbt_models"].name == "models"
    assert PATHS["app_data"].parts[-3:] == ("public", "app", "data")


def test_project_name():
    assert PROJECT_NAME == "Berlin Emergency Response"
