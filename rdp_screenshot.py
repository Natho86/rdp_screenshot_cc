#!/usr/bin/env python3
"""
RDP Screenshot Tool
Captures screenshots of RDP login screens from single or multiple targets.
Uses the aardwolf library for RDP connections.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


def create_output_dir():
    """Create timestamped output directory for screenshots."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"rdp_screenshots_{timestamp}")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def run_screenshot(url, targets, output_file, workers=10, timeout=10):
    """
    Run ardpscan to capture screenshots.

    Args:
        url: RDP connection URL (e.g., 'rdp://target')
        targets: List of target IPs/hostnames or path to file
        output_file: Path to output file
        workers: Number of parallel workers
        timeout: Connection timeout in seconds
    """
    venv_path = Path(__file__).parent / "venv" / "bin" / "ardpscan"

    cmd = [
        str(venv_path),
        "-s", "screen",
        "-w", str(workers),
        "-t", str(timeout),
        "-o", str(output_file),
        url
    ] + targets

    print(f"[*] Running: {' '.join(cmd)}")
    print(f"[*] Output will be saved to: {output_file}")
    print(f"[*] Starting scan with {workers} workers, {timeout}s timeout...")
    print()

    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running ardpscan: {e}")
        return False
    except FileNotFoundError:
        print(f"[!] Error: ardpscan not found. Make sure aardwolf is installed in the venv.")
        print(f"[!] Expected path: {venv_path}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Capture RDP login screen screenshots",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single target
  %(prog)s 192.168.1.100

  # Multiple targets from command line
  %(prog)s 192.168.1.100 192.168.1.101 192.168.1.102

  # Targets from file (one per line)
  %(prog)s -f targets.txt

  # With authentication (NTLM)
  %(prog)s -u "rdp+ntlm-password://DOMAIN\\user:pass@" 192.168.1.100

  # Custom workers and timeout
  %(prog)s -w 50 -t 15 -f targets.txt

Note: For capturing login screens, use 'rdp://' (no authentication).
      This only works when NLA (Network Level Authentication) is disabled.
        """
    )

    parser.add_argument(
        'targets',
        nargs='*',
        help='Target IP addresses or hostnames'
    )

    parser.add_argument(
        '-f', '--file',
        help='File containing target IPs/hostnames (one per line)'
    )

    parser.add_argument(
        '-u', '--url',
        default='rdp://',
        help='RDP connection URL template (default: rdp://)'
    )

    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=10,
        help='Number of parallel workers (default: 10)'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='Connection timeout in seconds (default: 10)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output directory (default: rdp_screenshots_TIMESTAMP)'
    )

    args = parser.parse_args()

    # Collect targets
    target_list = []

    if args.file:
        if not os.path.exists(args.file):
            print(f"[!] Error: Target file not found: {args.file}")
            return 1
        target_list.append(args.file)

    if args.targets:
        target_list.extend(args.targets)

    if not target_list:
        print("[!] Error: No targets specified. Use targets as arguments or -f/--file option.")
        parser.print_help()
        return 1

    # Create output directory
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True)
    else:
        output_dir = create_output_dir()

    output_file = output_dir / "screenshots.tsv"

    print("=" * 60)
    print("RDP Screenshot Capture Tool")
    print("=" * 60)
    print(f"URL Template: {args.url}")
    print(f"Targets: {len(target_list)} target(s) or file(s)")
    print(f"Workers: {args.workers}")
    print(f"Timeout: {args.timeout}s")
    print(f"Output: {output_dir}")
    print("=" * 60)
    print()

    # Prepare URL for ardpscan
    url = args.url
    # If URL has credentials but no @ at the end, add it
    if '://' in url and '@' not in url and not url.endswith('//'):
        url += '@'

    success = run_screenshot(url, target_list, output_file, args.workers, args.timeout)

    if success:
        print()
        print("=" * 60)
        print("[+] Scan completed successfully!")
        print(f"[+] Screenshots saved to: {output_dir}")
        print(f"[+] Results file: {output_file}")

        # Check if any screenshots were captured
        png_files = list(output_dir.glob("*.png"))
        if png_files:
            print(f"[+] Captured {len(png_files)} screenshot(s)")
        else:
            print("[!] No screenshots were captured. This could mean:")
            print("    - Targets are not reachable")
            print("    - RDP is not enabled on targets")
            print("    - Network Level Authentication (NLA) is enabled")
        print("=" * 60)
        return 0
    else:
        print()
        print("[!] Scan failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
