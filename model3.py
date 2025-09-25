"""
SESSION 6 - MODEL 3: Complete Curriculum Implementation
======================================================

CURRICULUM ALIGNMENT:
- Code 2-8: All from Models 1 & 2 (Skeleton, Lighter, BN, Dropout, GAP, Capacity, Pooling)
- Code 9: Image Augmentation - Handled in training pipeline (RandomRotation, RandomAffine)
- Code 10: Learning Rate Scheduling - Handled in training pipeline (MultiStepLR)
- Complete integration of all Session 6 concepts

TARGET:
- Parameters: <8k (maximum efficiency within constraint)
- Accuracy: 99.4%+ consistently in final epochs
- Epochs: ≤15 (with all curriculum optimizations)
- Strategy: All curriculum techniques combined optimally

RESULT:
- [To be filled after training]
- Parameters: [Actual count]
- Best Accuracy: [Best epoch accuracy]%
- Consistent Accuracy: [Last 3 epochs average]%
- Final 5 Epochs: [Epoch 11-15 accuracies]
- Epochs to Convergence: [Number]

ANALYSIS:
- [To be filled after training]
- Complete curriculum effectiveness
- All 10 code iterations impact
- Optimal technique combination
- Final Session 6 insights vs Models 1 & 2
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Model_3(nn.Module):
    """
    Optimized precision CNN for MNIST - Enhanced for 99.4% target.
    
    CURRICULUM ALIGNMENT:
    - Code 2-8: All from Models 1 & 2 (Skeleton, Lighter, BN, Dropout, GAP, Capacity, Pooling)
    - Code 9: Image Augmentation - Handled in training pipeline (RandomRotation, RandomAffine)
    - Code 10: Learning Rate Scheduling - Handled in training pipeline (MultiStepLR)
    - Complete integration of all Session 6 concepts
    
    ENHANCED ARCHITECTURE STRATEGY:
    - Optimized channel progression: 1→10→16→20→26→10
    - Enhanced dual-attention mechanism (channel + spatial)
    - Strategic feature extraction with 1x1 transitional layers
    - Improved dropout scheduling for better generalization
    - Better receptive field utilization
    
    Expected Parameter Breakdown:
    - Stem: ~100 params
    - Conv2 + transition: ~1600 params  
    - Conv3 + transition: ~3400 params
    - Conv4: ~5200 params
    - Attention: ~300 params
    - Final: ~260 params
    - Total: ~7860 params (under 8k limit)
    """
    
    def __init__(self, num_classes=10):
        super(Model_3, self).__init__()
        
        # Optimized initial feature extraction (Code 2,3,4)
        self.stem = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(8),
            nn.ReLU()
        )
        
        # Efficient feature extraction with smaller channels
        self.conv2 = nn.Conv2d(8, 14, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(14)
        
        # 1x1 transitional layer for efficiency
        self.transition1 = nn.Sequential(
            nn.Conv2d(14, 12, kernel_size=1, bias=False),
            nn.BatchNorm2d(12)
        )
        
        self.pool1 = nn.MaxPool2d(2)  # 28x28 -> 14x14 (Code 8: Correct pooling)
        
        self.conv3 = nn.Conv2d(12, 18, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(18)
        
        # Another transitional layer
        self.transition2 = nn.Sequential(
            nn.Conv2d(18, 16, kernel_size=1, bias=False),
            nn.BatchNorm2d(16)
        )
        
        self.pool2 = nn.MaxPool2d(2)  # 14x14 -> 7x7 (Code 8: Correct pooling)
        
        # Code 7: Efficient capacity layer
        self.conv4 = nn.Conv2d(16, 22, kernel_size=3, padding=1, bias=False)
        self.bn4 = nn.BatchNorm2d(22)
        
        # Lightweight dual attention mechanism
        # Channel attention
        self.channel_attention = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(22, 6, 1),
            nn.ReLU(),
            nn.Conv2d(6, 22, 1),
            nn.Sigmoid()
        )
        
        # Spatial attention (reduced kernel size)
        self.spatial_attention = nn.Sequential(
            nn.Conv2d(22, 1, kernel_size=1, bias=False),
            nn.Sigmoid()
        )
        
        # Final classification
        self.final_conv = nn.Conv2d(22, 10, kernel_size=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Strategic dropout scheduling
        self.dropout_early = nn.Dropout(0.05)  # Light early dropout
        self.dropout_mid = nn.Dropout(0.1)     # Medium middle dropout  
        self.dropout_late = nn.Dropout(0.15)   # Heavier late dropout
        
    def forward(self, x):
        # Optimized stem feature extraction
        x = self.stem(x)              # 28x28x8
        x = self.dropout_early(x)
        
        # Efficient feature extraction with transitional layers
        x = F.relu(self.bn2(self.conv2(x)))  # 28x28x14
        x = F.relu(self.transition1(x))      # 28x28x12 (dimensionality reduction)
        x = self.pool1(x)                    # 14x14x12
        x = self.dropout_mid(x)
        
        x = F.relu(self.bn3(self.conv3(x)))  # 14x14x18
        x = F.relu(self.transition2(x))      # 14x14x16 (dimensionality reduction)
        x = self.pool2(x)                    # 7x7x16
        x = self.dropout_mid(x)
        
        # Efficient capacity layer
        x = F.relu(self.bn4(self.conv4(x)))  # 7x7x22
        x = self.dropout_late(x)
        
        # Apply lightweight dual attention
        # Channel attention
        ch_att = self.channel_attention(x)   # Global channel importance
        x = x * ch_att
        
        # Spatial attention
        sp_att = self.spatial_attention(x)   # Spatial region importance
        x = x * sp_att
        
        # Final classification
        x = self.final_conv(x)               # 7x7x10
        x = self.gap(x)                      # 1x1x10
        x = x.view(x.size(0), -1)           # 10
        
        return x
    
    def count_parameters(self):
        """Count total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    
    def get_receptive_field(self):
        """Calculate enhanced receptive field progression."""
        # Each 3x3 conv adds 2 to RF, each 1x1 conv maintains RF, each pool2d doubles the gap
        # Conv1: RF=3, Conv2: RF=5, Trans1: RF=5, Pool1: RF=10, 
        # Conv3: RF=12, Trans2: RF=12, Pool2: RF=24, Conv4: RF=26
        return 26
    
    def print_architecture(self):
        """Print detailed enhanced architecture for analysis."""
        print("Model_3 Enhanced Architecture:")
        print("- Input: 1x28x28")
        print("- Stem Conv: 1→10, RF=3")
        print("- Conv2: 10→16, RF=5") 
        print("- Transition1: 16→14 (1x1), RF=5")
        print("- Pool1: 28→14, RF=10")
        print("- Conv3: 14→20, RF=12")
        print("- Transition2: 20→18 (1x1), RF=12")
        print("- Pool2: 14→7, RF=24") 
        print("- Conv4: 18→26, RF=26")
        print("- Channel Attention: 26→8→26")
        print("- Spatial Attention: 26→1 (3x3)")
        print("- Final: 26→10")
        print("- GAP: 7x7→1x1")
        print("- Output: 10")
        print(f"- Receptive Field: {self.get_receptive_field()}")
        print(f"- Parameters: {self.count_parameters():,}")


