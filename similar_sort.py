# -*- coding:utf-8 -*-

#
#python similor_sort.py --dir 629/
#


import turicreate as tc
import argparse
import os
import shutil
import time


def  main(dir, num):
    start_time = time.time()

    data_path = os.path.join(dir,"data")
    if os.path.exists(data_path):
        ref_data = tc.load_sframe(data_path)
    else:
        source_path = os.path.join(dir, "source")
        ref_data = tc.image_analysis.load_images(source_path)
        ref_data = ref_data.add_row_number()
        ref_data.save(data_path)

    mode_path = os.path.join(dir, "model")

    if os.path.exists(mode_path):
        model = tc.load_model(mode_path)
    else:
        model = tc.image_similarity.create(ref_data, label=None, feature=None, model='resnet-50', verbose=True)
        model.save(mode_path)
    """
    bm_path = os.path.join(dir, "classic")
    bm_list = os.listdir(bm_path)
    all=[]
    results = []
    for file in bm_list:
        img = tc.Image(os.path.join(bm_path, file))
        similar_images = model.query(img, k=15)
        for i in range(15):
            ref_label = similar_images[i]['reference_label']
            distance = similar_images[i]['distance']
            ref_row = ref_data[ref_label]
            path = ref_row['path']
            print(distance, path)
            if not (path in results):
                results.append(path)

    #for file in all:
    #    if all.count(file) > 1 and not (file in results):
    #        results.append(file)

    result_dir = os.path.join(dir, "sorted_dir")
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    for file in results:
        print(file)
        cp_path = os.path.join(result_dir, ('%s' % (os.path.basename(file))))
        shutil.copyfile(file, cp_path)

    """

    if num == 0:
        num = ref_data.num_rows()

    bm_path =  os.path.join(dir,"classic")
    bm_data = tc.image_analysis.load_images(bm_path)
    similar_images = model.query(bm_data, k=num)

    result_dir = os.path.join(dir,"sorted_dir")

    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    for i in range(num):
        ref_label = similar_images[i]['reference_label']
        distance = similar_images[i]['distance']
        #if distance < 20:
        ref_row = ref_data[ref_label]
        path = ref_row['path']
        print(i, distance, os.path.basename(path))
        cp_path = os.path.join(result_dir, ('%05f_%s' % (distance, os.path.basename(path))))
        #cp_path = os.path.join(result_dir, ('%s' % (os.path.basename(path))))
        shutil.copyfile(path, cp_path)
        print(path, cp_path)

    elapsed_time = time.time() - start_time
    print ("Time elapsed = %d"%(elapsed_time))


if __name__ == '__main__':
    dir = "./"
    out_dir = "./out_dir"
    selet_num = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir",    help="source to test")
    parser.add_argument("--selet_num",    help="src dir to copy")
    args = parser.parse_args()

    if args.dir:
        dir = args.dir
    if args.selet_num:
        selet_num = int(args.selet_num)
    main(dir, selet_num)
