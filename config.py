from utils.priors import *

iou_threshold = 0.5 # 0.5
center_variance = 0.1 # 0.1
size_variance = 0.2 # 0.2


MODEL_INPUT_SIZE = {
    'B0': 512,
    'B1': 544,
    'B2': 576, # 576
    'B3': 608,
    'B4': 640,
    'B5': 672,
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
            Spec(64, 8, BoxSizes(15, 31), [2]), # 0.029 | 0.041
            Spec(32, 16, BoxSizes(40, 82), [2]), # 0.078 | 0.111       + 0.049
            Spec(16, 32, BoxSizes(92, 184), [2]), # 0.179 | 0.359      + 0.101
            Spec(8, 64, BoxSizes(194, 228), [2]), # 0.378 | 0.445      + 0.199
            Spec(4, 128, BoxSizes(310, 386), [2]), # 0.605 | 0.753     + 0.227
        ]
    elif model_name == 'B1':
        return [
            Spec(68, 8, BoxSizes(16, 22), [2]),
            Spec(34, 16, BoxSizes(42, 60), [2]),
            Spec(17, 32, BoxSizes(92, 184), [2]),
            Spec(8, 64, BoxSizes(206, 242), [2]),
            Spec(4, 128, BoxSizes(329, 410), [2]),
        ]

    elif model_name == 'B2':
        return [
            Spec(72, 8, BoxSizes(17, 24), [2]),  # 0.039
            Spec(36, 16, BoxSizes(45, 64), [2]),  # 0.099
            Spec(18, 32, BoxSizes(103, 207), [2]),  # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(218, 256), [2]),  # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(348, 434), [2]),  # 0.599
        ]
    elif model_name == 'B3':
        return [
            Spec(76, 8, BoxSizes(18, 25), [2]),  # 0.039
            Spec(38, 16, BoxSizes(47, 67), [2]),  # 0.099
            Spec(19, 32, BoxSizes(109, 218), [2]),  # 0.238 -> 0.199
            Spec(9, 64, BoxSizes(230, 271), [2]),  # 0.449 -> 0.398
            Spec(5, 128, BoxSizes(368, 458), [2]),  # 0.599
        ]
    elif model_name == 'B4':
        return [
            Spec(80, 8, BoxSizes(19, 26), [2]), # 0.029 | 0.041
            Spec(40, 16, BoxSizes(50, 71), [2]), # 0.078 | 0.111       + 0.049
            Spec(20, 32, BoxSizes(115, 230), [2]), # 0.179 | 0.359      + 0.101
            Spec(9, 64, BoxSizes(242, 285), [2]), # 0.378 | 0.445      + 0.199
            Spec(5, 128, BoxSizes(387, 482), [2]), # 0.605 | 0.753     + 0.227
        ]

    elif model_name == 'B5':
        return [
            Spec(84, 8, BoxSizes(19, 28), [2]), # 0.029 | 0.041
            Spec(42, 16, BoxSizes(52, 75), [2]), # 0.078 | 0.111       + 0.049
            Spec(21, 32, BoxSizes(120, 241), [2]), # 0.179 | 0.359      + 0.101
            Spec(10, 64, BoxSizes(254, 299), [2]), # 0.378 | 0.445      + 0.199
            Spec(5, 128, BoxSizes(407, 506), [2]), # 0.605 | 0.753     + 0.227
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


"""
0531 input b0 512 test
            Spec(64, 8, BoxSizes(18, 22), [2]), # 0.039
            Spec(32, 16, BoxSizes(37, 48), [2]), # 0.099
            Spec(16, 32, BoxSizes(81, 119), [2]), # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(194, 224), [2]), # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(307, 347), [2]), # 0.599

AP 결과
{'aeroplane': 0.8648210683412043,
 'bicycle': 0.8765492680443105,
 'bird': 0.8647099591292886,
 'boat': 0.8140110295509727,
 'bottle': 0.6202741723609245,
 'bus': 0.8606765195812114,
 'car': 0.8692918665994208,
 'cat': 0.8769985225590029,
 'chair': 0.6645195423123669,
 'cow': 0.8191636266875512,
 'diningtable': 0.7107610016519993,
 'dog': 0.8757278275594026,
 'horse': 0.8795687113149608,
 'motorbike': 0.8652723457282876,
 'person': 0.8441757562347387,
 'pottedplant': 0.6314224068884745,
 'sheep': 0.8383114650027059,
 'sofa': 0.7933833484356535,
 'train': 0.894422399451095,
 'tvmonitor': 0.8012729150469864}
mAP결과: 0.8132666876240279

"""

"""
0601 input b0 512 test
            Spec(64, 8, BoxSizes(18, 18), [2]), # 0.039
            Spec(32, 16, BoxSizes(36, 36), [2]), # 0.099
            Spec(16, 32, BoxSizes(72, 72), [2]), # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(144, 144), [2]), # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(288, 288), [2]), # 0.599
            
      {'aeroplane': 0.8650881023953919,
 'bicycle': 0.8560582522491127,
 'bird': 0.8517710867527066,
 'boat': 0.7845387366219227,
 'bottle': 0.6110190959663719,
 'bus': 0.8485582066446883,
 'car': 0.8591530324311141,
 'cat': 0.8858926527438556,
 'chair': 0.6331358405405133,
 'cow': 0.8287569233197131,
 'diningtable': 0.7144780508112064,
 'dog': 0.8690191836430363,
 'horse': 0.8689763609634868,
 'motorbike': 0.8515864728904267,
 'person': 0.8209485820688821,
 'pottedplant': 0.5845704235632643,
 'sheep': 0.8349570973705477,
 'sofa': 0.7410423431261746,
 'train': 0.8867129184317929,
 'tvmonitor': 0.7867426150141565}
mAP결과: 0.7991502988774183
      
"""

"""
0601 input b0 512 test
            Spec(64, 8, BoxSizes(15, 31), [2]), # 0.039
            Spec(32, 16, BoxSizes(40, 82), [2]), # 0.099
            Spec(16, 32, BoxSizes(92, 184), [2]), # 0.238 -> 0.199
            Spec(8, 64, BoxSizes(194, 228), [2]), # 0.449 -> 0.398
            Spec(4, 128, BoxSizes(310, 386), [2]), # 0.599
            
AP 결과
{'aeroplane': 0.8616198718804391,
 'bicycle': 0.8648786724872177,
 'bird': 0.878285128315244,
 'boat': 0.8081795067359447,
 'bottle': 0.6394169187771519,
 'bus': 0.8395359872597871,
 'car': 0.8733094865413361,
 'cat': 0.8705314091973508,
 'chair': 0.6827697507016365,
 'cow': 0.8465508095736229,
 'diningtable': 0.7105902658489044,
 'dog': 0.8678275879385908,
 'horse': 0.878857043312034,
 'motorbike': 0.8546173430497646,
 'person': 0.8392487417091707,
 'pottedplant': 0.65443725852704,
 'sheep': 0.8539888824296853,
 'sofa': 0.7736000858373614,
 'train': 0.8928783136659507,
 'tvmonitor': 0.8451688339663902}
mAP결과: 0.8168145948877312

"""

"""
0602 input b1 544 test

            Spec(68, 8, BoxSizes(16, 22), [2]),
            Spec(34, 16, BoxSizes(42, 60), [2]),
            Spec(17, 32, BoxSizes(92, 184), [2]),
            Spec(8, 64, BoxSizes(206, 242), [2]),
            Spec(4, 128, BoxSizes(329, 410), [2]),
            
AP 결과
{'aeroplane': 0.8899181651034032,
 'bicycle': 0.885644805715953,
 'bird': 0.8713699968299433,
 'boat': 0.8218068374608906,
 'bottle': 0.6361410674844875,
 'bus': 0.869865292036819,
 'car': 0.8723429085304971,
 'cat': 0.8848338653563178,
 'chair': 0.7047569029805718,
 'cow': 0.869340274240229,
 'diningtable': 0.7338286953771369,
 'dog': 0.8906032122174099,
 'horse': 0.8942054041164287,
 'motorbike': 0.8725042128034948,
 'person': 0.854398113526022,
 'pottedplant': 0.6468219976231269,
 'sheep': 0.8581222079363471,
 'sofa': 0.7697557528179247,
 'train': 0.8923966131811474,
 'tvmonitor': 0.826807870058793}
mAP결과: 0.8272732097698473

"""


"""
0602 input b2 576 test

            Spec(76, 8, BoxSizes(18, 25), [2]),  # 0.039
            Spec(38, 16, BoxSizes(47, 67), [2]),  # 0.099
            Spec(19, 32, BoxSizes(109, 218), [2]),  # 0.238 -> 0.199
            Spec(9, 64, BoxSizes(230, 271), [2]),  # 0.449 -> 0.398
            Spec(5, 128, BoxSizes(368, 458), [2]),  # 0.599

AP 결과
{'aeroplane': 0.8730567176999042,
 'bicycle': 0.873589425178257,
 'bird': 0.885203777323433,
 'boat': 0.8209897117724092,
 'bottle': 0.6577331282508107,
 'bus': 0.862588893703592,
 'car': 0.8762507906275612,
 'cat': 0.894731764213472,
 'chair': 0.7003307030548865,
 'cow': 0.8767685008130601,
 'diningtable': 0.6519850778675054,
 'dog': 0.8922454943064331,
 'horse': 0.8824666499999378,
 'motorbike': 0.8782907544997988,
 'person': 0.8509294677300743,
 'pottedplant': 0.7103368546187655,
 'sheep': 0.8653746646753931,
 'sofa': 0.7979001744392298,
 'train': 0.897555492027914,
 'tvmonitor': 0.8523865411220368}
mAP결과: 0.8300357291962237
"""

"""
0603 input b3 608 test

            Spec(76, 8, BoxSizes(18, 25), [2]),  # 0.039
            Spec(38, 16, BoxSizes(47, 67), [2]),  # 0.099
            Spec(19, 32, BoxSizes(109, 218), [2]),  # 0.238 -> 0.199
            Spec(9, 64, BoxSizes(230, 271), [2]),  # 0.449 -> 0.398
            Spec(5, 128, BoxSizes(368, 458), [2]),  # 0.599

AP 결과
{'aeroplane': 0.8713631189425017,
 'bicycle': 0.891733931625732,
 'bird': 0.8885064917967715,
 'boat': 0.8371829685505383,
 'bottle': 0.66107955023727,
 'bus': 0.8891966354848452,
 'car': 0.8781601213727362,
 'cat': 0.8880886033134435,
 'chair': 0.7260799833057664,
 'cow': 0.8681774761186525,
 'diningtable': 0.8191339445404846,
 'dog': 0.8848247860106674,
 'horse': 0.8954163165103376,
 'motorbike': 0.8843015184022429,
 'person': 0.8500330805474964,
 'pottedplant': 0.7042720230226196,
 'sheep': 0.8622734605671724,
 'sofa': 0.8049328647736576,
 'train': 0.9002201530955329,
 'tvmonitor': 0.8573423514757263}
mAP결과: 0.8431159689847098

"""
"""
0612 input b4 640 test 

            Spec(80, 8, BoxSizes(19, 26), [2]), # 0.029 | 0.041
            Spec(40, 16, BoxSizes(50, 71), [2]), # 0.078 | 0.111       + 0.049
            Spec(20, 32, BoxSizes(115, 230), [2]), # 0.179 | 0.359      + 0.101
            Spec(9, 64, BoxSizes(242, 285), [2]), # 0.378 | 0.445      + 0.199
            Spec(5, 128, BoxSizes(387, 482), [2]), # 0.605 | 0.753     + 0.227
            
AP 결과
{'aeroplane': 0.888764181506636,
 'bicycle': 0.89565643851905,
 'bird': 0.8993081930605853,
 'boat': 0.8692451869789333,
 'bottle': 0.6679078765390377,
 'bus': 0.8955763414370649,
 'car': 0.8898277368042722,
 'cat': 0.9043371637762712,
 'chair': 0.7518002828908541,
 'cow': 0.9167969262698189,
 'diningtable': 0.7711326419951353,
 'dog': 0.8932916336660426,
 'horse': 0.8938578252151037,
 'motorbike': 0.901226101351994,
 'person': 0.8680026286213571,
 'pottedplant': 0.7174222047056174,
 'sheep': 0.8731438009440551,
 'sofa': 0.8234339330176226,
 'train': 0.9010553057536863,
 'tvmonitor': 0.8662576663325822}
mAP결과: 0.854402203469286
"""


"""
0615 b0 input 512  priors 동일

polyDecay = tf.keras.optimizers.schedules.PolynomialDecay(initial_learning_rate=base_lr,
                                                          decay_steps=200,
                                                          end_learning_rate=0.0001, power=0.5)
lr_scheduler = tf.keras.callbacks.LearningRateScheduler(polyDecay)

optimizer = tf.keras.optimizers.SGD(learning_rate=base_lr, momentum=0.9)
optimizer = mixed_precision.LossScaleOptimizer(optimizer, loss_scale='dynamic')  # tf2.4.1 이전

callback = [checkpoint, reduce_lr , lr_scheduler, testCallBack, tensorboard]

AP 결과

{'aeroplane': 0.8646110677691202,
 'bicycle': 0.8751551432926854,
 'bird': 0.8776209628840232,
 'boat': 0.8089655331875512,
 'bottle': 0.6225792098020899,
 'bus': 0.8540650930474732,
 'car': 0.8718347188691102,
 'cat': 0.8838951790069872,
 'chair': 0.6878156181674223,
 'cow': 0.8447975953368952,
 'diningtable': 0.6903933621899059,
 'dog': 0.8826570048341911,
 'horse': 0.8786505080250858,
 'motorbike': 0.862115570822286,
 'person': 0.8378868612464151,
 'pottedplant': 0.6607067161378294,
 'sheep': 0.8590544795077495,
 'sofa': 0.782103344259429,
 'train': 0.8953315477697475,
 'tvmonitor': 0.838361651598434}
mAP결과: 0.8189300583877216
"""