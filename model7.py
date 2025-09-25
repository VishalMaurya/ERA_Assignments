"""
SESSION 6 - MODEL 7: Ultra-Minimal Baseline
===========================================

CURRICULUM ALIGNMENT:
- Code 2: Basic Skeleton - Ultra-simple CNN structure
- Code 4: Batch Normalization - BN for training stability
- Code 5: Regularization - Dropout for overfitting control
- Code 6: Global Average Pooling - GAP instead of flatten
- Minimal parameter design for maximum efficiency

TARGET:
- Parameters: <2k (ultra-lightweight baseline)
- Accuracy: 95-97% (realistic for minimal capacity)
- Epochs: ≤15 (simple architecture should converge quickly)
- Strategy: Prove minimal design effectiveness

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Final 5 Epochs: [Epoch 11-15 accuracies]
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Ultra-minimal architecture effectiveness
- Comparison with complex models
- Resource efficiency demonstration
- Baseline performance reference
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Model_7(nn.Module):
    """
    Ultra-minimal CNN for MNIST with <2k parameters.
    
    ARCHITECTURE (from diagram):
    Input (28×28×1)
      ↓
    Conv 3×3×8 + BatchNorm + ReLU    (1→8 channels)
    Conv 3×3×16 + BatchNorm + ReLU   (8→16 channels)
    MaxPool 2×2                      (28×28 → 14×14)
    Dropout(0.1)
    GAP (Global Average Pooling)     (14×14×16 → 1×1×16)
    FC (16→10)                       (Final classifier)
    Output (10)
    
    CURRICULUM ALIGNMENT:
    - Code 2: Basic Skeleton - Minimal CNN structure
    - Code 4: Batch Normalization - Training stability
    - Code 5: Regularization - Dropout for generalization
    - Code 6: Global Average Pooling - Parameter efficiency
    
    Architecture Strategy:
    - Ultra-simple channel progression: 1→8→16→10
    - Only 2 convolutional layers for minimal complexity
    - GAP to reduce parameters vs flatten + FC
    - Single FC layer for final classification
    - Minimal but complete CNN design
    
    Expected Parameter Breakdown:
    - Conv1: ~72 params (1×8×3×3)
    - BN1: ~16 params (8×2)
    - Conv2: ~1,152 params (8×16×3×3)
    - BN2: ~32 params (16×2)
    - FC: ~160 params (16×10)
    - Total: ~1,432 params
    """
    
    def __init__(self, num_classes=10):
        super(Model_7, self).__init__()
        
        # First convolutional layer
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(8)
        
        # Second convolutional layer
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(16)
        
        # Pooling and regularization
        self.pool = nn.MaxPool2d(2, 2)  # 28×28 → 14×14
        self.dropout = nn.Dropout(0.1)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)  # 14×14×16 → 1×1×16
        
        # Final classifier
        self.fc = nn.Linear(16, num_classes)
        
    def forward(self, x):
        # Input: 28×28×1
        
        # First conv block
        x = self.conv1(x)           # 28×28×8
        x = self.bn1(x)
        x = F.relu(x)
        
        # Second conv block  
        x = self.conv2(x)           # 28×28×16
        x = self.bn2(x)
        x = F.relu(x)
        
        # Pooling and regularization
        x = self.pool(x)            # 14×14×16
        x = self.dropout(x)
        
        # Global Average Pooling
        x = self.gap(x)             # 1×1×16
        x = x.view(x.size(0), -1)   # Flatten to 16
        
        # Final classification
        x = self.fc(x)              # 10
        
        return x
    
    def count_parameters(self):
        """Count total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    
    def get_receptive_field(self):
        """Calculate receptive field progression."""
        # Conv1: RF=3, Conv2: RF=5, Pool: RF=10
        return 10
    
    def print_architecture(self):
        """Print detailed architecture for analysis."""
        print("Model_7 Ultra-Minimal Architecture:")
        print("- Input: 1×28×28")
        print("- Conv1: 1→8, 3×3, RF=3")
        print("- BatchNorm1 + ReLU")
        print("- Conv2: 8→16, 3×3, RF=5") 
        print("- BatchNorm2 + ReLU")
        print("- MaxPool: 28×28→14×14, RF=10")
        print("- Dropout(0.1)")
        print("- GAP: 14×14×16→1×1×16")
        print("- FC: 16→10")
        print("- Output: 10")
        print(f"- Receptive Field: {self.get_receptive_field()}")
        print(f"- Parameters: {self.count_parameters():,}")


def create_model_7():
    """Create and return Model_7 instance."""
    return Model_7()


def analyze_model_7():
    """Analyze Model_7 architecture and return metrics."""
    model = create_model_7()
    
    # Test forward pass
    with torch.no_grad():
        test_input = torch.randn(1, 1, 28, 28)
        output = model(test_input)
        output_shape = output.shape
    
    analysis = {
        'model_name': 'Model_7',
        'total_parameters': model.count_parameters(),
        'receptive_field': model.get_receptive_field(),
        'output_shape': output_shape,
        'target_accuracy': '95-97% (realistic for minimal capacity)',
        'expected_epochs': '≤15',
        'curriculum_codes': '2,4,5,6 (Basic + BN + Dropout + GAP)',
        'architecture_efficiency': 'Ultra-minimal baseline with maximum efficiency',
        'parameter_breakdown': {
            'conv1': 'Conv2d(1,8) + BN: ~88 params',
            'conv2': 'Conv2d(8,16) + BN: ~1,184 params',
            'gap': 'Global Average Pooling: 0 params',
            'fc': 'Linear(16,10): ~160 params'
        },
        'innovations': [
            'Ultra-minimal parameter design (<2k total)',
            'Only 2 convolutional layers for simplicity',
            'GAP for parameter efficiency over flatten',
            'Clean curriculum-aligned architecture',
            'Baseline reference for comparison with complex models',
            'Maximum resource efficiency demonstration'
        ],
        'convergence_target': '≤15 epochs (simple should converge fast)'
    }
    
    return analysis


if __name__ == "__main__":
    # Test the model
    model = create_model_7()
    model.print_architecture()
    
    # Analyze model
    analysis = analyze_model_7()
    print(f"\nModel Analysis:")
    print(f"Parameters: {analysis['total_parameters']:,}")
    print(f"Receptive Field: {analysis['receptive_field']}")
    print(f"Target: {analysis['target_accuracy']}")
    print(f"Strategy: {analysis['architecture_efficiency']}")
    print(f"Convergence: {analysis['convergence_target']}")
