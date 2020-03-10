#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
import argparse
import numpy as np


def compute(component):
    for filename in glob("./OUTPUT_FILES/*.semd"):
        c = filename.split("/")[-1].split(".")[-2]
        data = np.loadtxt(filename)
        zero_adj = not (component == "all" or component == c)
        if zero_adj:
            data[:, 1] = 0.0
        adj_filename = filename.replace("OUTPUT_FILES/", "SEM/").replace(
            ".semd", ".adj"
        )

        data[:, 1] = -np.gradient(data[:, 1])
        if zero_adj:
            print("writing zero adjoint for {}".format(adj_filename))
        else:
            print("writing adjoint for {}".format(adj_filename))
        np.savetxt(adj_filename, data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Adjoint Sources")
    parser.add_argument(
        "component", help="component", choices=("BXX", "BXY", "BXZ", "all")
    )
    args = parser.parse_args()

    compute(args.component)
