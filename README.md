
## Overview

Purpple is an open-source pentesting framework designed to streamline security testing by integrating multiple modules into a single, cohesive platform. It is tailored for both security professionals and enthusiasts who want a modular, extensible approach to penetration testing.

## Features

- **Modular Architecture:**  
  Organized into clearly defined modules to handle various aspects of pentesting, including OSINT, Scanning, Exploit Searches, and more.

- **CLI & Web GUI:**  
  Launch the framework via the command line or the upcoming web interface.

- **Easy Setup:**  
  Simple installation process using Python’s package management tools.

## Modules

- **CLI:**  
  Provides a command-line interface (CLI) to navigate and control the framework.

- **Modules Package:**  
  - **Blue:** (Placeholder for defensive or monitoring tools)
  - **Red:** Offensive tools including:
    - **ExploitSearch:** Tools to search and manage exploits.
    - **OSINT:** Open-source intelligence gathering utilities.
    - **Phishing:** Simulated phishing attack modules.
    - **Scanning:** Network and vulnerability scanning tools.
    - **Sniffer:** Network packet capturing and analysis.
    - **WebVuln:** Web vulnerability assessments, including tests for SQL injection, XSS, LFI, etc.

- **TXT Files:**  
  Contains auxiliary files such as API keys and URL lists.

## Installation

### Prerequisites

- **Python 3.12+**
- Virtual environment (recommended)

### Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/Purpple.git
   cd Purpple
   ```bash
2. **Install in editable mode:**

   ```bash
   pip install -e .
   
3. **Use**

   You can use it by writing
   ```bash
   Purpple
   
**WARNING**

I do not condone any malicious activity, this project is for **Education purpose ONLY**.
