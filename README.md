# CNN-with-Visualization

File description
---
cnn/fast_layers is a memory-access optimization version of layers.
cnn/layers is the initial version implementation of NN.
cnn/optim contains optimization methods like sgd, sgd_momentum.
cnn/solver is an encapsulation of all the logic necessary of training.
cnn/classifiers/ contains two NN modules, TwoLayerNet and TreeLayerNet
main_train is training program entrance without using Tensorflow.
main_train_tf using TF to construct a CNN.

visualize and visualize_utils contains all the visualization module.

Classification of MNIST without Dropout
---
I use main_train_tf to do the classification.


![](https://github.com/mungsoo/CNN-with-Visualization/blob/master/images/loss.jpg?raw=true)

![](https://github.com/mungsoo/CNN-with-Visualization/blob/master/images/result1.jpg?raw=true)

The result shows a high training accuracy and a low validation accuracy, which means the model overfits.

Classification of MNIST with Dropout
---

![](https://github.com/mungsoo/CNN-with-Visualization/blob/master/images/loss_drop.jpg?raw=true)

* Visualize 32 kernels
![](https://github.com/mungsoo/CNN-with-Visualization/blob/master/images/conv_filter.png?raw=true)

* Visualize output feature maps
![](https://github.com/mungsoo/CNN-with-Visualization/blob/master/images/embed.png?raw=true)

![](https://github.com/mungsoo/CNN-with-Visualization/blob/master/images/result2.jpg?raw=true)

From the result above, I found a way better validation accuracy.


Comments
--
CNN tends to overfits easily. A great way to solve the problem is to use dropout. The thoughts of dropout is
to deactivate and activate nodes in the network randomly, which makes the network structure different for each
training step. It just likes we are training multiple different networks with sharing weights. Like the thoughts
of bagging. And because of the random dropout, it cannot gurantee 2 hidden nodes are active simultaneously, so it
makes the update of weights do not depend on some specific patterns. 
