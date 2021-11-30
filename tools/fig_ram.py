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

# TICKLBLSIZE = 9
# LEGENDSIZE = 8
# AXISLBLSIZE = 11
TICKLBLSIZE = 8
LEGENDSIZE = 8
AXISLBLSIZE = 10

OUTDIR = "results/figs"

SRC = {
    "jelling":  "results/codesize_jelling.json",
    "statconn": "results/codesize_statconn.json",
}

ORDER = [
    "Newlib",
    "RIOT",
    "GNRC",
    "NimBLE",
    "IP-BLE-Adv",
    "6BLEMesh",
    "App"
]

CAT = {
    "pkg/nimble/nimble": "NimBLE",
    "pkg/nimble/porting": "NimBLE",
    "pkg/nimble/contrib": "NimBLE",
    "pkg/nimble/jelling": "IP-BLE-Adv",
    "pkg/nimble/netif": "6BLEMesh",
    "pkt/nimble/statconn": "6BLEMesh",
    "sys/net": "GNRC",
    "sys": "RIOT",
    "newlib": "Newlib",
    "share": "App",
    "core": "RIOT",
    "cpu": "RIOT",
    "unspecified": "RIOT",
    "fill": "RIOT",
    "ea": "App",
    "drivers": "RIOT",
    "boards": "RIOT",
}

MAP = {
    "d": "ram",
    "b": "ram",
    "t": "rom",
}

class Fig(Expbase):
    def __init__(self):
        super().__init__()

        base = os.path.splitext(os.path.basename(__file__))[0]
        self.out_pdf = os.path.join(self.basedir, OUTDIR, f'{base}.pdf')
        self.out_png = os.path.join(self.basedir, OUTDIR, f'{base}.png')
        print(self.out_pdf)

        self.dat = {}
        self.res = {}

        for name, file in SRC.items():
            with open(os.path.join(self.basedir, file), "r", encoding="utf-8") as f:
                self.dat[name] = json.load(f)
                self.res[name] = {}

        # create categories
        for path, cat in CAT.items():
            for name in SRC:
                if cat not in self.res[name]:
                    self.res[name][cat] = {"rom": 0, "ram": 0}

        # sum up code sizes for each category
        for name, symbols in self.dat.items():
            for sym in symbols["symbols"]:
                path = "/".join(sym["path"])
                for subpath, cat in CAT.items():
                    if path.startswith(subpath):
                        self.res[name][cat][MAP[sym["type"]]] += sym["size"]
                        break

        for name in SRC:
            print("\nname:", name)
            print("ROM:")
            s = 0
            for cat in ORDER:
                s += self.res[name][cat]["rom"]
                print(f'{cat:>15}: {self.res[name][cat]["rom"]:>8}')
            print(f'{"sum":>15}: {s:>8}')
            print("RAM:")
            s = 0
            for cat in ORDER:
                s += self.res[name][cat]["ram"]
                print(f'{cat:>15}: {self.res[name][cat]["ram"]:>8}')
            print(f'{"sum":>15}: {s:>8}')

    def make(self):
        fig, ax = plt.subplots(1, 1, sharex=True)
        fig.set_size_inches(5, 1.75)

        yt = ["6BLEMesh", "IP-BLE-Adv"] #, "6BLEMesh", "IP-BLE-Adv"]
        y_pos = np.arange(len(yt))
        dat = []
        lab = []
        for cat in ORDER:
            tmp = []
            # for rr in ("ram"):
            rr = "ram"
            for name in ("statconn", "jelling"):
                tmp.append(self.res[name][cat][rr])
            dat.append(tmp)
            lab.append(cat)

        patterns = [ "/////", "-----", "xxxxx", "\\\\\\\\\\", "|||||",  "+++++",  "/////"] #, "****", "oooo", "O", ".", "*" ]
        col = ["C0", "C5", "C6", "C8", "C1", "C3", "C7"]
        args = {"label": "", "left": None}
        last = [0] * 2
        for i, bar in enumerate(dat):
            args["label"] = lab[i]
            args["left"] = last
            ax.barh(y_pos, bar, align="center", **args, color=col[i], edgecolor='white', alpha=1, hatch=patterns[i])
            last = [sum(x) for x in zip(last, bar)]

        ax.set_ylim(-.5, 2.6)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(yt, size=AXISLBLSIZE)
        # ax.set_ylabel("moinfoo")

        ax.set_xlim(0, 75000)
        xt = np.arange(0, 75001, 5000)
        ax.set_xticks(xt)
        ax.set_xticklabels([f'{t / 1000:.0f}' for t in xt], size=TICKLBLSIZE)
        # for index, label in enumerate(ax.xaxis.get_ticklabels()):
        #     if index % 2 != 1:
        #         label.set_visible(False)

        # for tick in ax.yaxis.get_minor_ticks():
        #     tick.label.set_visible(False)

        ax.set_xlabel("Static RAM usage [KBytes]", size=AXISLBLSIZE)

        # ax.ayhspan(0, 50000, facecolor='silver', alpha=0.3)

        ax.legend(loc="upper center", ncol=4, borderaxespad=0.1, fontsize=LEGENDSIZE)

        # Set common labels
        # fig.text(0.558, 0.83, 'ROM', ha='center', va='center', size=AXISLBLSIZE)
        # fig.text(0.558, 0.35, 'RAM', ha='center', va='center', size=AXISLBLSIZE)

        plt.tight_layout()
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
