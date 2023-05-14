import os
from configparser import ConfigParser
from pathlib import Path
from subprocess import Popen
from typing import Tuple, Optional

def check_secrets(p: Path = Path('./secrets.ini'),
                  p2: Path = Path('./config.ini'),
                  s:
                  str = Path('./secrets_template').read_text()) -> Tuple[
                      Tuple[Path, Path],
                      Optional[str]]:
    """Checks two paths to see that both files exist,
    defaulting to ./secrets.ini and ./config.ini in
    the current directory. Takes a secrets template,
    or provides a default one, and returns a Tuple -
    containing another Tuple with the paths and the
    string containing a secrets_template or None

    Parameters
    ----------
    p : Path
 
    p2 : Path

    s : str
    
    Returns
    -------
    Tuple[Tuple[Path, Path], Optional[str]]
    """
    if Path.exists(p):
        secrets: str = s
    else:
        secrets = None    
    return ((p, p2), secrets)

def assert_config(t: Tuple[Tuple[Path,
                                 Path],
                           Optional[str]]) -> Tuple[
                               Path, Optional[str]]:
    """asserts against the tuple created by check_ini
    to ensure that second (config.ini) exists and returns
    a Tuple containg the rest of the input tuple
    contents as a flattened tuple

    Parameters
    ----------
    t : Tuple[Tuple[Path, Path], Optional[str]]

    Returns
    -------
    Tuple[Path, Optional[str]]
    """
    pname: str = t[0][1].name
    assertmsg: str = pname.format('%s borked, consult documentation')
    assert Path.exists(t[0][1]), assertmsg
    return (t[0][0], t[1])

def write_secrets_maybe(t: Tuple[Path,
                                 Optional[str]]) -> Tuple[
                                     Path, Optional[str]]:
    """checks against the tuple created by assert_config_ini 
    to ensure that the path (default ./secrets.ini) exists
    and returns a Tuple containing the Path and what was
    written, respectively

    Parameters
    ----------
    t : Tuple[Path, Optional[str]]

    Returns
    -------
    Tuple[Path, Optional[str]]
    """
    if (not Path.exists(t[0])) and t[1]:
        f: _io.TextIOWrapper = open(t[0], 'a')
        f.write(secrets_template)
        f.close()
        os.chmod(t[0], 0o600)
    pname: str = t[0].name
    assertmsg: str = pname.format('%s borked, consult documentation')
    assert Path.exists(t[0]), assertmsg
    return t

def write_config_path(p: Path) -> bool:
    """Writes the config_path field of the given type to
    the path p in that type's syntax

    Parameters
    ----------
    p : Path
        the path of the config file to be amended

    Returns
    -------
    bool
    """
    f: _io.TextIOWrapper = open(p, 'a')
    s: str = """
[config_path]
location = REPLACE
"""
    f.write(s.replace('REPLACE', './' + p.name))
    f.close()
    return True

def run_initial_checks(p: Optional[Path] = None,
                       p2: Optional[Path] = None,
                       s: Optional[str] = None) -> Tuple[
                                     Path, Optional[str]]:
    """Runs each of the initial checks on the configuration and
    the secrets files

    Parameters
    ----------
    p : Optional[Path]
        The path to the secrets file

    p2: Optional[Path]
        The path to the config file
    Returns
    -------
    Tuple[Path, Optional[str]]
    """
    cfg: ConfigParser = ConfigParser(interpolation=None)
    if p2:
        cfg.read(p2)
        if 'config_path' not in cfg.keys():
            write_config_path(p2)
    else:
        if p:
            p2 = Path('./config.ini')
        else:
            p, p2 = Path('./secrets.ini'), Path('./config.ini')
        cfg.read(p2)
        if 'config_path' not in cfg.keys():
            write_config_path(p2)
    return write_secrets_maybe(assert_config(check_secrets(p, p2, s)))

def check_cfg(cfg: ConfigParser) -> None:
    """Checks the ConfigParser object created from
    the config.ini and secrets.ini for the appropriate
    authorization info

    Parameters
    ----------
    cfg : ConfigParser
        The object generated from the .ini files

    Returns
    -------
    None
    """
    assert cfg['gobo_params']['key'], 'Google Books API Key required.'
    assert cfg['isbndb_headers']['Authorization'], 'ISBNDB API Key required.'
    return None

run_initial_checks()
cfg: ConfigParser = ConfigParser(interpolation=None)
cfg.read('./config.ini')
cfg.read('./secrets.ini')
check_cfg(cfg)
