# Author: Timothy Patten (patten@acin.tuwien.ac.at)
# Vision for Robotics Laboratory, Automation and Control Institute, Technical University of Vienna

"""Script to display object-wise scores."""

import os
import argparse
import numpy as np
import json

from bop_toolkit_lib import config
from bop_toolkit_lib import inout
from bop_toolkit_lib import misc


# PARAMETERS (some can be overwritten by the command line arguments below).
################################################################################
p = {
  # Folder with results to be evaluated.
  'results_path': config.results_path,

  # Folder for the calculated pose errors and performance scores.
  'eval_path': config.eval_path,

  # Objects.
  'objects': [2, 3, 5, 9, 10, 11, 12, 14, 15, 17]
}
################################################################################


# Command line arguments.
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--result_filenames',
                    help='Comma-separated names of files with results.')
args = parser.parse_args()

p['result_filenames'] = args.result_filenames.split(',')

# Get the directories of the metrics to display
score_files = {'add': 'error=add_ntop=-1/scores_th=0.100_min-visib=-1.000.json',
               'adi': 'error=adi_ntop=-1/scores_th=0.100_min-visib=-1.000.json',
               'vsd': 'error=vsd_ntop=-1_delta=15.000_tau=0.200/scores_th=0.300_min-visib=-1.000.json'}

# Iterate over scores
for result_filename in p['result_filenames']:
    # Result name
    result_name = os.path.splitext(os.path.basename(result_filename))[0]

    # Construct map to store all data
    object_scores = {}
    for ob in p['objects']:
        o_score = {}
        for sco in sorted(score_files.keys()):
            o_score[sco] = 0.0
        object_scores[ob] = o_score

    for sco in sorted(score_files.keys()):
        # Load the json file
        score_filename = os.path.join(p['eval_path'], result_name, score_files[sco])
        if not os.path.exists(score_filename):
            print('Cannot find file {}'.format(score_filename))
            continue

        with open(score_filename) as f:
            score_data = json.load(f)

        # Get the data per object
        obj_recalls = score_data['obj_recalls']

        for ob in p['objects']:
            object_scores[ob][sco] = obj_recalls[str(ob)]

    print(object_scores)
    print('\nObject-wise results in {}\n'.format(result_filename))
    print('Object  ADD     ADD-S   VSD')
    print('------------------------------')
    averages = {'add': 0.0, 'adi': 0.0, 'vsd': 0.0}
    for ob in p['objects']:
        print('{}  {:.4f}  {:.4f}  {:.4f}'.format(str(ob).zfill(6), object_scores[ob]['add'], object_scores[ob]['adi'],
                                                  object_scores[ob]['vsd']))
        averages['add'] += object_scores[ob]['add']
        averages['adi'] += object_scores[ob]['adi']
        averages['vsd'] += object_scores[ob]['vsd']
    print('------------------------------')
    num_objects = float(len(p['objects']))
    print('Avg.    {:.4f}  {:.4f}  {:.4f}'.format(averages['add'] / num_objects, averages['adi'] / num_objects,
                                                  averages['vsd'] / num_objects))

    print('\n ADD')
    for ob in p['objects']:
        print('{:.4f}'.format(object_scores[ob]['add']))

    print('\n ADD-S')
    for ob in p['objects']:
        print('{:.4f}'.format(object_scores[ob]['adi']))

    print('\n VSD')
    for ob in p['objects']:
        print('{:.4f}'.format(object_scores[ob]['vsd']))


