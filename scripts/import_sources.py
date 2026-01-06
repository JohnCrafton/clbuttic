#!/usr/bin/env python3
"""
Import and merge profanity lists from various sources into clbuttic tier structure.

Sources:
- dsojevic/profanity-list (English, with severity ratings)
- LDNOOBW (multilingual)

Tier mapping:
- Tier 1: Slurs, hate speech (severity 4 + racial/lgbtq tags, or explicit slurs)
- Tier 2: Strong profanity (severity 3-4, sexual/shock tags)
- Tier 3: Crude but mild (severity 1-2)
- Tier X: Contextually problematic (dual-meaning words)

Usage:
    1. Download source files to /tmp/:
       curl -sL "https://raw.githubusercontent.com/dsojevic/profanity-list/main/en.json" -o /tmp/profanity-en.json
       curl -sL "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en" -o /tmp/ldnoobw-en.txt
       curl -sL "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/es" -o /tmp/ldnoobw-es.txt
       curl -sL "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/fr" -o /tmp/ldnoobw-fr.txt
       curl -sL "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/de" -o /tmp/ldnoobw-de.txt
       curl -sL "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/pt" -o /tmp/ldnoobw-pt.txt

    2. Run this script:
       python3 scripts/import_sources.py
"""

import json
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
LISTS_DIR = PROJECT_ROOT / "lists"

# Words that should be Tier 1 regardless of source rating (slurs/hate speech)
TIER1_OVERRIDES = {
    # Racial slurs
    "nigger", "nigga", "niggers", "niggas", "negro", "negros",
    "chink", "chinks", "gook", "gooks", "spic", "spics", "spick", "spicks",
    "wetback", "wetbacks", "beaner", "beaners", "kike", "kikes",
    "coon", "coons", "darkie", "darkies", "darky", "jigaboo", "jigaboos",
    "pickaninny", "pickaninnies", "sambo", "sambos", "zipperhead",
    "porch monkey", "jungle bunny", "moon cricket", "tar baby",
    "chinaman", "chinamen", "ching chong", "slant eye", "slant eyes",
    "towelhead", "towelheads", "camel jockey", "sand nigger", "sand niggers",
    "raghead", "ragheads", "hajji", "haji",

    # Homophobic slurs
    "faggot", "faggots", "fag", "fags", "faggotry",
    "dyke", "dykes", "lesbo", "lesbos",
    "tranny", "trannies", "shemale", "shemales", "ladyboy", "ladyboys",
    "homo", "homos",

    # Disability slurs
    "retard", "retards", "retarded", "tard", "tards",
    "spastic", "spastics", "spaz", "spazz",
    "cripple", "cripples",

    # Antisemitic
    "heeb", "heebs", "hymie", "hymies", "yid", "yids",

    # Nazi/white supremacist
    "nazi", "nazis", "heil hitler", "sieg heil", "white power",
    "1488", "14/88",
}

# Words that should be Tier X (contextually problematic, have legitimate uses)
TIERX_WORDS = {
    "cock", "pussy", "ass", "balls", "nuts", "dick",
    "screw", "screwed", "blow", "suck", "sucked", "sucks",
    "boner", "horny", "laid", "wang",
    "lame", "dumb", "stupid", "idiot", "moron", "crazy", "insane", "psycho",
    "jesus", "christ", "god", "goddamn", "damn",
    "gay",  # Has legitimate non-pejorative use
}

# Words that are Tier 3 (mild)
TIER3_WORDS = {
    "crap", "crappy", "hell", "heck", "darn", "dang",
    "piss", "pissed", "pee", "poop", "fart", "butt", "butthole",
    "turd", "booty", "bloody", "bugger", "bollocks",
    "jerk", "loser", "sucks", "sucker",
}


def is_valid_word(word):
    """Check if word contains only valid characters (ASCII printable, no emoji)."""
    if not word:
        return False
    # Allow ASCII letters, numbers, spaces, hyphens, apostrophes, slashes
    for char in word:
        if not (char.isascii() and (char.isalnum() or char in " -'/.")):
            return False
    return True


