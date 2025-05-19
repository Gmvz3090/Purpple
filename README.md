
## Overview

Purpple is an open-source pentesting framework designed to streamline security testing by integrating multiple modules into a single, cohesive platform. It is tailored for both security professionals and enthusiasts who want a modular, extensible approach to penetration testing.

## ⚡ Quick start

```bash
# 1. Clone
git clone https://github.com/Gmvz3090/Purpple.git
cd Purpple

# 2. Dev install
pip install -e .

# 3. One-time API-key helper
python setup.py  # or simply run `purpple` and follow the prompts

# 4. Launch
purpple
````

The first run walks you through optional keys and stores them in `PurppleFramework.config.Config` for the current process only. ([GitHub][1])

**Prerequisites**

| Tool            | Status                                                        |
| --------------- | ------------------------------------------------------------- |
| Python 3.9-3.12 | interpreter only                                              |
| nmap ≥ 7.x      | needed for `Scanning → Nmap` & `Exploit Search` ([GitHub][2]) |
| tcpdump / root  | (recommended) to let Scapy sniff on privileged ports          |

---

## 🏗️ Project layout

```
PurppleFramework/
├─ cli/                # command-line entry & interactive menu
│  ├─ main.py
│  └─ menu.py          # module selector & dispatcher
├─ config.py           # in-memory API tokens
├─ modules/
│  └─ Red/
│     ├─ OSINT/        # shodan_search, censys_search, …
│     ├─ Scanning/     # nmap_scanner, crawler, ssltls
│     ├─ ExploitSearch/
│     ├─ WebVuln/      # xss, sqli, lfi, cors, apichecker
│     └─ Sniffer/      # live sniffer & summariser
└─ txts/               # runtime-generated lists (urls.txt, etc.)
```

Each sub-package exposes a `run_*` helper consumed by `cli/menu.py`, so you can bolt in new modules with minimal wiring. ([GitHub][3], [GitHub][4], [GitHub][5])

---

---

## 🤝 Contributing

1. Fork → create a feature branch.
2. Place new code in a suitably named sub-module under `modules/Red` or `modules/Blue`.
3. Add a checkbox label in `cli/menu.py` and call your `run_<feature>()`.
4. Run `black`/`ruff`, ensure it works on both **Python 3.10** and **3.12**.
5. Open a pull-request – tests and demo output screenshot appreciated!

---

## 🛣️ Roadmap

* **Report exporter** – markdown / HTML summaries after each module run.
* **Docker wrapper** – friction-free lab deploy.
  Feel free to raise issues with ideas or vote on existing ones.

---

## ⚖️ License & legal

Purpple ships under the **MIT licence** – do whatever you want, but **only** against systems you own *or* have *explicit written permission* to test.
The authors accept **no liability** for misuse. ([GitHub][1])

```

*Happy hacking – and don’t forget to ⭐ the project if it saves you time!*


