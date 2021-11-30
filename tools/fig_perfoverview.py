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
    "jelling_line_1s1h100b_i100_0": "ea_putnon_jelling_line_1s1h100b_i100/ea_putnon_jelling_line_1s1h100b_i100_20211126-023447",
    "jelling_line_1s1h100b_i25_0": "ea_putnon_jelling_line_1s1h100b_i25/ea_putnon_jelling_line_1s1h100b_i25_20211123-032746",
    "jelling_line_1s1h100b_i50_0": "ea_putnon_jelling_line_1s1h100b_i50/ea_putnon_jelling_line_1s1h100b_i50_20211123-071559",
    "jelling_line_1s1h100b_i75_0": "ea_putnon_jelling_line_1s1h100b_i75/ea_putnon_jelling_line_1s1h100b_i75_20211125-224517",
    "jelling_line_5s1h100b_i100_0": "ea_putnon_jelling_line_5s1h100b_i100/ea_putnon_jelling_line_5s1h100b_i100_20211126-062256",
    "jelling_line_5s1h100b_i25_0": "ea_putnon_jelling_line_5s1h100b_i25/ea_putnon_jelling_line_5s1h100b_i25_20211124-231607",
    "jelling_line_5s1h100b_i50_0": "ea_putnon_jelling_line_5s1h100b_i50/ea_putnon_jelling_line_5s1h100b_i50_20211125-030445",
    "jelling_line_5s1h100b_i75_0": "ea_putnon_jelling_line_5s1h100b_i75/ea_putnon_jelling_line_5s1h100b_i75_20211125-065302",
    "jelling_star_1s1h100b_i100_0": "ea_putnon_jelling_star_1s1h100b_i100/ea_putnon_jelling_star_1s1h100b_i100_20211122-125838",
    "jelling_star_1s1h100b_i100_1": "ea_putnon_jelling_star_1s1h100b_i100/ea_putnon_jelling_star_1s1h100b_i100_20211122-153544",
    "jelling_star_1s1h100b_i100_2": "ea_putnon_jelling_star_1s1h100b_i100/ea_putnon_jelling_star_1s1h100b_i100_20211126-000251",
    "jelling_star_1s1h100b_i25_0": "ea_putnon_jelling_star_1s1h100b_i25/ea_putnon_jelling_star_1s1h100b_i25_20211119-065431",
    "jelling_star_1s1h100b_i25_1": "ea_putnon_jelling_star_1s1h100b_i25/ea_putnon_jelling_star_1s1h100b_i25_20211123-005540",
    "jelling_star_1s1h100b_i50_0": "ea_putnon_jelling_star_1s1h100b_i50/ea_putnon_jelling_star_1s1h100b_i50_20211118-082505",
    "jelling_star_1s1h100b_i50_1": "ea_putnon_jelling_star_1s1h100b_i50/ea_putnon_jelling_star_1s1h100b_i50_20211123-044403",
    "jelling_star_1s1h100b_i75_0": "ea_putnon_jelling_star_1s1h100b_i75/ea_putnon_jelling_star_1s1h100b_i75_20211118-103044",
    "jelling_star_1s1h100b_i75_1": "ea_putnon_jelling_star_1s1h100b_i75/ea_putnon_jelling_star_1s1h100b_i75_20211123-083211",
    "jelling_star_1s1h100b_i75_2": "ea_putnon_jelling_star_1s1h100b_i75/ea_putnon_jelling_star_1s1h100b_i75_20211125-201258",
    "jelling_star_5s1h100b_i100_0": "ea_putnon_jelling_star_5s1h100b_i100/ea_putnon_jelling_star_5s1h100b_i100_20211126-035058",
    "jelling_star_5s1h100b_i25_0": "ea_putnon_jelling_star_5s1h100b_i25/ea_putnon_jelling_star_5s1h100b_i25_20211124-204357",
    "jelling_star_5s1h100b_i50_0": "ea_putnon_jelling_star_5s1h100b_i50/ea_putnon_jelling_star_5s1h100b_i50_20211125-003225",
    "jelling_star_5s1h100b_i75_0": "ea_putnon_jelling_star_5s1h100b_i75/ea_putnon_jelling_star_5s1h100b_i75_20211125-042104",
    "jelling_tree_1s1h100b_i100_0": "ea_putnon_jelling_tree_1s1h100b_i100/ea_putnon_jelling_tree_1s1h100b_i100_20211126-011846",
    "jelling_tree_1s1h100b_i25_0": "ea_putnon_jelling_tree_1s1h100b_i25/ea_putnon_jelling_tree_1s1h100b_i25_20211119-085506",
    "jelling_tree_1s1h100b_i25_1": "ea_putnon_jelling_tree_1s1h100b_i25/ea_putnon_jelling_tree_1s1h100b_i25_20211123-021141",
    "jelling_tree_1s1h100b_i50_0": "ea_putnon_jelling_tree_1s1h100b_i50/ea_putnon_jelling_tree_1s1h100b_i50_20211123-055958",
    "jelling_tree_1s1h100b_i75_0": "ea_putnon_jelling_tree_1s1h100b_i75/ea_putnon_jelling_tree_1s1h100b_i75_20211125-212904",
    "jelling_tree_5s1h100b_i100_0": "ea_putnon_jelling_tree_5s1h100b_i100/ea_putnon_jelling_tree_5s1h100b_i100_20211126-050700",
    "jelling_tree_5s1h100b_i25_0": "ea_putnon_jelling_tree_5s1h100b_i25/ea_putnon_jelling_tree_5s1h100b_i25_20211124-215957",
    "jelling_tree_5s1h100b_i50_0": "ea_putnon_jelling_tree_5s1h100b_i50/ea_putnon_jelling_tree_5s1h100b_i50_20211125-014831",
    "jelling_tree_5s1h100b_i75_0": "ea_putnon_jelling_tree_5s1h100b_i75/ea_putnon_jelling_tree_5s1h100b_i75_20211125-053701",
    "statconn_line_1s1h100b_i15r35_0": "ea_putnon_statconn_line_1s1h100b_i15r35/ea_putnon_statconn_line_1s1h100b_i15r35_20211122-101656",
    "statconn_line_1s1h100b_i40r60_0": "ea_putnon_statconn_line_1s1h100b_i40r60/ea_putnon_statconn_line_1s1h100b_i40r60_20211117-165433",
    "statconn_line_1s1h100b_i40r60_1": "ea_putnon_statconn_line_1s1h100b_i40r60/ea_putnon_statconn_line_1s1h100b_i40r60_20211118-201726",
    "statconn_line_1s1h100b_i65r85_0": "ea_putnon_statconn_line_1s1h100b_i65r85/ea_putnon_statconn_line_1s1h100b_i65r85_20211119-000921",
    "statconn_line_1s1h100b_i90r110_0": "ea_putnon_statconn_line_1s1h100b_i90r110/ea_putnon_statconn_line_1s1h100b_i90r110_20211119-053540",
    "statconn_line_5s1h100b_i15r35_0": "ea_putnon_statconn_line_5s1h100b_i15r35/ea_putnon_statconn_line_5s1h100b_i15r35_20211119-134339",
    "statconn_line_5s1h100b_i40r60_0": "ea_putnon_statconn_line_5s1h100b_i40r60/ea_putnon_statconn_line_5s1h100b_i40r60_20211122-182312",
    "statconn_line_5s1h100b_i65r85_0": "ea_putnon_statconn_line_5s1h100b_i65r85/ea_putnon_statconn_line_5s1h100b_i65r85_20211122-205920",
    "statconn_line_5s1h100b_i90r110_0": "ea_putnon_statconn_line_5s1h100b_i90r110/ea_putnon_statconn_line_5s1h100b_i90r110_20211122-233636",
    "statconn_star_1s1h100b_i15r35_0": "ea_putnon_statconn_star_1s1h100b_i15r35/ea_putnon_statconn_star_1s1h100b_i15r35_20211118-125114",
    "statconn_star_1s1h100b_i40r60_0": "ea_putnon_statconn_star_1s1h100b_i40r60/ea_putnon_statconn_star_1s1h100b_i40r60_20211118-174417",
    "statconn_star_1s1h100b_i65r85_0": "ea_putnon_statconn_star_1s1h100b_i65r85/ea_putnon_statconn_star_1s1h100b_i65r85_20211118-213616",
    "statconn_star_1s1h100b_i90r110_0": "ea_putnon_statconn_star_1s1h100b_i90r110/ea_putnon_statconn_star_1s1h100b_i90r110_20211116-134641",
    "statconn_star_1s1h100b_i90r110_1": "ea_putnon_statconn_star_1s1h100b_i90r110/ea_putnon_statconn_star_1s1h100b_i90r110_20211119-030234",
    "statconn_star_5s1h100b_i15r35_0": "ea_putnon_statconn_star_5s1h100b_i15r35/ea_putnon_statconn_star_5s1h100b_i15r35_20211119-111011",
    "statconn_star_5s1h100b_i40r60_0": "ea_putnon_statconn_star_5s1h100b_i40r60/ea_putnon_statconn_star_5s1h100b_i40r60_20211119-150254",
    "statconn_star_5s1h100b_i65r85_0": "ea_putnon_statconn_star_5s1h100b_i65r85/ea_putnon_statconn_star_5s1h100b_i65r85_20211119-190303",
    "statconn_star_5s1h100b_i90r110_0": "ea_putnon_statconn_star_5s1h100b_i90r110/ea_putnon_statconn_star_5s1h100b_i90r110_20211119-225556",
    "statconn_tree_1s1h100b_i15r35_0": "ea_putnon_statconn_tree_1s1h100b_i15r35/ea_putnon_statconn_tree_1s1h100b_i15r35_20211118-150852",
    "statconn_tree_1s1h100b_i40r60_0": "ea_putnon_statconn_tree_1s1h100b_i40r60/ea_putnon_statconn_tree_1s1h100b_i40r60_20211118-190049",
    "statconn_tree_1s1h100b_i65r85_0": "ea_putnon_statconn_tree_1s1h100b_i65r85/ea_putnon_statconn_tree_1s1h100b_i65r85_20211118-225246",
    "statconn_tree_1s1h100b_i90r110_0": "ea_putnon_statconn_tree_1s1h100b_i90r110/ea_putnon_statconn_tree_1s1h100b_i90r110_20211119-041905",
    "statconn_tree_5s1h100b_i15r35_0": "ea_putnon_statconn_tree_5s1h100b_i15r35/ea_putnon_statconn_tree_5s1h100b_i15r35_20211119-122644",
    "statconn_tree_5s1h100b_i40r60_0": "ea_putnon_statconn_tree_5s1h100b_i40r60/ea_putnon_statconn_tree_5s1h100b_i40r60_20211122-170610",
    "statconn_tree_5s1h100b_i65r85_0": "ea_putnon_statconn_tree_5s1h100b_i65r85/ea_putnon_statconn_tree_5s1h100b_i65r85_20211122-194229",
    "statconn_tree_5s1h100b_i90r110_0": "ea_putnon_statconn_tree_5s1h100b_i90r110/ea_putnon_statconn_tree_5s1h100b_i90r110_20211122-221945",
}

