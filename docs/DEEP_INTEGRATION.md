# Deep Integration: Fuzzy Matching (Design Document)

**Status: PLANNED - Not yet implemented**

This document describes a planned fuzzy matching system for catching evasion attempts. This is a design specification, not documentation for existing functionality.

## Problem Statement

Users trying to bypass filters get creative:

| Evasion Type | Example | Target Word |
|--------------|---------|-------------|
| Leetspeak | `4ss`, `@ss`, `a$$` | ass |
| Spacing | `a s s`, `a.s.s`, `a-s-s` | ass |
| Homoglyphs | Cyrillic 'a' instead of Latin 'a' | ass |
| Zero-width chars | Zero-width space inserted | ass |
| Mixed scripts | Cyrillic + Latin mix | ass |

## Proposed Solution

A separate "fuzzy agent" package that:
1. Normalizes input text (strips spacing, converts leetspeak, etc.)
2. Checks normalized text against word lists
3. Returns match information including the normalization applied

## Normalization Strategies

### Leetspeak

Character substitutions to detect:

| Original | Substitutions |
|----------|---------------|
| a | 4, @, ^ |
| e | 3 |
| i | 1, ! |
| o | 0 |
| s | 5, $ |
| t | 7, + |

### Homoglyphs

Visually similar characters from other scripts:

| Latin | Lookalikes |
|-------|------------|
| a | Cyrillic a, IPA a, Greek alpha |
| c | Cyrillic s, Greek lunate sigma |
| e | Cyrillic e, Greek epsilon |
| o | Cyrillic o, Greek omicron |
| p | Cyrillic r, Greek rho |

### Spacing

Normalize inserted characters:
- Spaces: `a s s` -> `ass`
- Punctuation: `a.s.s` -> `ass`
- Dashes: `a-s-s` -> `ass`
- Underscores: `a_s_s` -> `ass`

### Zero-Width Characters

Strip invisible Unicode:
- Zero-width space (U+200B)
- Zero-width non-joiner (U+200C)
- Zero-width joiner (U+200D)
- Word joiner (U+2060)

## Performance Considerations

Fuzzy matching is significantly slower than simple word matching. Recommendations:
1. Use simple whole-word checking first
2. Only run fuzzy checks on flagged or high-risk content
3. Cache results for repeated checks

## When to Use Fuzzy Matching

Good candidates:
- Usernames/display names (high evasion attempt rate)
- User-generated content in games
- Public comments on moderated platforms
- Content moderation review queues

Probably overkill:
- Chat/messaging (slows things down)
- Search queries (users rarely evade)
- Internal tools (trust your users)
- Performance-critical paths

## Implementation Status

This feature is not yet implemented. The design is provided here to:
1. Document the intended approach
2. Solicit feedback before implementation
3. Guide future development

Contributions welcome - see CONTRIBUTING.md.
