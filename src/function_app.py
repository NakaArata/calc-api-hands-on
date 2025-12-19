import logging
from decimal import Decimal, InvalidOperation

import azure.functions as func

_TEXT_PLAIN_UTF8 = {"Content-Type": "text/plain; charset=utf-8"}

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


def _bad_request(message: str) -> func.HttpResponse:
    return func.HttpResponse(message, status_code=400, headers=_TEXT_PLAIN_UTF8)


def _parse_decimal(raw: str) -> Decimal:
    try:
        value = Decimal(raw)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("not a number") from exc

    if not value.is_finite():
        raise ValueError("not finite")

    return value


def _decimal_to_text(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    if text == "-0":
        text = "0"
    return text


def _get_a_b(req: func.HttpRequest) -> tuple[Decimal, Decimal] | tuple[None, None]:
    a_raw = req.params.get("A")
    b_raw = req.params.get("B")

    if a_raw is None or b_raw is None:
        return None, None

    return _parse_decimal(a_raw), _parse_decimal(b_raw)


@app.route(route="mul", methods=["GET"])
def mul(req: func.HttpRequest) -> func.HttpResponse:
    try:
        a, b = _get_a_b(req)
        if a is None or b is None:
            return _bad_request("A and B are required")

        result = a * b
        return func.HttpResponse(_decimal_to_text(result), status_code=200, headers=_TEXT_PLAIN_UTF8)
    except ValueError:
        return _bad_request("A and B must be numbers")
    except Exception:
        logging.exception("Unhandled error in /mul")
        return func.HttpResponse("Internal Server Error", status_code=500, headers=_TEXT_PLAIN_UTF8)


@app.route(route="div", methods=["GET"])
def div(req: func.HttpRequest) -> func.HttpResponse:
    try:
        a, b = _get_a_b(req)
        if a is None or b is None:
            return _bad_request("A and B are required")

        if b == 0:
            return _bad_request("B must not be 0")

        result = a / b
        return func.HttpResponse(_decimal_to_text(result), status_code=200, headers=_TEXT_PLAIN_UTF8)
    except ValueError:
        return _bad_request("A and B must be numbers")
    except Exception:
        logging.exception("Unhandled error in /div")
        return func.HttpResponse("Internal Server Error", status_code=500, headers=_TEXT_PLAIN_UTF8)
