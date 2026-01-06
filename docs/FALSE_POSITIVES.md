# The False Positives Problem

This document explains why false positives matter and how Clbuttic handles them.

## The Clbuttic Mistake

The name "Clbuttic" comes from what happens when a naive profanity filter replaces "ass" everywhere it appears:

- "classic" -> "clbuttic"
- "assist" -> "buttist"
- "assume" -> "buttume"
- "assess" -> "buttess"
- "association" -> "buttociation"
- "passionate" -> "pbuttionate"
- "basement" -> "bbutement"
- "ambassador" -> "buttbuttador"

This is what happens when you use substring matching without an allowlist.

## The Scunthorpe Problem

Named after the UK town of Scunthorpe, whose residents couldn't sign up for AOL in 1996 because the town name contains "cunt".

Real examples of legitimate words/names blocked by naive filters:
- **Scunthorpe** - UK town
- **Penistone** - UK town
- **Lightwater** - UK town (contains "twat")
- **Essex** - UK county
- **Shitake/Shiitake** - mushroom
- **Cockatoo** - bird
- **Arsenal** - football club
- **Spotted Dick** - British dessert
- **Bangkok** - capital of Thailand

## How Clbuttic Handles This

### 1. Whole-Word Matching (Recommended)

The word lists are designed for whole-word matching, not substring matching. This eliminates 99% of false positives immediately.

Example logic:
```
Input: "classic"
Check: Is "classic" in the word list? No.
Result: Not blocked.

Input: "ass"
Check: Is "ass" in the word list? Yes (tier 2).
Result: Blocked.
```

### 2. Allowlists for Substring Mode

When you need substring detection (catching "dumbass" when "ass" is in your list), use the allowlist:

1. Check if input contains any blocked substring
2. If yes, check if the full word is in the allowlist
3. If in allowlist, allow it; otherwise block

This catches compound profanity while protecting legitimate words.

## Allowlist Contents

Our English allowlist includes:

### The "ass" family (~100 words)
classic, assist, assume, assess, associate, assemble, asset, assassin, bass, brass, class, compass, embassy, embarrass, grass, harass, mass, massage, morass, pass, passion, surpass, trespass...

### The Scunthorpe collection (~50 entries)
Place names, food terms, and proper nouns that trigger substring filters.

### Anatomical/medical terms used legitimately
circumstance, canal, analyze, dictionary, predict, constitute, title, attitude...

## Contributing to the Allowlist

If you find a false positive we've missed:

1. Check it's not already in `lists/[lang]/allowlist.txt`
2. Add it with a comment explaining which substring triggers it
3. Submit a PR

Priority order for additions:
1. Common words in everyday use
2. Place names and proper nouns
3. Technical/specialized terms
4. Rare but legitimate words

## Trade-offs

There's an inherent trade-off:

| Approach | False Positives | False Negatives |
|----------|-----------------|-----------------|
| Whole-word only | Very low | Higher (misses compounds) |
| Substring + allowlist | Low | Low |
| Substring, no allowlist | Very high | Very low |

We recommend whole-word matching because blocking "classic" is worse than missing "jackass".

## Further Reading

- [Wikipedia: Scunthorpe Problem](https://en.wikipedia.org/wiki/Scunthorpe_problem)
- [The Clbuttic Mistake](https://thedailywtf.com/articles/The-Clbuttic-Mistake-)
