import numpy as np

from cnn.layers import *
from cnn.fast_layers import *
from cnn.layer_utils import *


class ThreeLayerConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - relu - 2x2 max pool - affine - relu - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(self, input_dim=(3, 32, 32), num_filters=32, filter_size=7,
                 hidden_dim=100, num_classes=10, weight_scale=1e-3, reg=0.0,
                 dtype=np.float32):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Size of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        # Get input dimensions
        C, H, W = input_dim

        # Compute max pooling filter dimensions
        pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}
        HP = (H - pool_param['pool_height']) // pool_param['stride'] + 1
        WP = (W - pool_param['pool_width']) // pool_param['stride'] + 1

        # Set weights and biases dimension
        weigths_dim = [(num_filters, C, filter_size, filter_size),
                       (HP * WP * num_filters, hidden_dim),
                       (hidden_dim, num_classes)]
        biases_dim = [num_filters, hidden_dim, num_classes]

        # Initialize weights and biases
        for i in range(1, 4):
            self.params['W%d' % i] = np.random.normal(loc=0.0, scale=weight_scale,
                                                      size=weigths_dim[i - 1])
            self.params['b%d' % i] = np.zeros(biases_dim[i - 1])

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)

    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        W3, b3 = self.params['W3'], self.params['b3']

        # pass conv_param to the forward pass for the convolutional layer
        filter_size = W1.shape[2]
        conv_param = {'stride': 1, 'pad': (filter_size - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}


        # conv - relu - 2x2 max pool - affine - relu - affine - softmax
        # Convolutional pass
        if use_cython:
            conv_out, conv_cache = conv_forward_fast(X, W1, b1, conv_param)
        else:
            conv_out, conv_cache = conv_forward_naive(X, W1, b1, conv_param)

        # ReLU activation function
        conv_relu, conv_relu_cache = relu_forward(conv_out)

        # Max pooling layer
        if use_cython:
            max_out, max_cache = max_pool_forward_fast(conv_relu, pool_param)
        else:
            max_out, max_cache = max_pool_forward_naive(conv_relu, pool_param)

        # Affine forward
        affine_out, affine_cache = affine_forward(max_out, W2, b2)

        # ReLU affine
        affine_relu, affine_relu_cache = relu_forward(affine_out)

        # Compute scores
        scores, scores_cache = affine_forward(affine_relu, W3, b3)


        if y is None:
            return scores

        loss, grads = 0, {}


        # Compute loss and gradient with respect to the softmax function
        loss, dout = softmax_loss(scores, y)

        # Add L2 regularization to the loss function
        loss += 0.5 * self.reg * (np.sum(W1 * W1) + np.sum(W2 * W2) + np.sum(W3 * W3))

        # Backward through affine layer
        daffine, grads['W3'], grads['b3'] = affine_backward(dout, scores_cache)

        # Backward through ReLU activation
        daffine_relu = relu_backward(daffine, affine_relu_cache)

        # Backward through affine layer
        daffine, grads['W2'], grads['b2'] = affine_backward(daffine_relu, affine_cache)

        # Backward through the max pool layer
        if use_cython:
            dmax_pool = max_pool_backward_fast(daffine, max_cache)
        else:
            dmax_pool = max_pool_backward_naive(daffine, max_cache)

        # Backward through ReLU
        dX = relu_backward(dmax_pool, conv_relu_cache)

        # Backward through convnet
        if use_cython:
            dX, grads['W1'], grads['b1'] = conv_backward_fast(dX, conv_cache)
        else:
            dX, grads['W1'], grads['b1'] = conv_backward_naive(dX, conv_cache)

        # Add regularization to the gradients
        grads['W3'] += self.reg * W3
        grads['W2'] += self.reg * W2
        grads['W1'] += self.reg * W1


        return loss, grads
