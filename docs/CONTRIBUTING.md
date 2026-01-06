# Contributing to Clbuttic

Thanks for helping make profanity filtering less broken!

## How to Contribute

### Adding Words to Lists

1. **Identify the correct tier:**
   - **Tier 1**: Slurs and hate speech - words that should be blocked in virtually all contexts
   - **Tier 2**: Strong profanity - words to block in family-friendly contexts
   - **Tier 3**: Crude but mild - words to block only in formal contexts
   - **Tier X**: Contextually problematic - words with legitimate uses that are sometimes offensive

2. **Identify the correct language:**
   - Add words to the appropriate language folder under `lists/`
   - If starting a new language, create the folder structure first

3. **Submit a PR with:**
   - The word(s) added to the appropriate tier file
   - A brief justification in the PR description
   - Sources if relevant (especially for regional slurs)

### Adding False Positives to Allowlists

This is just as important as adding blocked words!

1. Find a word that would be incorrectly flagged by substring matching
2. Add it to the appropriate `allowlist.txt` for that language
3. Include a comment explaining which profanity substring it contains

### Adding New Languages

1. Create the language folder under `lists/` (use ISO 639-1 codes: `en`, `es`, `fr`, etc.)
2. Create at minimum:
   - `tier1.txt`
   - `tier2.txt`
   - `tier3.txt`
   - `allowlist.txt`
3. Include a comment header explaining regional considerations

## Guidelines

### Tier Classification

When deciding on tiers, consider:
- **Impact**: How harmful is the word when used as intended?
- **Context**: Is there any legitimate use case?
- **Regional variation**: Is this offensive everywhere or only in certain dialects?

### False Positive Priority

We care deeply about false positives. A filter that blocks "classic" is worse than useless.

Priority for allowlist entries:
1. Common English words (classic, assist, assume)
2. Place names (Scunthorpe, Essex)
3. Food/nature terms (shiitake, cockatoo)
4. Technical terms
5. Proper names

### What We Don't Accept

- Made-up words or extremely rare variants
- Personal vendettas against specific terms
- Words without clear offensive use
- Contributions without justification

## Questions?

Open an issue with the `question` label.
