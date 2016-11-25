"""
Generate data used in the HDF5DataLayer and GradientBasedSolver tests.
"""
import os
import numpy as np
import h5py
import skimage.io

te_tr = "Test"

res = 32

##################
from PIL import Image
baseDir = te_tr+"/"
images=[]
images_label = []
pokemon = sorted([i.strip() for i in open("Kanto.txt").readlines()])

for d in sorted(os.listdir(baseDir)):
    print(d)
    for f in sorted(os.listdir(baseDir + d)):
        # images.append(np.asarray(Image.open(baseDir + d + "/" + f).convert("RGBA").resize((res, res), Image.ANTIALIAS)))
        # images.append(np.asarray(Image.open(baseDir + d + "/" + f).convert("RGBA")))
        img = skimage.img_as_float(skimage.io.imread(baseDir + d + "/" + f)).astype(np.int8)
        if img.shape[2] == 4:
            img = img[:, :, :3]
        caffe_in = img.astype(np.int8, copy=False).transpose(2,0,1)
        images.append(caffe_in)
        images_label.append(pokemon.index(d.split(".")[0]))
###################

# Generate HDF5DataLayer sample_data.h5
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir+="/HDF5"+te_tr
os.makedirs(script_dir)

# num_images = len(images)
# height = images[0].shape[0]
# width = images[0].shape[1]
# channels = images[0].shape[2]
# total_size = num_images * height * width * channels

data = np.asarray(images)

# We had a bug where data was copied into label, but the tests weren't
# catching it, so let's make label 1-indexed.
# print(images_label[0])
label = np.asarray(images_label)
# print(label[0])
# label = label.astype('float32')

# We add an extra label2 dataset to test HDF5 layer's ability
# to handle arbitrary number of output ("top") Blobs.
# label2 = label + 1

# print (data)
print (len(label))

with h5py.File(script_dir + '/data.h5', 'w') as f:
    f['data'] = data
    f['label'] = label
    # f['label2'] = label2

# with h5py.File(script_dir + '/data_2_gzip.h5', 'w') as f:
#     f.create_dataset(
#         'data', data=data,
#         compression='gzip', compression_opts=1
#     )
#     f.create_dataset(
#         'label', data=label,
#         compression='gzip', compression_opts=1,
#         dtype='uint8',
#     )
#     f.create_dataset(
#         'label2', data=label2,
#         compression='gzip', compression_opts=1,
#         dtype='uint8',
#     )

with open(script_dir + '/data_list_'+te_tr+'.txt', 'w') as f:
    f.write(script_dir + '/data.h5\n')
#     f.write(script_dir + '/data_2_gzip.h5\n')

# # Generate GradientBasedSolver solver_data.h5

# num_cols = 3
# num_rows = 8
# height = 10
# width = 10

# data = np.random.randn(num_rows, num_cols, height, width)
# data = data.reshape(num_rows, num_cols, height, width)
# data = data.astype('float32')

# targets = np.random.randn(num_rows, 1)
# targets = targets.astype('float32')

# print data
# print targets

# with h5py.File(script_dir + '/solver_data.h5', 'w') as f:
#     f['data'] = data
#     f['targets'] = targets

# with open(script_dir + '/solver_data_list.txt', 'w') as f:
#     f.write('src/caffe/test/test_data/solver_data.h5\n')
