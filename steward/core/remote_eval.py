"""Remote evaluation hooks (best effort stub)."""
from __future__ import absolute_import, print_function

try:
    # Python 3
    from urllib import request as urllib_request
    from urllib import parse as urllib_parse
except ImportError:  # Python 2
    import urllib2 as urllib_request  # type: ignore
    import urllib as urllib_parse  # type: ignore


def evaluate(payload, url, timeout=5):
    """Send *payload* to *url* and return the decoded response."""
    if not url:
        return {"enabled": False, "error": "remote evaluation disabled"}
    data = urllib_parse.urlencode(payload).encode("utf-8")
    request = urllib_request.Request(url, data=data)
    try:
        response = urllib_request.urlopen(request, timeout=timeout)
        body = response.read()
    except Exception as exc:  # pragma: no cover - network failure handling
        return {"enabled": True, "error": str(exc)}
    try:
        body_text = body.decode("utf-8")
    except Exception:
        body_text = body
    return {"enabled": True, "response": body_text}
