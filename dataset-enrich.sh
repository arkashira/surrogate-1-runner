from lightning import Lightning, Teamspace, Machine, Studio

team = Teamspace("your-team")
studio_name = "surrogate-1-train"

existing = [s for s in team.studios if s.name == studio_name and s.status == "Running"]
if existing:
    studio = existing[0]
    print(f"Reusing running studio: {studio.id}")
else:
    studio = Studio.create(name=studio_name, machine=Machine.L40S, create_ok=True)

if studio.status != "Running":
    studio.start(machine=Machine.L40S)

job = studio.run(
    "python train-cdn.py --file-list snapshot-2026-05-02.json",
    wait=False,
)