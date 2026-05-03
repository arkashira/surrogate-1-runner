import os
from lightning import Studio, Teamspace, Machine

STUDIO_NAME = "surrogate-1-train"
MACHINE = Machine.L40S  # or priority order: try H200 in lightning-lambda-prod if quota

teamspace = Teamspace()
running = None
for s in teamspace.studios:
    if s.name == STUDIO_NAME and s.status == "Running":
        running = s
        break

if running:
    print(f"Reusing running studio: {running.name}")
    studio = running
else:
    print(f"Starting new studio: {STUDIO_NAME}")
    studio = Studio(
        name=STUDIO_NAME,
        machine=MACHINE,
        create_ok=True,
    )

# Ensure studio is running before .run()
if studio.status != "Running":
    print("Studio not running; starting...")
    studio.start(machine=MACHINE)

# Run training with CDN manifest
studio.run(
    "train.py",
    arguments=[
        "--manifest", "snapshots/2026-05-03/snapshot.json",
        "--output-dir", "outputs/run-001",
    ],
    cwd="/workspace",
)