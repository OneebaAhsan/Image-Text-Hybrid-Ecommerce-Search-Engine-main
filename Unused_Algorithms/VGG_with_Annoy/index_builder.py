import glob
import os
import pickle
from PIL import Image
from feature_extractor import FeatureExtractor

from annoy import AnnoyIndex

fe = FeatureExtractor()
a = AnnoyIndex(4096, 'angular')

img_paths = [img_path for img_path in sorted(glob.glob('../Shopon/*/*.png'))]
# png_paths = [img_path for img_path in sorted(glob.glob('static/dataset/MXR_Bookcovers/*.png'))]
# img_paths.extend(png_paths)
for idx, img_path in enumerate(img_paths):
    try:
        print(img_path)
        img = Image.open(img_path)  # PIL image
        feature = fe.extract(img)
        a.add_item(idx, feature)
    except Exception as e:
        print(e)

a.build(10)
a.save('index.ann')

a.load("index.ann")

# with open('index.pkl', 'wb') as f:
#     pickle.dump(a, f)

# a.build(-1)
print('index all images in database success!')
a.save('dataset.tree')
pickle.dump(img_paths, open('img_paths.pkl' ,'wb'))