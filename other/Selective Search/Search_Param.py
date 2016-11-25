# -*- coding: utf-8 -*-
import skimage.data
import skimage.io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
import numpy as np
import sys

# 512x512 (resolution to be set if input image is too low or too high)
# dont force a rectangular image to 512x512 sqaure
# works best without resizing
# if resoltuion is too low like 100x100, then maybe resize (but the perfotmance will decrease)

candidates = set()
merged_candidates = set()
refined = set()
final = set()
final_extended = set()

def contains():
    x1, y1, w1, h1 = p
    for x, y, w, h in candidates:
        if x1>=x and y1 >= y and x1+w1 <= x+w and y1+h1 <= y+h:
            return True
        if x1<=x and y1 <= y and x1+w1 >= x+w and y1+h1 >= y+h:
            candidates.remove((x, y, w, h))
            return False
    return False

def extend_superbox():
    pass

def draw_superbox():
    # (x1,y1) top-left coord, (x2,y2) bottom-right coord, (w,h) size
    remp = set(refined)
    ref = list(refined)
    while len(ref) > 0:
        x1, y1, w1, h1 = ref[0]

        if len(ref) == 1: # final box
            final.add((x1, y1, w1, h1))
        else:
            ref.remove((x1, y1, w1, h1))
            remp.remove((x1, y1, w1, h1))

        over = set()
        nonover = set()
        for x2, y2, w2, h2 in remp:
            A = {'x1': x1, 'y1': y1, 'x2': x1+w1, 'y2': y1+h1, 'w': w1, 'h': h1}
            B = {'x1': x2, 'y1': y2, 'x2': x2+w2, 'y2': y2+h2, 'w': w2, 'h': h2}

            # overlap between A and B
            SA = A['w']*A['h']
            SB = B['w']*B['h']
            SI = np.max([ 0, np.min([A['x2'],B['x2']]) - np.max([A['x1'],B['x1']]) ]) * np.max([ 0, np.min([A['y2'],B['y2']]) - np.max([A['y1'],B['y1']]) ])
            SU = SA + SB - SI
            overlap_AB = float(SI) / float(SU)
            # print(overlap_AB)
            #

            if overlap_AB >= 0.20:
                over.add((B['x1'],B['y1'],B['w'],B['h']))
        # print(len(over))
        if len(over) != 0: #Overlap
            remp = remp - over
            for i in over: ref.remove(i)
            over.add((A['x1'],A['y1'],A['w'],A['h']))
            # print(over)
            final.add((min([i[0] for i in over]), min([i[1] for i in over]), max([i[0]+i[2] for i in over]) - min([i[0] for i in over]), max([i[1]+i[3] for i in over]) - min([i[1] for i in over])))
        else:   #No overlap
            final.add((A['x1'],A['y1'],A['w'],A['h']))

# def contains_remove():

#     for x, y, w, h in merged_candidates:
#         f = False
#         temp = set(merged_candidates)
#         temp.remove((x, y, w, h))
#         for x1, y1, w1, h1 in temp:
#             if x1>=x and y1 >= y and x1+w1 <= x+w and y1+h1 <= y+h:
#                 f = False
#                 break
#             # if x1<=x and y1 <= y and x1+w1 >= x+w and y1+h1 >= y+h:
#             else:
#                 f = True
#         if f == True:
#             refined.add((x, y, w, h))

def contains_remove():
    for x, y, w, h in merged_candidates:
        temp = set(merged_candidates)
        temp.remove((x, y, w, h))
        test = []
        for x1, y1, w1, h1 in temp:
            A = {'x1': x, 'y1': y, 'x2': x+w, 'y2': y+h, 'w': w, 'h': h}
            B = {'x1': x1, 'y1': y1, 'x2': x1+w1, 'y2': y1+h1, 'w': w1, 'h': h1}
            # overlap between A and B
            SA = A['w']*A['h']
            SB = B['w']*B['h']
            SI = np.max([ 0, np.min([A['x2'],B['x2']]) - np.max([A['x1'],B['x1']]) ]) * np.max([ 0, np.min([A['y2'],B['y2']]) - np.max([A['y1'],B['y1']]) ])
            SU = SA + SB - SI
            overlap_AB = float(SI) / float(SU)
            if overlap_AB > 0.0:
                # if x1>=x and y1 >= y and x1+w1 <= x+w and y1+h1 <= y+h:
                if x1<=x and y1 <= y and x1+w1 >= x+w and y1+h1 >= y+h:
                    test.append(False)
                else:
                    test.append(True)
            else:
                test.append(True)
        if all(test):
            refined.add((x, y, w, h))

def mean_rect(l):
    return (min([i[0] for i in l]), min([i[1] for i in l]), max([i[0]+i[2] for i in l]) - min([i[0] for i in l]), max([i[1]+i[3] for i in l]) - min([i[1] for i in l]))
    # x = 0
    # y = 0
    # w = 0
    # h = 0
    # # print(l)
    # for x1, y1, w1, h1 in l:
    #     x+=x1
    #     y+=y1
    #     w+=w1
    #     h+=h1
    # return (int(x/len(l)),int(y/len(l)),int(w/len(l)),int(h/len(l)))

