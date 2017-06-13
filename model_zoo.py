
import tensorflow as tf
from tfwrapper import layers

NUM_CLASSES = 4

def lisa_net(images, training):

    # Lisa's best network to date with dilated convolutions

    conv1 = layers.conv2D_layer(images, 'conv1', num_filters=16)
    conv2 = layers.conv2D_layer(conv1, 'conv2', num_filters=16)
    conv3 = layers.conv2D_layer(conv2, 'conv3', num_filters=16)

    pool1 = layers.max_pool_layer(conv3)

    conv4 = layers.conv2D_dilated_layer(pool1, 'conv4', num_filters=32, rate=2)
    conv5 = layers.conv2D_dilated_layer(conv4, 'conv5', num_filters=32, rate=4)
    conv6 = layers.conv2D_dilated_layer(conv5, 'conv6', num_filters=32, rate=8)

    pool2 = layers.max_pool_layer(conv6)

    conv7 = layers.conv2D_layer(pool2, 'conv7', num_filters=64)
    conv8 = layers.conv2D_layer(conv7, 'conv8', num_filters=64)
    conv9 = layers.conv2D_layer(conv8, 'conv9', num_filters=64)

    pool3 = layers.max_pool_layer(conv9)

    deco3 = layers.deconv2D_layer(pool3, name='deco3', kernel_size=(16, 16), strides=(8, 8), num_filters=32)
    deco2 = layers.deconv2D_layer(pool2, name='deco2', kernel_size=(8, 8), strides=(4, 4), num_filters=32)
    deco1 = layers.deconv2D_layer(pool1, name='deco1', kernel_size=(4, 4), strides=(2, 2), num_filters=32)

    stack = tf.concat([deco1, deco2, deco3], axis=3, name='stacked')

    # stack = tf.add(deco2, deco3, name='sum') conv13 = layers.conv2D_layer(stack, 'conv13', num_filters=64, kernel_size=(1,1))

    conv13 = layers.conv2D_layer(stack, 'conv13', num_filters=64, kernel_size=(1, 1))
    conv14 = layers.conv2D_layer(conv13, 'conv14', num_filters=NUM_CLASSES, kernel_size=(1, 1),
                                    activation=layers.no_activation)

    return conv14


def lisa_net_deeper(images, training):

    # Deeper version of the lisa_net. Best performing network so far obtaining dice around 0.82

    conv1 = layers.conv2D_layer(images, 'conv1', num_filters=16)
    conv2 = layers.conv2D_layer(conv1, 'conv2', num_filters=16)
    conv3 = layers.conv2D_layer(conv2, 'conv3', num_filters=16)

    pool1 = layers.max_pool_layer(conv3)

    conv4 = layers.conv2D_dilated_layer(pool1, 'conv4', num_filters=32, rate=2)
    conv5 = layers.conv2D_dilated_layer(conv4, 'conv5', num_filters=32, rate=4)
    conv6 = layers.conv2D_dilated_layer(conv5, 'conv6', num_filters=32, rate=8)

    pool2 = layers.max_pool_layer(conv6)

    conv7 = layers.conv2D_layer(pool2, 'conv7', num_filters=64)
    conv8 = layers.conv2D_layer(conv7, 'conv8', num_filters=64)
    conv9 = layers.conv2D_layer(conv8, 'conv9', num_filters=64)

    pool3 = layers.max_pool_layer(conv9)

    conv10 = layers.conv2D_layer(pool3, 'conv10', num_filters=128)
    conv11 = layers.conv2D_layer(conv10, 'conv11', num_filters=128)

    deco3 = layers.deconv2D_layer(conv11, name='deco3', kernel_size=(16, 16), strides=(8, 8), num_filters=32)
    deco2 = layers.deconv2D_layer(pool2, name='deco2', kernel_size=(8, 8), strides=(4, 4), num_filters=32)
    deco1 = layers.deconv2D_layer(pool1, name='deco1', kernel_size=(4, 4), strides=(2, 2), num_filters=32)

    stack = tf.concat([deco1, deco2, deco3], axis=3, name='stacked')

    conv13 = layers.conv2D_layer(stack, 'conv13', num_filters=64, kernel_size=(1, 1))
    conv14 = layers.conv2D_layer(conv13, 'conv14', num_filters=NUM_CLASSES, kernel_size=(1, 1),
                                    activation=layers.no_activation)

    return conv14


