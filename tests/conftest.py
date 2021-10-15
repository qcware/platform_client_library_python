"""
Test configuration for pytest in an attempt to make some
regimes (such as connected IBMQ tests, or Vulcan tests)
selectable but not run as default.
"""

# see https://docs.pytest.org/en/stable/example/parametrize.html


def pytest_addoption(parser):
    parser.addoption(
        "--vulcan", action="store_true", help="run test for vulcan backends"
    )
    parser.addoption("--ibmq", action="store_true", help="run test for ibmq backends")
    parser.addoption(
        "--awsslow",
        action="store_true",
        help="run tests for braket schedule-window backends (ionq, rigetti)",
    )


# from some ideas in https://superorbit.al/journal/focusing-on-pytest/
def pytest_collection_modifyitems(session, config, items):
    deselected_items = []
    selected_items = []
    for item in items:
        if (
            "qcware/gpu_simulator" in item.nodeid or "qcware/gpu" in item.nodeid
        ) and not config.getoption("vulcan"):
            deselected_items.append(item)
        elif "ibmq" in item.nodeid and not config.getoption("ibmq"):
            deselected_items.append(item)
        elif (
            "awsbraket/ionq" in item.nodeid
            or "awsbraket/rigetti" in item.nodeid
            or "awsbraket/tn1" in item.nodeid
        ) and not config.getoption("awsslow"):
            deselected_items.append(item)
        else:
            selected_items.append(item)

    config.hook.pytest_deselected(items=deselected_items)
    items[:] = selected_items
