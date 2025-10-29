# RDP Screenshot Capture Tool

A Python script to capture screenshots of RDP (Remote Desktop Protocol) login screens from single targets or lists of targets. Built using the [aardwolf](https://github.com/skelsec/aardwolf) asynchronous RDP client library.

## Features

- Capture RDP login screen screenshots without authentication
- Support for single target or multiple targets
- Read targets from file (one per line)
- Parallel scanning with configurable worker count
- Customizable connection timeout
- Timestamped output directories
- Support for various RDP authentication methods (NTLM, Kerberos, etc.)

## Installation

1. **Clone and setup** (already completed):
   ```bash
   cd /home/nath/claude/rdp_screenshot_cc
   ```

2. **Virtual environment and dependencies** (already installed):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install aardwolf
   ```

## Usage

### Basic Usage

**Single target:**
```bash
./rdp_screenshot.py 192.168.1.100
```

**Multiple targets:**
```bash
./rdp_screenshot.py 192.168.1.100 192.168.1.101 192.168.1.102
```

**Targets from file:**
```bash
./rdp_screenshot.py -f targets.txt
```

### Advanced Usage

**Custom workers and timeout:**
```bash
./rdp_screenshot.py -w 50 -t 15 -f targets.txt
```

**Specify output directory:**
```bash
./rdp_screenshot.py -o my_rdp_scans 192.168.1.100
```

**With authentication (NTLM):**
```bash
./rdp_screenshot.py -u "rdp+ntlm-password://DOMAIN\\user:pass@" 192.168.1.100
```

**With authentication (Kerberos):**
```bash
./rdp_screenshot.py -u "rdp+kerberos-password://DOMAIN\\user:pass@win2019ad.test.corp/?dc=10.10.10.2" 192.168.1.100
```

### Command Line Options

```
positional arguments:
  targets               Target IP addresses or hostnames

options:
  -h, --help            Show help message
  -f FILE, --file FILE  File containing target IPs/hostnames (one per line)
  -u URL, --url URL     RDP connection URL template (default: rdp://)
  -w WORKERS, --workers WORKERS
                        Number of parallel workers (default: 10)
  -t TIMEOUT, --timeout TIMEOUT
                        Connection timeout in seconds (default: 10)
  -o OUTPUT, --output OUTPUT
                        Output directory (default: rdp_screenshots_TIMESTAMP)
```

## Target File Format

Create a text file with one target per line:

```
192.168.1.100
192.168.1.101
server.example.com
10.0.0.50
```

Example: `targets.txt`

## Output

Screenshots are saved in a timestamped directory (or custom directory if specified):
- Directory: `rdp_screenshots_YYYYMMDD_HHMMSS/`
- Screenshots: `rdpscreen_<target>_<timestamp>.png`
- Results file: `screenshots.tsv` (tab-separated values with base64 encoded data)

## RDP URL Format

The tool supports various RDP authentication methods through URL format:

### No Authentication (Login Screen Capture)
```
rdp://
```
**Note:** Only works when NLA (Network Level Authentication) is disabled on the server.

### With Credentials (Post-Login Screenshots)

**NTLM Authentication:**
```
rdp+ntlm-password://DOMAIN\user:password@
```

**Kerberos Authentication:**
```
rdp+kerberos-password://DOMAIN\user:password@target/?dc=10.10.10.2
```

**Plain Authentication (Old RDP):**
```
rdp+plain://user:password@
```

**Pass-the-Hash (NTLM):**
```
rdp+ntlm-password://DOMAIN\user:<NThash>@
```

### Additional URL Parameters

Add parameters to the URL using query string format:

```
rdp://target/?timeout=15&proxytype=socks5&proxyhost=127.0.0.1&proxyport=1080
```

**Common parameters:**
- `timeout` - Connection timeout in seconds
- `dc` - Domain controller IP (for Kerberos)
- `proxytype` - Proxy type (socks4, socks5, http)
- `proxyhost` - Proxy server address
- `proxyport` - Proxy server port

## Important Notes

### Network Level Authentication (NLA)

- **Login screen capture** (no auth) only works when NLA is **disabled**
- Most modern Windows servers have NLA **enabled** by default
- To capture login screens, targets must have NLA disabled
- For NLA-enabled servers, you need valid credentials

### Firewall and Network

- Ensure RDP port (default 3389) is accessible
- Check firewall rules on scanning machine and targets
- Consider network segmentation and routing

### Legal and Ethical Use

This tool is intended for:
- Authorized security assessments
- Penetration testing with proper authorization
- Internal network auditing
- Educational purposes in controlled environments

**Always obtain proper authorization before scanning networks you don't own.**

## Troubleshooting

### No screenshots captured

**Possible causes:**
1. **NLA is enabled** - Cannot capture login screens without disabling NLA
2. **Firewall blocking** - RDP port (3389) is not accessible
3. **RDP not enabled** - Remote Desktop is not enabled on target
4. **Network issues** - Target is not reachable
5. **Timeout too short** - Increase timeout with `-t` option

**Solutions:**
- Verify RDP is enabled: `nmap -p 3389 <target>`
- Check NLA status on Windows:
  ```powershell
  (Get-WmiObject -Class Win32_TSGeneralSetting -Namespace root\cimv2\TerminalServices).UserAuthenticationRequired
  ```
  (Returns 1 if NLA is enabled, 0 if disabled)
- Increase timeout: `-t 30`
- Increase workers for faster scanning: `-w 50`

### Connection errors

- Verify network connectivity: `ping <target>`
- Check if RDP port is open: `telnet <target> 3389` or `nc -zv <target> 3389`
- Try with verbose logging (modify script to add logging)

## Direct Usage of ardpscan

You can also use the `ardpscan` command directly:

```bash
./venv/bin/ardpscan -s screen -w 10 -t 10 -o output.tsv rdp:// 192.168.1.100 192.168.1.101
```

## Technical Details

### Built on Aardwolf

This tool uses [aardwolf](https://github.com/skelsec/aardwolf), an asynchronous RDP/VNC client library for Python:
- Headless operation (no GUI required)
- Async/await support for concurrent connections
- Multiple authentication methods (NTLM, Kerberos, Plain)
- CredSSP support for Network Level Authentication
- Built-in proxy support (SOCKS/HTTP)

### How it Works

1. Creates RDP connection to target
2. Waits for screen data (default 5 seconds)
3. Captures desktop buffer as PNG image
4. Saves screenshot to output directory
5. Terminates connection

### Performance

- Default: 10 parallel workers
- Recommended for large scans: 50-100 workers (adjust based on network capacity)
- Each connection has independent timeout
- Failed connections don't block other workers

## Examples

### Quick Scan

Scan a single server:
```bash
./rdp_screenshot.py 192.168.1.100
```

### Department Scan

Scan all servers in a department (from file):
```bash
./rdp_screenshot.py -f department_servers.txt -w 25
```

### Authenticated Scan

Capture post-login screenshots with credentials:
```bash
./rdp_screenshot.py -u "rdp+ntlm-password://CORP\\admin:P@ssw0rd@" -f servers.txt
```

### Fast Scan

High-speed scan with many workers:
```bash
./rdp_screenshot.py -f large_target_list.txt -w 100 -t 5
```

### Through Proxy

Scan through SOCKS proxy:
```bash
./rdp_screenshot.py -u "rdp://?proxytype=socks5&proxyhost=127.0.0.1&proxyport=1080" 192.168.1.100
```

## License

This project uses the aardwolf library. See the aardwolf directory for its license.

## Credits

- **Aardwolf** - [@skelsec](https://github.com/skelsec/aardwolf) - Asynchronous RDP client library
- Built for penetration testing and security assessments

## Support

For issues with:
- **This wrapper script** - Check this README or modify the script
- **Aardwolf library** - Visit https://github.com/skelsec/aardwolf
- **RDP protocol** - Consult Microsoft RDP documentation
