#!/usr/bin/env pytest -vs
"""Tests for example container."""

ENV_VAR = "ECHO_MESSAGE"
ENV_VAR_VAL = "Hello World from docker-compose!"
SECRET_QUOTE = (
    "There are no secrets better kept than the secrets everybody guesses."  # nosec
)
VERSION_FILE = "src/version.txt"


def test_container_count(dockerc):
    """Verify the test composition and container."""
    assert len(dockerc.containers()) == 2, "Wrong number of containers were running."


def test_wait_for_exits(main_container, version_container):
    """Wait for containers to exit."""
    assert main_container.wait() == 0, "Container service (main) did not exit cleanly"
    assert (
        version_container.wait() == 0
    ), "Container service (version) did not exit cleanly"


def test_output(main_container):
    """Verify the container had the correct output."""
    main_container.wait()  # make sure container exited if running test isolated
    log_output = main_container.logs().decode("utf-8")
    assert SECRET_QUOTE in log_output, "Secret not found in log output."


def test_version_matches(version_container):
    """Verify the container outputs the correct version."""
    version_container.wait()  # make sure container exited if running test isolated
    log_output = version_container.logs().decode("utf-8").strip()
    pkg_vars = {}
    with open(VERSION_FILE) as f:
        exec(f.read(), pkg_vars)  # nosec
    project_version = pkg_vars["__version__"]
    assert (
        log_output == project_version
    ), f"Container version output does not match project version file {VERSION_FILE}"
    assert (
        version_container.labels["version"] == project_version
    ), "Dockerfile version label does not match project version"