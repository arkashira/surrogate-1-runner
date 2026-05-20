#!/usr/bin/env bash
# .github/actions/format/entrypoint.sh
# ------------------------------------------------------------
# Format‑check + diff‑summary generator
# ------------------------------------------------------------
set -euo pipefail
IFS=$'\n\t'

# ---------- Configuration ----------
IGNORE_FILE=".surrogateignore"
# Extensions we know how to format
EXTS=("js" "ts" "json" "md" "py" "yaml" "yml")

# ---------- Helper: ignore logic ----------
should_ignore() {
    local path="$1"
    # No ignore file → nothing to ignore
    [[ -f "$IGNORE_FILE" ]] || return 1

    while IFS= read -r pattern || [[ -n "$pattern" ]]; do
        # Strip leading/trailing whitespace
        pattern="${pattern#"${pattern%%[![:space:]]*}"}"
        pattern="${pattern%"${pattern##*[![:space:]]}"}"
        # Skip blanks & comments
        [[ -z "$pattern" || "$pattern" == \#* ]] && continue
        # Convert a simple glob to a regex‑compatible pattern
        # (bash's [[ $path == $pattern ]] already supports globs)
        if [[ "$path" == $pattern ]]; then
            return 0   # match → ignore
        fi
    done < "$IGNORE_FILE"
    return 1           # no match → do NOT ignore
}

# ---------- Helper: run a formatter in “check” mode ----------
run_formatter() {
    local file="$1"
    case "${file##*.}" in
        js|ts|json|md)
            # prettier must be installed in the runner (preinstalled on ubuntu‑latest)
            prettier --check "$file" >/dev/null 2>&1 && return 0 || return 1
            ;;
        py)
            # black must be installed (we install it in the workflow)
            black --check "$file" >/dev/null 2>&1 && return 0 || return 1
            ;;
        yaml|yml)
            # yamllint – we use a permissive config that only cares about tabs/CRLF
            yamllint -d "{extends: relaxed, rules: {line-length: {max: 0}}}" "$file" >/dev/null 2>&1 && return 0 || return 1
            ;;
        *)
            return 0   # unknown extension → treat as “already ok”
            ;;
    esac
}

# ---------- Temp directory for intermediate files ----------
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

DIFF_SUMMARY="$TMPDIR/diff_summary.txt"
FORMAT_ISSUES="$TMPDIR/formatting_issues.txt"

# Initialise output files
printf "## Diff Summary\n\n" > "$DIFF_SUMMARY"
printf "" > "$FORMAT_ISSUES"

# ---------- Counters ----------
total=0 formatted=0 needs_format=0 ignored=0

# ---------- Main file walk ----------
while IFS= read -r -d '' file; do
    rel="${file#./}"               # path relative to repo root

    # Skip ignored files
    if should_ignore "$rel"; then
        ((ignored++))
        continue
    fi

    ((total++))

    # Run the appropriate formatter in check‑only mode
    if run_formatter "$rel"; then
        ((formatted++))
    else
        ((needs_format++))
        echo "$rel" >> "$FORMAT_ISSUES"
    fi
done < <(find . -type f \
            \( -name "*.js" -o -name "*.ts" -o -name "*.json" -o -name "*.md" \
               -o -name "*.py" -o -name "*.yaml" -o -name "*.yml" \) \
            -not -path '*/.git/*' -not -path '*/node_modules/*' -print0)

# ---------- Build the human‑readable summary ----------
{
    echo "### Files checked: $total"
    echo "- Properly formatted: $formatted"
    echo "- Need formatting:   $needs_format"
    echo "- Ignored:            $ignored"
    echo ""

    if (( needs_format > 0 )); then
        echo "### Files that need formatting"
        echo ""
        while IFS= read -r f; do
            echo "- \`$f\`"
        done < "$FORMAT_ISSUES"
    else
        echo "All checked files are correctly formatted 🎉"
    fi
} >> "$DIFF_SUMMARY"

# ---------- Emit artifacts for the workflow ----------
cp "$DIFF_SUMMARY"   diff_summary.txt
cp "$FORMAT_ISSUES"  formatting_issues.txt

# ---------- Exit status ----------
if (( needs_format > 0 )); then
    echo "Formatting problems detected – see diff_summary.txt"
    exit 1
else
    echo "✅ No formatting problems."
    exit 0
fi