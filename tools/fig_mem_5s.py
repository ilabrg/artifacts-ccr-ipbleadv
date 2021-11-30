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

OUTDIR = "results/figs"
TICKLBLSIZE = 9
LEGENDSIZE = 9
AXISLBLSIZE = 11

MBUF_SIZE = 199

SRC = {
    "adv_star_1s": "ea_putnon_jelling_star_1s1h100b_i50/ea_putnon_jelling_star_1s1h100b_i50_20211123-044403",
    "adv_tree_1s": "ea_putnon_jelling_tree_1s1h100b_i50/ea_putnon_jelling_tree_1s1h100b_i50_20211123-055958",
    "adv_line_1s": "ea_putnon_jelling_line_1s1h100b_i50/ea_putnon_jelling_line_1s1h100b_i50_20211123-071559",
    "adv_star_5s": "ea_putnon_jelling_star_5s1h100b_i50/ea_putnon_jelling_star_5s1h100b_i50_20211125-003225",
    "adv_tree_5s": "ea_putnon_jelling_tree_5s1h100b_i50/ea_putnon_jelling_tree_5s1h100b_i50_20211125-014831",
    "adv_line_5s": "ea_putnon_jelling_line_5s1h100b_i50/ea_putnon_jelling_line_5s1h100b_i50_20211125-030445",
    "con_star_1s": "ea_putnon_statconn_star_1s1h100b_i40r60/ea_putnon_statconn_star_1s1h100b_i40r60_20211118-174417",
    "con_tree_1s": "ea_putnon_statconn_tree_1s1h100b_i40r60/ea_putnon_statconn_tree_1s1h100b_i40r60_20211118-190049",
    "con_line_1s": "ea_putnon_statconn_line_1s1h100b_i40r60/ea_putnon_statconn_line_1s1h100b_i40r60_20211118-201726",
    "con_star_5s": "ea_putnon_statconn_star_5s1h100b_i40r60/ea_putnon_statconn_star_5s1h100b_i40r60_20211119-150254",
    "con_tree_5s": "ea_putnon_statconn_tree_5s1h100b_i40r60/ea_putnon_statconn_tree_5s1h100b_i40r60_20211122-170610",
    "con_line_5s": "ea_putnon_statconn_line_5s1h100b_i40r60/ea_putnon_statconn_line_5s1h100b_i40r60_20211122-182312",
}

USE = [
    # "adv_star_1s",
    # "adv_tree_1s",
    # "adv_line_1s",
    # "con_star_1s",
    # "con_tree_1s",
    # "con_line_1s",

    "adv_star_5s",
    "adv_tree_5s",
    "adv_line_5s",
    "con_star_5s",
    "con_tree_5s",
    "con_line_5s",
]


class Results(Ana):
    def __init__(self, logfile):
        super().__init__(logfile)
        self.plotter.show_plot = False # todo

        self.expstats = Expstats(self)
        self.llstats = LLStats(self)
        self.parse_log(self.update)
        self.expstats.finish()
        self.llstats.finish()

        self.llstats.plot_bufusage(["nrf52dk-6"])
        self.llstats.plot_bufusage(["nrf52840dk-10"])


    def update(self, time, node, line):
        self.expstats.update(time, node, line)
        self.llstats.update(time, node, line)