def lisa_net_deeper_bn(images, training):

    # The above net with batch normalised convolution layers. Doesn't work well with adam or momentum optimizer
    # I have a feeling it might work with standard SGD and a high learning rate (0.1)

    conv1 = layers.conv2D_layer_bn(images, 'conv1', num_filters=16, training=training)
    conv2 = layers.conv2D_layer_bn(conv1, 'conv2', num_filters=16, training=training)
    conv3 = layers.conv2D_layer_bn(conv2, 'conv3', num_filters=16, training=training)

    pool1 = layers.max_pool_layer(conv3)

    conv4 = layers.conv2D_dilated_layer_bn(pool1, 'conv4', num_filters=32, rate=2, training=training)
    conv5 = layers.conv2D_dilated_layer_bn(conv4, 'conv5', num_filters=32, rate=4, training=training)
    conv6 = layers.conv2D_dilated_layer_bn(conv5, 'conv6', num_filters=32, rate=8, training=training)

    pool2 = layers.max_pool_layer(conv6)

    conv7 = layers.conv2D_layer_bn(pool2, 'conv7', num_filters=64, training=training)
    conv8 = layers.conv2D_layer_bn(conv7, 'conv8', num_filters=64, training=training)
    conv9 = layers.conv2D_layer_bn(conv8, 'conv9', num_filters=64, training=training)

    pool3 = layers.max_pool_layer(conv9)

    conv10 = layers.conv2D_layer_bn(pool3, 'conv10', num_filters=128, training=training)
    conv11 = layers.conv2D_layer_bn(conv10, 'conv11', num_filters=128, training=training)

    deco3 = layers.deconv2D_layer_bn(conv11, name='deco3', kernel_size=(16, 16), strides=(8, 8), num_filters=32, training=training)
    deco2 = layers.deconv2D_layer_bn(pool2, name='deco2', kernel_size=(8, 8), strides=(4, 4), num_filters=32, training=training)
    deco1 = layers.deconv2D_layer_bn(pool1, name='deco1', kernel_size=(4, 4), strides=(2, 2), num_filters=32, training=training)

    stack = tf.concat([deco1, deco2, deco3], axis=3, name='stacked')

    conv13 = layers.conv2D_layer_bn(stack, 'conv13', num_filters=64, kernel_size=(1, 1), training=training)
    conv14 = layers.conv2D_layer_bn(conv13, 'conv14', num_filters=NUM_CLASSES, kernel_size=(1, 1),
                                    activation=layers.no_activation, training=training)

    return conv14


def dilation_after_max_pool(images, training):

    # lisa deeper but with dilations after max pool instead of just one block
    # Appears to perform similarly to the lisa_net_deeper

    conv1 = layers.conv2D_layer(images, 'conv1', num_filters=16)
    conv2 = layers.conv2D_layer(conv1, 'conv2', num_filters=16)
    conv3 = layers.conv2D_layer(conv2, 'conv3', num_filters=16)

    pool1 = layers.max_pool_layer(conv3)

    conv4 = layers.conv2D_dilated_layer(pool1, 'conv4', num_filters=32, rate=2)
    conv5 = layers.conv2D_layer(conv4, 'conv5', num_filters=32)
    conv6 = layers.conv2D_layer(conv5, 'conv6', num_filters=32)

    pool2 = layers.max_pool_layer(conv6)

    conv7 = layers.conv2D_dilated_layer(pool2, 'conv7', num_filters=64, rate=2)
    conv8 = layers.conv2D_layer(conv7, 'conv8', num_filters=64)
    conv9 = layers.conv2D_layer(conv8, 'conv9', num_filters=64)

    pool3 = layers.max_pool_layer(conv9)

    conv10 = layers.conv2D_dilated_layer(pool3, 'conv10', num_filters=128, rate=2)
    conv11 = layers.conv2D_layer(conv10, 'conv11', num_filters=128)

    deco3 = layers.deconv2D_layer(conv11, name='deco3', kernel_size=(16, 16), strides=(8, 8), num_filters=32)
    deco2 = layers.deconv2D_layer(pool2, name='deco2', kernel_size=(8, 8), strides=(4, 4), num_filters=32)
    deco1 = layers.deconv2D_layer(pool1, name='deco1', kernel_size=(4, 4), strides=(2, 2), num_filters=32)

    stack = tf.concat([deco1, deco2, deco3], axis=3, name='stacked')

    conv13 = layers.conv2D_layer(stack, 'conv13', num_filters=64, kernel_size=(1, 1))
    conv14 = layers.conv2D_layer(conv13, 'conv14', num_filters=NUM_CLASSES, kernel_size=(1, 1),
                                    activation=layers.no_activation)

    return conv14

