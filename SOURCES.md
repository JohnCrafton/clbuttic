# Data Sources & Attribution

Clbuttic incorporates data from the following open-source projects. We are grateful to their maintainers and contributors.

## Primary Sources

### LDNOOBW (List of Dirty, Naughty, Obscene, and Otherwise Bad Words)
- **URL**: https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words
- **License**: CC-BY-4.0 (Creative Commons Attribution 4.0 International)
- **Used for**: Multi-language word lists (en, es, fr, de, pt, and others)
- **Origin**: Originally from Shutterstock's autocomplete filter
- **Notes**: Provides broad coverage across 28+ languages

### dsojevic/profanity-list
- **URL**: https://github.com/dsojevic/profanity-list
- **License**: MIT
- **Used for**: English tier classification (severity ratings 1-4, tags)
- **Notes**: The severity ratings and tags (racial, lgbtq, sexual, shock) were used to assign words to our tier system

### words/cuss
- **URL**: https://github.com/words/cuss
- **License**: MIT
- **Used for**: Cross-reference and validation
- **Notes**: Includes "sureness" ratings indicating likelihood of profane usage

## Tier Mapping

We mapped source data to our tier system as follows:

| Source | Our Tier | Criteria |
|--------|----------|----------|
| dsojevic severity 4 + racial/lgbtq tags | Tier 1 | Slurs, hate speech |
| dsojevic severity 3-4 + sexual/shock tags | Tier 2 | Strong profanity |
| dsojevic severity 1-2 | Tier 3 | Crude but mild |
| Words with dual meanings | Tier X | Contextually problematic |
| LDNOOBW (non-English) | Tier 2 | Pending native speaker review |

## Manual Curation

In addition to automated import, we manually curated:
- Tier 1 overrides for known slurs that may have been miscategorized
- Tier X assignments for words with legitimate non-profane uses
- The English allowlist for false positive prevention

## Contributing

If you notice:
- A word that should be in a different tier
- A missing word that should be included
- A false positive that needs to be allowlisted

Please see [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for how to submit changes.

## License Compliance

This project is licensed under CC-BY-4.0 to comply with LDNOOBW's license requirements. Attribution is provided in this file and in the LICENSE file.

When using Clbuttic in your own projects, please include attribution as described in the LICENSE file.
