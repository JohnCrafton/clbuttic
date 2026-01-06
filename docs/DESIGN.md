# Clbuttic

**A profanity filter that won't turn "classic" into "clbuttic".**

> The "Clbuttic Mistake" is what happens when a naive profanity filter replaces "ass" everywhere it appears - turning "classic" into "clbuttic", "assist" into "buttist", and "assumption" into... well, you can guess.

---

## What Is This?

An open-source, multi-language, tiered profanity/slur dictionary that's **obsessively false-positive-aware**:
- Package manager distribution (npm, pip, crates, etc.)
- Minimal footprint for embedding
- Git LFS for word lists (keeps normal clones clean)
- Built from the ground up to avoid the mistakes the name warns about

This is a **give-back project** - a genuine gap in the ecosystem where most profanity filters are:
- Hilariously incomplete
- Overly aggressive (blocking "grass" because it contains "ass")
- English-only
- Proprietary APIs with per-call pricing

---

## Core Concept: Tiered Severity

Word lists organized by severity level:

| Tier | Description | Example Use Case |
|------|-------------|------------------|
| **Tier 1** | Nuclear - slurs, hate speech | Block always |
| **Tier 2** | Strong profanity | Block in family contexts |
| **Tier 3** | Crude but mild | Block in formal contexts |
| **Tier X** | Contextually problematic | User-defined policies |

Each tier available as separate importable lists or combined.

---

## Multi-Language Support

From day one, not an afterthought:
- English (primary)
- Spanish
- French
- German
- Portuguese
- (expand based on contributor interest)

Language-specific considerations:
- Conjugation variants (Spanish verb forms, etc.)
- Regional variations (UK vs US, Latin American vs Castilian Spanish)
- False positives that are language-specific

---

## Technical Architecture

### Repository Structure
```
clbuttic/
├── lists/
│   ├── en/
│   │   ├── tier1.txt
│   │   ├── tier2.txt
│   │   ├── tier3.txt
│   │   └── tierx.txt
│   ├── es/
│   ├── fr/
│   └── ...
├── packages/
│   ├── npm/
│   ├── pip/
│   └── cargo/
├── scripts/
│   └── build-packages.sh
├── docs/
│   ├── CONTRIBUTING.md
│   ├── FALSE_POSITIVES.md
│   └── DEEP_INTEGRATION.md
└── .gitattributes  # LFS config
```

### Git LFS Strategy
- Word list files tracked via LFS
- Normal clone gets pointer files only
- Explicit `git lfs pull` to get actual lists
- Keeps repo size minimal for casual inspection

