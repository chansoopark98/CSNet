import tensorflow_datasets as tfds
import argparse
import os
import tensorflow as tf
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.layers.experimental import preprocessing
from preprocessing import *
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_dir",    type=str,   help="데이터셋 다운로드 디렉토리 설정", default='./datasets/')
parser.add_argument("--train_dataset",  type=str,   help="학습에 사용할 dataset 설정 coco or voc", default='cityscapes')

args = parser.parse_args()
DATASET_DIR = args.dataset_dir
TRAIN_MODE = args.train_dataset

os.makedirs(DATASET_DIR, exist_ok=True)
AUTO = tf.data.experimental.AUTOTUNE


if TRAIN_MODE == 'voc':
    train_pascal_12 = tfds.load('voc/2012', data_dir=DATASET_DIR, split='train')
    valid_train_12 = tfds.load('voc/2012', data_dir=DATASET_DIR, split='validation')

    train_pascal_07 = tfds.load("voc", data_dir=DATASET_DIR, split='train')
    valid_train_07 = tfds.load("voc", data_dir=DATASET_DIR, split='validation')

    test_data = tfds.load('voc', data_dir=DATASET_DIR, split='test')

    train_data = train_pascal_07.concatenate(train_pascal_12)
    valid_data = valid_train_07.concatenate(valid_train_12)

    number_train = train_data.reduce(0, lambda x, _: x + 1).numpy()
    print("학습 데이터 개수", number_train)

    number_valid = valid_data.reduce(0, lambda x, _: x + 1).numpy()
    print("검증 데이터 개수", number_valid)

    number_test = test_data.reduce(0, lambda x, _: x + 1).numpy()
    print("테스트 데이터 개수:", number_test)


elif TRAIN_MODE == 'coco' :
    train_data = tfds.load('coco/2017', data_dir=DATASET_DIR, split='train')
    valid_data = tfds.load('coco/2017', data_dir=DATASET_DIR, split='validation')
    test_data = tfds.load('coco/2017', data_dir=DATASET_DIR, split='test')

    number_train = train_data.reduce(0, lambda x, _: x + 1).numpy()
    print("학습 데이터 개수", number_train)

    number_valid = valid_data.reduce(0, lambda x, _: x + 1).numpy()
    print("검증 데이터 개수", number_valid)

    number_test = test_data.reduce(0, lambda x, _: x + 1).numpy()
    print("테스트 데이터 개수:", number_test)

elif TRAIN_MODE == 'cityscapes':
    download_config = tfds.download.DownloadConfig(
        manual_dir=DATASET_DIR + '/downloads', extract_dir=DATASET_DIR + '/cityscapes')

    # train_ds = tfds.load('cityscapes/semantic_segmentation', data_dir=DATASET_DIR, split='train',
    #                      download_and_prepare_kwargs={"download_config": download_config})
    # valid_ds = tfds.load('cityscapes/semantic_segmentation', data_dir=DATASET_DIR, split='validation',
    #                      download_and_prepare_kwargs={"download_config": download_config})
    # test_ds = tfds.load('cityscapes/semantic_segmentation', data_dir=DATASET_DIR, split='test',
    #                     download_and_prepare_kwargs={"download_config": download_config})

    train_ds = tfds.load('cityscapes/semantic_segmentation', data_dir=DATASET_DIR, split='train'
                         )
    valid_ds = tfds.load('cityscapes/semantic_segmentation', data_dir=DATASET_DIR, split='validation'
                         )
    test_ds = tfds.load('cityscapes/semantic_segmentation', data_dir=DATASET_DIR, split='test'
                        )

    prepare_trainData = cityScapes(train_ds, [512, 1024], 1, True)
    prepare_trainData_v = cityScapes(valid_ds, [512, 1024], 1, False)


    img = prepare_trainData.take(1)
    v_img = prepare_trainData_v.take(1)

    from tensorflow.keras.applications.imagenet_utils import preprocess_input
    for x, y in img:
        print(x)


        # plt.imshow(x[0])
        # plt.show()

    for x, y in v_img:
        print(x)
        # plt.imshow(x[0])
        # plt.show()















