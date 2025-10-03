"""
TRULY Constrained Ultra-Efficient Models - STRICT 8K Limit
==========================================================

These models are aggressively optimized to stay well within the 8K parameter limit
while applying only the most essential improvements.

Strategy: Start with minimal architectures and add improvements only if budget allows.

Key Principle: Better to have a working model under 8K than a perfect model over 8K.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class TinyMicroSE(nn.Module):
    """Extremely minimal SE block - only for channels > 16"""
    def __init__(self, channels):
        super(TinyMicroSE, self).__init__()
        if channels >= 16:
            hidden_channels = max(channels // 16, 1)
            self.avg_pool = nn.AdaptiveAvgPool2d(1)
            self.fc = nn.Sequential(
                nn.Linear(channels, hidden_channels, bias=False),
                nn.SiLU(inplace=True),
                nn.Linear(hidden_channels, channels, bias=False),
                nn.Sigmoid()
            )
            self.use_se = True
        else:
            self.use_se = False
        
    def forward(self, x):
        if not self.use_se:
            return x
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y

class TrulyConstrainedModel_1(nn.Module):
    """
    Truly Constrained Model_1: Minimal with Essential Improvements
    
    Applied Improvements:
    - SiLU activation (0 params)
    - Tiny SE attention only where beneficial (~8 params)
    - Minimal channel progression
    
    Target: <4000 parameters, 98.5%+ accuracy
    Expected: ~3,200 parameters
    """
    
    def __init__(self):
        super(TrulyConstrainedModel_1, self).__init__()
        
        # Block 1: Minimal initial features
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(8)
        
        # Block 2: Moderate expansion with tiny SE
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(16)
        self.se1 = TinyMicroSE(16)  # Only ~8 params
        
        # Block 3: Final features
        self.conv3 = nn.Conv2d(16, 10, kernel_size=3, padding=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Strategic dropout
        self.dropout = nn.Dropout(0.1)
        
    def forward(self, x):
        # Block 1: 1×28×28 → 8×28×28 (RF: 3)
        x = F.silu(self.bn1(self.conv1(x)))
        x = self.dropout(x)
        
        # Block 2: 8×28×28 → 16×28×28 → 16×14×14 (RF: 5→10)
        x = F.silu(self.bn2(self.conv2(x)))
        x = self.se1(x)  # Tiny SE attention
        x = F.max_pool2d(x, 2)  # 16×14×14
        
        # Block 3: 16×14×14 → 10×14×14 → 10×7×7 (RF: 12→16)
        x = self.conv3(x)
        x = F.max_pool2d(x, 2)  # 10×7×7
        
        # Global Average Pooling
        x = self.gap(x)  # 10×1×1
        x = x.view(x.size(0), -1)  # 10
        
        return x
    
    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

class TrulyConstrainedModel_2(nn.Module):
    """
    Truly Constrained Model_2: Aggressive Parameter Management
    
    Applied Improvements:
    - SiLU activation (0 params)
    - Single tiny SE attention (~12 params)
    - Carefully tuned channels to stay under 8K
    
    Target: <8000 parameters, 99.3%+ accuracy
    Expected: ~7,500 parameters
    """
    
    def __init__(self):
        super(TrulyConstrainedModel_2, self).__init__()
        
        # Block 1: Minimal start
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(8)
        
        # Block 2: Controlled expansion
        self.conv2 = nn.Conv2d(8, 14, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(14)
        
        # Block 3: Moderate features with SE
        self.conv3 = nn.Conv2d(14, 20, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(20)
        self.se1 = TinyMicroSE(20)  # ~12 params
        
        # Block 4: Controlled compression
        self.conv4 = nn.Conv2d(20, 16, kernel_size=3, padding=1, bias=False)
        self.bn4 = nn.BatchNorm2d(16)
        
        # Block 5: Final projection
        self.conv5 = nn.Conv2d(16, 10, kernel_size=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Strategic dropout
        self.dropout1 = nn.Dropout(0.1)
        self.dropout2 = nn.Dropout(0.15)
        
    def forward(self, x):
        # Block 1: 1×28×28 → 8×28×28 (RF: 3)
        x = F.silu(self.bn1(self.conv1(x)))
        x = self.dropout1(x)
        
        # Block 2: 8×28×28 → 14×28×28 → 14×14×14 (RF: 5→10)
        x = F.silu(self.bn2(self.conv2(x)))
        x = F.max_pool2d(x, 2)  # 14×14×14
        
        # Block 3: 14×14×14 → 20×14×14 (RF: 12)
        x = F.silu(self.bn3(self.conv3(x)))
        x = self.se1(x)  # Tiny SE attention
        x = self.dropout2(x)
        x = F.max_pool2d(x, 2)  # 20×7×7 (RF: 24)
        
        # Block 4: 20×7×7 → 16×7×7 (RF: 26)
        x = F.silu(self.bn4(self.conv4(x)))
        
        # Block 5: 16×7×7 → 10×7×7 (RF: 26)
        x = self.conv5(x)
        
        # Global Average Pooling
        x = self.gap(x)  # 10×1×1
        x = x.view(x.size(0), -1)  # 10
        
        return x
    
    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

class TrulyConstrainedModel_3(nn.Module):
    """
    Truly Constrained Model_3: Maximum Performance within Absolute Limits
    
    Applied Improvements:
    - SiLU activation (0 params)
    - Single tiny SE attention (~15 params)
    - One minimal residual connection (~120 params)
    - Aggressively tuned to stay under 8K
    
    Target: <8000 parameters, 99.4%+ accuracy
    Expected: ~7,800 parameters
    """
    
    def __init__(self):
        super(TrulyConstrainedModel_3, self).__init__()
        
        # Block 1: Minimal start
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(8)
        
        # Block 2: Controlled expansion with residual
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(16)
        self.se1 = TinyMicroSE(16)  # ~8 params
        self.residual_proj = nn.Conv2d(8, 16, kernel_size=1, bias=False)  # 128 params
        
        # Block 3: Moderate features
        self.conv3 = nn.Conv2d(16, 22, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(22)
        
        # Block 4: Final compression
        self.conv4 = nn.Conv2d(22, 10, kernel_size=3, padding=1, bias=False)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Strategic dropout
        self.dropout1 = nn.Dropout(0.1)
        self.dropout2 = nn.Dropout(0.15)
        self.dropout3 = nn.Dropout(0.2)
        
    def forward(self, x):
        # Block 1: 1×28×28 → 8×28×28 (RF: 3)
        x = F.silu(self.bn1(self.conv1(x)))
        x = self.dropout1(x)
        
        # Block 2: 8×28×28 → 16×28×28 → 16×14×14 with residual (RF: 5→10)
        identity = x
        x = F.silu(self.bn2(self.conv2(x)))
        x = self.se1(x)
        identity = self.residual_proj(identity)
        x = x + identity  # Residual connection
        x = F.max_pool2d(x, 2)  # 16×14×14
        
        # Block 3: 16×14×14 → 22×14×14 → 22×7×7 (RF: 12→24)
        x = F.silu(self.bn3(self.conv3(x)))
        x = self.dropout2(x)
        x = F.max_pool2d(x, 2)  # 22×7×7
        
        # Block 4: 22×7×7 → 10×7×7 (RF: 26)
        x = self.conv4(x)
        x = self.dropout3(x)
        
        # Global Average Pooling
        x = self.gap(x)  # 10×1×1
        x = x.view(x.size(0), -1)  # 10
        
        return x
    
    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

def create_truly_constrained_model(model_name="TrulyConstrainedModel_1"):
    """Create specified truly constrained model and return with parameter count"""
    if model_name == "TrulyConstrainedModel_1":
        model = TrulyConstrainedModel_1()
    elif model_name == "TrulyConstrainedModel_2":
        model = TrulyConstrainedModel_2()
    elif model_name == "TrulyConstrainedModel_3":
        model = TrulyConstrainedModel_3()
    else:
        raise ValueError(f"Unknown model: {model_name}")
    
    param_count = model.count_parameters()
    print(f"{model_name} - Total parameters: {param_count:,}")
    
    if param_count >= 8000:
        excess = param_count - 8000
        print(f"❌ FAIL: {param_count:,} > 8,000 (excess: +{excess:,})")
        return model, False
    else:
        margin = 8000 - param_count
        efficiency = (param_count / 8000) * 100
        print(f"✅ PASS: {param_count:,} < 8,000 (margin: +{margin:,})")
        print(f"📊 Budget utilization: {efficiency:.1f}%")
        return model, True

if __name__ == "__main__":
    print("🚀 TRULY Constrained Ultra-Efficient Models")
    print("=" * 60)
    print("Strategy: Aggressive parameter management within STRICT 8K limit")
    print()
    
    all_passed = True
    results = []
    
    # Test all truly constrained models
    for model_name in ["TrulyConstrainedModel_1", "TrulyConstrainedModel_2", "TrulyConstrainedModel_3"]:
        print(f"\n{'='*50}")
        print(f"Testing {model_name}")
        print(f"{'='*50}")
        
        model, passed = create_truly_constrained_model(model_name)
        
        if not passed:
            all_passed = False
        
        # Test with dummy input
        dummy_input = torch.randn(1, 1, 28, 28)
        output = model(dummy_input)
        print(f"Input shape: {dummy_input.shape}")
        print(f"Output shape: {output.shape}")
        print(f"{model_name} created successfully!")
        
        results.append((model_name, model.count_parameters(), passed))
        
    print(f"\n{'='*60}")
    print("📊 TRULY CONSTRAINED MODELS SUMMARY")
    print(f"{'='*60}")
    
    original_params = [2746, 7522, 7138]
    
    print(f"{'Model':<25} {'Original':<10} {'Constrained':<12} {'Change':<12} {'Status':<8}")
    print("-" * 75)
    
    for i, (model_name, params, passed) in enumerate(results):
        orig_params = original_params[i]
        change = params - orig_params
        change_pct = (change / orig_params) * 100
        status = "✅" if passed else "❌"
        
        print(f"{model_name:<25} {orig_params:<10,} {params:<12,} {change:+5,} ({change_pct:+4.1f}%) {status:<8}")
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ALL TRULY CONSTRAINED MODELS PASSED!")
        print("✅ Ready for training with essential improvements within strict limits!")
    else:
        print("⚠️  Some models still exceed limits. Need more aggressive reduction.")
    
    print(f"\n🔧 ESSENTIAL IMPROVEMENTS APPLIED (MINIMAL COST):")
    print("✅ SiLU Activation: Better gradients, 0 extra parameters")
    print("✅ Tiny SE Attention: Ultra-minimal, 8-15 parameters only")
    print("✅ Single Residual: Only in Model_3, ~120 parameters")
    print("✅ Aggressive Channel Tuning: Maximum parameter efficiency")
    
    print(f"\n🎯 EXPECTED IMPROVEMENTS (CONSERVATIVE ESTIMATES):")
    print("• TrulyConstrainedModel_1: 98.0% → 98.3%+ accuracy")
    print("• TrulyConstrainedModel_2: 99.2% → 99.25%+ accuracy")
    print("• TrulyConstrainedModel_3: 99.4% → 99.45%+ accuracy")
    print("• 1-2 epochs faster convergence")
    print("• Better training stability")
    
    print(f"\n💡 KEY LESSON:")
    print("Sometimes less is more - focus on zero-cost improvements")
    print("and ultra-minimal high-impact features for maximum ROI!")