# SRC2 = {
#     "adv_star_p1s_i25":  "ip-over-ble-adv/ea_putnon_star_i1s_1h_ai25ms_me3_si30ms_sw30ms_b100_20211110-212649",
#     "adv_star_p1s_i100": "ip-over-ble-adv/ea_putnon_star_i1s_1h_ai100ms_me3_si30ms_sw30ms_b100_20211110-224024",
#     "adv_star_p5s_i25":  "ip-over-ble-adv/ea_putnon_star_i5s_1h_ai25ms_me3_si30ms_sw30ms_b100_20211110-235433",
#     "adv_star_p5s_i100": "ip-over-ble-adv/ea_putnon_star_i5s_1h_ai100ms_me3_si30ms_sw30ms_b100_20211111-010736",

#     "adv_tree_p1s_i25":  "ip-over-ble-adv/ea_putnon_tree_i1s_1h_ai25ms_me3_si30ms_sw30ms_b100_20211112-022915",
#     "adv_tree_p1s_i100": "ip-over-ble-adv/ea_putnon_tree_i1s_1h_ai100ms_me3_si30ms_sw30ms_b100_20211112-034224",

#     "adv_line_p1s_i25":  "ip-over-ble-adv/ea_putnon_line_i1s_1h_ai25ms_me3_si30ms_sw30ms_b100_20211112-072433",
#     "adv_line_p1s_i100": "ip-over-ble-adv/ea_putnon_line_i1s_1h_ai100ms_me3_si30ms_sw30ms_b100_20211112-083815",
# }

