from typing import Callable, Literal, Optional, Union

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.sparse import csr_array
from scipy.stats import rankdata


def clear_axis(axis):
    axis.set_xticks([])
    axis.set_yticks([])


def get_relative_measurement(ax, main_ax, measurement="height"):
    """
    Get the height of an axis's bounding box, as a fraction of main_ax's height.
    """
    fig = ax.figure
    fig.canvas.draw()  # ensure renderer is up-to-date
    renderer = fig.canvas.get_renderer()

    # Get height in inches for the label axis and the main axis
    label_bbox = ax.get_tightbbox(renderer=renderer)
    main_bbox = main_ax.get_tightbbox(renderer=renderer)
    if measurement == "height":
        label_height_inches = label_bbox.height
        main_height_inches = main_bbox.height
    elif measurement == "width":
        label_height_inches = label_bbox.width
        main_height_inches = main_bbox.width

    return label_height_inches / main_height_inches


def draw_label_arc(ax, row_label, col_label):
    # Parameters
    xshift = -0.04
    yshift = 0.02
    center = (0 + xshift, 1 + yshift)
    radius = 0.05
    theta1 = 110  # Start angle in degrees (positive y-axis)
    theta2 = 160  # End angle in degrees (negative x-axis)

    # Draw the arc (no arrowhead)
    arc = Arc(
        center,
        width=2 * radius,
        height=2 * radius,
        angle=0,
        theta1=theta1,
        theta2=theta2,
        linewidth=2,
        color="black",
        clip_on=False,
        transform=ax.transAxes,
    )
    ax.add_patch(arc)

    # Add an arrowhead at the end of the arc
    # Compute end point of the arc
    start_angle_rad = np.radians(theta2)
    start_point = (
        center[0] + radius * np.cos(start_angle_rad),
        center[1] + radius * np.sin(start_angle_rad),
    )

    end_angle_rad = np.radians(theta1)
    end_point = (
        center[0] + radius * np.cos(end_angle_rad),
        center[1] + radius * np.sin(end_angle_rad),
    )
    dx = -np.sin(end_angle_rad)
    dy = np.cos(end_angle_rad)

    arrow_tip = end_point
    tip_pad = 0.02
    arrow = FancyArrowPatch(
        posA=arrow_tip,
        posB=(arrow_tip[0] - tip_pad * dx, arrow_tip[1] - tip_pad * dy),
        arrowstyle="->",
        mutation_scale=15,
        color="black",
        linewidth=2,
        clip_on=False,
        transform=ax.transAxes,
    )
    ax.add_patch(arrow)

    ax.text(
        start_point[0],
        start_point[1],
        row_label,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize="medium",
    )
    ax.text(
        end_point[0] + tip_pad,
        end_point[1],
        col_label,
        transform=ax.transAxes,
        ha="left",
        va="center",
        fontsize="medium",
    )


