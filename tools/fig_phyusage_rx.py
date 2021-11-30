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


SRC = {
    "adv_star": "ea_putnon_jelling_star_1s1h100b_i50/ea_putnon_jelling_star_1s1h100b_i50_20211123-044403",
    "adv_tree": "ea_putnon_jelling_tree_1s1h100b_i50/ea_putnon_jelling_tree_1s1h100b_i50_20211123-055958",
    "adv_line": "ea_putnon_jelling_line_1s1h100b_i50/ea_putnon_jelling_line_1s1h100b_i50_20211123-071559",
    "con_star": "ea_putnon_statconn_star_1s1h100b_i40r60/ea_putnon_statconn_star_1s1h100b_i40r60_20211118-174417",
    "con_tree": "ea_putnon_statconn_tree_1s1h100b_i40r60/ea_putnon_statconn_tree_1s1h100b_i40r60_20211118-190049",
    "con_line": "ea_putnon_statconn_line_1s1h100b_i40r60/ea_putnon_statconn_line_1s1h100b_i40r60_20211118-201726",
}

LABEL = {
    "con_i50_pdr": "6LoBLE: CoAP PDR",
    "con_i50_ll_pdr_sum": "6LoBLE: Link layer PDR",
}

OUTDIR = "results/figs"

TICKLBLSIZE = 9
LEGENDSIZE = 9
AXISLBLSIZE = 11


class Results(Ana):
    def __init__(self, logfile):
        super().__init__(logfile)
        self.plotter.show_plot = False # todo

        self.expstats = Expstats(self)
        self.llstats = LLStats(self)
        # self.topo = Topo(self)

        self.parse_log(self.update)

        self.expstats.finish()
        self.llstats.finish()
        # self.topo.finish()

        self.llstats.plot_phy_usage_sum(nodes=["nrf52840dk-10"])
        self.llstats.plot_phy_usage_sum(nodes=["nrf52dk-6"])


    def update(self, time, node, line):
        self.expstats.update(time, node, line)
        self.llstats.update(time, node, line)
        # self.topo.update(time, node, line)



