import tensorflow as tf
import networkx as nx

# Example 3.8 from 'Probabilistic Graphical Models' by Koller and Friedman
# Values used are from Figure 4.1

G = nx.Graph()
G.add_nodes_from(['A', 'B', 'C', 'D'])
G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')])

# phi_1(A, B)
phi1 = tf.constant([30, 5, 1, 10.0], shape=[2, 2, 1, 1])
# phi_2(B, C)
phi2 = tf.constant([100, 1, 1, 100.0], shape=[1, 2, 2, 1])
# phi3_(C, D)
phi3 = tf.constant([1, 100, 100, 1.0], shape=[1, 1, 2, 2])
# NB: we need to enter values with highest dimension last
# phi4_(A, D)
phi4 = tf.constant([100, 1, 1, 100.0], shape=[2, 1, 1, 2])
# Un-normalized probability P_tilde
P_tilde = phi1 * phi2 * phi3 * phi4
# Partition function
Z = tf.reduce_sum(P_tilde)
# Normalized probability
P = P_tilde/Z

# Marginals
P_a = tf.reduce_sum(P, axis=[1, 2, 3])
P_b = tf.reduce_sum(P, axis=[0, 2, 3])
P_c = tf.reduce_sum(P, axis=[0, 1, 3])
P_d = tf.reduce_sum(P, axis=[0, 1, 2])
# P(B=b1|C=c0)
P_b1_c0 = tf.reduce_sum(P, axis=[0, 3])[1, 0] / tf.reduce_sum(P, axis=[0, 1, 3])[0]
# P(b|C=c0)
P_b_c0 = tf.reduce_sum(P, axis=[0, 3])[:, 0] / tf.reduce_sum(P, axis=[0, 1, 3])[0]
# P(a, b)
P_ab = tf.reduce_sum(P, axis=[2, 3])

with tf.Session() as sess:
    res = sess.run([P, P_a, P_b, P_c, P_d, P_b1_c0, P_b_c0, P_ab])