class AxisGrid:
    def __init__(
        self,
        ax,
        spines=True,
    ):
        fig = ax.figure
        divider = make_axes_locatable(ax)
        self.spines = spines
        self.fig = fig
        self.ax = ax
        self.divider = divider
        self.top_axs = []
        self.left_axs = []
        self.bottom_axs = []
        self.right_axs = []
        self.side_axs = {
            "top": self.top_axs,
            "bottom": self.bottom_axs,
            "left": self.left_axs,
            "right": self.right_axs,
        }

    @property
    def all_top_axs(self):
        return [self.ax] + self.top_axs

    @property
    def all_bottom_axs(self):
        return [self.ax] + self.bottom_axs

    @property
    def all_left_axs(self):
        return [self.ax] + self.left_axs

    @property
    def all_right_axs(self):
        return [self.ax] + self.right_axs

    def append_axes(self, side, size="10%", pad="auto", **kwargs) -> plt.Axes:
        # NOTE: old way was using shared axes, but labels kept getting annoying
        # kws = {}
        # if side in ["top", "bottom"]:
        #     kws["sharex"] = self.ax
        # elif side in ["left", "right"]:
        #     kws["sharey"] = self.ax

        if pad == "auto":
            if len(self.side_axs[side]) > 0:
                last_ax = self.side_axs[side][-1]
                measurement = "height" if side in ["top", "bottom"] else "width"
                pad = get_relative_measurement(last_ax, self.ax, measurement)
            else:
                pad = 0.0

        # NOTE: this was VERY fragile, could not figure out how to do it in right in
        # float or in manual axes_size like pad = axes_size.from_any(
        #   pad, fraction_ref=axes_size.AxesX(self.ax)
        # )
        pad = f"{pad * 100}%"
        ax = self.divider.append_axes(side, size=size, pad=pad, **kwargs)

        clear_axis(ax)
        ax.tick_params(
            which="both",
            length=0,
        )

        if side in ["top", "bottom"]:
            ax.set_xlim(self.ax.get_xlim())
        elif side in ["left", "right"]:
            ax.set_ylim(self.ax.get_ylim())

        self.side_axs[side].append(ax)
        return ax

    def set_title(self, title, **kwargs):
        for ax in self.all_top_axs:
            ax.set_title("", **kwargs)
        text = self.all_top_axs[-1].set_title(title, **kwargs)
        return text

    def set_xlabel(self, xlabel, **kwargs):
        for ax in self.all_bottom_axs:
            ax.set_xlabel("", **kwargs)
        # NOTE a bit of an abuse of notation here but putting xlabel on the top
        text = self.all_top_axs[-1].set_title(xlabel, **kwargs)
        return text

    def set_ylabel(self, ylabel, **kwargs):
        for ax in self.all_left_axs:
            ax.set_ylabel("", **kwargs)
        text = self.all_left_axs[-1].set_ylabel(ylabel, **kwargs)
        return text

    def set_corner_title(self, title, **kwargs):
        """
        Set a title in the top left corner of the grid.
        """
        # ax = self.all_top_axs[-1]

        text = self.ax.text(0, 1, title, ha="right", rotation=0, **kwargs)
        return text


def draw_bracket(ax, start, end, axis="x", color="black"):
    lx = np.linspace(-np.pi / 2.0 + 0.05, np.pi / 2.0 - 0.05, 500)
    tan = np.tan(lx)
    curve = np.hstack((tan[::-1], tan))
    x = np.linspace(start, end, 1000)
    if axis == "x":
        ax.plot(x, -curve, color=color)
    elif axis == "y":
        ax.plot(curve, x, color=color)


def draw_box(ax, start, end, axis="x", color="black", alpha=0.5, lw=0.5):
    if axis == "x":
        rect = plt.Rectangle(
            (start, 0),
            end - start,
            1,
            color=color,
        )
        ax.axvline(start, lw=0.5, alpha=0.5, color="black", zorder=2)
    elif axis == "y":
        rect = plt.Rectangle(
            (0, start),
            1,
            end - start,
            color=color,
        )
        ax.axhline(start, lw=0.5, alpha=0.5, color="black", zorder=2)
    ax.add_patch(rect)


def add_position_column(nodes, pos_key="position"):
    if pos_key in nodes.columns:
        pos_key = "_" + pos_key
        pos_key = add_position_column(nodes, pos_key)
    else:
        nodes[pos_key] = np.arange(len(nodes))
    return pos_key