class Fig(Expbase):
    def __init__(self):
        super().__init__()

        base = os.path.splitext(os.path.basename(__file__))[0]
        self.out_pdf = os.path.join(self.basedir, OUTDIR, f'{base}.pdf')
        self.out_png = os.path.join(self.basedir, OUTDIR, f'{base}.png')
        print(self.out_pdf)

        self.dat = {}
        self.boxes = {}

        for src, base in SRC.items():
            self._loadsrc(src, base, "_phy_usage_sum_nrf52840dk-10", "_leaf", self.logdir)
            self._loadsrc(src, base, "_phy_usage_sum_nrf52dk-6", "_root", self.logdir)
        # for src, base in SRC2.items():
        #     self._loadsrc(src, base, "_phy_usage_sum_nrf52840dk-10", "_leaf", self.logdir2)
        #     self._loadsrc(src, base, "_phy_usage_sum_nrf52dk-6", "_root", self.logdir2)

        self.parse()


    def _loadsrc(self, name, base, suffix, suffix_new, logdir):
        if "ip-over-ble" in base:
            filebase = base.split("/")[1]
            plotbase = "_".join(filebase.split("_")[:-1])
            file = os.path.join(self.plotdir, f'{plotbase}', f'{filebase}{suffix}.json')
        else:
            file = os.path.join(self.plotdir, f'{base}{suffix}.json')
        if not os.path.isfile(file):
            rawfile = os.path.join(logdir, f'{base}.dump')
            print(f'generating {file}')
            print(f'      from {rawfile}')
            Results(rawfile)

        print(f'loading {file}')
        self.dat[f'{name}{suffix_new}'] = self.load(file)


    def parse(self):
        for name, dat in self.dat.items():
            self.boxes[name] = {"rx": [], "tx": [], "acc": []}
            for off, stat in enumerate(("rx", "tx", "acc")):
                for i in range(len(dat["data"][off]["y"])):
                    if dat["data"][off]["x"][i] < 0 or dat["data"][off]["x"][i] > 3600:
                        continue
                    self.boxes[name][stat].append(dat["data"][off]["y"][i])




    def make(self):
        fig, ax = plt.subplots(1, 2, sharex=True)
        fig.set_size_inches(5, 1.5)

        lab = ["star", "tree", "line", "star", "tree", "line"]
        titles = ("Root node (consumer)", "Leaf node (producer)")
        dat0 = ("adv_star_root", "adv_tree_root", "adv_line_root", "con_star_root", "con_tree_root", "con_line_root")
        dat1 = ("adv_star_leaf", "adv_tree_leaf", "adv_line_leaf", "con_star_leaf", "con_tree_leaf", "con_line_leaf")

        # ax[0][0].boxplot([self.boxes[name]["tx"] for name in dat0], whis=[0, 100])
        # ax[0][1].boxplot([self.boxes[name]["tx"] for name in dat1], whis=[0, 100])
        ax[0].boxplot([self.boxes[name]["rx"] for name in dat0], whis=[0, 100])
        ax[1].boxplot([self.boxes[name]["rx"] for name in dat1], whis=[0, 100])


        ax[0].set_ylim([0, 6])
        ax[1].set_ylim([0, 6])

        yt = {
            "title": "Radio activity\n[0:100%]",
            "t": np.arange(0.0, 101, 20),
            "lim": [-5, 100],
        }

        for col, a in enumerate(ax):
            a.set_title(f'{titles[col]}', size=AXISLBLSIZE)
            a.set_xticks([1, 2, 3, 4, 5, 6])
            # a.set_xlim(xlim)
                # a.set_xlabel("Experiment runtime [s]")
            a.set_xticklabels([f'{l}' for l in lab], size=TICKLBLSIZE)

            a.set_yticks(yt["t"])
            a.set_ylim(yt["lim"])
            if col != 0:
                a.set_yticklabels([])
            else:
                # a.set_ylabel(yt[row]["title"], size=AXISLBLSIZE)
                a.set_yticklabels([f'{l:.1f}' for l in yt["t"]], size=TICKLBLSIZE)
            a.yaxis.grid(True)

            a.axvspan(3.5, 6.5, facecolor='grey', alpha=0.2)

        # Set common labels
        fig.text(0.52, 0.00, 'Network topology', ha='center', va='center', size=AXISLBLSIZE)
        fig.text(0.00, 0.42, 'Radio activity [%]', ha='center', va='center', rotation='vertical', size=AXISLBLSIZE)


        # fig.text(0.21,   0.85, 'IP-BLE-Adv', ha='center', va='center', size=TICKLBLSIZE)
        # fig.text(0.41,   0.85, '6BLEMesh', ha='center', va='center', size=TICKLBLSIZE)
        # fig.text(0.62,   0.85, 'IP-BLE-Adv', ha='center', va='center', size=TICKLBLSIZE)
        # fig.text(0.81,  0.85, '6BLEMesh', ha='center', va='center', size=TICKLBLSIZE)
        fig.text(0.23, 0.51, 'IP-BLE-Adv', ha='center', va='center', size=TICKLBLSIZE)
        fig.text(0.44, 0.51, '6BLEMesh', ha='center', va='center', size=TICKLBLSIZE)
        fig.text(0.66, 0.51, 'IP-BLE-Adv', ha='center', va='center', size=TICKLBLSIZE)
        fig.text(0.87, 0.51, '6BLEMesh', ha='center', va='center', size=TICKLBLSIZE)

        # ax.set_ylabel("moinfoo")
        # ax.set_title("Herrlich")

        # plt.xlabel("Experiment runtime [in s]")
        # plt.ylabel("moisnen")


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
