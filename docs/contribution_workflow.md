## Documentation Contribution Workflow

This workflow defines the process for proposing, reviewing, and merging documentation changes.

### Overview

| Phase | Actor | Action |
|-------|-------|--------|
| Submit | Contributor | Create/edit markdown file, open PR with label |
| Review | Reviewer | Assess quality, leave feedback |
| Approve | Team Lead | Merge approved PRs to main |

### 1. Submitting a Contribution

1. **Create or edit** a markdown file in the `docs/` directory
2. **Commit** changes to a feature branch (not `main`)
3. **Open a PR** targeting `main` with:
   - Title format: `docs: <brief description>`
   - Label: `docs-contribution`
4. **Optional**: Record contribution in system (see Section 4)

### 2. Review Process

1. Team leads/reviewers are notified of PRs with `docs-contribution` label
2. Reviewers verify:
   - Clarity and accuracy
   - Style guide compliance
   - Proper formatting (headers, code blocks, links)
3. Review outcome:
   - **Approved**: Lead merges to `main`
   - **Changes requested**: Contributor updates PR, re-requests review

### 3. Approval & Merge Rules

- **Only Team Leads** can approve and merge documentation PRs
- **Squash merge** recommended to keep history clean
- **Auto-deployment**: GitHub Pages rebuilds automatically on merge

### 4. Integration with ContributionManager

The `ContributionManager` class provides programmatic tracking for:
- CI/CD integration (auto-log contributions)
- Dashboards showing contribution status
- Audit trails for compliance

**When to use:**
- Automated tracking via CI scripts
- Generating contribution reports
- Building custom review dashboards

**When NOT required:**
- Simple one-off documentation fixes
- Teams already using GitHub's native PR tracking

---

### 5. Search & Access

- **URL**: `https://<org>.github.io/<repo>/`
- **Search**: Built-in GitHub Pages search (or Algolia DocSearch for larger docs)
- **Versioning**: Tag releases for historical versions

---

**Key Principle**: The GitHub PR workflow is the source of truth. ContributionManager is an optional layer for teams wanting programmatic access to contribution data.