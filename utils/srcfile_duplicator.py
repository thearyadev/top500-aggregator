import importlib
import os
import shutil
import uuid

src = "./assets/hero_images/Mauga.png"
train_dst = "./assets/top_500_unprocessed_images/train/40/"  # ensure these directories are created
test_dst = "./assets/top_500_unprocessed_images/test/40/"  # ensure these directories are created

for i in range(108):
    shutil.copyfile(src, train_dst + uuid.uuid4().hex + ".png")

for i in range(27):
    shutil.copyfile(src, test_dst + uuid.uuid4().hex + ".png")