def lisa_net_one_more_pool(images, training):

    # Not fully investigated yet

    conv1 = layers.conv2D_layer(images, 'conv1', num_filters=16)
    conv2 = layers.conv2D_layer(conv1, 'conv2', num_filters=16)
    conv3 = layers.conv2D_layer(conv2, 'conv3', num_filters=16)

    pool1 = layers.max_pool_layer(conv3)

    conv4 = layers.conv2D_dilated_layer(pool1, 'conv4', num_filters=32, rate=2)
    conv5 = layers.conv2D_dilated_layer(conv4, 'conv5', num_filters=32, rate=4)
    conv6 = layers.conv2D_dilated_layer(conv5, 'conv6', num_filters=32, rate=8)

    pool2 = layers.max_pool_layer(conv6)

    conv7 = layers.conv2D_layer(pool2, 'conv7', num_filters=64)
    conv8 = layers.conv2D_layer(conv7, 'conv8', num_filters=64)
    conv9 = layers.conv2D_layer(conv8, 'conv9', num_filters=64)

    pool3 = layers.max_pool_layer(conv9)

    conv10 = layers.conv2D_layer(pool3, 'conv10', num_filters=128)
    conv11 = layers.conv2D_layer(conv10, 'conv11', num_filters=128)
    conv12 = layers.conv2D_layer(conv11, 'conv12', num_filters=128)

    pool4 = layers.max_pool_layer(conv12)

    deco4 = layers.deconv2D_layer(pool4, name='deco4', kernel_size=(32, 32), strides=(16, 16), num_filters=32)
    deco3 = layers.deconv2D_layer(pool3, name='deco3', kernel_size=(16, 16), strides=(8, 8), num_filters=32)
    deco2 = layers.deconv2D_layer(pool2, name='deco2', kernel_size=(8, 8), strides=(4, 4), num_filters=32)
    deco1 = layers.deconv2D_layer(pool1, name='deco1', kernel_size=(4, 4), strides=(2, 2), num_filters=32)

    stack = tf.concat([deco1, deco2, deco3, deco4], axis=3, name='stacked')

    conv13 = layers.conv2D_layer(stack, 'conv13', num_filters=64, kernel_size=(1, 1))
    conv14 = layers.conv2D_layer(conv13, 'conv14', num_filters=NUM_CLASSES, kernel_size=(1, 1),
                                    activation=layers.no_activation)

    return conv14

def lisa_net_3pool_stack_convs(images, training):

    # Not fully investigated yet

    conv1 = layers.conv2D_layer(images, 'conv1', num_filters=16)
    conv2 = layers.conv2D_layer(conv1, 'conv2', num_filters=16)
    conv3 = layers.conv2D_layer(conv2, 'conv3', num_filters=16)

    pool1 = layers.max_pool_layer(conv3)

    conv4 = layers.conv2D_dilated_layer(pool1, 'conv4', num_filters=32, rate=2)
    conv5 = layers.conv2D_dilated_layer(conv4, 'conv5', num_filters=32, rate=4)
    conv6 = layers.conv2D_dilated_layer(conv5, 'conv6', num_filters=32, rate=8)

    pool2 = layers.max_pool_layer(conv6)

    conv7 = layers.conv2D_layer(pool2, 'conv7', num_filters=64)
    conv8 = layers.conv2D_layer(conv7, 'conv8', num_filters=64)
    conv9 = layers.conv2D_layer(conv8, 'conv9', num_filters=64)

    pool3 = layers.max_pool_layer(conv9)

    conv10 = layers.conv2D_layer(pool3, 'conv10', num_filters=128)
    conv11 = layers.conv2D_layer(conv10, 'conv11', num_filters=128)
    conv12 = layers.conv2D_layer(conv11, 'conv12', num_filters=128)

    deco4 = layers.deconv2D_layer(conv12, name='deco4', kernel_size=(16, 16), strides=(8, 8), num_filters=32)
    deco3 = layers.deconv2D_layer(conv9, name='deco3', kernel_size=(8, 8), strides=(4, 4), num_filters=32)
    deco2 = layers.deconv2D_layer(conv6, name='deco2', kernel_size=(4, 4), strides=(2, 2), num_filters=32)
    deco1 = layers.deconv2D_layer(conv3, name='deco1', kernel_size=(2, 2), strides=(1, 1), num_filters=32)

    stack = tf.concat([deco1, deco2, deco3, deco4], axis=3, name='stacked')

    conv13 = layers.conv2D_layer(stack, 'conv13', num_filters=64, kernel_size=(1, 1))
    conv14 = layers.conv2D_layer(conv13, 'conv14', num_filters=NUM_CLASSES, kernel_size=(1, 1),
                                    activation=layers.no_activation)

    return conv14

def dialated_convs_nopool(images, training):

    # Dialated network with no max pooling
    # Doesn't work at all.

    conv1 = layers.conv2D_layer(images, 'conv1', num_filters=16)
    conv2 = layers.conv2D_layer(conv1, 'conv2', num_filters=16)
    conv3 = layers.conv2D_layer(conv2, 'conv3', num_filters=16)

    avg1 = tf.nn.max_pool(conv3, padding='SAME', ksize=(1,3,3,1), strides=(1,1,1,1))
    dial1 = layers.conv2D_dilated_layer(avg1, 'dial1', num_filters=16, rate=2)
    dial2 = layers.conv2D_dilated_layer(dial1, 'dial2', num_filters=16, rate=4)

    conv4 = layers.conv2D_layer(dial2, 'conv4', num_filters=32)
    conv5 = layers.conv2D_layer(conv4, 'conv5', num_filters=32)
    conv6 = layers.conv2D_layer(conv5, 'conv6', num_filters=32)

    avg2 = tf.nn.max_pool(conv6, padding='SAME', ksize=(1,3,3,1), strides=(1,1,1,1))
    dial3 = layers.conv2D_dilated_layer(avg2, 'dial3', num_filters=32, rate=2)
    dial4 = layers.conv2D_dilated_layer(dial3, 'dial4', num_filters=32, rate=4)

    conv7 = layers.conv2D_layer(dial4, 'conv7', num_filters=64)
    conv8 = layers.conv2D_layer(conv7, 'conv8', num_filters=64)
    conv9 = layers.conv2D_layer(conv8, 'conv9', num_filters=64)

    avg3 = tf.nn.max_pool(conv9, padding='SAME', ksize=(1,3,3,1), strides=(1,1,1,1))
    dial5 = layers.conv2D_dilated_layer(avg3, 'dial5', num_filters=64, rate=2)
    dial6 = layers.conv2D_dilated_layer(dial5, 'dial6', num_filters=64, rate=4)

    conv10 = layers.conv2D_layer(dial6, 'conv10', num_filters=128)
    conv11 = layers.conv2D_layer(conv10, 'conv11', num_filters=NUM_CLASSES, kernel_size=(1, 1),
                                    activation=layers.no_activation)

    return conv11


def inference_stack_decos(images, training):

    # Stack all deconvolutions instead of the max pooling layers
    # Not sure how this one performed, I think okay.

    conv1 = layers.conv2D_layer(images, 'conv1', num_filters=16)
    conv2 = layers.conv2D_layer(conv1, 'conv2', num_filters=16)
    conv3 = layers.conv2D_layer(conv2, 'conv3', num_filters=16)

    pool1 = layers.max_pool_layer(conv3)

    conv4 = layers.conv2D_layer(pool1, 'conv4', num_filters=32)
    conv5 = layers.conv2D_layer(conv4, 'conv5', num_filters=32)
    conv6 = layers.conv2D_layer(conv5, 'conv6', num_filters=32)

    pool2 = layers.max_pool_layer(conv6)

    conv7 = layers.conv2D_layer(pool2, 'conv7', num_filters=64)
    conv8 = layers.conv2D_layer(conv7, 'conv8', num_filters=64)
    conv9 = layers.conv2D_layer(conv8, 'conv9', num_filters=64)

    pool3 = layers.max_pool_layer(conv9)

    deco3 = layers.deconv2D_layer(pool3, name='deco3', kernel_size=(16,16), strides=(8,8), num_filters=32)
    deco2 = layers.deconv2D_layer(pool2, name='deco2', kernel_size=(8,8), strides=(4,4), num_filters=32)
    deco1 = layers.deconv2D_layer(pool1, name='deco1', kernel_size=(4,4), strides=(2,2), num_filters=32)

    stack = tf.concat([deco1, deco2, deco3], axis=3, name='stacked')

    #stack = tf.add(deco2, deco3, name='sum')

    conv10 = layers.conv2D_layer(stack, 'conv10', num_filters=64, kernel_size=(1,1))
    conv11 = layers.conv2D_layer(conv10, 'conv11', num_filters=NUM_CLASSES, kernel_size=(1,1), activation=layers.no_activation)

    return conv11

def inference_test(images, training):

    # Not as good as the lisa net, but performed okay-ish

    conv1 = layers.conv2D_layer(images, 'conv1', num_filters=16)
    conv2 = layers.conv2D_layer(conv1, 'conv2', num_filters=16)
    conv3 = layers.conv2D_layer(conv2, 'conv3', num_filters=16)

    pool1 = layers.max_pool_layer(conv3)

    conv4 = layers.conv2D_layer(pool1, 'conv4', num_filters=32)
    conv5 = layers.conv2D_layer(conv4, 'conv5', num_filters=32)
    conv6 = layers.conv2D_layer(conv5, 'conv6', num_filters=32)

    pool2 = layers.max_pool_layer(conv6)

    conv7 = layers.conv2D_layer(pool2, 'conv7', num_filters=64)
    conv8 = layers.conv2D_layer(conv7, 'conv8', num_filters=64)
    conv9 = layers.conv2D_layer(conv8, 'conv9', num_filters=64)

    pool3 = layers.max_pool_layer(conv9)

    conv10 = layers.conv2D_layer(pool3, 'conv10', num_filters=64)
    conv11 = layers.conv2D_layer(conv10, 'conv11', num_filters=64)

    deco3 = layers.deconv2D_layer(conv11, name='deco3', kernel_size=(16,16), strides=(8,8), num_filters=32)
    deco2 = layers.deconv2D_layer(conv9, name='deco2', kernel_size=(8,8), strides=(4,4), num_filters=32)
    deco1 = layers.deconv2D_layer(conv6, name='deco1', kernel_size=(4,4), strides=(2,2), num_filters=32)

    stack = tf.concat([deco1, deco2, deco3], axis=3, name='stacked')

    #stack = tf.add(deco2, deco3, name='sum')

    conv12 = layers.conv2D_layer(stack, 'conv12', num_filters=64, kernel_size=(1,1))
    conv13 = layers.conv2D_layer(conv12, 'conv13', num_filters=NUM_CLASSES, kernel_size=(1,1), activation=layers.no_activation)

    return conv13

def stack_all_convs(images, training):

    # I think I never actually tried this net.

    conv1 = layers.conv2D_layer(images, 'conv1', num_filters=16)
    conv2 = layers.conv2D_layer(conv1, 'conv2', num_filters=16)
    conv3 = layers.conv2D_layer(conv2, 'conv3', num_filters=16)

    pool1 = layers.max_pool_layer(conv3)

    conv4 = layers.conv2D_layer(pool1, 'conv4', num_filters=32)
    conv5 = layers.conv2D_layer(conv4, 'conv5', num_filters=32)
    conv6 = layers.conv2D_layer(conv5, 'conv6', num_filters=32)

    pool2 = layers.max_pool_layer(conv6)

    conv7 = layers.conv2D_layer(pool2, 'conv7', num_filters=64)
    conv8 = layers.conv2D_layer(conv7, 'conv8', num_filters=64)
    conv9 = layers.conv2D_layer(conv8, 'conv9', num_filters=64)

    pool3 = layers.max_pool_layer(conv9)

    conv10 = layers.conv2D_layer(pool3, 'conv10', num_filters=128)
    conv11 = layers.conv2D_layer(conv10, 'conv11', num_filters=128)
    conv12 = layers.conv2D_layer(conv11, 'conv12', num_filters=128)

    deco3 = layers.deconv2D_layer(conv12, name='deco3', kernel_size=(16,16), strides=(8,8), num_filters=32)
    deco2 = layers.deconv2D_layer(conv9, name='deco2', kernel_size=(8,8), strides=(4,4), num_filters=32)
    deco1 = layers.deconv2D_layer(conv6, name='deco1', kernel_size=(4,4), strides=(2,2), num_filters=32)

    stack = tf.concat([conv3, deco1, deco2, deco3], axis=3, name='stacked')

    #stack = tf.add(deco2, deco3, name='sum')

    conv13 = layers.conv2D_layer(stack, 'conv13', num_filters=64, kernel_size=(1,1))
    conv14 = layers.conv2D_layer(conv13, 'conv14', num_filters=NUM_CLASSES, kernel_size=(1,1), activation=layers.no_activation)

    return conv14