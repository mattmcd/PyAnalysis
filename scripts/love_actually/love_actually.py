from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.cluster.hierarchy import dendrogram, linkage
import ggplot as gg
import networkx as nx

"""Python version of the 'Analyzing networks of characters in "Love Actually"'
[blog post|http://varianceexplained.org/r/love-actually-network] by David Robinson"""

data_dir = os.path.join(os.getenv('MDA_DATA_DIR', '/home/mattmcd/Work/Data'), 'LoveActually')


def read_script():
    """Read the Love Actually script from text file into list of lines
    The script is first Google hit for 'Love Actually script' as a doc
    file.  Use catdoc or Libre Office to save to text format.
    """
    with open(os.path.join(data_dir, 'love_actually.txt'), 'r') as f:
        lines = [line.strip() for line in f]
    return lines


def read_actors():
    """Read the mapping from character to actor using the varianceexplained data file
    Used curl -O http://varianceexplained.org/files/love_actually_cast.csv to get a local copy
    """
    return pd.read_csv(os.path.join(data_dir, 'love_actually_cast.csv'))


def parse_script(raw):
    df = pd.DataFrame(raw, columns=['raw'])

    df = df.query('raw != ""')
    df = df[~df.raw.str.contains("(song)")]
    lines = (df.
             assign(is_scene=lambda d: d.raw.str.contains(" Scene ")).
             assign(scene=lambda d: d.is_scene.cumsum()).
             query('not is_scene'))
    speakers = lines.raw.str.extract('(?P<speaker>[^:]*):(?P<dialogue>.*)')
    lines = (pd.concat([lines, speakers], axis=1).
             dropna().
             assign(line=lambda d: np.cumsum(~d.speaker.isnull())))

    lines.drop(['raw', 'is_scene'], axis=1, inplace=True)

    return lines


def read_all():
    lines = parse_script(read_script())
    cast = read_actors()
    combined = lines.merge(cast).sort('line').assign(
        character=lambda d: d.speaker + ' (' + d.actor + ')').reindex()
    # Decode bytes to unicode
    combined['character'] = map(lambda s: s.decode('utf-8'), combined['character'])
    return combined


def get_scene_speaker_matrix(lines):
    by_speaker_scene = lines.groupby(['character', 'scene'])['line'].count()
    speaker_scene_matrix = by_speaker_scene.unstack().fillna(0)
    return by_speaker_scene, speaker_scene_matrix


def plot_dendrogram(mat, normalize=True):
    # Cluster and plot dendrogram.  Return order after clustering.
    if normalize:
        # Normalize by number of lines
        mat = mat.div(mat.sum(axis=1), axis=0)
    Z = linkage(mat, method='complete', metric='cityblock')
    labels = mat.index
    f = plt.figure()
    ax = f.add_subplot(111)
    R = dendrogram(Z, leaf_rotation=90, leaf_font_size=8,
               labels=labels, ax=ax, color_threshold=-1)
    f.tight_layout()
    ordering = R['ivl']
    return ordering


def get_scenes_with_multiple_characters(by_speaker_scene):
    # Filter speaker scene dataframe to remove scenes with only one speaker

    # n_scene x 1 Series with index 'scene'
    filt = by_speaker_scene.count('scene') > 1
    # n_scene x n_character Index
    scene_index = by_speaker_scene.index.get_level_values('scene')
    # n_scene x n_character boolean vector
    ind = filt[scene_index].values
    return by_speaker_scene[ind]


def order_scenes(scenes, ordering=None):
    # Order scenes by e.g. leaf order after hierarchical clustering
    scenes = scenes.reset_index()
    scenes['scene'] = scenes['scene'].astype('category')
    scenes['character'] = scenes['character'].astype('category', categories=ordering)
    scenes['character_code'] = scenes['character'].cat.codes
    return scenes


def plot_timeline(scenes):
    # Plot character vs scene timelime
    # NB: due to limitations in Python ggplot we need to plot with scene on y-axis
    # in order to label x-ticks by character.
    # scale_x_continuous and scale_y_continuous behave slightly differently.

    print (gg.ggplot(gg.aes(y='scene', x='character_code'), data=scenes) +
            gg.geom_point() + gg.labs(x='Character', y='Scene') +
           gg.scale_x_continuous(
               labels=scenes['character'].cat.categories.values.tolist(),
           breaks=range(len(scenes['character'].cat.categories))) +
           gg.theme(axis_text_x=gg.element_text(angle=30, hjust=1, size=10)))


def get_cooccurrence_matrix(speaker_scene_matrix, ordering=None):
    # Co-occurrence matrix for the characters, ignoring last scene where all are present
    scene_ind = speaker_scene_matrix.astype(bool).sum() < 10
    if ordering:
        mat = speaker_scene_matrix.loc[ordering, scene_ind]
    else:
        mat = speaker_scene_matrix.loc[:, scene_ind]
    return mat.dot(mat.T)


def plot_heatmap(cooccur_mat):
    # Plot co-ccurrence matrix as heatmap
    plt.figure()
    plt.pcolor(cooccur_mat)


def plot_network(cooccur_mat):
    # Plot co-occurence matrix as network diagram
    G = nx.Graph(cooccur_mat.values)
    pos = nx.graphviz_layout(G)  # NB: needs pydot installed
    plt.figure()
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='c')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(
        G, pos,
        labels={i: s for (i, s) in enumerate(cooccur_mat.index.values)},
        font_size=10)
    plt.axis('off')
    plt.show()


def run():
    # Run the entire analysis

    # Read in script and cast into a dataframe
    lines = read_all()
    # Print the first few rows
    print(lines.head(10))
    # Group by speaker and scene and construct the speaker-scene matrix
    by_speaker_scene, speaker_scene_matrix = get_scene_speaker_matrix(lines)
    # Hierarchical cluster and return order of leaves
    ordering = plot_dendrogram(speaker_scene_matrix)
    print(ordering)
    # Order the scenes by cluster leaves order
    scenes = order_scenes(get_scenes_with_multiple_characters(by_speaker_scene), ordering)
    # Plot a timeline of characters vs scene
    plot_timeline(scenes)
    # Plot heatmap of co-occurrence matrix
    cooccur_mat = get_cooccurrence_matrix(speaker_scene_matrix, ordering)
    plot_heatmap(cooccur_mat)
    # Plot network graph of co-occurrence matrix
    plot_network(cooccur_mat)
    return by_speaker_scene, speaker_scene_matrix, ordering, scenes, cooccur_mat
