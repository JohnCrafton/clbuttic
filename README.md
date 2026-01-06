# Clbuttic

**A profanity filter that won't turn "classic" into "clbuttic".**

> The "Clbuttic Mistake" is what happens when a naive profanity filter replaces "ass" everywhere it appears - turning "classic" into "clbuttic", "assist" into "buttist", and "assumption" into... well, you can guess.

## What Is This?

An open-source, multi-language, tiered profanity/slur dictionary that's **obsessively false-positive-aware**:

- Curated word lists organized by severity
- Multi-language support from day one
- Git LFS for word lists (keeps clones clean)
- Built to avoid the mistakes the name warns about

Most profanity filters are:
- Hilariously incomplete
- Overly aggressive (blocking "grass" because it contains "ass")
- English-only
- Proprietary APIs with per-call pricing

Clbuttic is none of those things.

## Current Status

This project currently provides **curated word lists only**. Package implementations (npm, pip, cargo) are planned but not yet available.

## Word Lists

Lists are organized by language and tier:

```
lists/
├── en/
│   ├── tier1.txt      # Slurs, hate speech (277 words)
│   ├── tier2.txt      # Strong profanity (549 words)
│   ├── tier3.txt      # Crude but mild (104 words)
│   ├── tierx.txt      # Contextually problematic (37 words)
│   └── allowlist.txt  # False positive protection
├── es/                # Spanish (68 words)
├── fr/                # French (91 words)
├── de/                # German (66 words)
└── pt/                # Portuguese (76 words)
```

## Tiered Severity

Words are organized by severity level:

| Tier | Description | Example Use Case |
|------|-------------|------------------|
| **Tier 1** | Slurs, hate speech | Block always |
| **Tier 2** | Strong profanity | Block in family contexts |
| **Tier 3** | Crude but mild | Block in formal contexts |
| **Tier X** | Contextually problematic | User-defined policies |

Each tier is available as a separate file or can be combined as needed.

## Multi-Language Support

- English (en) - 967 words across tiers, plus allowlist
- Spanish (es) - 68 words (needs tier classification)
- French (fr) - 91 words (needs tier classification)
- German (de) - 66 words (needs tier classification)
- Portuguese (pt) - 76 words (needs tier classification)

Non-English lists currently need native speaker review for proper tier assignment.

## False Positive Handling

### The Problem

Naive substring filters cause disasters:
- "classic" -> "clbuttic"
- "Scunthorpe" -> blocked (UK town)
- "shiitake" -> blocked (mushroom)

### Our Solution

1. **Whole-word matching recommended** - no substring disasters
2. **Curated allowlists** - "classic", "assist", "Scunthorpe" all pass
3. **Allowlist for substring mode** - when you need it, with protection

See [docs/FALSE_POSITIVES.md](docs/FALSE_POSITIVES.md) for the full story.

## Git LFS

Word lists are tracked with Git LFS to keep the repo lightweight:

```bash
# Normal clone gets pointer files only
git clone <repo-url>

# Pull actual word lists when needed
git lfs pull
```

## Contributing

We welcome contributions! See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

Priority areas:
- Non-English tier classification (native speakers needed)
- Missing words (with justification)
- False positives we've missed
- Package implementations

## License

CC-BY-4.0 (Creative Commons Attribution 4.0 International)

This project incorporates data from [LDNOOBW](https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words) (CC-BY-4.0), [dsojevic/profanity-list](https://github.com/dsojevic/profanity-list) (MIT), and [words/cuss](https://github.com/words/cuss) (MIT). See [SOURCES.md](SOURCES.md) for full attribution.