def load_dsojevic_json(filepath):
    """Load and parse the dsojevic profanity-list JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_ldnoobw_txt(filepath):
    """Load LDNOOBW text file (one word per line)."""
    words = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word and not word.startswith('#') and is_valid_word(word):
                words.add(word)
    return words


def categorize_dsojevic_entry(entry):
    """
    Categorize a dsojevic entry into our tier system.

    Returns: (tier, words) where tier is 1, 2, 3, or 'x'
    """
    severity = entry.get('severity', 3)
    tags = set(entry.get('tags', []))
    match_str = entry.get('match', '')

    # Extract individual words/phrases from match patterns
    # Format: "word1|word2|phrase with spaces"
    words = set()
    for part in match_str.split('|'):
        word = part.strip().lower()
        if word and '*' not in word and is_valid_word(word):
            words.add(word)

    if not words:
        return None, set()

    # Check overrides first
    for word in words:
        if word in TIER1_OVERRIDES:
            return 1, words

    # Tier 1: racial or lgbtq slurs (severity 3-4)
    if ('racial' in tags or 'lgbtq' in tags) and severity >= 3:
        return 1, words

    # Check for tier X (contextual)
    if any(w in TIERX_WORDS for w in words):
        return 'x', words

    # Check for tier 3 (mild)
    if any(w in TIER3_WORDS for w in words) or severity <= 2:
        return 3, words

    # Severity 4 + shock -> Tier 2 (strong but not slurs)
    if severity == 4 and 'shock' in tags:
        return 2, words

    # Severity 3-4 + sexual -> Tier 2
    if severity >= 3 and 'sexual' in tags:
        return 2, words

    # Default: severity 3-4 -> Tier 2, severity 1-2 -> Tier 3
    if severity >= 3:
        return 2, words
    else:
        return 3, words


def process_english():
    """Process English sources and create tiered lists."""
    tier1 = set()
    tier2 = set()
    tier3 = set()
    tierx = set()

    # Add our manual overrides
    tier1.update(TIER1_OVERRIDES)
    tierx.update(TIERX_WORDS)
    tier3.update(TIER3_WORDS)

    # Process dsojevic data
    dsojevic_path = Path('/tmp/profanity-en.json')
    if dsojevic_path.exists():
        entries = load_dsojevic_json(dsojevic_path)
        for entry in entries:
            tier, words = categorize_dsojevic_entry(entry)
            if tier == 1:
                tier1.update(words)
            elif tier == 2:
                tier2.update(words)
            elif tier == 3:
                tier3.update(words)
            elif tier == 'x':
                tierx.update(words)
    else:
        print(f"  Warning: {dsojevic_path} not found, skipping", file=sys.stderr)

    # Process LDNOOBW English (add to tier 2 if not already categorized)
    ldnoobw_path = Path('/tmp/ldnoobw-en.txt')
    if ldnoobw_path.exists():
        ldnoobw_words = load_ldnoobw_txt(ldnoobw_path)
        for word in ldnoobw_words:
            # Check if already categorized
            if word in tier1 or word in tierx or word in tier3:
                continue
            # Check overrides
            if word in TIER1_OVERRIDES:
                tier1.add(word)
            elif word in TIERX_WORDS:
                tierx.add(word)
            elif word in TIER3_WORDS:
                tier3.add(word)
            else:
                tier2.add(word)
    else:
        print(f"  Warning: {ldnoobw_path} not found, skipping", file=sys.stderr)

    # Remove overlaps (higher tier wins)
    tier2 -= tier1
    tier3 -= tier1
    tier3 -= tier2
    tierx -= tier1  # Slurs are never "contextual"

    return tier1, tier2, tier3, tierx


def process_other_language(lang_code):
    """Process LDNOOBW list for non-English language."""
    ldnoobw_path = Path(f'/tmp/ldnoobw-{lang_code}.txt')
    if not ldnoobw_path.exists():
        print(f"  Warning: {ldnoobw_path} not found, skipping", file=sys.stderr)
        return set(), set(), set(), set()

    words = load_ldnoobw_txt(ldnoobw_path)

    # For non-English, we don't have severity data, so put everything in tier2
    # Users/contributors can refine later
    tier1 = set()
    tier2 = words
    tier3 = set()
    tierx = set()

    return tier1, tier2, tier3, tierx


def write_tier_file(filepath, words, header_comment):
    """Write a tier file with sorted words."""
    filepath.parent.mkdir(parents=True, exist_ok=True)

    sorted_words = sorted(words)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header_comment)
        f.write('\n')
        for word in sorted_words:
            f.write(f'{word}\n')

    return len(sorted_words)


def main():
    print("Clbuttic word list importer")
    print("=" * 40)
    print()

    print("Processing English sources...")
    en_tier1, en_tier2, en_tier3, en_tierx = process_english()

    # Write English files
    en_dir = LISTS_DIR / 'en'

    count1 = write_tier_file(
        en_dir / 'tier1.txt',
        en_tier1,
        "# Tier 1: Slurs, hate speech\n"
        "# These should be blocked in virtually all contexts\n"
        "# Sources: dsojevic/profanity-list, LDNOOBW, manual curation\n"
    )

    count2 = write_tier_file(
        en_dir / 'tier2.txt',
        en_tier2,
        "# Tier 2: Strong profanity\n"
        "# Block in family-friendly contexts\n"
        "# Sources: dsojevic/profanity-list, LDNOOBW\n"
    )

    count3 = write_tier_file(
        en_dir / 'tier3.txt',
        en_tier3,
        "# Tier 3: Crude but mild\n"
        "# Block in formal contexts only\n"
        "# Sources: dsojevic/profanity-list, LDNOOBW\n"
    )

    countx = write_tier_file(
        en_dir / 'tierx.txt',
        en_tierx,
        "# Tier X: Contextually problematic\n"
        "# These words have legitimate uses but are often used offensively\n"
        "# Requires user-defined policies\n"
    )

    print(f"  English: tier1={count1}, tier2={count2}, tier3={count3}, tierx={countx}")

    # Process other languages
    for lang in ['es', 'fr', 'de', 'pt']:
        print(f"Processing {lang}...")
        tier1, tier2, tier3, tierx = process_other_language(lang)

        lang_dir = LISTS_DIR / lang

        # For non-English, just write tier2 (all words) for now
        count = write_tier_file(
            lang_dir / 'tier2.txt',
            tier2,
            f"# Tier 2: Strong profanity ({lang})\n"
            f"# Source: LDNOOBW\n"
            f"# NOTE: These need manual review for tier classification\n"
        )

        # Create placeholder files for other tiers
        for tier_file in ['tier1.txt', 'tier3.txt', 'tierx.txt']:
            tier_path = lang_dir / tier_file
            if not tier_path.exists():
                tier_path.write_text(f"# {tier_file.replace('.txt', '').title()} ({lang})\n# TODO: Needs curation\n")

        # Create placeholder allowlist
        allowlist_path = lang_dir / 'allowlist.txt'
        if not allowlist_path.exists():
            allowlist_path.write_text(f"# Allowlist ({lang})\n# TODO: Add language-specific false positives\n")

        print(f"  {lang}: tier2={count} (needs manual tier assignment)")

    print()
    print("Done! Review the generated files and refine tier assignments.")


if __name__ == '__main__':
    main()
