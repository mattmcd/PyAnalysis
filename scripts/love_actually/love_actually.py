from __future__ import division
import numpy as np
import pandas as pd
import os

"""Python version of the 'Analyzing networks of characters in "Love Actually"'
[blog post|http://varianceexplained.org/r/love-actually-network] by David Robinson"""

data_dir = '/home/mattmcd/Work/Data/LoveActually'


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
    return lines.merge(cast).sort('line').assign(character=lambda d: d.speaker + ' (' + d.actor + ')').reindex()


def get_scene_speaker_matrix(lines, normalize=True):
    mat = lines.groupby(['scene', 'character'])['line'].count().unstack().fillna(0)
    if normalize:
        # Normalize by number of lines
        mat = mat.div(mat.sum(axis=0), axis=1)
    return mat
