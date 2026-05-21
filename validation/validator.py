import torch
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score
import numpy as np

def validate_model(model, val_loader, device):
    """
    Validates the model on the validation dataset.
    
    Args:
        model: Trained PyTorch model
        val_loader: DataLoader for validation data
        device: torch.device (e.g., 'cuda' or 'cpu')
    
    Returns:
        dict: {'pass': bool, 'metrics': dict}
    """
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for batch in val_loader:
            inputs, labels = batch['input_ids'], batch['labels']
            inputs, labels = inputs.to(device), labels.to(device)
            
            outputs = model(inputs)
            _, preds = torch.max(outputs, dim=1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    accuracy = accuracy_score(all_labels, all_preds)
    return {
        'pass': accuracy > 0.85,
        'metrics': {'accuracy': accuracy}
    }