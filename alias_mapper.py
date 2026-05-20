import os

def lookup_alias(alias, aliases):
    return aliases.get(alias)

def resolve_alias(alias):
    aliases = load_aliases()
    return lookup_alias(alias, aliases)