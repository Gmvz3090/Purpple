# PurppleFramework/cli/setup.py
import questionary
from PurppleFramework.config import Config
from setuptools import setup, find_packages

setup(
    name='PurppleFramework',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'purpple=PurppleFramework.cli.main:main'
        ]
    }
)

def one_time_setup():
    print("\n=== One-Time API Key Setup ===")
    print("Press Enter to skip any key you don't have.\n")

    vt_api = questionary.text("Enter VirusTotal API key (optional):").ask()
    st_api = questionary.text("Enter SecurityTrails API key (optional):").ask()
    shodan_api = questionary.text("Enter Shodan API key (optional):").ask()
    censys_id = questionary.text("Enter Censys API ID (optional):").ask()
    censys_secret = questionary.text("Enter Censys API secret (optional):").ask()

    # Store them in Config (None if the user left it blank)
    Config.vt_api_key = vt_api.strip() or None
    Config.st_api_key = st_api.strip() or None
    Config.shodan_api_key = shodan_api.strip() or None
    Config.censys_id = censys_id.strip() or None
    Config.censys_secret = censys_secret.strip() or None

    print("\n[*] Setup complete. Your API keys are now stored in memory.")
    print("    They will be used automatically for OSINT modules.\n")
