import lightning as L
from lightning.pytorch.utilities import rank_zero_only
from data.cdn_stream import make_cdn_dataset

def get_or_create_studio(name: str, machine: L.Machine = L.Machine.L40S):
    teamspace = L.Teamspace()
    for s in teamspace.studios:
        if s.name == name and s.status == "Running":
            print(f"Reusing running studio: {name}")
            return s
    print(f"Creating studio: {name}")
    return L.Studio(name=name, machine=machine, create_ok=True)

def train_with_cdn(manifest_path: str, studio_name: str = "surrogate-1-cdn"):
    studio = get_or_create_studio(studio_name)
    if studio.status != "Running":
        print("Studio not running; restarting...")
        studio.start(machine=L.Machine.L40S)

    dataset = list(make_cdn_dataset(manifest_path, shard_id=0, n_shards=1))
    print(f"Loaded {len(dataset)} pairs via CDN (zero HF API calls)")

    # Replace with your DataModule/Model/Trainer
    # dm = YourDataModule(dataset)
    # model = YourModel()
    # trainer = L.Trainer(max_epochs=1, devices=1)
    # trainer.fit(model, dm)

    rank_zero_only(print)("Training step skipped (replace with your trainer)")

if __name__ == "__main__":
    import sys
    manifest = sys.argv[1] if len(sys.argv) > 1 else "manifest-2026-05-03.json"
    train_with_cdn(manifest)