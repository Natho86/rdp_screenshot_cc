# Quick Start Guide

Get started with RDP screenshot capture in under 5 minutes!

## Prerequisites

- Python 3.9+ installed
- Network access to target RDP servers
- Targets with NLA (Network Level Authentication) disabled for login screen capture

## Installation

The project is already set up! The virtual environment and aardwolf library are installed.

## Quick Test

### 1. Test with a Single Target

```bash
./rdp_screenshot.py 192.168.1.100
```

Replace `192.168.1.100` with your target IP.

### 2. Test with Multiple Targets

Create a file called `targets.txt`:

```bash
cp targets.txt.example targets.txt
# Edit targets.txt with your actual targets
nano targets.txt
```

Run the scan:

```bash
./rdp_screenshot.py -f targets.txt
```

### 3. View Results

Screenshots will be saved in a timestamped directory:

```bash
ls rdp_screenshots_*
```

Open the PNG files to view captured screenshots:

```bash
# On Linux
xdg-open rdp_screenshots_*/rdpscreen_*.png

# On macOS
open rdp_screenshots_*/rdpscreen_*.png

# Or use your preferred image viewer
```

## Common Use Cases

### Internal Network Audit

Scan your internal servers to verify RDP configurations:

```bash
# Create targets file with your servers
echo "server1.internal" > my_servers.txt
echo "server2.internal" >> my_servers.txt
echo "10.0.0.50" >> my_servers.txt

# Run scan
./rdp_screenshot.py -f my_servers.txt -w 20 -t 15
```

### Penetration Test

Capture login screens during external pentest:

```bash
# Single target with custom timeout
./rdp_screenshot.py -t 30 203.0.113.100

# Multiple targets from recon
./rdp_screenshot.py -f discovered_rdp_hosts.txt -w 50
```

### Authenticated Screenshots

Capture post-login screenshots with credentials:

```bash
# NTLM authentication
./rdp_screenshot.py -u "rdp+ntlm-password://DOMAIN\\user:password@" 192.168.1.100

# For multiple servers
./rdp_screenshot.py -u "rdp+ntlm-password://DOMAIN\\user:password@" -f servers.txt
```

## Troubleshooting Quick Fixes

### No screenshots captured?

1. **Check if target is reachable:**
   ```bash
   ping 192.168.1.100
   ```

2. **Check if RDP port is open:**
   ```bash
   nmap -p 3389 192.168.1.100
   # or
   nc -zv 192.168.1.100 3389
   ```

3. **Increase timeout:**
   ```bash
   ./rdp_screenshot.py -t 30 192.168.1.100
   ```

4. **Check if NLA is disabled** (for login screen capture):
   - Login screen capture only works when NLA is disabled
   - If NLA is enabled, you need credentials

### Permission denied?

Make sure the script is executable:

```bash
chmod +x rdp_screenshot.py
```

### Virtual environment issues?

Verify aardwolf is installed:

```bash
./venv/bin/pip list | grep aardwolf
```

If not installed:

```bash
./venv/bin/pip install aardwolf
```

## Tips for Success

1. **Start small**: Test with 1-2 targets first
2. **Adjust workers**: Use `-w 50` for faster scans of many targets
3. **Set appropriate timeout**: `-t 15` or `-t 30` for slow networks
4. **Check NLA status**: Login screen capture requires NLA to be disabled
5. **Use credentials**: If NLA is enabled, provide valid credentials with `-u`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize worker count and timeout for your network
- Set up target lists for recurring scans
- Integrate into your security testing workflow

## Getting Help

If you encounter issues:

1. Check the [README.md](README.md) troubleshooting section
2. Verify network connectivity and RDP availability
3. Review ardpscan output for specific error messages
4. Visit https://github.com/skelsec/aardwolf for aardwolf library issues

## Safety and Ethics

Always ensure you have proper authorization before scanning any network or system you don't own. Unauthorized access to computer systems is illegal in most jurisdictions.

This tool is intended for:
- Authorized security assessments
- Penetration testing with explicit permission
- Internal network auditing
- Educational purposes in lab environments
