
# Kaguya

Multi-purpose Discord bot wrriten in (mostly) Python.

## Features (on development)
- Word look-up on Merriam-Webster dictionary (almost finished)
- Wikipedia article summary (almost finished)
- Codeforces related features (on dev)
- General purpose features (on dev)
## Changelog
### v1.0
First official release of the bot. Some of the much needed functions are ready.
The bot consists of three cogs as can be seen in [main.py](https://github.com/20toduc01/Kaguya/blob/v1.0/main.py): GeneralPurpose, CodeforcesCommands and GeneratorCommands.
General purpose commands:
- Added *insult* command (roast someone)
- Added *define* command (word definition look-up in formal dictionary)
- Added *wiki* command (Wikipedia article look-up)
- Added *roll* command (return a random number in range [1;100])

Codeforces Commands:
- Added *cfinfo* command (Codeforces handle brief info look-up)
- Added *cfrating* command (rating graph of Codeforces users)
- Added *cfload* command (an auxiliary command to update Codeforces problem database)
- Added *cfproblem* command (return information of problems having specified tags)

Generator Commands:
- Added *gentree* command (generate a random tree containing V vertices)
- Added *genarray* command (generate an array of fixed length)
- Added *genperm* command (generate a permutation of N first positive integers)