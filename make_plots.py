from utils import *


def make_plots(bar_plots_name, plots_name, file_names):
    """
    Uses the JSON data in the given 'file_names' to write aggregate bar plots
    to 'bar_plots_name' and aggregate plots to 'plots_name'.
    """
    data = [read_json_data(file) for file in file_names]
    output_bar_multiple(bar_plots_name, data)
    output_plot_multiple(plots_name, data)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        eprint("usage:", sys.argv[0], "<json-file-name> ...")
        eprint("  Makes aggregate plots from all the data in the given JSON "
               "files.")
        sys.exit(1)
    else:
        make_plots("bar_plots.html", "plots.html", sys.argv[1:])