DIST = {
    # star 1s
    "0-0": ["jelling_star_1s1h100b_i25_1", "jelling_star_1s1h100b_i50_1", "jelling_star_1s1h100b_i75_2", "jelling_star_1s1h100b_i100_2"],
    "0-1": ["statconn_star_1s1h100b_i15r35_0", "statconn_star_1s1h100b_i40r60_0", "statconn_star_1s1h100b_i65r85_0", "statconn_star_1s1h100b_i90r110_1"],
    # tree 1s
    "0-2": ["jelling_tree_1s1h100b_i25_1", "jelling_tree_1s1h100b_i50_0", "jelling_tree_1s1h100b_i75_0", "jelling_tree_1s1h100b_i100_0"],
    "0-3": ["statconn_tree_1s1h100b_i15r35_0", "statconn_tree_1s1h100b_i40r60_0", "statconn_tree_1s1h100b_i65r85_0", "statconn_tree_1s1h100b_i90r110_0"],
    # line 1s
    "0-4": ["jelling_line_1s1h100b_i25_0", "jelling_line_1s1h100b_i50_0", "jelling_line_1s1h100b_i75_0", "jelling_line_1s1h100b_i100_0"],
    "0-5": ["statconn_line_1s1h100b_i15r35_0", "statconn_line_1s1h100b_i40r60_1", "statconn_line_1s1h100b_i65r85_0", "statconn_line_1s1h100b_i90r110_0"],
    # star 5s
    "1-0": ["jelling_star_5s1h100b_i25_0", "jelling_star_5s1h100b_i50_0", "jelling_star_5s1h100b_i75_0", "jelling_star_5s1h100b_i100_0"],
    "1-1": ["statconn_star_5s1h100b_i15r35_0", "statconn_star_5s1h100b_i40r60_0", "statconn_star_5s1h100b_i65r85_0", "statconn_star_5s1h100b_i90r110_0"],
    # tree 5s
    "1-2": ["jelling_tree_5s1h100b_i25_0", "jelling_tree_5s1h100b_i50_0", "jelling_tree_5s1h100b_i75_0", "jelling_tree_5s1h100b_i100_0"],
    "1-3": ["statconn_tree_5s1h100b_i15r35_0", "statconn_tree_5s1h100b_i40r60_0", "statconn_tree_5s1h100b_i65r85_0", "statconn_tree_5s1h100b_i90r110_0"],
    # line 5s
    "1-4": ["jelling_line_5s1h100b_i25_0", "jelling_line_5s1h100b_i50_0", "jelling_line_5s1h100b_i75_0", "jelling_line_5s1h100b_i100_0"],
    "1-5": ["statconn_line_5s1h100b_i15r35_0", "statconn_line_5s1h100b_i40r60_0", "statconn_line_5s1h100b_i65r85_0", "statconn_line_5s1h100b_i90r110_0"],
}

LAB = {
    "i15r35": "[15:35]ms",
    "i40r60": "[40:60]ms",
    "i65r85": "[65:85]ms",
    "i90r110": "[90:110]ms",
    "i25":  "25ms",
    "i50": "50ms",
    "i75": "75ms",
    "i100": "100ms",
}

COL = {
    "i15r35": "C4",
    "i40r60": "C5",
    "i65r85": "C6",
    "i90r110": "C8",
    "i25":  "C0",
    "i50": "C1",
    "i75": "C2",
    "i100": "C3",
}


ORDER = [
    "adv_star_p5s_i100ms",
    # "adv_30ms_star",
    # "adv_i30_tree",
]

SUFFIX = "_cdf.json"
OUTDIR = "results/figs"

TICKLBLSIZE = 9
LEGENDSIZE = 8
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

        self.expstats.plot_cdf()


    def update(self, time, node, line):
        self.expstats.update(time, node, line)
        self.llstats.update(time, node, line)
        # self.topo.update(time, node, line)


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
            self._load(name, file, base, self.logdir)

        # for name, base in SRC2.items():
        #     filebase = base.split("/")[1]
        #     plotbase = "_".join(filebase.split("_")[:-1])
        #     file = os.path.join(self.plotdir, f'{plotbase}', f'{filebase}{SUFFIX}')
        #     self._load(name, file, base, self.logdir2)


    def _load(self, name, file, base, logdir):
        if not os.path.isfile(file):
            dumpfile = os.path.join(logdir, f'{base}.dump')
            print(f'generating {file}')
            print(f'source:    {dumpfile}')
            Results(os.path.join(logdir, f'{base}.dump'))

        print(f'loading {file}')
        self.dat[name] = self.load(file)


    def make(self):
        fig, ax = plt.subplots(2, 6, sharex=True)
        fig.set_size_inches(12, 4)

        for row, ar in enumerate(ax):
            for col, a in enumerate(ar):
                postr = f'{row}-{col}'

                if postr in DIST:
                    for name in DIST[postr]:
                        itvl = name.split("_")[-2]
                        if not "i" in itvl:
                            itvl = name.split("_")[-1]
                        col = COL[itvl]
                        lab = LAB[itvl]
                        a.plot(self.dat[name]["data"][1]["x"], self.dat[name]["data"][1]["y"], color=col, label=lab)

                        print(f'{name:<35}: {self.dat[name]["data"][1]["y"][-1] * 100}%')

        yt = [
            {
                "title": "Producer interval 1s\nCDF [0:1.0]",
                "t": np.arange(0.0, 1.02, .2),
                "lim": [0, 1.02],
            },
            {
                "title": "Producer interval 5s\nCDF [0:1.0]",
                "t": np.arange(0.0, 1.02, .2),
                "lim": [0, 1.02],
            },
        ]

        leg = {
            "0-4": "upper right",
        }

        xticks = np.arange(0.0, 2.1, .25)
        xlim = [0.0, 2.2]

        titles = ["IP-BLE-Adv", "6BLEMesh", "IP-BLE-Adv", "6BLEMesh", "IP-BLE-Adv", "6BLEMesh"]


        for row, ar in enumerate(ax):
            for col, a in enumerate(ar):
                postr = f'{row}-{col}'

                if postr in leg:
                    loc = leg[postr]
                else:
                    loc = "lower right"
                a.legend(fontsize=LEGENDSIZE, loc=loc)

                if row == 0:
                    a.set_title(f'{titles[col]}', size=AXISLBLSIZE)

                a.set_xticks(xticks)
                a.set_xlim(xlim)
                if row != len(ax) - 1:
                    a.set_xticklabels([])
                else:
                    # a.set_xlabel("Experiment runtime [s]")
                    a.set_xticklabels([f'{l:.1f}' for l in xticks], size=TICKLBLSIZE)
                    for index, label in enumerate(a.xaxis.get_ticklabels()):
                        if index % 2 != 0:
                            label.set_visible(False)
                a.xaxis.grid(True)

                a.set_yticks(yt[row]["t"])
                a.set_ylim(yt[row]["lim"])
                if col != 0:
                    a.set_yticklabels([])
                else:
                    a.set_ylabel(yt[row]["title"], size=AXISLBLSIZE)
                    a.set_yticklabels([f'{l:.1f}' for l in yt[row]["t"]], size=TICKLBLSIZE)
                a.yaxis.grid(True)

                # if col == 5:
                #     a2 = a.twinx()
                #     a2.set_yticks([])
                #     a2.set_yticklabels([])
                #     if row == 0:
                #         a2.set_ylabel("Producer interval 1s", size=AXISLBLSIZE)
                #     if row == 1:
                #         a2.set_ylabel("Producer interval 5s", size=AXISLBLSIZE)

                if (col % 2) == 1:
                    a.axvspan(0.0, 2.2, facecolor='silver', alpha=0.3)


        # Set common labels
        fig.text(0.53, 0.00, 'RTT of CoAP messages [s]', ha='center', va='center', size=AXISLBLSIZE)
        # fig.text(0.00, 0.5, 'Memory Usage [bytes]', ha='center', va='center', rotation='vertical', size=AXISLBLSIZE)

        fig.text(0.20, 1.0, 'Star topology', ha='center', va='center', size=AXISLBLSIZE)
        fig.text(0.51, 1.0, 'Tree topology', ha='center', va='center', size=AXISLBLSIZE)
        fig.text(0.82, 1.0, 'Line topology', ha='center', va='center', size=AXISLBLSIZE)

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
