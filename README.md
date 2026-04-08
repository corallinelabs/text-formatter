# text-formatter

Cleans up text copied from terminal output — strips trailing whitespace, fixes hard line breaks, and optionally formats as a PR description.

## Setup

Make the script executable:

```
chmod +x textfmt.py
```

Optionally, symlink it to a directory on your PATH so you can run it from anywhere:

```
ln -s "$(pwd)/textfmt.py" /usr/local/bin/textfmt
```

## Usage

Copy text to your clipboard, then:

```
# Clean up terminal formatting
pbpaste | ./textfmt.py | pbcopy

# Format as PR description (summary line + bullets)
pbpaste | ./textfmt.py --pr | pbcopy
```

The result is placed back on your clipboard, ready to paste.

### Modes

**Default** — strips trailing whitespace, removes terminal padding, and rejoins hard-wrapped lines into proper paragraphs. Preserves bullet points and paragraph breaks.

**`--pr`** — same cleanup, then reformats as a PR description: a summary line (no trailing period) followed by bullet points.
