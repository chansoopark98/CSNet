from utils.priors import *

iou_threshold = 0.5 # 0.5
center_variance = 0.1 # 0.1
size_variance = 0.2 # 0.2


MODEL_INPUT_SIZE = {
    'B0': 512,
    'B1': 544,
    'B2': 576, # 576
    'B3': 704,
    'B4': 768,
    'B5': 832,
    'B6': 896,
    'B7': 960
}

class TrainHyperParams:
    def __init__(self):
        self.optimizer_name = 'sgd'
        self.weight_decay = 0.0005
        self.learning_rate = 0.001
        self.momentum = 0.9
        self.lr_decay_steps = 200
        self.epochs = 200

    def setOptimizers(self):
        try:
            if self.optimizer_name == 'sgd':
                return tf.keras.optimizers.SGD(learning_rate=self.learning_rate, momentum=self.momentum)

            elif self.optimizer_name == 'adam':
                return tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

            elif self.optimizer_name == 'rmsprop':
                return tf.keras.optimizers.RMSprop(learning_rate=self.learning_rate)
        except:
            print("check optimizers name")

""" anchor test 

            Spec(64, 8, BoxSizes(19, 22), [2]), # 0.029
            Spec(32, 16, BoxSizes(41, 51), [2]), # 0.08
            Spec(16, 32, BoxSizes(102, 112), [2]), # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(204, 224), [2]), # 0.4
            Spec(4, 128, BoxSizes(332, 347), [2]), # 0.65
            
            target:
               1,602,228 voc



"""


""" origin B0 
            Spec(64, 8, BoxSizes(20, 25), [2]),  # 0.039
            Spec(32, 16, BoxSizes(41, 51), [2]),  # 0.099
            Spec(16, 32, BoxSizes(92, 112), [2]),  # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(194, 224), [2]),  # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(307, 347), [2]),  # 0.599
            
            target:
                1,468,685 voc
                54,849,050 coco


"""

""" 0531 test b0 512
            Spec(64, 8, BoxSizes(15, 22), [2]), # 0.029
            Spec(32, 16, BoxSizes(41, 51), [2]), # 0.08
            Spec(16, 32, BoxSizes(102, 112), [2]), # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(204, 224), [2]), # 0.4
            Spec(4, 128, BoxSizes(332, 347), [2]), # 0.65
            
            traget:
                1,585,209
                54,641,603 coco
"""
def set_priorBox(model_name):
    if model_name == 'B0':
        return [
            Spec(64, 8, BoxSizes(18, 22), [2]), # 0.039
            Spec(32, 16, BoxSizes(37, 48), [2]), # 0.099
            Spec(16, 32, BoxSizes(81, 119), [2]), # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(194, 224), [2]), # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(307, 347), [2]), # 0.599
        ]
    elif model_name == 'B1':
        return [
            Spec(68, 8, BoxSizes(18, 22), [2]), # 0.039
            Spec(34, 16, BoxSizes(37, 48), [2]), # 0.099
            Spec(17, 32, BoxSizes(81, 119), [2]), # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(194, 224), [2]), # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(307, 347), [2]), # 0.599
        ]

    elif model_name == 'B2':
        return [
            Spec(72, 8, BoxSizes(15, 22), [2]),  # 0.039
            Spec(36, 16, BoxSizes(37, 48), [2]),  # 0.099
            Spec(18, 32, BoxSizes(81, 119), [2]),  # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(163, 224), [2]),  # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(307, 347), [2]),  # 0.599
        ]


"""
0529 B2 Input size 544

            Spec(68, 8, BoxSizes(18, 22), [2]), # 0.039
            Spec(34, 16, BoxSizes(37, 48), [2]), # 0.099
            Spec(17, 32, BoxSizes(81, 119), [2]), # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(194, 224), [2]), # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(307, 347), [2]), # 0.599

기존 augmentation 방법으로 학습 
sgd momentum 약 250epoch 학습

  AP 결과
{'aeroplane': 0.8634389240911035,
 'bicycle': 0.8683981914576192,
 'bird': 0.8785208592011551,
 'boat': 0.828494806422587,
 'bottle': 0.6254045336515125,
 'bus': 0.8711601450249413,
 'car': 0.8687860727647553,
 'cat': 0.89812422728918,
 'chair': 0.6886957859100759,
 'cow': 0.8586690603806931,
 'diningtable': 0.7274975275276174,
 'dog': 0.8780796203018911,
 'horse': 0.8785347115372254,
 'motorbike': 0.8796464633922897,
 'person': 0.8523341250203799,
 'pottedplant': 0.663297841135211,
 'sheep': 0.856575101536427,
 'sofa': 0.7836286951668396,
 'train': 0.885383040768544,
 'tvmonitor': 0.8387045052330191}
mAP결과: 0.8246687118906533      
"""


"""
0530 B2 input 574 test

            Spec(72, 8, BoxSizes(18, 22), [2]),  # 0.039
            Spec(36, 16, BoxSizes(37, 48), [2]),  # 0.099
            Spec(18, 32, BoxSizes(81, 119), [2]),  # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(194, 224), [2]),  # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(307, 347), [2]),  # 0.599
            
기존 AUGMENTATION 
SGD MOMENTUM EPOCH 100
초기 LR 0.0005
WEIGHT DECAY 사용
POLIY LEARNING RATE DECAY 사용 초기 0.0001까지 200에폭구간동안 감소 비율
            


AP 결과
{'aeroplane': 0.8730012138558549,
 'bicycle': 0.8735031048919283,
 'bird': 0.8806218687894342,
 'boat': 0.8047434334772208,
 'bottle': 0.6301341786575964,
 'bus': 0.867596011662763,
 'car': 0.8689365489845348,
 'cat': 0.8833248549021493,
 'chair': 0.7085935114452341,
 'cow': 0.8629199290218322,
 'diningtable': 0.7153557953184085,
 'dog': 0.8819458603846347,
 'horse': 0.870680323818259,
 'motorbike': 0.8647709490146268,
 'person': 0.8583747005852433,
 'pottedplant': 0.6842448677158138,
 'sheep': 0.8627006505956938,
 'sofa': 0.7536834623476657,
 'train': 0.873683782035446,
 'tvmonitor': 0.8339486149723939}
mAP결과: 0.8226381831238367
"""

"""
0531 input 512 b0 test

            Spec(64, 8, BoxSizes(15, 22), [2]), # 0.029
            Spec(32, 16, BoxSizes(41, 51), [2]), # 0.08
            Spec(16, 32, BoxSizes(102, 112), [2]), # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(204, 224), [2]), # 0.4
            Spec(4, 128, BoxSizes(332, 347), [2]), # 0.65
            
            
AP 결과
{'aeroplane': 0.8557817018688885,
 'bicycle': 0.8751340758878764,
 'bird': 0.8605898865670873,
 'boat': 0.7999331132871784,
 'bottle': 0.6065403943182868,
 'bus': 0.8557189909071415,
 'car': 0.8603956736978895,
 'cat': 0.8878611558014267,
 'chair': 0.658413937503987,
 'cow': 0.812781170383734,
 'diningtable': 0.7590876800899486,
 'dog': 0.8814910350119332,
 'horse': 0.8688647425212326,
 'motorbike': 0.8680983021632257,
 'person': 0.8337417588883341,
 'pottedplant': 0.622348469763159,
 'sheep': 0.8232202568362248,
 'sofa': 0.8007975202342302,
 'train': 0.8902653968156188,
 'tvmonitor': 0.794042865703595}
mAP결과: 0.8107554064125498
"""
