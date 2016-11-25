import skimage.io
import selectivesearch

img = skimage.io.imread('93.jpg')
img_lbl, regions = selectivesearch.selective_search(img, scale=500, sigma=0.9, min_size=10)
print(regions)
# regions = selective_search(img,color_spaces = ['rgb', 'hsv'],ks = [50, 150, 300],feature_masks = [(0, 0, 1, 1)])
# for v, (i0, j0, i1, j1) in regions:
