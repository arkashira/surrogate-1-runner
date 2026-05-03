- name: Generate file manifest (Mac/runner)
  run: |
    python tools/snapshot_manifest.py --date $(date +%Y-%m-%d) --out file_manifest.json
  env:
    HF_TOKEN: ${{ secrets.HF_TOKEN }}