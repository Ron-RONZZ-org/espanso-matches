# Espanso AGENTS.md

## Overview
Text expansion match files for espanso

## Architecture
```
espanso/
├── base.yml        # Common/default matches
├── code.yml        # Code snippets
├── git.yml         # Git commands
└── README.md       # Usage guide
```

## Subcomponents
| Component | Purpose |
|-----------|---------|
| base.yml | Core/common expansions |
| code.yml | Programming snippets |
| git.yml | Git command shortcuts |

## Configuration
- YAML format matching espanso spec
- Modular - users can symlink entire dir or specific files

## Key Design Decisions

### Split YAML Files by Category
Espanso automatically loads all YAML files in `$CONFIG/match/` (and subfolders). Split matches by category to avoid the "large config" problem:
- `code.yml` - programming snippets
- `git.yml` - git command shortcuts
- `math.yml` - mathematical notation
- `unicode.yml` - special characters
- `emails.yml` - email templates

### Cursor Positioning with `force_mode`
The cursor hint (`$|$`) can break when replacements contain quotes, backticks, or multi-byte characters because the injection method (clipboard vs keystrokes) can produce different character counts.

**Solution**: Use `force_mode: keys` for affected matches:
```yaml
- trigger: ":rh"
  replace: '«$|$»'
  force_mode: keys
```
This forces keystroke injection which is more precise for cursor positioning.

### YAML Quoting
Prefer single quotes for YAML values containing double quotes or special characters:
```yaml
- trigger: ":dq"
  replace: '"$|$"'  # single quotes outside, double inside
```

### Search with Alt+Space
Use the built-in search bar (`Alt+Space` by default) to search by **replacement text**, not just the trigger.

### Opt-in Loading with `_` Prefix
Files starting with `_` are not auto-loaded. Use `imports:` in other files to selectively include them:
```yaml
import:
  - _personal.yml
```

## Dependencies
- espanso (https://espanso.org)
- No third-party extensions required - use built-in features

## Integration Points
- Espanso watches this directory for match files
- Can combine multiple yml files

## Usage
```bash
# IMPORTANT: Stop espanso first before symlinking!
espanso stop

# Symlink entire directory
ln -sf ~/.basculer/espanso ~/.config/espanso

# Restart espanso
espanso start

# Or symlink individual files
ln -sf ~/.basculer/espanso/code.yml ~/.config/espanso/match/code
```