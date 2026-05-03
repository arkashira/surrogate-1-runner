#!/usr/bin/env python3
import os
from lightning import Lightning, L40S, Teamspace

STUDIO_NAME = os.getenv("LIGHTNING_STUDIO_NAME", "surrogate-1-train")

def get_or_create_studio():
    # Reuse running studio
    for s in Teamspace.studios:
        if s.name == STUDIO_NAME and s.status == "running":
            print(f"Reusing running studio: {s.name}")
            return s
    # Create if not exists (will reuse stopped studio object via create_ok)
    print(f"Creating/reusing studio: {STUDIO_NAME}")
    return Lightning.Studio(
        name=STUDIO_NAME,
        machine=L40S,
        create_ok=True,
    )

def ensure_running(studio):
    if studio.status != "running":
        print(f"Studio stopped ({studio.status}), restarting...")
        studio.target.start(machine=L40S)
    return studio

if __name__ == "__main__":
    studio = get_or_create_studio()
    studio = ensure_running(studio)
    print(f"Studio {studio.name} is {studio.status}")