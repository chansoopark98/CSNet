from model.model_builder import ModelBuilder
from utils.model_post_processing import post_process
from utils.load_datasets import GenerateDatasets
from utils.priors import *
from utils.model_evaluation import eval_detection_voc
from utils.get_flops import get_flops
import argparse
import time
import os
import tensorflow as tf
from tqdm import tqdm

tf.keras.backend.clear_session()

parser = argparse.ArgumentParser()
parser.add_argument("--backbone_name",      type=str,    help="Pretrained backbone name\
                                                               |   model_name    : description | \
                                                               [ 1. mobilenetv2       : MobileNetV2 ]\
                                                               [ 2. mobilenetv3s      : MobileNetV3-Small ] \
                                                               [ 3. mobilenetv3l      : MobileNetV3-Large ] \
                                                               [ 4. efficient_lite_v0 : EfficientNet-Lite-B0 ]\
                                                               [ 5. efficientv2b0  : EfficientNet-V2-B0 ]\
                                                               [ 6. efficientv2b3  : EfficientNet-V2-B3 ]",
                    default='efficient_lite_v0')
parser.add_argument("--image_norm_type",    type=str,    help="Set RGB image nornalize format (tf or torch or no)\
                                                               [ 1. tf    : Rescaling RGB image -1 ~ 1 from imageNet ]\
                                                               [ 2. torch : Rescaling RGB image 0 ~ 1 from imageNet ]\
                                                               [ 3. else  : Rescaling RGB image 0 ~ 1 only divide 255 ]",
                    default='div')
parser.add_argument("--batch_size",         type=int,    help="Evaluation batch size",
                    default=1)
parser.add_argument("--image_size",         type=tuple,  help="Model image size (input resolution H,W)",
                    default=(300, 300))
parser.add_argument("--dataset_dir",        type=str,    help="Dataset directory",
                    default='./datasets/')
parser.add_argument("--checkpoint_dir",     type=str,    help="Setting the model storage directory",
                    default='./checkpoints/')
parser.add_argument("--weight_path",        type=str,    help="Saved model weights directory",
                    default='0817/_0817_efficient_lite_v0_v0_voc_ce_e300_b32_lr0.001_single_relu6_sep-conv_best_loss.h5')

parser.add_argument("--gpu_num",            type=int,    help="Set GPU number to use(When without distribute training)",
                    default=0)

args = parser.parse_args()

if __name__ == '__main__':
    tf.config.set_soft_device_placement(True)

    gpu_number = '/device:GPU:' + str(args.gpu_num)
    with tf.device(gpu_number):
        # Set target transforms
        spec_list = convert_spec_list()
        priors = create_priors_boxes(specs=spec_list, image_size=args.image_size[0], clamp=True)
        target_transform = MatchingPriors(priors, center_variance, size_variance, iou_threshold)

        # Configuration test(valid) datasets
        dataset_config = GenerateDatasets(data_dir=args.dataset_dir, image_size=args.image_size,
                                          batch_size=args.batch_size, target_transform=target_transform,
                                          image_norm_type=args.image_norm_type,
                                          dataset_name='voc')
        test_dataset = dataset_config.get_testData(test_data=dataset_config.test_data)
        test_steps = dataset_config.number_test // args.batch_size

        # Model build and load pre-trained weights
        model = ModelBuilder(image_size=args.image_size, num_classes=dataset_config.num_classes).build_model(args.backbone_name)
        model.load_weights(args.checkpoint_dir + args.weight_path)
        model.summary()

        # Model warm up
        _ = model.predict(tf.zeros((1, args.image_size[0], args.image_size[1], 3)))

        # Prepare original labels
        voc_difficults = []
        voc_bboxes = []
        voc_labels = []
        for sample in dataset_config.test_data:             
            labels = sample['objects']['label'].numpy()
            boxes = sample['objects']['bbox'].numpy()[:, [1, 0, 3, 2]]
            is_difficult = sample['objects']['is_difficult'].numpy()
            voc_labels.append(labels)
            voc_bboxes.append(boxes)
            voc_difficults.append(is_difficult)

        avg_duration = 0
        post_avg_duration = 0
        # Eval
        print("Evaluating..")
        pred_bboxes = []
        pred_labels = []
        pred_scores = []

        for x, _ in tqdm(test_dataset, total=test_steps):
            # Check inference time
            start = time.process_time()
            pred = model.predict_on_batch(x)
            duration = (time.process_time() - start)
            avg_duration += duration

            post_start = time.process_time()
            predictions = post_process(pred,
                                    target_transform,
                                    classes=dataset_config.num_classes,
                                    confidence_threshold=0.01)
            post_duration = (time.process_time() - post_start)
            post_avg_duration += post_duration

            for prediction in predictions:
                boxes, scores, labels = prediction
                pred_bboxes.append(boxes)
                pred_labels.append(labels.astype(int) - 1)
                pred_scores.append(scores)

        answer = eval_detection_voc(pred_bboxes=pred_bboxes,
                                pred_labels=pred_labels,
                                pred_scores=pred_scores,
                                gt_bboxes=voc_bboxes,
                                gt_labels=voc_labels,
                                gt_difficults=voc_difficults,
                                use_07_metric=True)


        print('Model FLOPs {0}'.format(get_flops(model=model, batch_size=1)))
        print('Avg inference time : {0}sec.'.format((avg_duration / dataset_config.number_test)))
        print('Post porcessing Avg inference time : {0}sec.'.format((post_duration / dataset_config.number_test)))
        ap_dict = dict(zip(CLASSES, answer['ap']))
        print('AP per classes : {0}.'.format((ap_dict)))
        print('Image size : {0},  mAP : {1}'.format(args.image_size, answer['map']))