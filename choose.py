#!/usr/bin/env python3

from typing import Optional
from fuzzywuzzy import process

def wisely(among: Optional[dict] = None
           ) -> Optional[str]:
    """Selects the node nearest to the others in terms of Levenshtein
    distance

    Parameters
    ----------
    among : Optional[dict]
        A dictionary containing strings as keys and values

    Returns
    -------
    Optional[str]
        A string from the dictionary values that is most similar
        to the other values that contain non-empty strings
    """
    if among:
        if len(among) == 1:
            return among[[k for k in among.keys()][0]]
        elif len(among) == 2:
            return among[[k for k in among.keys()][1]]
        else:
            best = [None, 0]
            for k in among.keys():
                l: list = process.extract(among[k],
                                          [v for v in among.values()])
                total: int = sum([t[1] for t in l])
                if total > best[1]:
                    best = [k, total]
            return among[best[0]]
    return None
