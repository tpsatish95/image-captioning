# -*- coding: utf-8 -*-
import skimage.io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
import numpy as np
import skimage.transform
import os
import sys

candidates = set()
merged_candidates = set()
refined = set()
final = set()

def contains():
    x1, y1, w1, h1 = p
    for x, y, w, h in candidates:
        if x1>=x and y1 >= y and x1+w1 <= x+w and y1+h1 <= y+h:
            return True
        if x1<=x and y1 <= y and x1+w1 >= x+w and y1+h1 >= y+h:
            candidates.remove((x, y, w, h))
            return False
    return False

def extend_rect(l):
    return (min([i[0] for i in l]), min([i[1] for i in l]), max([i[0]+i[2] for i in l]) - min([i[0] for i in l]), max([i[1]+i[3] for i in l]) - min([i[1] for i in l]))

def draw_superbox(finals=[]):
    noover = []
    refinedT = []

    global final
    final = set()

    # (x1,y1) top-left coord, (x2,y2) bottom-right coord, (w,h) size
    if finals != []:
        refinedT = finals
    else:
        refinedT = refined
    remp = set(refinedT)
    ref = list(refinedT)

    while len(ref) > 0:
        x1, y1, w1, h1 = ref[0]

        if len(ref) == 1: # final box
            final.add((x1, y1, w1, h1))
            ref.remove((x1, y1, w1, h1))
            remp.remove((x1, y1, w1, h1))
        else:
            ref.remove((x1, y1, w1, h1))
            remp.remove((x1, y1, w1, h1))

        over = set()
        for x2, y2, w2, h2 in remp:
            A = {'x1': x1, 'y1': y1, 'x2': x1+w1, 'y2': y1+h1, 'w': w1, 'h': h1}
            B = {'x1': x2, 'y1': y2, 'x2': x2+w2, 'y2': y2+h2, 'w': w2, 'h': h2}

            # overlap between A and B
            SA = A['w']*A['h']
            SB = B['w']*B['h']
            SI = np.max([ 0, np.min([A['x2'],B['x2']]) - np.max([A['x1'],B['x1']]) ]) * np.max([ 0, np.min([A['y2'],B['y2']]) - np.max([A['y1'],B['y1']]) ])
            SU = SA + SB - SI
            overlap_AB = float(SI) / float(SU)
            overlap_A = float(SI) / float(SA)
            overlap_B = float(SI) / float(SB)

            if overlap_A >= 0.40 or overlap_B >= 0.40:
                over.add((B['x1'],B['y1'],B['w'],B['h']))

        if len(over) != 0: #Overlap
            remp = remp - over
            for i in over: ref.remove(i)
            over.add((A['x1'],A['y1'],A['w'],A['h']))
            # print(over)
            final.add((min([i[0] for i in over]), min([i[1] for i in over]), max([i[0]+i[2] for i in over]) - min([i[0] for i in over]), max([i[1]+i[3] for i in over]) - min([i[1] for i in over])))
            # final.add((np.mean([i[0] for i in over]), np.mean([i[1] for i in over]), np.mean([i[2] for i in over]), np.mean([i[3] for i in over])))
            noover.append(False)
        else:   #No overlap
            final.add((x1,y1,w1,h1))
            noover.append(True)

    if all(noover):
        return
    else:
        draw_superbox(final)
        return

def contains_remove():

    for x, y, w, h in merged_candidates:
        f = False
        temp = set(merged_candidates)
        temp.remove((x, y, w, h))
        for x1, y1, w1, h1 in temp:
            if x1>=x and y1 >= y and x1+w1 <= x+w and y1+h1 <= y+h:
                f = False
                break
            # if x1<=x and y1 <= y and x1+w1 >= x+w and y1+h1 >= y+h:
            else:
                f = True
        if f == True:
            refined.add((x, y, w, h))

def mean_rect(l):
    return (min([i[0] for i in l]), min([i[1] for i in l]), max([i[0]+i[2] for i in l]) - min([i[0] for i in l]), max([i[1]+i[3] for i in l]) - min([i[1] for i in l]))

def merge():
    global width, height
    thresh = int(((width+height)/2)*(0.14))
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

name = sys.argv[1]
img = skimage.io.imread(name)
width = len(img[0])
height = len(img)

if width*height < 256*256*(0.95) and abs(width-height) <= 3 :
    new_size  = 512
    height = int(new_size * height / width)
    width  = new_size
    print("Me1")
elif width*height < 220*220*(1.11):
    new_size  = 256
    height = int(new_size * height / width)
    width  = new_size
    print("Me2")
elif width*height < 256*256:
    new_size  = 256
    height = int(new_size * height / width)
    width  = new_size
    print("Me21")
elif width*height > 512*512*(0.99)  and width < 800 and height < 800:
    new_size  = 512
    height = int(new_size * height / width)
    width  = new_size
    print("Me3")
elif width*height < 512*512*(0.95) and width*height > 256*256*(1.15):
    new_size  = 512
    height = int(new_size * height / width)
    width  = new_size
    print("Me4")

tried = []
while True:
    tried.append(width)
    candidates = set()
    merged_candidates = set()
    refined = set()
    final = set()
    final_extended = set()
    text_boxes = set()
    text=set()
    text_cut = set()
    no_text = set()
    for sc in [350,450,500]:
        for sig in [0.8]:
            for mins in [30,60,120]: # important
                img = skimage.io.imread(name)[:,:,:3]
                if height == len(img) and width == len(img[0]):
                    pass
                else:
                    img = skimage.transform.resize(img, (height, width))
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
                    if w >= (img.shape[0]-1)*(0.7) and h >= (img.shape[1]-1)*(0.7):
                        continue
                    candidates.add(r['rect'])
                print(str(sc)+"_"+str(sig)+"_"+str(mins))


    print(candidates)
    merge()
    print(refined)
    draw_superbox()
    print(final)

    # draw rectangles on the original image
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(img)
    for x, y, w, h in final:
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

    img1 = skimage.io.imread(name)[:,:,:3]
    if height == len(img1) and width == len(img1[0]):
        pass
    else:
        img1 = skimage.transform.resize(img1, (height, width))
    ij = 1
    for x, y, w, h in final:
        skimage.io.imsave(str(ij)+"_sub_"+name, img1[y:y+h,x:x+w])
        ij+=1
    plt.savefig("final_"+name)
    plt.close('all')

    if len(final) == 0 and len(tried) < 3:
        print(width)
        img = skimage.io.imread(name)
        twidth = len(img[0])
        theight = len(img)

        new_size = list(set([256,512,twidth]) - set(tried))[0]
        height = int(new_size * theight / twidth)
        width = new_size

    else:
        break
