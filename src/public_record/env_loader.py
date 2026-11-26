"""Load environment variables from the one shared APEX secrets file.

Where the file is: APEX_ENV_FILE if set, otherwise ~/.config/apex/secrets.env
(on Termux: /data/data/com.termux/files/home/.config/apex/secrets.env).

Precedence, highest first:
  1. Variables already in the process environment
  2. <PROJECT>__NAME entries in the shared file, applied as NAME for this project
  3. Plain NAME entries in the shared file
  4. The project's own local .env, kept only as a fallback while you migrate
Blank values in the shared file are ignored.
"""
import os
import stat
from pathlib import Path
from typing import Dict, Mapping, MutableMapping, Optional

from dotenv import dotenv_values


def _read(path) -> Dict[str, str]:
    """Parse an env file; an unquoted value that is only a # comment counts as blank."""
    out = {}
    for k, v in dotenv_values(path).items():
        if v is None or v.lstrip().startswith("#"):
            v = ""
        out[k] = v
    return out

ALIASES = {
    "SUPABASE_PROJECT_URL": "SUPABASE_URL",
    "SUPABASE_SERVICE_KEY": "SUPABASE_SERVICE_ROLE_KEY",
    "TELEGRAM_TOKEN": "TELEGRAM_BOT_TOKEN",
}


def shared_env_path(env: Mapping[str, str] = os.environ) -> Path:
    return Path(env.get("APEX_ENV_FILE") or Path.home() / ".config" / "apex" / "secrets.env")


def load_env(project: Optional[str] = None,
             shared_file: Optional[Path] = None,
             local_file: Optional[Path] = Path(".env"),
             env: Optional[MutableMapping[str, str]] = None,
             quiet: bool = False) -> Dict[str, object]:
    env = os.environ if env is None else env
    shared_file = Path(shared_file) if shared_file else shared_env_path(env)
    merged: Dict[str, str] = {}

    local_found = bool(local_file) and Path(local_file).is_file()
    if local_found:
        merged.update({k: v for k, v in _read(local_file).items() if v})

    shared_found = shared_file.is_file()
    if shared_found:
        shared = {k: v for k, v in _read(shared_file).items() if v}
        merged.update({k: v for k, v in shared.items() if "__" not in k})
        if project:
            prefix = project.upper() + "__"
            merged.update({k[len(prefix):]: v for k, v in shared.items() if k.startswith(prefix)})
        if os.name != "nt" and shared_file.stat().st_mode & (stat.S_IRWXG | stat.S_IRWXO) and not quiet:
            print(f'[env] warning: {shared_file} is readable by other users, run: chmod 600 "{shared_file}"')

    for alias, canonical in ALIASES.items():
        if canonical not in merged and alias in merged:
            merged[canonical] = merged[alias]
        if alias not in merged and canonical in merged:
            merged[alias] = merged[canonical]

    applied = 0
    for k, v in merged.items():
        if k not in env:
            env[k] = v
            applied += 1

    if not quiet:
        where = f"shared file {shared_file}" if shared_found else f"no shared file at {shared_file}"
        print(f"[env] {where}{', plus local .env fallback' if local_found else ''}; {applied} variables set")
    return {"shared_file": str(shared_file), "shared_found": shared_found,
            "local_found": local_found, "applied": applied}
