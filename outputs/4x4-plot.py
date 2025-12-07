
# import matplotlib.pyplot as plt
# import pandas as pd
# import glob
# import os
# import re  # Import regex module for smarter text finding

# def plot_results():
#     # 1. Define the path where your CSVs are
#     # Make sure this matches your folder structure exactly
#     path = "./4x4/" 
#     all_files = glob.glob(os.path.join(path, "*.csv"))
    
#     if not all_files:
#         print(f"❌ No CSV files found in {path}")
#         print("Please check: 1. Did the training finish? 2. Is the path correct?")
#         return

#     print(f"Found {len(all_files)} files. Processing...")

#     data = []
    
#     # 2. Iterate through files and extract data
#     for filename in all_files:
#         try:
#             # Read the CSV
#             df = pd.read_csv(filename)
            
#             # --- THE FIX: ROBUST PARSING ---
#             # We look for the pattern "ep" followed by digits (e.g., ep1, ep20)
#             # regardless of where it is in the filename.
#             match_ep = re.search(r"ep(\d+)", filename)
            
#             if match_ep:
#                 ep_num = int(match_ep.group(1))
#             else:
#                 # If we can't find 'epX', we skip this file to avoid the KeyError
#                 print(f"⚠️ Warning: Could not find episode number in file: {filename}")
#                 continue

#             # Calculate the metric you want (Total Waiting Time)
#             # 'system_total_waiting_time' is usually accumulated, so we take the MAX or the MEAN 
#             # depending on how you want to view it. Usually MEAN is safer for general performance.
#             mean_waiting_time = df['system_total_waiting_time'].mean()
            
#             data.append({
#                 'episode': ep_num, 
#                 'waiting_time': mean_waiting_time
#             })
            
#         except Exception as e:
#             print(f"Error processing file {filename}: {e}")

#     # 3. Create DataFrame and Plot
#     if not data:
#         print("❌ No valid data extracted. Check your CSV filenames.")
#         return

#     df_plot = pd.DataFrame(data)

#     # Sort just in case
#     df_plot = df_plot.sort_values(by='episode')

#     # Group by episode to average the results across your 30 runs
#     # This is where your error happened previously. Now 'episode' definitely exists.
#     avg_results = df_plot.groupby('episode').mean().reset_index()

#     print("Generating plot...")
    
#     plt.figure(figsize=(10, 6))
#     plt.plot(avg_results['episode'], avg_results['waiting_time'], marker='o', linestyle='-', color='b')
    
#     plt.title("Average Traffic Waiting Time (Lower is Better)")
#     plt.xlabel("Episode")
#     plt.ylabel("System Total Waiting Time (Average)")
#     plt.grid(True)
    
#     # Save the plot too, just in case
#     plt.savefig(os.path.join(path, "result_graph.png"))
#     print(f"Graph saved to {os.path.join(path, 'result_graph.png')}")
    
#     plt.show()

# if __name__ == "__main__":
#     plot_results()

import argparse
import glob
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = False



sns.set(
    style="darkgrid",
    rc={
        "figure.figsize": (7.2, 4.45),
        "text.usetex": False,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
        "font.size": 15,
        "figure.autolayout": True,
        "axes.titlesize": 16,
        "axes.labelsize": 17,
        "lines.linewidth": 2,
        "lines.markersize": 6,
        "legend.fontsize": 15,
    },
)
colors = sns.color_palette("colorblind", 4)
# colors = sns.color_palette("Set1", 2)
# colors = ['#FF4500','#e31a1c','#329932', 'b', 'b', '#6a3d9a','#fb9a99']
dashes_styles = cycle(["-", "-.", "--", ":"])
sns.set_palette(colors)
colors = cycle(colors)


def moving_average(interval, window_size):
    if window_size == 1:
        return interval
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, "same")


def plot_df(df, color, xaxis, yaxis, ma=1, label=""):
    df[yaxis] = pd.to_numeric(df[yaxis], errors="coerce")  # convert NaN string to NaN value

    mean = df.groupby(xaxis).mean()[yaxis]
    std = df.groupby(xaxis).std()[yaxis]
    if ma > 1:
        mean = moving_average(mean, ma)
        std = moving_average(std, ma)

    x = df.groupby(xaxis)[xaxis].mean().keys().values
    plt.plot(x, mean, label=label, color=color, linestyle=next(dashes_styles))
    plt.fill_between(x, mean + std, mean - std, alpha=0.25, color=color, rasterized=True)

    # plt.ylim([0,200])
    # plt.xlim([40000, 70000])


if __name__ == "__main__":
    prs = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""Plot Traffic Signal Metrics"""
    )
    prs.add_argument("-f", nargs="+", required=True, help="Measures files\n")
    prs.add_argument("-l", nargs="+", default=None, help="File's legends\n")
    prs.add_argument("-t", type=str, default="", help="Plot title\n")
    prs.add_argument("-yaxis", type=str, default="system_total_waiting_time", help="The column to plot.\n")
    prs.add_argument("-xaxis", type=str, default="step", help="The x axis.\n")
    prs.add_argument("-ma", type=int, default=1, help="Moving Average Window.\n")
    prs.add_argument("-sep", type=str, default=",", help="Values separator on file.\n")
    prs.add_argument("-xlabel", type=str, default="Time step (seconds)", help="X axis label.\n")
    prs.add_argument("-ylabel", type=str, default="Total waiting time (s)", help="Y axis label.\n")
    prs.add_argument("-output", type=str, default=None, help="PDF output filename.\n")

    args = prs.parse_args()
    labels = cycle(args.l) if args.l is not None else cycle([str(i) for i in range(len(args.f))])

    plt.figure()

    # File reading and grouping
    for file in args.f:
        main_df = pd.DataFrame()
        for f in glob.glob(file + "*"):
            df = pd.read_csv(f, sep=args.sep)
            if main_df.empty:
                main_df = df
            else:
                main_df = pd.concat((main_df, df))

        # Plot DataFrame
        plot_df(main_df, xaxis=args.xaxis, yaxis=args.yaxis, label=next(labels), color=next(colors), ma=args.ma)

    plt.title(args.t)
    plt.ylabel(args.ylabel)
    plt.xlabel(args.xlabel)
    plt.ylim(bottom=0)

    if args.output is not None:
        plt.savefig(args.output + ".pdf", bbox_inches="tight")

    plt.show()     