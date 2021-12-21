import tensorflow as tf


#%% constant
tf1 = tf.constant([3,4,5], tf.float32)
tf2 = tf.constant([3,4,5])
tf3 = tf.constant([
    [1, 2],
    [3, 4]
])

#%% variable
w = tf.Variable(1.0)
w.assign(2)

#%% fields

tf1.shape  # (3,)
tf3.shape  # (2,2)