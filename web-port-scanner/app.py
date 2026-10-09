import socket  # Provides access to lower-level networking primitives (used here to open raw TCP connections for port scanning).
import requests  # An HTTP library used to make web requests easily (GET, POST, etc.) for directory fuzzing.

# ==========================================
# 1. Configuration Settings
# ==========================================

# Target host to scan. "127.0.0.1" refers to 'localhost' (your own machine).
target_host = "127.0.0.1"

# List of common network ports to probe during Phase 1:
# 21: FTP, 22: SSH, 80: HTTP, 443: HTTPS, 8080: Alternative HTTP port.
port_list = [21, 22, 80, 443, 8080]

# List of common directory/endpoint paths to test on discovered web servers in Phase 2.
word_list = ["admin", "login", "uploads", "backup"]

# Standard HTTP Request Headers sent with every HTTP request:
# - User-Agent identifies the client making the request.
# - Accept tells the server what content formats the client prefers.
# - Connection: 'close' tells the server to close the connection after responding (prevents persistent connection overhead).
http_headers = {
    'User-Agent': 'MyCustomSecurityScanner/1.0 (+http://127.0.0.1)',
    'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9, */*;q=0.8',
    'Accept-Language': 'en-US, en;q=0.5',
    'Connection': 'close'
}


# ==========================================
# 2. Phase 1 Function (Port Scanner)
# ==========================================
def scan_ports(host, ports):
    """
    Scans a given host over a list of TCP ports to identify which ones are open.
    Returns a list of open ports that support HTTP web traffic (80, 443, 8080).
    """
    print(f"\n--- [Phase 1] Scanning Ports on {host} ---")
    
    # Initialize an empty list to store ports that are both open and host web services.
    open_web_ports = []

    # Iterate through each port in the provided list
    for port in ports:
        # Create a new socket object:
        # - socket.AF_INET specifies IPv4 addressing.
        # - socket.SOCK_STREAM specifies TCP protocol (connection-oriented).
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a connection timeout of 1.5 seconds so the script doesn't hang indefinitely on closed/filtered ports.
        s.settimeout(1.5)
        
        # Attempt to connect to the target (host, port) pair.
        # connect_ex() returns 0 on successful TCP handshake; otherwise, it returns an error code integer.
        result = s.connect_ex((host, port))
        
        # Check if the connection attempt succeeded
        if result == 0:
            print(f"[+] Port {port} is OPEN")
            
            # Filter specifically for common HTTP/web application ports
            if port in [80, 443, 8080]:
                open_web_ports.append(port)
        else:
            print(f"[-] Port {port} is CLOSED")
            
        # Close the socket object to free system resources before checking the next port.
        s.close()
        
    # Return the list of open web ports to the caller.
    return open_web_ports


# ==========================================
# 3. Phase 2 Function (Directory Fuzzer)
# ==========================================
def fuzz_directories(host, port, wordlist):
    """
    Takes an active host and web port, constructs full URLs for each entry in the wordlist,
    and checks if the endpoints exist on the web server.
    """
    # Construct the root URL for the web server (e.g., http://127.0.0.1:80)
    base_url = f"http://{host}:{port}"
    print(f"\n--- [Phase 2] Fuzzing Directories on {base_url} ---")

    # Iterate through each word (directory/endpoint) in the wordlist
    for endpoint in wordlist:
        # Combine base URL and endpoint (e.g., http://127.0.0.1:80/admin)
        full_url = f"{base_url}/{endpoint}"
        
        try:
            # Send an HTTP GET request to the target URL.
            # - headers: Custom headers defined above.
            # - timeout: Wait a maximum of 2.0 seconds for the server to respond.
            response = requests.get(full_url, headers=http_headers, timeout=2.0)
            
            # HTTP 200 OK: The directory/page exists and is accessible.
            if response.status_code == 200:
                print(f"[+] FOUND (200 OK)    : {full_url}")
                
            # HTTP 403 Forbidden: The directory exists, but access is restricted.
            elif response.status_code == 403:
                print(f"[!] FORBIDDEN (403)   : {full_url}")
                
        # Handle exceptions gracefully (e.g., connection timeouts, DNS failures, or unreachable hosts).
        except requests.exceptions.RequestException:
            # Skip the current endpoint and continue fuzzing the next item in the wordlist.
            continue


# ==========================================
# 4. Main Execution Block
# ==========================================
# This check ensures the code inside runs only when the file is executed directly 
# (e.g., `python script.py`), not when imported as a module in another script.
if __name__ == "__main__":
    
    # Step A: Run Phase 1 port scan to identify open web ports on target_host.
    discovered_ports = scan_ports(target_host, port_list)
    
    # Step B: Check if any web-capable open ports were found during Phase 1.
    if discovered_ports:
        # Iterate over each discovered web port and perform Phase 2 directory fuzzing.
        for web_port in discovered_ports:
            fuzz_directories(target_host, web_port, word_list)
    else:
        # Output message if no web ports responded during Phase 1.
        print("\n[-] No open web ports found to fuzz.")