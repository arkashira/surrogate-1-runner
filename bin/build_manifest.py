from data.cdn_loader import CDNParquetPairs
from lightning import Fabric

fabric = Fabric()
train_ds = CDNParquetPairs("snapshots/2026-05-03/snapshot.json")
train_dl = torch.utils.data.DataLoader(train_ds, batch_size=8, num_workers=4)
train_dl = fabric.setup_dataloaders(train_dl)