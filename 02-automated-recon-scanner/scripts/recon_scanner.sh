#!/usr/bin/env bash
# Automated Nmap Attack Surface Scanner & Report Generator
# Author: Obiwan Obibo (BitzMiner322)
# Usage: ./recon_scanner.sh <target_ip_or_hostname>

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <target_ip_or_hostname>"
  echo "Example: $0 127.0.0.1"
  exit 1
fi

TARGET="$1"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
REPORT_DIR="./reports"
REPORT_FILE="${REPORT_DIR}/recon_${TARGET}_${TIMESTAMP}.txt"

mkdir -p "$REPORT_DIR"

echo "=================================================="
echo "[*] Starting Automated Attack Surface Scan"
echo "[*] Target: $TARGET"
echo "[*] Timestamp: $TIMESTAMP"
echo "=================================================="

nmap -sV -sC -T4 --open "$TARGET" -oN "$REPORT_FILE"

echo ""
echo "=================================================="
echo "[+] Scan Complete! Summary of Exposed Services:"
echo "=================================================="
grep -E "^[0-9]+/(tcp|udp).*open" "$REPORT_FILE" || echo "No open ports detected."
echo ""
echo "[+] Full report saved to: $REPORT_FILE"
