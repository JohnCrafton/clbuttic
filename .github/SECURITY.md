# Security Policy

## Scope

This security policy applies to the clbuttic project, which provides curated
profanity word lists. While this project doesn't execute code in most use cases,
security considerations still apply.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Potential Security Concerns

### Word List Integrity

The primary security concern for this project is **word list integrity**:

- Malicious additions that could cause false positives (blocking legitimate words)
- Removal of important terms that should be blocked
- Injection of content designed to cause issues in downstream consumers

### Import Script

The `scripts/import_sources.py` script fetches data from external sources.
Users should:

- Review the script before running
- Verify the integrity of fetched data
- Only run in trusted environments

## Reporting a Vulnerability

If you discover a security issue, please report it responsibly:

1. **Do NOT open a public issue** for security vulnerabilities
2. Email the maintainers at **report@crafton.dev**
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Resolution Timeline**: Depends on severity, typically 1-4 weeks

### Disclosure Policy

- We follow coordinated disclosure
- We will credit reporters (unless they prefer anonymity)
- We aim to fix issues before public disclosure

## Security Best Practices for Users

When using clbuttic word lists in your applications:

1. **Validate input**: Don't assume word lists are safe for use in regex without escaping
2. **Pin versions**: Use specific releases rather than always pulling latest
3. **Review changes**: Check release notes before updating
4. **Defense in depth**: Don't rely solely on word lists for content moderation

## Not a Vulnerability

The following are NOT security vulnerabilities:

- Missing words from the lists (submit a PR instead)
- Disagreements about tier classification
- Feature requests
- General bugs in documentation
