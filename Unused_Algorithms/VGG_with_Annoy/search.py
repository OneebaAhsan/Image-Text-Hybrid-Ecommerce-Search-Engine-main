from PIL import Image
import time
from feature_extractor import FeatureExtractor
import pickle
from annoy import AnnoyIndex

annoy = AnnoyIndex(4096, 'angular')
annoy.load('dataset.tree')
img_paths = pickle.load(open('img_paths.pkl', 'rb'))

fe = FeatureExtractor()

test_image_path = input('Enter the path of the image you want to search: ')
test_image = Image.open(test_image_path)
initial_time = time.time()
query = fe.extract(test_image)
ids, dists = annoy.get_nns_by_vector(query, 10, search_k=-1, include_distances=True)
scores = [(img_paths[id], dist) for id, dist in zip(ids, dists)]
final_time = time.time()

print('Searching for:', test_image_path)
print('Found:')
for img_path, dist in scores:
    print('\t{} (score: {})'.format(img_path, dist))
