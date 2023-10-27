import itertools
import sys
from collections import defaultdict

import matplotlib.pyplot as plt
import csv
import glob
import numpy as np
import seaborn as sns  # for nicer graphics

BINS = 20
SCORE_THRESHOLD = -1
EXCLUDE = ['translator-A']
cmap = plt.get_cmap('jet_r')
Υ_CROP = 20
X_STEP = 5

def read_scores(path):
    scores = defaultdict(lambda: defaultdict(list))
    filenames = glob.glob(path)
    print(filenames)
    for filename in filenames:
        with open(filename) as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                system = row[1]
                system = system.replace('CASIA-SLT', 'CASIA')
                system = system.replace('knowcomp', 'KNOWCOMP')
                system = system.replace('baseline_signsuisse', 'BASELINE')
                segment_id = row[7] + ":" + row[2]
                score = int(row[6])
                if score > SCORE_THRESHOLD and system not in EXCLUDE:
                    scores[system][segment_id].append(score)

    avg_scores = defaultdict(list)
    segment_ids_per_score = defaultdict(list)
    for system, scores_per_segment in scores.items():

        for segment, segment_scores in scores_per_segment.items():
            avg_scores[system].append(np.mean(segment_scores))
            segment_ids_per_score[np.mean(segment_scores)].append(f"{system}:{segment}")

    for score, segment_ids in sorted(segment_ids_per_score.items(), reverse=True)[:20]:
        print(score, segment_ids)

    return avg_scores


def create_histogram(scores):

    # plt.figure(figsize=(8, 6))
    # N = len(scores.keys())
    # for i, system in enumerate(scores.keys()):
    #     print(system, len(scores[system]))
    #     color = cmap(float(i) / N)
    #     n, x, _ = plt.hist(scores[system], bins=BINS, alpha=0.5, label=system, color=color)

    sns.set_style({'font.family': 'serif', 'font.serif': 'Free Serif'})
    # sns.displot(scores, bins=BINS, element="step", multiple="stack")
    # plt.savefig("../results/histogram_stacked.pdf")
    # sns.displot(scores, bins=BINS, element="step",  aspect=1)
    step = 100/BINS
    bins = np.arange(0-step/2.0, 105+step/2.0, step=step)

    ax = sns.histplot(scores, bins=bins)
    ax.set_axisbelow(True)
    hatches = itertools.cycle(['//', '\\\\', '||', 'oo', 'x', '*', 'O', '.'])
    for i, (container, handle) in enumerate(zip(ax.containers, ax.get_legend().legend_handles[::-1])):
        # if i % BINS == 0:
        hatch = next(hatches)
        handle.set_hatch(hatch)

        # iterate through each rectangle in the container
        for rectangle in container:
            # set the rectangle hatch
            rectangle.set_hatch(hatch)

    # plt.yscale('log')
    # ax.legend()

    plt.xticks(np.arange(0, 110, step=X_STEP))
    ax.grid(axis='y')
    if Υ_CROP is not None:
        plt.ylim(0, Υ_CROP)
        plt.yticks(np.arange(0, Υ_CROP, step=5))
    plt.margins(x=0, y=0)
    plt.savefig("../results/histogram_transparent.pdf")

    # sns.displot(scores, kind="kde")
    # plt.ylim(0, 0.25)
    # plt.savefig("../results/density.pdf")


    # sns.histplot(data=scores, bins=BINS, stat='density', alpha=0.2, kde=True,
    #              element='step', linewidth=0.5,
    #              line_kws=dict(alpha=0.5, linewidth=1.5))

    # plt.savefig("histogram.pdf")
    # plt.legend(loc='upper right')
    plt.show()


if __name__ == '__main__':
    scores = read_scores(sys.argv[1])
    create_histogram(scores)
