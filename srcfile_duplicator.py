import os
import shutil
import uuid

# src = "./assets/hero_images/LifeWeaver.png"
# dst = "./assets/top_500_unprocessed_images/train/38/"

# for i in range(108):
#     shutil.copyfile(src, dst + uuid.uuid4().hex + ".png")

import importlib

package = importlib.import_module("models.thearyadev-2023-04-30")

print(getattr(package, "Model"))
## lol.