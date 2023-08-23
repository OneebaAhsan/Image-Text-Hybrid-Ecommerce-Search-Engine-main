import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
import glob
import pickle
from datetime import datetime
from annoy import AnnoyIndex

b = AnnoyIndex(2048, 'angular')
b.load('dataset.tree')
img_paths = pickle.load(open('img_paths.pkl', 'rb'))

fe = FeatureExtractor()

test_image_path = input('Enter the path of the image you want to search: ')
test_image = Image.open(test_image_path)
query = fe.extract(test_image)
ids, dists = b.get_nns_by_vector(query, 10, search_k=-1, include_distances=True)
scores = [(img_paths[id], dist) for id, dist in zip(ids, dists)]

print('\n\n\n')
print('Searching for:', test_image_path)
print('Found:')
for img_path, dist in scores:
    print('\t{} (score: {})'.format(img_path, dist))