### Package Distribution
Each package should:
- Ship with pre-bundled lists (user doesn't need LFS)
- Expose simple API: `isForbidden(word, tier, lang)`
- Allow custom list injection
- Be dependency-free where possible

---

## API Design (Conceptual)

### JavaScript/TypeScript
```javascript
import { check, Tier, Lang } from 'clbuttic';

// Simple check
check('word');  // { forbidden: true, tier: 2, lang: 'en' }

// With options
check('word', { 
  tiers: [Tier.ONE, Tier.TWO],
  langs: [Lang.EN, Lang.ES]
});

// Batch check
checkMany(['word1', 'word2', 'word3']);
```

### Python
```python
from clbuttic import check, Tier, Lang

# Simple check
check("word")  # ForbiddenResult(forbidden=True, tier=2, lang="en")

# With options
check("word", tiers=[Tier.ONE, Tier.TWO], langs=[Lang.EN, Lang.ES])
```

### Rust
```rust
use clbuttic::{check, Tier, Lang};

let result = check("word", &[Tier::One, Tier::Two], &[Lang::En]);
```

---

## False Positive Handling

### The Clbuttic Hall of Fame
Real-world filter failures that turned normal words into nonsense:
- "classic" -> "clbuttic"
- "assist" -> "buttist"
- "assume" -> "buttume"
- "assess" -> "buttess"
- "association" -> "buttociation"
- "passionate" -> "pbuttionate"
- "basement" -> "bbutement"
- "ambassador" -> "buttbuttador"

### The Scunthorpe Problem
Real place names, words, and names that trigger naive filters:
- Scunthorpe (UK town)
- Shitake (mushroom)
- Cockatoo (bird)
- Essex (UK county)
- Penistone (UK town)
- Lightwater (UK town - contains "twat")
- Arsenal (football club)
- Spotted Dick (British dessert)

### Strategy
1. **Allowlist file** per language with known false positives
2. **Whole-word matching** by default (not substring)
3. **Context-aware mode** (optional) for substring detection with allowlist exceptions
4. **Documentation** explaining the tradeoffs

---

## Deep Integration: Fuzzy Matching Agent

**Bonus README for advanced users.**

A local agent pattern for catching:
- Leetspeak variants (4ss, @ss, a$$)
- Unicode homoglyphs (аss using Cyrillic 'а')
- Spacing tricks (a s s, a.s.s)
- Zero-width character insertion
- Mixed-script attacks

### Concept
```javascript
import { createFuzzyAgent } from 'clbuttic/fuzzy';

const agent = createFuzzyAgent({
  lists: ['tier1', 'tier2'],
  langs: ['en'],
  strategies: ['leetspeak', 'homoglyph', 'spacing']
});

agent.check('4$$h0le');  // { forbidden: true, normalized: 'asshole', tier: 2 }
```

This is intentionally separate from core - it's heavier, slower, and many use cases don't need it.

---

## Project Origin

This concept emerged from working on a game (goblinseeker) where I initially wanted player-typed input but needed profanity filtering. Landed on a different solution (silly combination scrolls instead of typing) but the underlying problem remained interesting.

The ecosystem genuinely lacks a well-maintained, multi-language, tiered, OSS solution with sensible defaults and false-positive awareness.

---

## Open Questions / Things to Ralph-Wiggum

1. **List curation** - Where do the initial lists come from? Academic sources? Existing OSS projects? Manual curation?

2. **Contribution model** - How do people propose additions? PRs with justification? Voting?

3. **Versioning** - Semantic versioning for the *API*, but what about the lists? Do list updates trigger minor versions?

4. **Tier X semantics** - Is this "user-defined" or "contextually problematic" (like "retard" which is a real word but often used as a slur)?

5. **Compound detection** - Should "dumbass" be tier 2 even if "dumb" and "ass" are individually tier 3?

6. **Cultural sensitivity** - Some words are slurs in one dialect but neutral in another. How to handle?

7. **Monetization** - Is this purely OSS give-back, or is there a hosted API play? (Probably pure OSS, but worth thinking about)

8. **Name availability confirmed** - ✅ `clbuttic` appears available on npm, pypi, crates.io

---

## First Steps (If Building)

1. [x] ~~Verify "clbuttic" name availability on npm, pypi, crates.io~~ ✅ Looks clear
2. [ ] Find 2-3 existing word list sources to bootstrap from
3. [ ] Define exact tier boundaries with examples
4. [ ] Build minimal Node package first (fastest iteration)
5. [ ] Create contribution guidelines
6. [ ] Set up LFS and repo structure
7. [ ] Write the false positives documentation
8. [ ] Draft the "deep integration" fuzzy matcher README

---

## References / Prior Art

- [bad-words](https://www.npmjs.com/package/bad-words) - Popular but English-only, no tiers
- [profanity-filter](https://pypi.org/project/profanity-filter/) - Python, ML-based, heavier
- [List of Dirty, Naughty, Obscene, and Otherwise Bad Words](https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words) - Good word source, unmaintained
- Google's "What Do You Love" filter lists (historical)
- Various game company internal lists (not public)

---

*"The clbuttic mistake: when your filter turns 'classic' into 'clbuttic', 'assume' into 'buttume', and 'assist' into 'buttist'. Don't be that filter."*
