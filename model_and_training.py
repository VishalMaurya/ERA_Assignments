# model_and_training.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as T

# Albumentations for augmentation
import albumentations as A
from albumentations.pytorch import ToTensorV2
import numpy as np

# -----------------------
# Depthwise separable conv
# -----------------------
class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_ch, out_ch, kernel_size=3, stride=1, padding=1, dilation=1):
        super().__init__()
        self.dw = nn.Conv2d(in_ch, in_ch, kernel_size=kernel_size, stride=stride,
                            padding=padding, dilation=dilation, groups=in_ch, bias=False)
        self.pw = nn.Conv2d(in_ch, out_ch, kernel_size=1, bias=False)
        self.bn = nn.BatchNorm2d(out_ch)
        self.act = nn.ReLU(inplace=True)
    def forward(self, x):
        x = self.dw(x)
        x = self.pw(x)
        x = self.bn(x)
        return self.act(x)

# -----------------------
# The network (meets constraints)
# -----------------------
class CIFAR_GAP_Net(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        # Block 1: Conv 3x3 stride2 -> downsample 32x32 -> 16x16
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1, bias=False), # stride2
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
        )
        # Block 2: Depthwise separable conv with stride2 -> downsample 16x16 -> 8x8
        self.dw_sep = DepthwiseSeparableConv(in_ch=32, out_ch=64, kernel_size=3, stride=2, padding=1)
        # Block 3: Dilated conv (dilation=2) (no downsample) -> keeps 8x8
        self.dilated1 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=2, dilation=2, bias=False), # dilated conv
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )
        # Block 4: Conv 3x3 stride2 -> downsample 8x8 -> 4x4
        self.conv5 = nn.Sequential(
            nn.Conv2d(64, 96, kernel_size=3, stride=2, padding=1, bias=False), # stride2
            nn.BatchNorm2d(96),
            nn.ReLU(inplace=True),
            nn.Conv2d(96, 96, kernel_size=1, stride=1, bias=False),
            nn.BatchNorm2d(96),
            nn.ReLU(inplace=True),
        )
        # Extra dilated conv (dilation=4) to expand RF (no downsample)
        self.dilated2 = nn.Sequential(
            nn.Conv2d(96, 96, kernel_size=3, stride=1, padding=4, dilation=4, bias=False),
            nn.BatchNorm2d(96),
            nn.ReLU(inplace=True),
        )
        # GAP + classifier
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(96, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.dw_sep(x)
        x = self.dilated1(x)
        x = self.conv5(x)
        x = self.dilated2(x)
        x = self.gap(x)             # -> (B, 96, 1, 1)
        x = torch.flatten(x, 1)     # -> (B, 96)
        out = self.fc(x)
        return out

# -----------------------
# Utility: count params
# -----------------------
def count_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

# -----------------------
# Augmentations (Albumentations)
# -----------------------
# CIFAR-10 channel-wise mean (standard): (0.4914, 0.4822, 0.4465)
CIFAR_MEAN = (0.4914, 0.4822, 0.4465)

train_transforms = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=15, p=0.5),
    A.CoarseDropout(max_holes=1, max_height=16, max_width=16, min_holes=1, min_height=16, min_width=16,
                    fill_value=[int(255*m) for m in CIFAR_MEAN], mask_fill_value=None, p=0.5),
    A.Normalize(mean=CIFAR_MEAN, std=(0.247, 0.243, 0.261)),
    ToTensorV2(),
])

# For validation/test: just normalize and to-tensor
val_transforms = A.Compose([
    A.Normalize(mean=CIFAR_MEAN, std=(0.247, 0.243, 0.261)),
    ToTensorV2(),
])

# Wrappers to use albumentations with torchvision datasets
class AlbumentationsTransform:
    def __init__(self, aug): self.aug = aug
    def __call__(self, img):
        # img is PIL Image -> convert to np
        arr = np.array(img)
        res = self.aug(image=arr)
        return res['image']

# -----------------------
# Training recipe (skeleton)
# -----------------------
def get_dataloaders(batch_size=128, num_workers=4):
    train_ds = torchvision.datasets.CIFAR10(root='./data', train=True, download=True,
                                            transform=AlbumentationsTransform(train_transforms))
    val_ds = torchvision.datasets.CIFAR10(root='./data', train=False, download=True,
                                          transform=AlbumentationsTransform(val_transforms))
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)
    return train_loader, val_loader

# Example training loop skeleton (fill in logging/checkpointing)
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for x,y in loader:
        x,y = x.to(device), y.to(device)
        optimizer.zero_grad()
        out = model(x)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * x.size(0)
        preds = out.argmax(dim=1)
        correct += (preds==y).sum().item()
        total += x.size(0)
    return running_loss/total, correct/total

def eval_epoch(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for x,y in loader:
            x,y = x.to(device), y.to(device)
            out = model(x)
            loss = criterion(out, y)
            running_loss += loss.item() * x.size(0)
            preds = out.argmax(dim=1)
            correct += (preds==y).sum().item()
            total += x.size(0)
    return running_loss/total, correct/total

# Example: instantiation + training hyperparams
if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CIFAR_GAP_Net(num_classes=10).to(device)
    print("Params:", count_params(model))  # expected ~198666
    train_loader, val_loader = get_dataloaders(batch_size=128)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)  # label smoothing helps
    optimizer = optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200)

    # Train for many epochs (example)
    for epoch in range(1, 201):
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = eval_epoch(model, val_loader, criterion, device)
        scheduler.step()
        print(f"Epoch {epoch:03d}: train_loss {train_loss:.4f}, train_acc {train_acc:.4f}, val_acc {val_acc:.4f}")
        # save best model, early stop, etc.
