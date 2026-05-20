import os
import json
from transformers import AutoModelForTokenClassification, AutoTokenizer
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from nltk.tokenize import word_tokenize

class InvoiceDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data[idx]['text']
        labels = self.data[idx]['labels']

        encoding = self.tokenizer.encode_plus(
            text,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(labels, dtype=torch.long),
        }

class InvoiceParser(nn.Module):
    def __init__(self):
        super(InvoiceParser, self).__init__()
        self.model = AutoModelForTokenClassification.from_pretrained('distilbert-base-uncased', num_labels=8)

    def forward(self, input_ids, attention_mask):
        outputs = self.model(input_ids, attention_mask=attention_mask)
        return outputs.logits

def train_model(model, device, loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for batch in loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    return total_loss / len(loader)

def evaluate_model(model, device, loader, criterion):
    model.eval()
    total_loss = 0
    predictions = []
    labels = []
    with torch.no_grad():
        for batch in loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, batch['labels'].to(device))

            total_loss += loss.item()
            _, predicted = torch.max(outputs, dim=1)
            predictions.extend(predicted.cpu().numpy())
            labels.extend(batch['labels'].cpu().numpy())

    return total_loss / len(loader), f1_score(labels, predictions, average='macro')

def extract_invoice_fields(file_path):
    # Load pre-trained model and tokenizer
    model = InvoiceParser()
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

    # Load invoice data
    if file_path.endswith('.pdf'):
        images = convert_from_path(file_path)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image)
    elif file_path.endswith('.jpg') or file_path.endswith('.png'):
        text = pytesseract.image_to_string(Image.open(file_path))
    else:
        with open(file_path, 'r') as f:
            text = f.read()

    # Preprocess text data
    tokens = word_tokenize(text)
    labels = [0] * len(tokens)

    # Create dataset and data loader
    dataset = InvoiceDataset([{'text': text, 'labels': labels}], tokenizer)
    loader = DataLoader(dataset, batch_size=1, shuffle=False)

    # Evaluate model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    criterion = nn.CrossEntropyLoss()

    loss, f1 = evaluate_model(model, device, loader, criterion)

    # Extract invoice fields
    fields = []
    with torch.no_grad():
        for batch in loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            outputs = model(input_ids, attention_mask)
            _, predicted = torch.max(outputs, dim=1)
            fields.extend(predicted.cpu().numpy())

    return fields

def main():
    # Train model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = InvoiceParser()
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-5)

    # Load training data
    train_data = []
    with open('/opt/axentx/surrogate-1/data/invoice_samples/train.json', 'r') as f:
        for line in f:
            train_data.append(json.loads(line))

    # Create dataset and data loader
    dataset = InvoiceDataset(train_data, AutoTokenizer.from_pretrained('distilbert-base-uncased'))
    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    for epoch in range(5):
        loss = train_model(model, device, loader, optimizer, criterion)
        print(f'Epoch {epoch+1}, Loss: {loss}')

    # Evaluate model
    test_data = []
    with open('/opt/axentx/surrogate-1/data/invoice_samples/test.json', 'r') as f:
        for line in f:
            test_data.append(json.loads(line))

    test_dataset = InvoiceDataset(test_data, AutoTokenizer.from_pretrained('distilbert-base-uncased'))
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

    loss, f1 = evaluate_model(model, device, test_loader, criterion)
    print(f'Test Loss: {loss}, F1 Score: {f1}')

    # Save model
    torch.save(model.state_dict(), '/opt/axentx/surrogate-1/models/invoice_parser.pth')

if __name__ == '__main__':
    main()