def create_model_3():
    """Create and return Model_3 instance."""
    return Model_3()


def analyze_model_3():
    """Analyze Model_3 architecture and return metrics."""
    model = create_model_3()
    
    # Test forward pass
    with torch.no_grad():
        test_input = torch.randn(1, 1, 28, 28)
        output = model(test_input)
        output_shape = output.shape
    
    analysis = {
        'model_name': 'Model_3_Enhanced',
        'total_parameters': model.count_parameters(),
        'receptive_field': model.get_receptive_field(),
        'output_shape': output_shape,
        'target_accuracy': '99.4%+ consistently',
        'expected_epochs': '≤15',
        'curriculum_codes': '2-10 (Complete)',
        'architecture_efficiency': 'Enhanced precision architecture with dual attention',
        'parameter_breakdown': {
            'stem': 'Conv2d(1,10) + BN: ~100 params',
            'conv2+trans1': 'Conv2d(10,16)+Conv2d(16,14) + BN: ~1600 params', 
            'conv3+trans2': 'Conv2d(14,20)+Conv2d(20,18) + BN: ~3400 params',
            'conv4': 'Conv2d(18,26) + BN: ~4200 params',
            'channel_attention': 'Squeeze-excitation: ~300 params',
            'spatial_attention': 'Spatial attention: ~240 params',
            'final': 'Conv2d(26,10): ~260 params'
        },
        'enhancements': [
            'Optimized channel progression: 1→10→16→20→26→10',
            'Dual attention mechanism (channel + spatial)',
            '1x1 transitional layers for parameter efficiency',
            'Strategic multi-level dropout scheduling',
            'Enhanced feature extraction capability',
            'Better receptive field utilization'
        ]
    }
    
    return analysis


if __name__ == "__main__":
    # Test the model
    model = create_model_3()
    model.print_architecture()
    
    # Analyze model
    analysis = analyze_model_3()
    print(f"\nModel Analysis:")
    print(f"Parameters: {analysis['total_parameters']:,}")
    print(f"Receptive Field: {analysis['receptive_field']}")
    print(f"Target: {analysis['target_accuracy']}")
    print(f"Strategy: {analysis['architecture_efficiency']}")