import itertools
import time
import requests
import argparse
import sys
import logging
from requests.exceptions import RequestException

# Suppress SSL warnings (if target has invalid SSL certificates)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up logging for both console and file output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bruteforce_output.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Function to generate 500,000 common website directories
def generate_directories(file_path='common_directories_500000.txt'):
    logging.info("Generating 500,000 common directories...")

    # Common prefixes: includes admin, dev, language-specific directories
    prefixes = [
        'admin', 'backup', 'test', 'dev', 'assets', 'config', 'upload', 'login', 'dashboard', 'panel',
        'portal', 'staging', 'user', 'private', 'secret', 'hidden', 'old', 'archive', 'db', 'db_backup',
        'root', 'public', 'server', 'download', 'data', 'secure', 'cpanel', 'manager', 'sys', 'file',
        'docs', 'logs', 'tmp', 'beta', 'release', 'site', 'setup', 'app', 'api', 'bin', 'core', 'static',
        # Language and framework-specific
        'php', 'python', 'node', 'javascript', 'ruby', 'perl', 'java', 'html', 'css', 'django', 'flask',
        'rails', 'express', 'laravel', 'symfony', 'codeigniter', 'spring', 'nestjs', 'nextjs', 'vue', 'react'
    ]

    # Common suffixes: includes versions, backups, and language/framework directories
    suffixes = [
        '1', '2', '3', '4', 'v1', 'v2', 'v3', 'backup', 'panel', 'login', 'data', 'db', 'test', 'new', 'old', 'archive',
        'secure', 'upload', 'files', 'logs', 'settings', 'images', 'temp', '2020', '2021', '2022', 'prod', 'beta', 'latest',
        # Language and framework-specific directories
        'node_modules', 'vendor', 'public', 'env', 'bin', 'lib', 'include', 'static', 'dist', 'src', 'build', 'target',
        'migrations', 'uploads', 'config', 'tmp', 'cache', 'views', 'components', 'controllers', 'models', 'routes'
    ]

    # Additional suffix modifiers for versions, environments, etc.
    more_suffixes = [
        '', 'alpha', 'beta', 'latest', 'staging', 'prod', 'dev', 'uat', 'preprod', 'final', 'live', 'preview', 'release', 'test'
    ]

    # Generate the directory combinations
    final_combinations = []
    for prefix, suffix in itertools.product(prefixes, suffixes):
        for extra_suffix in more_suffixes:
            directory = f"{prefix}/{suffix}{extra_suffix}"
            final_combinations.append(directory)

    # Limit the list to 500,000 directories
    final_combinations = final_combinations[:500000]

    # Write the directories to a file
    with open(file_path, 'w') as file:
        for directory in final_combinations:
            file.write(f"{directory}\n")

    logging.info(f"Generated {len(final_combinations)} directories and saved to '{file_path}'.")

# Function to check a directory
def check_directory(url, directory, timeout=10):
    """Check if a directory exists by sending a request."""
    full_url = f"{url.rstrip('/')}/{directory.strip()}/"  # Ensure proper URL format
    try:
        response = requests.get(full_url, timeout=timeout, verify=False)
        # Check if the directory exists (status codes 200 and 403 are typical signs)
        if response.status_code in [200, 403]:
            logging.info(f"[+] Found: {full_url} (Status: {response.status_code})")
            return full_url  # Return the full URL for further checks
        else:
            logging.info(f"[-] Not Found: {full_url} (Status: {response.status_code})")
    except RequestException as e:
        logging.error(f"[!] Error checking {full_url}: {e}")
    return None

# Function to check if a directory is publicly writable
def check_public_write(url, timeout=10):
    """Attempt to write to the directory using HTTP methods like PUT or POST."""
    try:
        # Attempt an HTTP PUT request to test for write permissions
        test_file_url = f"{url.rstrip('/')}/test_write.txt"
        response = requests.put(test_file_url, data="test", timeout=timeout, verify=False)

        if response.status_code in [201, 204]:
            logging.info(f"[!!] Publicly writable: {url}")
            # Log the publicly writable directory to a file
            with open('publiclywriteable.txt', 'a') as writable_file:
                writable_file.write(f"{url}\n")
            return True
    except RequestException as e:
        logging.error(f"[!] Error trying to write to {url}: {e}")
    return False

# Function to brute force directories using a wordlist
def brute_force_directories(url, wordlist, delay=0.5, timeout=10):
    """Brute force hidden directories using a wordlist."""
    try:
        with open(wordlist, 'r') as file:
            directories = file.readlines()
    except FileNotFoundError:
        logging.error(f"[!] Wordlist file '{wordlist}' not found.")
        sys.exit(1)

    logging.info(f"[~] Starting directory brute-forcing on: {url}")
    for directory in directories:
        directory_url = check_directory(url, directory, timeout=timeout)
        if directory_url:
            # Check if the found directory is publicly writable
            check_public_write(directory_url, timeout=timeout)
        time.sleep(delay)  # Add delay between requests to avoid rate-limiting or being blocked

def main():
    parser = argparse.ArgumentParser(description="Website Hidden Directory Brute Force with Auto-generated Wordlist")
    parser.add_argument("url", help="Target website URL (e.g., https://example.com)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout (in seconds)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between requests (in seconds)")
    parser.add_argument("--generate", action="store_true", help="Generate a 500,000 directory wordlist before scanning")
    args = parser.parse_args()

    # Check if the user wants to generate a new wordlist
    if args.generate:
        # Generate the 500,000 directory wordlist
        generate_directories()

    # Use the generated wordlist for brute forcing
    wordlist = 'common_directories_500000.txt'

    # Perform brute force directory checking
    brute_force_directories(args.url, wordlist, delay=args.delay, timeout=args.timeout)

if __name__ == '__main__':
    main()
