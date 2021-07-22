import efficientnet.keras as efn
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Conv2D, Add, Activation, Dropout ,BatchNormalization,  UpSampling2D,\
    SeparableConv2D, MaxPooling2D, Concatenate, DepthwiseConv2D, GlobalAveragePooling2D, Reshape, multiply, add, ReLU
from functools import reduce

NUM_CHANNELS = [64, 64, 88, 112, 160, 224, 288, 288, 288]
#NUM_CHANNELS = [48, 64, 88, 112, 160, 244, 288, 288]
FPN_TIMES = [1, 3, 4, 5, 6, 7, 7, 7, 7]
CLS_TIEMS = [1, 3, 3, 3, 4, 4, 4, 4, 4]


MOMENTUM = 0.997
EPSILON = 1e-4

GET_EFFICIENT_NAME = {
    'B0': ['block3b_add', 'block5c_add', 'block7a_project_bn'],
    'B1': ['block3c_add', 'block5d_add', 'block7b_add'],
    'B2': ['block3c_add', 'block5d_add', 'block7b_add'],
    'B3': ['block3c_add', 'block5e_add', 'block7b_add'],
    'B4': ['block3d_add', 'block5f_add', 'block7b_add'],
    'B5': ['block3e_add', 'block5g_add', 'block7c_add'],
    'B6': ['block3f_add', 'block5h_add', 'block7c_add'],
    'B7': ['block3g_add', 'block5j_add', 'block7d_add'],
}

MODEL_NAME = {
    'B0': 0,
    'B1': 1,
    'B2': 2,
    'B3': 3,
    'B4': 4,
    'B5': 5,
    'B6': 6,
    'B7': 7,
}


def remove_dropout(model):
    for layer in model.layers:
        if isinstance(layer, Dropout):
            layer.rate = 0
    model_copy = keras.models.clone_model(model)
    model_copy.set_weights(model.get_weights())
    del model

    return model_copy



def create_efficientNet(base_model_name, pretrained=True, IMAGE_SIZE=[1024, 2048], trainable=True):
    if pretrained is False:
        weights = None



    else:
        weights = "imagenet"

    if base_model_name == 'B0' or 'B0-tiny':
        base = efn.EfficientNetB0(weights=weights, include_top=False, input_shape=[*IMAGE_SIZE, 3])

    elif base_model_name == 'B1':
        base = efn.EfficientNetB1(weights=weights, include_top=False, input_shape=[*IMAGE_SIZE, 3])

    elif base_model_name == 'B2':
        base = efn.EfficientNetB2(weights=weights, include_top=False, input_shape=[*IMAGE_SIZE, 3])

    elif base_model_name == 'B3':
        base = efn.EfficientNetB3(weights=weights, include_top=False, input_shape=[*IMAGE_SIZE, 3])

    elif base_model_name == 'B4':
        base = efn.EfficientNetB4(weights=weights, include_top=False, input_shape=[*IMAGE_SIZE, 3])

    elif base_model_name == 'B5':
        base = efn.EfficientNetB5(weights=weights, include_top=False, input_shape=[*IMAGE_SIZE, 3])

    elif base_model_name == 'B6':
        base = efn.EfficientNetB6(weights=weights, include_top=False, input_shape=[*IMAGE_SIZE, 3])

    elif base_model_name == 'B7':
        base = efn.EfficientNetB7(weights=weights, include_top=False, input_shape=[*IMAGE_SIZE, 3])

    base = remove_dropout(base)
    base.trainable = trainable


    return base



def csnet_seg_model(base_model_name, pretrained=True, IMAGE_SIZE=[512, 512], backbone_trainable=True):
    base = create_efficientNet(base_model_name, pretrained, IMAGE_SIZE, trainable=backbone_trainable)

    layer_names = GET_EFFICIENT_NAME[base_model_name]

    # get extra layer
    # p3 = base.get_layer(layer_names[0]).output #
    # p5 = base.get_layer(layer_names[1]).output #
    p7 = base.get_layer(layer_names[2]).output # 32, 64, 320
    print(p7)
    p7 = SeparableConv2D(19, 3, padding='same',
                         depthwise_initializer=tf.keras.initializers.VarianceScaling(),
                         pointwise_initializer=tf.keras.initializers.VarianceScaling())(p7)


    up_2x = UpSampling2D()(p7)
    up_4x = UpSampling2D()(up_2x)
    up_8x = UpSampling2D()(up_4x)
    up_16x = UpSampling2D()(up_8x)
    up_32x = UpSampling2D()(up_16x)



    return base.input, up_32x