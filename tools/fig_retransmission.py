#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2019 Hauke Petersen <hauke.petersen@fu-berlin.de>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

import os
import sys
from pathlib import Path
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent))

import re
import math
import json
import argparse
from datetime import datetime
from tools.exputil.expbase import Expbase
from tools.exputil.ana import Ana
from tools.exputil.topo import Topo
from tools.exputil.expstats import Expstats
from tools.exputil.alive import Alive
from tools.exputil.ifconfigval import Ifconfigval
from tools.exputil.llstats import LLStats

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

TICKLBLSIZE = 9
LEGENDSIZE = 8
AXISLBLSIZE = 11

SRC = {
    "jelling_star_1s1h100b_i50_e1_0": "ea_putnon_jelling_star_1s1h100b_i50_e1/ea_putnon_jelling_star_1s1h100b_i50_e1_20211124-111311",
    "jelling_star_1s1h100b_i50_e2_0": "ea_putnon_jelling_star_1s1h100b_i50_e2/ea_putnon_jelling_star_1s1h100b_i50_e2_20211124-122942",
    "jelling_star_1s1h100b_i50_e3_0": "ea_putnon_jelling_star_1s1h100b_i50_e3/ea_putnon_jelling_star_1s1h100b_i50_e3_20211124-134549",
    "jelling_star_1s1h100b_i50_e4_0": "ea_putnon_jelling_star_1s1h100b_i50_e4/ea_putnon_jelling_star_1s1h100b_i50_e4_20211124-150321",
    "jelling_star_1s1h100b_i50_e5_0": "ea_putnon_jelling_star_1s1h100b_i50_e5/ea_putnon_jelling_star_1s1h100b_i50_e5_20211124-161943",
    "jelling_star_1s1h100b_i50_e6_0": "ea_putnon_jelling_star_1s1h100b_i50_e6/ea_putnon_jelling_star_1s1h100b_i50_e6_20211124-173733",

    "jelling_star_5s1h100b_i50_e1_0": "ea_putnon_jelling_star_5s1h100b_i50_e1/ea_putnon_jelling_star_5s1h100b_i50_e1_20211124-185412",
    "jelling_star_5s1h100b_i50_e1_1": "ea_putnon_jelling_star_5s1h100b_i50_e1/ea_putnon_jelling_star_5s1h100b_i50_e1_20211125-081038",
    "jelling_star_5s1h100b_i50_e2_0": "ea_putnon_jelling_star_5s1h100b_i50_e2/ea_putnon_jelling_star_5s1h100b_i50_e2_20211125-092635",
    "jelling_star_5s1h100b_i50_e3_0": "ea_putnon_jelling_star_5s1h100b_i50_e3/ea_putnon_jelling_star_5s1h100b_i50_e3_20211125-104241",
    "jelling_star_5s1h100b_i50_e4_0": "ea_putnon_jelling_star_5s1h100b_i50_e4/ea_putnon_jelling_star_5s1h100b_i50_e4_20211125-115835",
    "jelling_star_5s1h100b_i50_e5_0": "ea_putnon_jelling_star_5s1h100b_i50_e5/ea_putnon_jelling_star_5s1h100b_i50_e5_20211125-131444",
    "jelling_star_5s1h100b_i50_e6_0": "ea_putnon_jelling_star_5s1h100b_i50_e6/ea_putnon_jelling_star_5s1h100b_i50_e6_20211125-143030",
}

PLOT = {
    "jelling_star_1s1h100b_i50_e1_0": {"color": "C0", "label": "0 retransmissions"},
    "jelling_star_1s1h100b_i50_e2_0": {"color": "C1", "label": "1 retransmissions"},
    "jelling_star_1s1h100b_i50_e3_0": {"color": "C2", "label": "2 retransmissions"},
    "jelling_star_1s1h100b_i50_e4_0": {"color": "C3", "label": "3 retransmissions"},
    "jelling_star_1s1h100b_i50_e5_0": {"color": "C4", "label": "4 retransmissions"},
    "jelling_star_1s1h100b_i50_e6_0": {"color": "C5", "label": "5 retransmissions"},
}
PLOT2 = {
    "jelling_star_5s1h100b_i50_e1_0": {"color": "C0", "label": "0 retransmissions"},
    "jelling_star_5s1h100b_i50_e2_0": {"color": "C1", "label": "1 retransmissions"},
    "jelling_star_5s1h100b_i50_e3_0": {"color": "C2", "label": "2 retransmissions"},
    "jelling_star_5s1h100b_i50_e4_0": {"color": "C3", "label": "3 retransmissions"},
    "jelling_star_5s1h100b_i50_e5_0": {"color": "C4", "label": "4 retransmissions"},
    "jelling_star_5s1h100b_i50_e6_0": {"color": "C5", "label": "5 retransmissions"},
}

