import torch
from torch.utils.data import DataLoader
from .validation.validator import validate_model
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_model(train_loader, val_loader, model, optimizer, criterion, epochs, val_threshold=0.85):
    """
    Trains the model and validates it after each epoch.
    
    Args:
        train_loader: DataLoader for training data
        val_loader: DataLoader for validation data
        model: PyTorch model
        optimizer: Optimizer
        criterion: Loss function
        epochs: Number of training epochs
        val_threshold: Minimum validation accuracy to pass (default: 0.85)
    
    Returns:
        Trained model if validation passes, else None
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for epoch in range(epochs):
        # Training phase
        model.train()
        total_train_loss = 0
        for batch in train_loader:
            inputs, labels = batch['input_ids'], batch['labels']
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            total_train_loss += loss.item()
        
        # Validation phase
        val_result = validate_model(model, val_loader, device)
        logger.info(f"Epoch {epoch+1}/{epochs} - Validation Accuracy: {val_result['metrics']['accuracy']:.4f}")
        
        if not val_result['pass']:
            logger.warning(f"Validation failed at epoch {epoch+1}. Stopping training.")
            return None
    
    logger.info("Training completed successfully.")
    return model