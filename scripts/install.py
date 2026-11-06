#!/usr/bin/env python3
"""Copy skills to an explicitly chosen project; never overwrite existing skills."""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def install(target, platform, dry_run=False):
    target = Path(target).expanduser().resolve()
    if not target.is_dir():
        raise ValueError('Target must be an existing project directory')
    prefix = '.agents' if platform == 'codex' else '.claude'
    base = target / prefix / 'skills'
    # Do not follow destination symlinks outside the requested project.
    for part in (target / prefix, base):
        if part.is_symlink():
            raise ValueError(f'Refusing symlink destination: {part}')
    sources = sorted((ROOT / 'skills').iterdir())
    destinations = [(src, base / src.name) for src in sources if src.is_dir()]
    conflicts = [str(dst) for _, dst in destinations if dst.exists() or dst.is_symlink()]
    if conflicts:
        raise FileExistsError('No files changed; existing skill(s): ' + ', '.join(conflicts))
    for src, dst in destinations:
        print(('Would copy ' if dry_run else 'Copying ') + str(dst))
        if not dry_run:
            shutil.copytree(src, dst)
    return [dst for _, dst in destinations]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform', required=True, choices=['codex', 'claude'])
    parser.add_argument('--target', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        install(args.target, args.platform, args.dry_run)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + '\n')

if __name__ == '__main__':
    main()
