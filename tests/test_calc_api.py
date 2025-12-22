import azure.functions as func

import function_app


def _make_req(path: str, params: dict[str, str]) -> func.HttpRequest:
    return func.HttpRequest(
        method="GET",
        url=f"http://localhost{path}",
        headers={},
        params=params,
        route_params={},
        body=b"",
    )


def _body_text(resp: func.HttpResponse) -> str:
    body = resp.get_body()
    if isinstance(body, (bytes, bytearray)):
        return body.decode("utf-8")
    return str(body)


def test_mul_success_integer() -> None:
    req = _make_req("/mul", {"A": "2", "B": "3"})
    resp = function_app.mul(req)

    assert resp.status_code == 200
    assert resp.headers.get("Content-Type") == "text/plain; charset=utf-8"
    assert _body_text(resp) == "6"


def test_div_success_float() -> None:
    req = _make_req("/div", {"A": "5", "B": "2"})
    resp = function_app.div(req)

    assert resp.status_code == 200
    assert resp.headers.get("Content-Type") == "text/plain; charset=utf-8"
    assert _body_text(resp) == "2.5"


def test_missing_params_is_400() -> None:
    req = _make_req("/mul", {"A": "2"})
    resp = function_app.mul(req)

    assert resp.status_code == 400
    assert resp.headers.get("Content-Type") == "text/plain; charset=utf-8"
    assert _body_text(resp) == "A and B are required"


def test_non_numeric_is_400() -> None:
    req = _make_req("/mul", {"A": "x", "B": "3"})
    resp = function_app.mul(req)

    assert resp.status_code == 400
    assert resp.headers.get("Content-Type") == "text/plain; charset=utf-8"
    assert _body_text(resp) == "A and B must be numbers"


def test_div_by_zero_is_400() -> None:
    req = _make_req("/div", {"A": "1", "B": "0"})
    resp = function_app.div(req)

    assert resp.status_code == 400
    assert resp.headers.get("Content-Type") == "text/plain; charset=utf-8"
    assert _body_text(resp) == "B must not be 0"


def test_nan_is_rejected() -> None:
    req = _make_req("/mul", {"A": "NaN", "B": "1"})
    resp = function_app.mul(req)

    assert resp.status_code == 400
    assert resp.headers.get("Content-Type") == "text/plain; charset=utf-8"
    assert _body_text(resp) == "A and B must be numbers"
