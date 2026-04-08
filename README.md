# riptide

Cleans up text copied from terminal output — strips trailing whitespace, fixes hard line breaks, and optionally formats as a PR description. Useful for Claude output.

NOTE: Use this tool at your own risk. It's under development and may change without warning.

## Usage

Copy text to your clipboard and then run it like demonstrated below:

```
# Clean up terminal formatting
pbpaste | ./riptide.py | pbcopy

# Format as PR description (summary line + bullets)
pbpaste | ./riptide.py --pr | pbcopy
```

The result is placed back on your clipboard, ready to paste.

### Optional Setup

If you'd like, make the script executable and symlink it to a directory on your PATH:

```
chmod +x riptide.py
ln -s "$(pwd)/riptide.py" /usr/local/bin/riptide
```

It can also be helpful to make an alias like the following:

```
alias rip="pbpaste | riptide --pr | pbcopy"
```

or

```
alias rip="pbpaste | /path/to/riptide.py --pr | pbcopy"
```

### Modes

- **Default** — strips trailing whitespace, removes terminal padding, and rejoins hard-wrapped lines into proper paragraphs. Preserves bullet points and paragraph breaks.
- **`--pr`** — same cleanup, then reformats as a PR description: a summary line (no trailing period) followed by bullet points.
