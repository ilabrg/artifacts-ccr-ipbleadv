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
    # "con_i50":  "ea_putnon_statconn_star_1s24h100b_i40r60/ea_putnon_statconn_star_1s24h100b_i40r60_20211116-150233",
    # "jel_i50":  "ea_putnon_jelling_star_1s24h100b_i50/ea_putnon_jelling_star_1s24h100b_i50_20211123-151753",
    "jel_i50": "ea_putnon_jelling_star_1s24h100b_i50/ea_putnon_jelling_star_1s24h100b_i50_20211129-065621",
}

OUTDIR = "results/figs"
SUFFIX = "_jel_adv_pkt_cnt"

TICKLBLSIZE = 9
LEGENDSIZE = 9
AXISLBLSIZE = 11


class Results(Ana):
    def __init__(self, logfile):
        super().__init__(logfile)
        self.plotter.show_plot = False # todo

        self.expstats = Expstats(self)
        self.llstats = LLStats(self)
        self.parse_log(self.update)
        self.expstats.finish()
        self.llstats.finish()

        self.llstats.plot_jelling_adv_pkt_cnt(binsize=10)


    def update(self, time, node, line):
        self.expstats.update(time, node, line)
        self.llstats.update(time, node, line)



class Fig(Expbase):
    def __init__(self):
        super().__init__()

        base = os.path.splitext(os.path.basename(__file__))[0]
        self.out_pdf = os.path.join(self.basedir, OUTDIR, f'{base}.pdf')
        self.out_png = os.path.join(self.basedir, OUTDIR, f'{base}.png')
        print(self.out_pdf)

        self.dat = {}
        for name, base in SRC.items():
            file = os.path.join(self.plotdir, f'{base}{SUFFIX}.json')
            if not os.path.isfile(file):
                dumpfile = os.path.join(self.logdir, f'{base}.dump')
                print(f'generating: {file}')
                print(f'source:     {dumpfile}')
                Results(dumpfile)
            print(f'loading:    {file}')
            self.dat[name] = self.load(file)

        # print("PDR:")
        # for name in sorted(list(PLOT.keys())):
        #     print(f'{name}: {self.dat[name]["data"][1]["y"][-1] * 100}%')


    def _loadsrc(self, name, suffix):
        base = SRC[name]
        file = os.path.join(self.plotdir, f'{base}{suffix}.json')
        if not os.path.isfile(file):
            print(f'generating {file}')
            Results(os.path.join(self.logdir, f'{base}.dump'))

        print(f'loading {file}')
        self.dat[f'{name}{suffix}'] = self.load(file)


    def make(self):
        fig, ax = plt.subplots(1, 1, sharex=True)
        fig.set_size_inches(5, 2.2)

        cfg = {"idx": 1, "col": "C3", "lab": "Non-related\nadvertising\npackets\n"}
        ax.plot(self.dat["jel_i50"]["data"][cfg["idx"]]["x"], self.dat["jel_i50"]["data"][cfg["idx"]]["y"], color=cfg["col"], label=cfg["lab"])
        cfg = {"idx": 0, "col": "C2", "lab": "IP-BLE-Adv\npackets"}
        ax.plot(self.dat["jel_i50"]["data"][cfg["idx"]]["x"], self.dat["jel_i50"]["data"][cfg["idx"]]["y"], color=cfg["col"], label=cfg["lab"])

        # set generic axis options
        # ax.set_xlim(0.0, 86400)
        # ax.set_xticks(np.arange(0, 86401, 3600))
        ax.set_xlim(0.0, 61200)
        ax.set_xticks(np.arange(0, 61201, 3600))

        xl = list(range(7,25)) + list(range(1, 16))
        # xl = list(range(15,25)) + list(range(1, 16))
        ax.set_xticklabels([f'{h}:00' for h in xl], size=TICKLBLSIZE)
        for index, label in enumerate(ax.xaxis.get_ticklabels()):
            if index % 2 != 0:
                label.set_visible(False)

        yt = np.arange(0.0, 10001, 2000)
        ax.set_ylim(yt[0], 10000)
        ax.set_yticks(yt)
        ax.set_yticklabels(["0", "2k", "4k", "6k", "8k", " 10k"], size=TICKLBLSIZE)
        ax.xaxis.grid(True)
        ax.yaxis.grid(True)

        ax.legend(fontsize=LEGENDSIZE, loc="upper right", borderaxespad=0.1, ncol=1)
        ax.set_xlabel("Time of day [hh:mm]", size=AXISLBLSIZE)
        ax.set_ylabel("Packet count [#]", size=AXISLBLSIZE)

        # Set common labels
        # fig.text(0.5, 0.00, 'Experiment runtime [h]', ha='center', va='center', size=AXISLBLSIZE)
        # fig.text(0.00, 0.5, 'PDR [0:1.0]', ha='center', va='center', rotation='vertical', size=AXISLBLSIZE)


        plt.tight_layout()
        # plt.subplots_adjust(left=0.1, right=1.0, hspace=0.15)
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
