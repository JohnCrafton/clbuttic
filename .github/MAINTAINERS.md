# Maintainer Guide

This document contains setup instructions and guidelines for project maintainers.

## Initial Setup Checklist

After pushing to GitHub, complete these steps in the GitHub web UI:

### 1. Branch Protection Rules

Go to **Settings > Branches > Add branch protection rule**

For the `main` branch, enable:

- [x] **Require a pull request before merging**
  - [x] Require approvals: 1 (adjust based on team size)
  - [x] Dismiss stale pull request approvals when new commits are pushed
  - [x] Require approval of the most recent reviewable push

- [x] **Require status checks to pass before merging** (once CI is set up)
  - [x] Require branches to be up to date before merging

- [x] **Require conversation resolution before merging**

- [x] **Do not allow bypassing the above settings**
  - Even admins should go through PRs for accountability

- [x] **Restrict who can push to matching branches** (optional)
  - Add specific maintainers if desired

- [x] **Block force pushes**

- [x] **Block deletions**

### 2. Enable GitHub Discussions

Go to **Settings > General > Features**

- [x] Enable Discussions (for Q&A, ideas, etc.)

### 3. Configure Security Settings

Go to **Settings > Security**

- [x] Enable Dependabot alerts (if using dependencies later)
- [x] Enable Secret scanning

Go to **Settings > Code security and analysis**

- [x] Enable Dependency graph
- [x] Enable Dependabot security updates

### 4. Set Up Labels

Recommended labels for issues:

| Label | Color | Description |
|-------|-------|-------------|
| `word-list` | #0E8A16 | Changes to word lists |
| `addition` | #84B6EB | Adding new words |
| `false-positive` | #FBCA04 | Allowlist additions |
| `bug` | #D73A4A | Something isn't working |
| `enhancement` | #A2EEEF | New feature or request |
| `documentation` | #0075CA | Documentation only |
| `good first issue` | #7057FF | Good for newcomers |
| `help wanted` | #008672 | Extra attention needed |
| `wontfix` | #FFFFFF | Won't be worked on |
| `duplicate` | #CFD3D7 | Duplicate issue |
| `invalid` | #E4E669 | Not valid |
| `question` | #D876E3 | Further info requested |
| `lang:en` | #BFD4F2 | English language |
| `lang:es` | #BFD4F2 | Spanish language |
| `lang:fr` | #BFD4F2 | French language |
| `lang:de` | #BFD4F2 | German language |
| `lang:pt` | #BFD4F2 | Portuguese language |

### 5. Update Placeholder Text

Search and replace these placeholders in the repository:

- ~~`[INSERT CONTACT EMAIL]` in CODE_OF_CONDUCT.md~~ Done: john@crafton.dev
- ~~`[INSERT SECURITY EMAIL]` in .github/SECURITY.md~~ Done: report@crafton.dev
- ~~`YOUR_USERNAME` in .github/ISSUE_TEMPLATE/config.yml~~ Done: JohnCrafton

### 6. Repository Settings

Go to **Settings > General**

- Add topics: `profanity-filter`, `word-list`, `content-moderation`, `bad-words`, `hate-speech-detection`
- Add description: "A profanity filter that won't turn 'classic' into 'clbuttic'"
- Set website URL (if applicable)

## Reviewing Word List PRs

When reviewing PRs that modify word lists:

1. **Verify tier classification** - Is the word in the right tier?
2. **Check for duplicates** - Is this word already in another tier?
3. **Validate format** - Lowercase, alphabetically sorted?
4. **Consider false positives** - Could this cause substring issues?
5. **Review justification** - Is there sufficient reason for the change?

## Release Process

1. Update version (when packages exist)
2. Update changelog
3. Create GitHub release with notes
4. Packages auto-publish (when CI is set up)

## Responding to Security Issues

1. Acknowledge within 48 hours
2. Assess severity
3. Fix in private fork if needed
4. Coordinate disclosure
5. Credit reporter (if desired)
