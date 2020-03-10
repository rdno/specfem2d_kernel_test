#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata


def grid(x, y, z, resX=500, resY=500):
    """
    Converts 3 column data to grid
    """

    xi = np.linspace(min(x), max(x), resX)
    yi = np.linspace(min(y), max(y), resY)
    X, Y = np.meshgrid(xi, yi)

    Z = griddata((x, y), z, (X, Y), method="linear")

    return X, Y, Z


def plot_bin(
    x,
    y,
    z,
    vmax=None,
    vmin=None,
    title="",
    colorlabel="",
    colorbar=True,
    auto_boundary=True,
    output_file="",
    fig=None,
    ax=None,
    cmap="RdBu",
):

    if vmax is None:
        vmax = np.max(np.abs(z))
    if vmin is None:
        vmin = -vmax

    X, Y, Z = grid(x, y, z)
    width = x.max() - x.min()
    height = y.max() - y.min()
    aspect_ratio = width / height

    fig_is_given = False
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=(3*aspect_ratio, 3))
    else:
        fig_is_given = True

    im = ax.imshow(
        Z,
        vmax=vmax,
        vmin=vmin,
        extent=[x.min(), x.max(), y.min(), y.max()],
        cmap=cmap,
        origin="lower",
    )

    if colorbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im, ax=ax, cax=cax)
        cbar.set_label(colorlabel)

    if auto_boundary:
        ax.set_xlim([min(x), max(x)])
        ax.set_ylim([min(y), max(y)])

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Z (m)")
    fig.tight_layout()

    if title:
        ax.set_title(title)
    if output_file:
        fig.savefig(output_file)
    elif not fig_is_given:
        plt.show()
    return fig, ax


def read_data(filename):
    nbytes = os.path.getsize(filename)
    with open(filename, "rb") as f:
        f.seek(0)
        n = np.fromfile(f, dtype="int32", count=1)[0]

        if n == nbytes - 8:
            f.seek(4)
            data = np.fromfile(f, dtype="float32")
            return data[:-1]
        else:
            f.seek(0)
            data = np.fromfile(f, dtype="float32")
    return data


def read_all_data(folder, suffix):
    for i, filename in enumerate(
        glob(os.path.join(folder, "proc0*_{}.bin".format(suffix)))
    ):
        if i == 0:
            data = read_data(filename)
        else:
            new_data = read_data(filename)
            data = np.append(data, new_data, axis=0)
    return data


def plot_kernel(folder, kernel, vmax=None, output_file=None):
    x = read_all_data(folder, "x")
    z = read_all_data(folder, "z")
    k = read_all_data(folder, kernel)
    plot_bin(x, z, k, title=kernel, vmax=vmax, output_file=output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot kernel")
    parser.add_argument("folder", help="folder")
    parser.add_argument("kernel", help="kernel")
    parser.add_argument("-m", "--vmax", help="Maximum value", default=None, type=float)
    parser.add_argument("-o", "--output-file", help="output file")

    args = parser.parse_args()
    plot_kernel(args.folder, args.kernel, vmax=args.vmax, output_file=args.output_file)