def adjacencyplot(
    adjacency: Union[np.ndarray, csr_array, pd.DataFrame],
    nodes: pd.DataFrame = None,
    groupby: Optional[list[str]] = None,
    sortby: Optional[list[str]] = None,
    group_element: Literal["box", "bracket"] = "box",
    group_axis_size: str = "1%",
    node_palette: Optional[dict] = None,
    edge_palette: Optional[Union[str, dict, Callable]] = "Greys",
    ax: Optional[plt.Axes] = None,
    figsize: tuple = (8, 8),
    edge_size: bool = True,
    edge_hue: bool = False,
    hue_norm: Optional[tuple] = None,
    sizes: tuple = (1, 10),
    edge_linewidth: float = 0.05,
    label_fontsize: Union[float, int, str] = "medium",
    title_fontsize: Union[float, int, str] = "large",
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    arc_labels: Optional[tuple] = ("Pre", "Post"),
    **kwargs,
):
    """
    Plot an adjacency matrix with optional grouping and sorting specified by node data.

    Parameters
    ----------
    adjacency :
        Adjacency matrix to plot. Only non-zero entries will be plotted.
    nodes :
        DataFrame containing node information, needs to be specified to use sorting and
        grouping features.
    groupby :
        Columns in `nodes` to group by. Adjacency matrix will be sorted into these
        groups and each group will be represented by a different color or bracket on the
        margins of the plot.
    sortby :
        Columns in `nodes` to sort by. The adjacency matrix will be sorted according to
        these columns, and sorting happens within each group if `groupby` is specified.
    group_element :
        Specifies how to represent groups on the margins of the plot. Can be either
        "box" or "bracket".
    group_axis_size :
        Size of the group axes on the margins of the plot. Should be a string like
        "1%" for relative sizing.
    node_palette :
        A dictionary mapping node labels to colors.
    edge_palette :
        A color palette for the edges. Can be a string (e.g., "Greys") or a
        dictionary mapping edge weights to colors.
    ax :
        Matplotlib Axes object to plot on. If None, a new figure and axes will be
        created.
    figsize :
        Size of the figure to create if `ax` is None.
    edge_size :
        If True, the size of the points in the scatter plot will be determined by the
        weight of the edges in the adjacency matrix.
    edge_hue :
        If True, the color of the points in the scatter plot will be determined by the
        rank of the edge weights in the adjacency matrix.
    sizes :
        A tuple specifying the minimum and maximum sizes of the points in the scatter
        plot.
    edge_linewidth :
        Width of the lines representing edges in the scatter plot.
    label_fontsize :
        Font size for the labels on the axes.
    title_fontsize :
        Font size for the title of the plot.
    xlabel :
        Label for the x-axis.
    ylabel :
        Label for the y-axis.
    title :
        Title for the plot.
    arc_labels :
        A tuple containing the labels for the arc connecting the rows and columns, for
        example indicating "pre" and "post."
    **kwargs :
        Additional keyword arguments passed to the seaborn scatterplot function for
        plotting the edges.

    Returns
    -------
    ax :
        The matplotlib Axes object containing the plot.
    grid :
        An AxisGrid object containing the group axes for the plot, including any created
        axes on the margins for grouping. This object can be used for setting titles and
        labels cleanly.
    """
    if nodes is None:
        nodes = pd.DataFrame(index=np.arange(adjacency.shape[0]))
    nodes = nodes.reset_index().copy()
    if sortby is not None:
        if isinstance(sortby, str):
            sortby = [sortby]
    else:
        sortby = []
    if groupby is not None:
        if isinstance(groupby, str):
            groupby = [groupby]
    else:
        groupby = []
    sort_by = groupby + sortby

    nodes = nodes.sort_values(sort_by)

    if isinstance(adjacency, pd.DataFrame):
        # NOTE: this ignores the index of the DataFrame completely
        adjacency = adjacency.values

    sources, targets = np.nonzero(adjacency)
    data = adjacency[sources, targets]

    pos_key = add_position_column(nodes)

    # remap sources and targets to sorted node positions
    sources = nodes.loc[sources][pos_key].values
    targets = nodes.loc[targets][pos_key].values

    ranked_data = rankdata(data, method="average") / len(data)

    if edge_size:
        size = data
    else:
        size = None

    if edge_hue:
        hue = ranked_data
    else:
        hue = None
        edge_palette = None

    if ax is None:
        _, ax = plt.subplots(figsize=figsize)

    sns.scatterplot(
        y=sources,
        x=targets,
        size=size,
        hue=hue,
        hue_norm=hue_norm,
        ax=ax,
        legend=False,
        sizes=sizes,
        palette=edge_palette,
        linewidth=edge_linewidth,
        color="black",
        **kwargs,
    )

    if adjacency.shape[0] == adjacency.shape[1]:
        ax.axis("square")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.5, adjacency.shape[0] - 0.5)
    ax.set_ylim(adjacency.shape[1] - 0.5, -0.5)

    grid = AxisGrid(ax)

    # add groupby indicators starting from last to first
    for i, level in enumerate(groupby[::-1]):
        cax_left = grid.append_axes(
            "left", size=group_axis_size, pad="auto", zorder=len(sort_by) - i
        )
        cax_top = grid.append_axes(
            "top", size=group_axis_size, pad="auto", zorder=len(sort_by) - i
        )
        if group_element == "bracket":
            cax_left.spines[["top", "bottom", "left", "right"]].set_visible(False)
            cax_top.spines[["top", "bottom", "left", "right"]].set_visible(False)

        # means = nodes.groupby(level)[pos_key].mean().rename("mean")
        # starts = nodes.groupby(level)[pos_key].min().rename("start")
        # ends = nodes.groupby(level)[pos_key].max().rename("end")

        means = (
            nodes.groupby(groupby[: len(groupby) - i])[pos_key]
            .mean()
            .rename("mean")
            .droplevel(groupby[: len(groupby) - i - 1])
        )
        starts = (
            nodes.groupby(groupby[: len(groupby) - i])[pos_key]
            .min()
            .rename("start")
            .droplevel(groupby[: len(groupby) - i - 1])
        )
        ends = (
            nodes.groupby(groupby[: len(groupby) - i])[pos_key]
            .max()
            .rename("end")
            .droplevel(groupby[: len(groupby) - i - 1])
        )
        info = pd.concat([starts, ends], axis=1)

        for group_name, (start, end) in info.iterrows():
            if group_element == "box":
                draw_box(cax_left, start, end, axis="y", color=node_palette[group_name])
                draw_box(cax_top, start, end, axis="x", color=node_palette[group_name])

            elif group_element == "bracket":
                draw_bracket(
                    cax_left, start, end, axis="y", color=node_palette[group_name]
                )
                draw_bracket(
                    cax_top, start, end, axis="x", color=node_palette[group_name]
                )

            ax.axhline(start, lw=0.5, alpha=0.5, color="black", zorder=-1)
            ax.axvline(start, lw=0.5, alpha=0.5, color="black", zorder=-1)

            if end == (len(nodes) - 1):
                ax.axhline(len(nodes), lw=0.5, alpha=0.5, color="black", clip_on=False)
                ax.axvline(len(nodes), lw=0.5, alpha=0.5, color="black", clip_on=False)

        cax_left.set_yticks(means.values)
        ticklabels = cax_left.set_yticklabels(means.index, rotation=0, fontsize=8)
        for label, color in zip(ticklabels, means.index.map(node_palette)):
            label.set_color(color)

        cax_top.set_xticks(means.values)
        cax_top.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ticklabels = cax_top.set_xticklabels(
            means.index, rotation=45, fontsize=label_fontsize, ha="left"
        )
        for label, color in zip(ticklabels, means.index.map(node_palette)):
            label.set_color(color)
            label.set_in_layout(True)

    if xlabel is not None:
        grid.set_xlabel(xlabel, fontsize=label_fontsize)
    if ylabel is not None:
        grid.set_ylabel(ylabel, fontsize=label_fontsize)
    if title is not None:
        grid.set_title(title, fontsize=title_fontsize)

    if isinstance(arc_labels, tuple):
        draw_label_arc(ax, *arc_labels)

    return ax, grid
