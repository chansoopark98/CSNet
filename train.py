import tensorflow_datasets as tfds
#import tensorflow as tf
#import tensorflow.keras as keras
#import numpy as np
from utils.priors import *
import os
from preprocessing import prepare_dataset
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint

from model.pascal_loss import total_loss
from model.pascal_main import ssd
from tensorflow.keras.utils import plot_model
from calc_flops import get_flops

#from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2_as_graph
tf.autograph.set_verbosity(3, True)
CONTINUE_TRAINING = False
SAVE_MODEL_NAME = '0202_main'
DATASET_DIR = './datasets/'
IMAGE_SIZE = [384, 384]
BATCH_SIZE = 1
MODEL_NAME = 'B0'
EPOCHS = 200
TRAIN_MODE = 'pascal'
checkpoint_filepath = './checkpoints/'
base_lr = 1e-3


train_coco, t_info = tfds.load('coco/2017', data_dir=DATASET_DIR, split='train',with_info=True)
set = t_info.features
name=t_info.features['objects']['label'].num_classes
empty = tf.raw_ops.Empty(
    shape=(1,), dtype=tf.float32,
)
allowed = tf.constant(1, dtype=tf.int64)
# train_coco = train_coco.filter(lambda x: x['objects']['label'] == empty)
train_coco = train_coco.filter(lambda x: tf.reduce_all(tf.not_equal(tf.size(x['objects']['bbox']),0)))
# 123287


valid_coco = tfds.load('coco/2017', data_dir=DATASET_DIR, split='validation')
# valid_coco = valid_coco.filter(lambda x: x['objects']['label'] == allowed )
valid_coco = valid_coco.filter(lambda x: tf.reduce_all(tf.not_equal(tf.size(x['objects']['bbox']),0)))
test_coco = tfds.load('coco/2017', data_dir=DATASET_DIR, split='test')
train_data = train_coco.concatenate(valid_coco)
test_data = test_coco
# a = train_data['objects']['label']
# print(a)a = train_data

# labels = train_coco['objects']['label']
# train_pascal_12, info = tfds.load('voc/2012', data_dir=DATASET_DIR, split='train', with_info=True)
# valid_train_12 = tfds.load('voc/2012', data_dir=DATASET_DIR, split='validation')
#
# train_pascal_07 = tfds.load("voc", data_dir=DATASET_DIR, split='train')
# valid_train_07 = tfds.load("voc", data_dir=DATASET_DIR, split='validation')
# test_data = tfds.load('voc', data_dir=DATASET_DIR, split='test')
# train_data = train_pascal_07.concatenate(valid_train_07).concatenate(train_pascal_12).concatenate(valid_train_12)

number_train = 123287
print("학습 데이터 개수", number_train)
number_test = 40670
print("테스트 데이터 개수:", number_test)



iou_threshold = 0.5
center_variance = 0.1
size_variance = 0.2
# train.py에서 priors를 변경하면 model/ssd.py도 수정해야함
# specs = [
#                 Spec(75, 4, BoxSizes(15, 30), [2]),
#                 Spec(38, 8, BoxSizes(30, 60), [2]),
#                 Spec(19, 16, BoxSizes(60, 111), [2, 3]),
#                 Spec(10, 32, BoxSizes(111, 162), [2, 3]),
#                 Spec(5, 64, BoxSizes(162, 213), [2, 3]),
#                 Spec(3, 100, BoxSizes(213, 264), [2]),
#                 Spec(1, 300, BoxSizes(264, 315), [2])
#         ]
specs = [
                Spec(48, 8, BoxSizes(40, 90), [2]),
                Spec(24, 16, BoxSizes(90, 151), [2, 3]),
                Spec(12, 32, BoxSizes(151, 212), [2, 3]),
                Spec(6, 64, BoxSizes(212, 273), [2, 3]),
                Spec(3, 128, BoxSizes(273, 334), [2]),
                Spec(1, 384, BoxSizes(334, 395), [2])
        ]

priors = generate_ssd_priors(specs, IMAGE_SIZE[0])
target_transform = MatchPrior(priors, center_variance, size_variance, iou_threshold)

# 데이터세트 인스턴스화 (input은 300x300@3 labels은 8732)
training_dataset = prepare_dataset(train_data, IMAGE_SIZE, BATCH_SIZE, target_transform, 'coco',train=True)
validation_dataset = prepare_dataset(test_data, IMAGE_SIZE, BATCH_SIZE, target_transform, 'coco', train=False)

print("백본 EfficientNet{0} .".format(MODEL_NAME))
model = ssd(MODEL_NAME)
if CONTINUE_TRAINING is True:
    model.load_weights(checkpoint_filepath+SAVE_MODEL_NAME+'.h5')

steps_per_epoch = number_train // BATCH_SIZE
validation_steps = number_test // BATCH_SIZE
print("학습 배치 개수:", steps_per_epoch)
print("검증 배치 개수:", validation_steps)
model.summary()

flops = get_flops(model, BATCH_SIZE)
print(f"FLOPS: {flops}")

#plot_model(model,'model_b0.png',show_shapes=True)

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-5, verbose=1)
checkpoint = ModelCheckpoint(checkpoint_filepath+SAVE_MODEL_NAME+'.h5', monitor='val_loss', save_best_only=True, save_weights_only=True, verbose=1)

model.compile(
    optimizer = tf.keras.optimizers.Adam(learning_rate=base_lr),
    loss = total_loss
)


history = model.fit(training_dataset,
                    validation_data=validation_dataset,
                    steps_per_epoch=steps_per_epoch,
                    validation_steps=validation_steps,
                    epochs=EPOCHS,
                    callbacks=[reduce_lr,checkpoint])

# def make_directory(target_path):
#   if not os.path.exists(target_path):
#     os.mkdir(target_path)
#     print('Directory ', target_path, ' Created ')
#   else:
#     print('Directory ', target_path, ' already exists')
#
# print('TensorFlow version: {}'.format(tf.__version__))
# SAVED_MODEL_PATH = './saved_model'
# make_directory(SAVED_MODEL_PATH)
# MODEL_DIR = SAVED_MODEL_PATH
#
#
# version = SAVE_MODEL_NAME
# export_path = os.path.join(MODEL_DIR, str(version))
# print('export_path = {}\n'.format(export_path))
#
# tf.keras.models.save_model(
#   model,
#   export_path,
#   overwrite=True,
#   include_optimizer=True,
#   save_format=None,
#   signatures=None,
#   options=None
# )
# print('\nSaved model:')
