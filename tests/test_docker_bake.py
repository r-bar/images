from collections import Counter
import typing as t
import json
import subprocess
import pytest


@pytest.fixture(scope="session")
def bake_config() -> dict[str, t.Any]:
    config_data = subprocess.check_output(
        ["docker", "buildx", "bake", "--print"], text=True
    )
    return json.loads(config_data)


def test_all_targets_have_latest(bake_config: dict[str, t.Any]) -> None:
    """Ensure for each base image, there is exactly one target tagged "latest"."""
    bases = {}
    for target_name, target_data in bake_config["target"].items():
        for tag in target_data.get("tags", []):
            base, tag = tag.split(":")
            bases.setdefault(base, Counter())[tag] += 1
    for base, tag_counts in bases.items():
        latest_count = tag_counts["latest"]
        assert latest_count == 1, (
            f'Expected exactly one target with tag "latest" for base {base}, but found {latest_count}'
        )


def test_matching_target_name(bake_config: dict[str, t.Any]) -> None:
    """Ensure image tags match target names to catch bad target names and sloppy copy pasting"""
    for target_name, target_data in bake_config["target"].items():
        for tag in target_data.get("tags", []):
            image_name, _tag = tag.split(":")
            base_name = image_name.split("/")[-1]
            assert target_name.startswith(base_name), "The target name should match the image name"
