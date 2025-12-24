#!/bin/bash
set -euo pipefail

# Record timestamp and Python version
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
python_version=$(python3 --version | tr -d '\n')

# Write full pip freeze and compute its hash
pip_freeze_file="submission/pip_freeze.txt"
python3 -m pip freeze > "$pip_freeze_file"
pip_freeze_sha=$(sha256sum "$pip_freeze_file" | awk '{print $1}')

# Define input and output paths
input_file="raw/bpi_incidents_ledger.csv"
output_dir="submission/derived"
mkdir -p "$output_dir"

# Compute input hash
input_sha=$(sha256sum "$input_file" | awk '{print $1}')

# Build and run the harness command
cmd="python3 occ_harness.py --ledger $input_file --horizon_days 30 --window_days 90 --output_dir $output_dir"
rm -f "$output_dir"/timeseries.csv "$output_dir"/diagnostics.json || true
eval "$cmd"

# Compute output hashes
ts_sha=$(sha256sum "$output_dir/timeseries.csv" | awk '{print $1}')
diag_sha=$(sha256sum "$output_dir/diagnostics.json" | awk '{print $1}')

# Write run log
cat <<EOF > submission/RUNLOG.txt
timestamp: $timestamp
python_version: $python_version
input_sha256: $input_sha
pip_freeze_sha256: $pip_freeze_sha
command: $cmd
output_hashes:
  timeseries.csv: $ts_sha
  diagnostics.json: $diag_sha
EOF
