from shutil import copy
import sys


sys.path.append(".")


from model import NNModel, transformer
import torch.nn as nn
import torch
import torchvision # type: ignore
from pathlib import Path
from typing import Final
from heroes import Heroes
import uuid
from torch.utils.data import DataLoader
import shutil
CLASS_SIZE: Final[int] = 250
NUM_EPOCH: Final[int] = 5

def get_key_by_value(inputDict: dict[int, str], value: str) -> int:
    # if this returns none (not found) the caller will throw an exception. 
    return next((key for key, val in inputDict.items() if val == value), None) # type: ignore


def make_fs_dataset(assets_directory: Path) -> Path:
    hero_dir = assets_directory / "heroes"
    dataset_dir = assets_directory / "dataset"

    if dataset_dir.exists:
        shutil.rmtree(str(dataset_dir))
    dataset_dir.mkdir()


    assert hero_dir.exists()
    assert dataset_dir.exists()


    labels = Heroes().hero_labels

    for hero_image in hero_dir.iterdir():
        target_dir = dataset_dir / str(get_key_by_value(labels, hero_image.name.replace(".png", "")))
        target_dir.mkdir()
        for _ in range(CLASS_SIZE):
            shutil.copy(str(hero_image), str(target_dir /(uuid.uuid4().hex + ".png")))
        
    return dataset_dir


def main():
    dataset_path = make_fs_dataset(Path("./assets"))

    dataset = torchvision.datasets.ImageFolder(root=str(dataset_path), transform=transformer)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    test_dataset = torchvision.datasets.ImageFolder(root=str(dataset_path), transform=transformer)
    test_dataloader = DataLoader(test_dataset, batch_size=32)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = NNModel(num_classes=len(dataset.classes)).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()
    
    for epoch in range(NUM_EPOCH):
        model.train()
        
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()

            outputs = model(images)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()

        model.eval()
        val_loss = 0
        correct = 0
        with torch.no_grad():
            for images, labels in test_dataloader:
                outputs = model(images.to(device))
                val_loss += loss_fn(outputs, labels.to(device)).item()
                _, predicted = torch.max(outputs.data, 1)
                correct += (predicted == labels.to(device)).sum().item()
        val_accuracy  = correct / len(test_dataset)
        print(f"Epoch {epoch+1}: Validation Loss: {val_loss:.4f}, Accuracy: {val_accuracy:.2f}")
    
    model_dir = Path("./models/tm")
    model_dir.mkdir()

    torch.save(model.state_dict(), str(model_dir / "model.pth"))
    with open(model_dir / "classes", "w+") as f:
        f.write("\n".join(dataset.classes))
    
    shutil.copy(Path("./classifier/model.py"), model_dir / "model.py")


if __name__ == "__main__":
    main()