class Fig(Expbase):
    def __init__(self):
        super().__init__()

        self.dat = {}

        base = os.path.splitext(os.path.basename(__file__))[0]
        self.out_pdf = os.path.join(self.basedir, OUTDIR, f'{base}.pdf')
        self.out_png = os.path.join(self.basedir, OUTDIR, f'{base}.png')
        print(f'output: {self.out_pdf}')

        for src, base in SRC.items():
            self._loadsrc(src, base, "_buf_msys_nrf52840dk-10", "_leaf", self.logdir)
            self._loadsrc(src, base, "_buf_msys_nrf52dk-6", "_root", self.logdir)

        # parse data
        self.res_root = []
        self.res_leaf = []
        for base in USE:
            for name in [f'{base}{s}' for s in ("_root", "_leaf")]:
                print(name)
                tmp = []
                for i, x in enumerate(self.dat[name]["data"][0]["x"]):
                    if x >= 0 and x <= 3600:
                        if self.dat[name]["data"][0]["y"][i] > 0:
                            tmp.append(self.dat[name]["data"][0]["y"][i] * MBUF_SIZE)

                if "_root" in name:
                    self.res_root.append(tmp)
                elif "_leaf" in name:
                    self.res_leaf.append(tmp)

        print(len(self.res_root))


    def _loadsrc(self, name, base, suffix, suffix_new, logdir):
        file = os.path.join(self.plotdir, f'{base}{suffix}.json')
        if not os.path.isfile(file):
            rawfile = os.path.join(logdir, f'{base}.dump')
            print(f'generating {file}')
            print(f'      from {rawfile}')
            Results(rawfile)

        print(f'loading {file}')
        self.dat[f'{name}{suffix_new}'] = self.load(file)


    def make(self):
        fig, ax = plt.subplots(1, 2, sharex=True)
        fig.set_size_inches(5, 1.5)

        titles = ("Root node (consumer)", "Leaf node (producer)")
        lab = ["star", "tree", "line", "star", "tree", "line"]

        ax[0].boxplot(self.res_root, whis=[0, 100])
        ax[1].boxplot(self.res_leaf, whis=[0, 100])

        yt = {
            "title": "Buffer usage [bytes]",
            "t": np.arange(0.0, 7001, 2000),
            "lim": [0, 7000],
        }

        for col, a in enumerate(ax):
            a.set_title(f'{titles[col]}', size=AXISLBLSIZE)
            a.set_xticks([1, 2, 3, 4, 5, 6])
            # a.set_xlim(xlim)
                # a.set_xlabel("Experiment runtime [s]")
            a.set_xticklabels([f'{l}' for l in lab], size=TICKLBLSIZE)

            a.set_ylim(yt["lim"])
            a.set_yticks(yt["t"])
            if col != 0:
                a.set_yticklabels([])
            else:
                # a.set_ylabel(yt[row]["title"], size=AXISLBLSIZE)
                a.set_yticklabels([f'{l / 1000:.0f}' for l in yt["t"]], size=TICKLBLSIZE)
            a.yaxis.grid(True)

            a.axvspan(3.5, 6.5, facecolor='grey', alpha=0.2)

        # Set common labels
        fig.text(0.52, 0.00, 'Network topology', ha='center', va='center', size=AXISLBLSIZE)
        fig.text(-0.02, 0.42, 'NimBLE buffer\nusage [Kbytes]', ha='center', va='center', rotation='vertical', size=AXISLBLSIZE)


        # fig.text(0.21,   0.85, 'IP-BLE-Adv', ha='center', va='center', size=TICKLBLSIZE)
        # fig.text(0.41,   0.85, '6BLEMesh', ha='center', va='center', size=TICKLBLSIZE)
        # fig.text(0.62,   0.85, 'IP-BLE-Adv', ha='center', va='center', size=TICKLBLSIZE)
        # fig.text(0.81,  0.85, '6BLEMesh', ha='center', va='center', size=TICKLBLSIZE)
        fig.text(0.18, 0.61, 'IP-BLE-Adv', ha='center', va='center', size=TICKLBLSIZE)
        fig.text(0.42, 0.61, '6BLEMesh', ha='center', va='center', size=TICKLBLSIZE)
        fig.text(0.65, 0.61, 'IP-BLE-Adv', ha='center', va='center', size=TICKLBLSIZE)
        fig.text(0.87, 0.61, '6BLEMesh', ha='center', va='center', size=TICKLBLSIZE)

        plt.tight_layout()
        plt.subplots_adjust(wspace=0.05, hspace=0.15)
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
