from torch.utils.data import DataLoader

train_data = CDNParquetIterable()
loader = DataLoader(train_data, batch_size=8, num_workers=2)

for batch in loader:
    # batch = {"prompt": [...], "response": [...]}
    ...