def merge():
    global width, height
    thresh = int(((width+height)/2)*(0.14)) #0.01

    tempc = set()
    for x, y, w, h in candidates:
        if (x, y, w, h) in tempc: continue
        temp = set()
        temp.add((x, y, w, h))
        for x1, y1, w1, h1 in candidates:
            if abs(x1-x) <= thresh and abs(y1-y) <= thresh and abs(w1-w) <= thresh and abs(h1-h) <= thresh:
                temp.add((x1, y1, w1, h1))
                tempc.add((x1, y1, w1, h1))
        merged_candidates.add(mean_rect(temp))
    contains_remove()

for sc in [350,450,500]:
    for sig in [0.8]:
        for mins in [30,60,120]: # important
            name = sys.argv[1]  # Filename
            img = skimage.io.imread(name)[:,:,:3]
            # perform selective search
            img_lbl, regions = selectivesearch.selective_search(
                img, scale=sc, sigma= sig,min_size = mins)

            for r in regions:
                # excluding same rectangle (with different segments)
                if r['rect'] in candidates:
                    continue
                # excluding regions smaller than 2000 pixels
                if r['size'] < 2000:
                    continue
                # distorted rects
                x, y, w, h = r['rect']
                if w / h > 1.2 or h / w > 1.2:
                    continue
                if w >= (img.shape[0]-1)*(0.9) and h >= (img.shape[1]-1)*(0.9):
                    continue
                candidates.add(r['rect'])
            print(str(sc)+"_"+str(sig)+"_"+str(mins))

# name = "PokeLARGE.jpg"  # Filename
img = skimage.io.imread(name)
width = len(img[0])
height = len(img)

# candidates={(0, 0, 278, 235), (0, 141, 221, 218), (98, 102, 211, 177), (0, 0, 274, 235), (11, 263, 94, 96), (211, 96, 257, 263), (295, 70, 323, 289), (93, 192, 148, 144), (0, 141, 166, 163), (474, 199, 147, 145), (576, 283, 63, 72), (12, 263, 91, 90), (0, 30, 346, 329), (295, 92, 208, 238), (0, 129, 162, 135), (493, 126, 128, 138), (166, 104, 149, 178), (182, 105, 197, 174), (474, 203, 146, 141), (398, 102, 241, 208), (0, 141, 220, 211), (577, 283, 62, 72), (474, 199, 146, 145), (339, 98, 244, 241), (0, 30, 349, 329), (161, 270, 59, 59), (93, 236, 112, 100), (0, 149, 217, 210), (30, 176, 134, 128), (32, 149, 185, 192), (0, 0, 274, 251), (499, 132, 121, 132), (1, 135, 147, 126), (29, 175, 137, 129), (433, 165, 151, 133), (29, 175, 135, 129), (0, 135, 148, 126), (342, 70, 161, 173), (295, 69, 344, 290), (161, 270, 60, 60), (0, 2, 349, 357), (0, 118, 287, 241), (295, 70, 344, 289), (234, 105, 98, 116), (11, 263, 92, 90), (339, 98, 245, 240), (0, 2, 346, 357), (502, 151, 137, 137), (161, 269, 59, 62), (0, 141, 221, 189), (2, 134, 146, 129), (340, 98, 244, 240), (543, 251, 80, 71), (171, 104, 303, 255), (577, 283, 62, 71), (342, 70, 184, 173), (342, 70, 297, 289), (160, 270, 60, 60), (1, 129, 174, 200), (433, 165, 150, 133), (8, 129, 166, 146), (98, 97, 240, 239), (161, 269, 60, 62), (342, 70, 276, 289), (1, 18, 406, 341), (342, 70, 276, 236), (171, 104, 289, 242), (0, 141, 220, 188), (234, 98, 266, 241), (463, 199, 158, 145), (171, 97, 167, 163), (543, 234, 79, 79), (295, 92, 305, 267), (160, 270, 63, 60), (171, 97, 167, 170), (171, 96, 170, 171), (342, 70, 175, 173), (171, 97, 170, 170), (2, 135, 146, 126), (1, 3, 419, 356), (171, 97, 170, 163), (4, 18, 396, 341), (545, 237, 78, 76), (505, 105, 105, 92), (212, 98, 246, 261), (340, 98, 244, 246), (339, 92, 300, 252), (0, 118, 286, 241), (463, 199, 159, 145), (0, 132, 208, 221), (499, 126, 122, 138), (210, 88, 193, 194), (0, 254, 93, 105), (339, 98, 244, 240), (30, 175, 175, 161), (295, 92, 315, 267), (161, 271, 59, 58), (0, 141, 208, 212), (340, 98, 243, 240), (341, 92, 298, 252), (161, 271, 59, 60), (161, 270, 59, 61), (234, 98, 266, 245), (234, 98, 266, 240), (499, 126, 121, 138), (463, 106, 176, 209)}

print(candidates)
merge()
print(refined)
draw_superbox()
print(final)

# draw rectangles on the original image
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
ax.imshow(img)
for x, y, w, h in refined:
    rect = mpatches.Rectangle(
        (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
    ax.add_patch(rect)

i=1
for x, y, w, h in refined:
	i+=1
	skimage.io.imsave(str(i)+".jpg", skimage.io.imread(name)[y:y+h, x:x+w]) # crop
plt.savefig(name+".jpg")

plt.close('all')
