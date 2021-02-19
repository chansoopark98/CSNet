import tensorflow as tf
import numpy as np

def smooth_l1(labels, scores, sigma=1.0):
    diff = scores-labels
    abs_diff = tf.abs(diff)
    return tf.where(tf.less(abs_diff, 1/(sigma**2)), 0.5*(sigma*diff)**2, abs_diff-1/(2*sigma**2))


def hard_negative_mining(loss, labels, neg_pos_ratio):
    """
    It used to suppress the presence of a large number of negative prediction.
    It works on image level not batch level.
    For any example/image, it keeps all the positive predictions and
     cut the number of negative predictions to make sure the ratio
     between the negative examples and positive examples is no more
     the given ratio for an image.
    Args:
        loss (N, num_priors): the loss for each example.
        labels (N, num_priors): the labels.
        neg_pos_ratio:  the ratio between the negative examples and positive examples.
    """
    pos_mask = labels > 0
    # print(pos_mask)
    num_pos = tf.math.reduce_sum(tf.cast(pos_mask, tf.float32), axis=1, keepdims=True)
    num_neg = num_pos * neg_pos_ratio

    loss = tf.where(pos_mask, tf.convert_to_tensor(np.NINF), loss)

    indexes = tf.argsort(loss, axis=1, direction='DESCENDING')
    orders = tf.argsort(indexes, axis=1)
    neg_mask = tf.cast(orders, tf.float32) < num_neg

    return tf.logical_or(pos_mask ,neg_mask)




def total_loss(y_true, y_pred, num_classes=81):
    """Compute classification loss and smooth l1 loss.
        Args:
            confidence (batch_size, num_priors, num_classes): class predictions.
            predicted_locations (batch_size, num_priors, 4): predicted locations.
            labels (batch_size, num_priors): real labels of all the priors.
            gt_locations (batch_size, num_priors, 4): real boxes corresponding all the priors.
    """
    # y_true[:, :, :num_classes] = None, 13792, None )
    test_label = y_true[:, :, :num_classes] # (None, 13792, None)

    a = test_label[:,]
    b = test_label[:,:,]
    c = test_label[:,:,:,]
    #test_label_unstack = tf.unstack(test_label, 1, axis=0) # 13792, None
    #test_label_unstack = tf.unstack(y_true_unstack, None, -1)
    # None, 1 = 1, None ( 13792개 )

    test_classes = test_label[2][1] # (None, )

    label = tf.where(tf.equal(tf.size(test_label[2][1]), 0), test_label[2][1], tf.constant(1., dtype=tf.float32) )




    labels = tf.argmax(test_label, axis=2) # (None, 13792)
    confidence = y_pred[:,:,:num_classes] # (None, None, 81)


    # Reduction axis 1 is empty in shape [13792,0]

    predicted_locations = y_pred[:,:,num_classes:] # (None, None, 81 )
    gt_locations = y_true[:,:,num_classes:] # ( None, 13792, None)+
    unstack_gt_locations_axis0 = tf.unstack(gt_locations, 1, axis=0)

    #unstack_gt_locations_axis1 = tf.unstack(gt_locations, 0, axis=1)
    unstack_gt_locations_axis2 = tf.unstack(gt_locations, 1, axis=2)
    a = gt_locations[:,0] # (13792, None)
    b = gt_locations[:,-1] # (13792, None)
    c = gt_locations[:,:,0] # (13792, None)
    d = gt_locations[:,:,-1] # (13792, None)
    e = gt_locations[:,:,0:] [0][0] # (13792, None)


    #gt_locations[:, :, 0:][0][0] = ex
    #print(ex)
    #gt_locations[3] = ex



    neg_pos_ratio = 3.0
    # derived from cross_entropy=sum(log(p))
    loss = -tf.nn.log_softmax(confidence, axis=2)[:, :, 0]
    loss = tf.stop_gradient(loss)
    # print(loss)
    mask = hard_negative_mining(loss, labels, neg_pos_ratio)
    mask = tf.stop_gradient(mask)
    # return mask
    confidence = tf.boolean_mask(confidence, mask)
    classification_loss = tf.math.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(logits = tf.reshape(confidence, [-1, num_classes]), labels = tf.boolean_mask(labels, mask)))
    # return classification_loss
    pos_mask = labels > 0
    predicted_locations = tf.reshape(tf.boolean_mask(predicted_locations, pos_mask), [-1, 4])
    gt_locations = tf.reshape(tf.boolean_mask(gt_locations, pos_mask), [-1, 4])

    smooth_l1_loss = tf.math.reduce_sum(smooth_l1(scores=predicted_locations,labels=gt_locations))
    num_pos = tf.cast(tf.shape(gt_locations)[0], tf.float32)
    loc_loss = smooth_l1_loss / num_pos
    class_loss = classification_loss / num_pos
    # print(num_pos)
    mbox_loss = loc_loss + class_loss
    return  mbox_loss

