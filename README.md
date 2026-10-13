# CORS Misconfiguration Scanner

A custom Python-based DAST (Dynamic Application Security Testing) tool designed to identify CORS (Cross-Origin Resource Sharing) misconfigurations. 

This tool was built from scratch to automate the discovery of reflected origin vulnerabilities, including subdomain trust issues and regex bypasses. It leverages concurrency for high-speed scanning and provides clear, color-coded terminal output.

## Features

*   **Subdomain Enumeration & Live Checking:** Automatically discovers live subdomains using RapidDNS and HackerTarget APIs.
*   **Dynamic Payload Generation:** Generates a comprehensive list of origin payloads, including:
    *   Basic arbitrary origins (`https://evil.com`)
    *   The `null` origin (sandboxed iframe bypass)
    *   Regex bypasses (Prefix/Suffix manipulation like `https://target.com.evil.com`)
    *   TLD swapping (`.com`, `.net`, `.org`, etc.)
    *   **Same-Site Subdomain Trust:** Tests if the API trusts other subdomains (`https://blog.target.com`), which can lead to ATO if an XSS exists on a sibling subdomain.
*   **Concurrent Scanning:** Uses `ThreadPoolExecutor` to send multiple requests simultaneously, significantly reducing scan time.
*   **Authenticated Testing:** Supports session cookies to test endpoints that require authentication.



## author

Linkedin: https://www.linkedin.com/in/mohamed-ahmed-664790433


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cors-scanner.git
   cd cors-scanner
   python3 cors.py




