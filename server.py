from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
import sys
import auth
import supervision

HOST = "0.0.0.0"
PORT = 8080

def _json_response(handler, code, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)

def _read_body(handler):
    length = int(handler.headers.get("Content-Length", 0) or 0)
    raw = handler.rfile.read(length) if length > 0 else b""
    ctype = (handler.headers.get("Content-Type") or "").lower()
    if "application/json" in ctype and raw:
        try: return json.loads(raw.decode("utf-8"))
        except: return {}
    if "application/x-www-form-urlencoded" in ctype and raw:
        return {k: v[0] for k, v in parse_qs(raw.decode("utf-8")).items()}
    return {}

def _require_login(b_or_q):
    user = str((b_or_q.get("user") or "")).strip()
    pwd = str((b_or_q.get("password") or "")).strip()
    if not user or not pwd: return (False, user, pwd, "invalid credentials")
    u = auth.findUser(user)
    if u is None or u.get("password") != pwd: return (False, user, pwd, "wrong credentials")
    if u.get("session") is not True: return (False, user, pwd, "user not logged in")
    return (True, user, pwd, "ok")

class SupervisionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        q = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        if path == "/health": return _json_response(self, 200, {"status": "ok"})
        ok, user, pwd, msg = _require_login(q)
        if not ok: return _json_response(self, 401, {"error": msg})

        if path == "/list": return _json_response(self, 200, {"contracts": supervision.listContracts()})
        if path == "/search":
            found = supervision.searchContract((q.get("number") or "").strip())
            if not found: return _json_response(self, 404, {"error": "not found"})
            return _json_response(self, 200, found)
        if path == "/tracking/list":
            res = supervision.listTrackings((q.get("number") or "").strip())
            if isinstance(res, list): return _json_response(self, 200, {"trackings": res})
            return _json_response(self, 404, {"error": res})
        if path == "/tracking/avg":
            res = supervision.avgProgress((q.get("number") or "").strip())
            if isinstance(res, dict): return _json_response(self, 200, res)
            return _json_response(self, 404, {"error": res})
        if path == "/stats": return _json_response(self, 200, supervision.stats())
        return _json_response(self, 404, {"error": "unknown endpoint"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        b = _read_body(self)

        if path == "/user/register":
            msg = auth.registerUser(str(b.get("user","")).strip(), str(b.get("password","")).strip(), str(b.get("role","")).strip(), str(b.get("email","")).strip(), str(b.get("age","")).strip())
            if msg == "ok": return _json_response(self, 201, {"message": "registered"})
            return _json_response(self, 400, {"error": msg})

        if path == "/user/session":
            flag = str(b.get("flag", "false")).strip().lower() == "true"
            res = auth.openCloseSession(str(b.get("user", "")).strip(), str(b.get("password", "")).strip(), flag)
            # Si res es un diccionario, significa que inició sesión bien y trajo los datos
            if isinstance(res, dict): return _json_response(self, 200, {"message": "session updated", "user_data": res})
            return _json_response(self, 401, {"error": res})

        ok, user, pwd, msg = _require_login(b)
        if not ok: return _json_response(self, 401, {"error": msg})

        if path == "/register":
            if not auth.hasRole(user, ("supervisor", "admin")): return _json_response(self, 403, {"error": "unauthorized"})
            msg2 = supervision.registerContract(str(b.get("number", "")).strip(), str(b.get("contractor", "")).strip(), str(b.get("object", "")).strip(), str(b.get("start", "")).strip(), str(b.get("end", "")).strip(), str(b.get("value", "")).strip(), str(b.get("supervisor", "")).strip(), str(b.get("status", "")).strip(), str(b.get("email", "")).strip())
            if msg2 == "ok": return _json_response(self, 201, {"message": "registered"})
            return _json_response(self, 400, {"error": msg2})

        if path == "/tracking/add":
            if not auth.hasRole(user, ("supervisor", "admin")): return _json_response(self, 403, {"error": "unauthorized"})
            msg2 = supervision.addTracking(str(b.get("number", "")).strip(), str(b.get("date", "")).strip(), str(b.get("desc", "")).strip(), str(b.get("progress", "")).strip(), str(b.get("obs", "")).strip())
            if msg2 == "ok": return _json_response(self, 201, {"message": "added"})
            return _json_response(self, 400, {"error": msg2})

        if path == "/update":
            if not auth.hasRole(user, ("supervisor", "admin")): return _json_response(self, 403, {"error": "unauthorized"})
            msg2 = supervision.updateContract(str(b.get("number", "")).strip(), str(b.get("contractor", "")).strip(), str(b.get("object", "")).strip(), str(b.get("start", "")).strip(), str(b.get("end", "")).strip(), str(b.get("value", "")).strip(), str(b.get("supervisor", "")).strip(), str(b.get("status", "")).strip(), str(b.get("email", "")).strip())
            if msg2 == "ok": return _json_response(self, 200, {"message": "updated"})
            return _json_response(self, 400, {"error": msg2})

        if path == "/cancel":
            msg2 = supervision.cancelContract(str(b.get("number", "")).strip(), str(b.get("reason", "Sin motivo")).strip())
            if msg2 == "ok": return _json_response(self, 200, {"message": "canceled"})
            return _json_response(self, 400, {"error": msg2})

        if path == "/export":
            if not auth.hasRole(user, ("admin",)): return _json_response(self, 403, {"error": "unauthorized"})
            supervision.exportCsv()
            return _json_response(self, 200, {"message": "exported"})

        return _json_response(self, 404, {"error": "unknown endpoint"})

if __name__ == "__main__":
    HTTPServer((HOST, PORT), SupervisionHandler).serve_forever()