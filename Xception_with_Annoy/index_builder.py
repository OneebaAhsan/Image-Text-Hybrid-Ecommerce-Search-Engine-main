import glob
import os
import pickle
from PIL import Image
from feature_extractor import FeatureExtractor

from annoy import AnnoyIndex

fe = FeatureExtractor()
annoy = AnnoyIndex(2048, 'angular')

img_paths = [img_path for img_path in sorted(glob.glob('../Shopon/*/*.png'))]
for idx, img_path in enumerate(img_paths):
    try:
        print(img_path)
        img = Image.open(img_path)  # PIL image
        feature = fe.extract(img)
        annoy.add_item(idx, feature)
    except Exception as e:
        print(e)

annoy.build(10)
annoy.save('index.ann')

print('index all images in database success!')
annoy.save('dataset.tree')
pickle.dump(img_paths, open('img_paths.pkl' ,'wb'))