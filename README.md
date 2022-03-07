# team-local-tactics
### Mandatory assignment group 42: Mats Omland Dyrøy, Jan Erik Syltøy

A game for the mandatory assignment

## Data
Data is saved to the `server/data/` folder.

### Champions
Champions are stored as a CSV file in the `champions.cvs` file.
Each line represents a single champion.
The lines are formatted as such: `name`, `rock %`, `paper %`, `scissors %`.

### Match history
Match history is stored on a per champion basis in a file `matches_<champion name>.csv`.
Each line represents a single match.
The lines are formatted as such: `opposing champion name`, `shape`, `opposing shape`, `score`.
`score` is `0` if match was a tie, `1` if champion won, `-1` if opposing champion won.