SUFFIX = "_cdf.json"
OUTDIR = "results/figs"

class Results(Ana):
    def __init__(self, logfile):
        super().__init__(logfile)
        self.plotter.show_plot = False # todo

        self.expstats = Expstats(self)
        # self.llstats = LLStats(self)

        self.parse_log(self.update)

        self.expstats.finish()
        # self.llstats.finish()

        self.expstats.plot_cdf()


    def update(self, time, node, line):
        self.expstats.update(time, node, line)
        # self.llstats.update(time, node, line)


class Fig(Expbase):
    def __init__(self):
        super().__init__()

        self.dat = {}

        base = os.path.splitext(os.path.basename(__file__))[0]
        self.out_pdf = os.path.join(self.basedir, OUTDIR, f'{base}.pdf')
        self.out_png = os.path.join(self.basedir, OUTDIR, f'{base}.png')
        print(f'output: {self.out_pdf}')

        for name, base in SRC.items():
            file = os.path.join(self.plotdir, f'{base}{SUFFIX}')
            if not os.path.isfile(file):
                dumpfile = os.path.join(self.logdir, f'{base}.dump')
                print(f'generating: {file}')
                print(f'source:     {dumpfile}')
                Results(dumpfile)

            print(f'loading:    {file}')
            self.dat[name] = self.load(file)

        print("PDR:")
        for name in sorted(list(PLOT.keys())):
            print(f'{name}: {self.dat[name]["data"][1]["y"][-1] * 100}%')


    def make(self):
        fig, axs = plt.subplots(1, 2, sharex=True)
        fig.set_size_inches(5.7, 2.0)

        # for name, ctx in PLOT.items():
        for name, ctx in sorted(list(PLOT.items()), key=lambda x:x[0].lower(), reverse=True):
            axs[0].plot(self.dat[name]["data"][1]["x"], self.dat[name]["data"][1]["y"], **ctx)
        for name, ctx in sorted(list(PLOT2.items()), key=lambda x:x[0].lower(), reverse=True):
            axs[1].plot(self.dat[name]["data"][1]["x"], self.dat[name]["data"][1]["y"], **ctx)

        # set generic axis options
        for col, ax in enumerate(axs):
            xt = np.arange(0, .65, .05)
            ax.set_xlim(0.0, .6)
            ax.set_xticks(xt)
            ax.set_xticklabels([f'{l:.1f}' for l in xt], size=TICKLBLSIZE)
            for index, label in enumerate(ax.xaxis.get_ticklabels()):
                if index % 2 != 1:
                    label.set_visible(False)

            yt = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
            ax.set_ylim(0.0, 1.05)
            ax.set_yticks(yt)
            ax.xaxis.grid(True)
            ax.yaxis.grid(True)

            # ax.set_xlabel("RTT [s]", size=AXISLBLSIZE)
            if col == 0:
                ax.set_title("Producer interval 1s", size=AXISLBLSIZE)
                ax.set_yticklabels([f'{l:.1f}' for l in yt], size=TICKLBLSIZE)
                ax.set_ylabel("CDF [0:1.0]", size=AXISLBLSIZE)
            else:
                ax.set_yticklabels([])

            if col == 1:
                ax.set_title("Producer interval 5s", size=AXISLBLSIZE)
                ax.legend(fontsize=LEGENDSIZE, loc="lower right")

        # Set common labels
        fig.text(0.55, 0.00, 'RTT of CoAP messages [s]', ha='center', va='center', size=AXISLBLSIZE)
        # fig.text(0.00, 0.5, 'CDF', ha='center', va='center', rotation='vertical', size=AXISLBLSIZE)



        # ax.set_ylabel("moinfoo")
        # ax.set_title("Herrlich")

        # plt.xlabel("Experiment runtime [in s]")
        # plt.ylabel("moisnen")


        plt.tight_layout()
        plt.subplots_adjust(wspace=0.05, hspace=0.05)
        plt.savefig(self.out_pdf, dpi=300, format='pdf', bbox_inches='tight')
        plt.savefig(self.out_png, dpi=300, format='png', bbox_inches='tight', pad_inches=0.01)
        plt.show()
        plt.close()

    def load(self, file):
        path = os.path.join(self.plotdir, file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            sys.exit("Error: unable to load file {}: {}".format(file, e))


def main():
    f = Fig()
    f.make()


if __name__ == "__main__":
    main()
