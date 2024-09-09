Website Hidden Directory Brute Force Script

This script is designed to perform brute force discovery of hidden directories on a target website using a wordlist. It can also check for publicly writable directories, making it useful for security assessments. The script includes an option to generate a wordlist of 500,000 common directories and uses the generated wordlist for the brute-forcing process.
Features

    Directory Discovery: Brute forces directories using a customizable wordlist.
    Wordlist Generation: Option to generate a wordlist of 500,000 common directories based on predefined prefixes and suffixes.
    Public Write Check: Automatically attempts to identify directories that are publicly writable.
    Logging: Logs results both to the console and to a file (bruteforce_output.log).
    Delay and Timeout Options: Customizable delay between requests to prevent rate-limiting, and adjustable request timeouts.

Requirements

    Python 3.x
    requests library (pip install requests)
    Disable SSL warnings for invalid certificates using urllib3.

Installation

    Clone the repository or download the script.
    Install required Python dependencies:

    bash

    pip install requests

Usage

    Basic Usage: To perform brute-force directory discovery on a target website, provide the URL as an argument:

    bash

python bruteforce.py https://example.com

Generate Wordlist: To generate a wordlist of 500,000 directories before starting the brute force process, use the --generate option:

bash

python bruteforce.py https://example.com --generate

Custom Timeout: To specify a custom timeout for each request, use the --timeout argument (default is 10 seconds):

bash

python bruteforce.py https://example.com --timeout 15

Custom Delay: To specify a delay between requests (useful to avoid rate-limiting or blocking), use the --delay argument (default is 0.5 seconds):

bash

    python bruteforce.py https://example.com --delay 1

Example

bash

python bruteforce.py https://example.com --generate --timeout 15 --delay 0.5

This command will generate a wordlist, use it to brute-force directories on https://example.com with a 15-second request timeout and a 0.5-second delay between requests.
Logs

    All log messages are saved in the bruteforce_output.log file, including found directories and publicly writable directories.
    Publicly writable directories are also saved to a separate file publiclywriteable.txt.

Script Functions

    generate_directories(file_path): Generates 500,000 common directory paths and writes them to the specified file.
    check_directory(url, directory, timeout): Sends a GET request to check if the directory exists on the target URL.
    check_public_write(url, timeout): Attempts to write a test file to the directory to check for public write permissions.
    brute_force_directories(url, wordlist, delay, timeout): Reads the wordlist and performs brute force directory discovery on the target URL.

Notes

    The script automatically disables SSL warnings when dealing with websites that have invalid SSL certificates.
    Ensure that you have the appropriate permissions to scan the target website.

Disclaimer

This tool is for educational purposes only. Unauthorized use of this script on websites you do not own or have permission to test may be illegal. Always ensure you have proper authorization before running security assessments on any system.
License

This project is licensed under the MIT License.
