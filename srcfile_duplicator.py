import os
import uuid
import shutil

src = "./assets/hero_images/LifeWeaver.png"
dst = "./assets/top_500_unprocessed_images/train/38/"

for i in range(108):
    shutil.copyfile(src, dst + uuid.uuid4().hex + ".png")
