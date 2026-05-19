from exercises.ex17_cloudwan_drift import compare_routes


def test_all_routes_present_no_drift():
    actual_routes = ["172.20.0.0/16", "172.22.0.0/16", "10.30.0.0/16"]
    expected = ["172.20.0.0/16", "172.22.0.0/16", "10.30.0.0/16"]
    should_not_have = ["192.168.10.0/24"]

    missing, leaked, present = compare_routes(actual_routes, expected, should_not_have)

    assert present == ["172.20.0.0/16", "172.22.0.0/16", "10.30.0.0/16"]
    assert missing == []
    assert leaked == []


def test_missing_route_detected():
    actual_routes = ["172.20.0.0/16", "172.22.0.0/16"]
    expected = ["172.20.0.0/16", "172.22.0.0/16", "10.30.0.0/16"]
    should_not_have = ["192.168.10.0/24"]

    missing, leaked, present = compare_routes(actual_routes, expected, should_not_have)

    assert missing == ["10.30.0.0/16"]
    assert leaked == []
    assert present == ["172.20.0.0/16", "172.22.0.0/16"]


def test_leaked_route_detected():
    actual_routes = ["172.20.0.0/16", "192.168.10.0/24"]
    expected = ["172.20.0.0/16"]
    should_not_have = ["192.168.10.0/24", "0.0.0.0/0"]

    missing, leaked, present = compare_routes(actual_routes, expected, should_not_have)

    assert missing == []
    assert leaked == ["192.168.10.0/24"]
    assert present == ["172.20.0.0/16"]


def test_both_missing_and_leaked():
    actual_routes = ["172.20.0.0/16", "0.0.0.0/0"]
    expected = ["172.20.0.0/16", "10.40.0.0/16"]
    should_not_have = ["0.0.0.0/0", "192.168.10.0/24"]

    missing, leaked, present = compare_routes(actual_routes, expected, should_not_have)

    assert missing == ["10.40.0.0/16"]
    assert leaked == ["0.0.0.0/0"]
    assert present == ["172.20.0.0/16"]


def test_empty_actual_routes():
    actual_routes = []
    expected = ["172.20.0.0/16", "10.30.0.0/16"]
    should_not_have = ["192.168.10.0/24"]

    missing, leaked, present = compare_routes(actual_routes, expected, should_not_have)

    assert missing == ["172.20.0.0/16", "10.30.0.0/16"]
    assert leaked == []
    assert present == []
