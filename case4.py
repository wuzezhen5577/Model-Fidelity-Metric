from mfm import *
from read_file import *

class case_4_real_world_data():
    def __init__(self, write=False, reader=read_file(), mfm_temp=mfm()):
        self.write = write
        self.reader = reader
        self.mfm_temp = mfm_temp

    def two_examples(self):
        flow_near_constant = self.reader.read_flow('data/05120500_05_model_output.txt')
        flow_phase = self.reader.read_flow('data/06409000_05_model_output.txt')
        fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(8, 4.5))
        ax1.plot(flow_near_constant['sim'], color='#4477AA', alpha=0.8, linestyle='--', label='Simulation', lw=1.5,
                 zorder=2)
        ax1.plot(flow_near_constant['obs'], color='#EE6677', alpha=0.8, label='Observation', lw=1.5, zorder=1)
        ax1.legend(prop={'family': 'Times New Roman', 'size': 18}, frameon=False)
        ax1.set_title(r'$\bf{(a)}$ 05120500', fontname='Times New Roman', fontsize=18)
        ax1.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax1.set_ylabel('Value', fontname='Times New Roman', fontsize=18)

        ax2.plot(flow_phase['sim'], color='#4477AA', alpha=0.8, linestyle='--', label='Simulation', lw=1.5, zorder=2)
        ax2.plot(flow_phase['obs'], color='#EE6677', alpha=0.8, label='Observation', lw=1.5, zorder=1)
        ax2.set_title(r'$\bf{(b)}$ 06409000', fontname='Times New Roman', fontsize=18)
        ax2.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax2.set_ylabel('Value', fontname='Times New Roman', fontsize=18)

        for ax in [ax1, ax2]:
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_fontname('Times New Roman')
                tick.set_fontsize(16)
        plt.tight_layout()

        if self.write:
            print('\033[1;31mSaving case4_flow...\033[0m')
            plt.savefig('temp/case4_flow.png', dpi=300, bbox_inches='tight')
            plt.savefig('temp/case4_flow.pdf', dpi=300, bbox_inches='tight')
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')

        plt.show()

        return 0

    def radar(self):
        flow_05120500 = self.reader.read_flow('data/05120500_05_model_output.txt')
        mfm_05120500 = self.mfm_temp.model_fidelity_metric(flow_05120500['sim'], flow_05120500['obs'])
        print('mfm_05120500\t', mfm_05120500)

        flow_06409000 = self.reader.read_flow('data/06409000_05_model_output.txt')
        mfm_06409000 = self.mfm_temp.model_fidelity_metric(flow_06409000['sim'], flow_06409000['obs'])
        print('mfm_06409000\t', mfm_06409000)


        # 1. 定义指标名称和数据
        labels = ['MFM', 'exp(- NMAEp)', 'PPF', r'$\omega$', r'$\varphi$', r'$\eta$']
        sample_05120500 = [mfm_05120500['MFM'], mfm_05120500['exp(- NMAEp)'], mfm_05120500['PPF'], mfm_05120500['omega'],
                           mfm_05120500['varphi'], mfm_05120500['eta']]
        sample_06409000 = [mfm_06409000['MFM'], mfm_06409000['exp(- NMAEp)'], mfm_06409000['PPF'], mfm_06409000['omega'],
                           mfm_06409000['varphi'], mfm_06409000['eta']]

        # 2. 计算角度（每个轴的角度）
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        sample_05120500 += sample_05120500[:1]  # 闭合图形
        sample_06409000 += sample_06409000[:1]
        angles += angles[:1]

        # 3. 绘图
        fig, ax = plt.subplots(figsize=(8, 5), subplot_kw=dict(polar=True))
        ax.plot(angles, sample_05120500, 'o-', label='Site 05120500', color="#3F4A8A", )
        ax.plot(angles, sample_06409000, 'o-', label='Site 06409000', color="#DE2D26")
        ax.fill(angles, sample_05120500, color="#3F4A8A", alpha=0.25)
        ax.fill(angles, sample_06409000, color="#DE2D26", alpha=0.25)

        # 4. 设置标签
        ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=18, fontname="Times New Roman")
        ax.set_ylim(0, 1.1)  # 根据你的数据范围调整
        ax.legend(loc='upper right', bbox_to_anchor=(1.45, 0.2), frameon=False,
                  prop={'family': 'Times New Roman', 'size': 18})
        # ax.tick_params(labelsize=16)
        yticks = [0.2, 0.4, 0.6, 0.8, 1.0]
        ax.set_yticks(yticks)
        ax.set_yticklabels([f"{y:.1f}" for y in yticks],
                           fontsize=18, fontname="Times New Roman")
        plt.tight_layout()

        if self.write:
            print('\033[1;31mSaving case_4_radar...\033[0m')
            plt.savefig("temp/case_4_radar.png", dpi=300, bbox_inches='tight')
            plt.savefig("temp/case_4_radar.pdf", dpi=300, bbox_inches='tight')
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')

        plt.show()

        return 0

    def spatial_distribution(self):
        import matplotlib.colors as mcolors
        import matplotlib.gridspec as gridspec  # Import gridspec
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        # --- Set global font to Times New Roman ---
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = 'Times New Roman'
        plt.rcParams['font.sans-serif'] = 'Times New Roman'
        plt.rcParams['mathtext.fontset'] = 'stix'  # A good companion for Times

        # --- 1. Define and Register the Custom Colormap ---

        # The 'batlow' hex codes you provided
        batlow_colors = [
            "#051a33",  # dark blue
            "#3b5d7c",  # medium blue
            "#7ea6c5",  # light blue
            "#c9d9b7",  # pale green
            "#f7e79c",  # yellow
            "#f1b27a",  # orange
            "#d96d5e",  # red
            "#ac2e4b",  # dark red
        ]

        # Create a matplotlib colormap object from the list of colors
        batlow_cmap = mcolors.LinearSegmentedColormap.from_list("batlow", batlow_colors)

        # --- 2. Load and Prepare Data ---

        # Define file paths
        # GOF_FILE = 'temp/case4_mfm_restrict_365.txt'
        # ERROR_FILE = 'temp/case4_error.txt'

        # Load the data from both files
        df_gof = self.reader.read_result('data/case_4_mfm.txt')
        # df_err = read_result(ERROR_FILE)

        # Combine the relevant columns into one DataFrame
        df_all = df_gof[['lat', 'lon', 'GOF_stat', 'score']]

        # Set the desired order as requested by the user
        gof_stats = ['MFM', 'KGE', 'RMSE', 'NSE', 'mKGE', 'NRMSE']

        # Get the min/max score across *all* stats for a consistent color scale
        # We will clip all values to the [0, 1] range as requested
        vmin = 0
        vmax = 1

        # --- 3. Create the Plots ---

        # Define a map projection for the US
        map_projection = ccrs.LambertConformal(central_longitude=-96.0, central_latitude=39.0)

        # Define the projection of our data (standard lat/lon)
        data_projection = ccrs.PlateCarree()

        # Create a 2x3 grid of subplots, specifying the projection
        fig = plt.figure(figsize=(8, 5.5))  # Made figure wider for the 3rd column

        # Create a 4-row, 3-col grid.
        # Rows 0,1 are for maps. Row 2 for colorbar. Row 3 for histogram.
        gs = gridspec.GridSpec(4, 3, figure=fig,
                               height_ratios=[5, 5, 0.5, 4],  # Gave a bit more room for cbar title
                               hspace=0.45, wspace=0)  # hspace adjusts vertical space, wspace adjusts horizontal

        # Create the 6 map axes
        ax1 = fig.add_subplot(gs[0, 0], projection=map_projection)
        ax2 = fig.add_subplot(gs[0, 1], projection=map_projection)
        ax3 = fig.add_subplot(gs[0, 2], projection=map_projection)
        ax4 = fig.add_subplot(gs[1, 0], projection=map_projection)
        ax5 = fig.add_subplot(gs[1, 1], projection=map_projection)
        ax6 = fig.add_subplot(gs[1, 2], projection=map_projection)
        map_axes = [ax1, ax2, ax3, ax4, ax5, ax6]

        # Create the colorbar axis (spans all columns, in row 2)
        cbar_ax = fig.add_subplot(gs[2, :])
        cbar_ax.set_position([0.125, 0.37, 0.775, 0.03])

        # Create the histogram axis (spans all columns, in row 3)
        hist_ax = fig.add_subplot(gs[3, :])

        # We need to save the last scatter plot for the colorbar
        sc = None

        numbering = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

        # Loop through each statistic and its corresponding subplot axis
        for i, (ax, stat) in enumerate(zip(map_axes, gof_stats)):
            # Filter the DataFrame for the current statistic
            df_stat = df_all[df_all['GOF_stat'] == stat]

            # Add map features like coastlines and state borders
            ax.add_feature(cfeature.COASTLINE, lw=1, zorder=2)
            ax.add_feature(cfeature.BORDERS, linestyle='-', lw=0.8, zorder=2)
            ax.add_feature(cfeature.STATES, linestyle='--', alpha=0.3, lw=0.5, zorder=1)

            # Set the map's boundaries (extent) to focus on the US
            ax.set_extent([-125, -66.5, 24, 50], crs=data_projection)

            # Create the scatter plot
            sc = ax.scatter(
                df_stat['lon'],
                df_stat['lat'],
                c=df_stat['score'],
                cmap=batlow_cmap,  # Use the colormap object directly
                vmin=vmin,
                vmax=vmax,
                transform=data_projection,
                s=12.5,  # size of markers
                edgecolor='black',
                linewidth=0.2,
                zorder=3  # Plot points on top of map features
            )

            # Set the title for each subplot
            ax.set_title(rf"$\bf{(numbering[i])}$ {stat}", fontname='Times New Roman', fontsize=16)

        # --- 4. Add a Single, Shared Colorbar ---

        # Create the colorbar using the 'sc' scatter plot object as a reference
        cbar = fig.colorbar(sc, cax=cbar_ax, orientation='horizontal')

        # Set the title *above* the colorbar
        # cbar.ax.set_title('Score Value', fontsize=16, fontname='Times New Roman', pad=5)

        cbar.ax.tick_params(labelsize=16)
        for label in cbar.ax.get_xticklabels():
            label.set_fontname('Times New Roman')

        # --- 5. Add Distribution Histogram ---

        # Define colors and alphas as requested
        colors = {
            "MFM": "#4477AA",
            "NSE": "#EE6677",
            "KGE": "#228833",
            "mKGE": "#CCBB44",
            "RMSE": "#66CCEE",  # New color for RMSE
            "NRMSE": "#AA3377"  # New color for NRMSE
        }
        alphas = {
            "MFM": 1.0,
            "NSE": 0.5,
            "KGE": 0.5,
            "mKGE": 0.6,
            "RMSE": 0.7,
            "NRMSE": 0.8
        }

        # Define the requested stacking order (higher zorder is on top)
        zorders = {
            "MFM": 1,
            "NSE": 2,
            "mKGE": 3,
            "KGE": 4,
            "RMSE": 5,
            "NRMSE": 6
        }

        # Define common bins for the histogram
        bins = np.linspace(0, 1, 25)  # Use the same 0-1 range as the map

        # Plot a histogram for each statistic
        for stat in gof_stats:
            scores = df_all[df_all['GOF_stat'] == stat]['score']
            print(stat)
            print(np.min(scores), np.max(scores))
            # Use clip to keep data within the 0-1 plotting range
            # This will stack all RMSE values > 1 into the last bin
            hist_ax.hist(scores.clip(0, 1),
                         bins=bins,
                         color=colors[stat],
                         alpha=alphas[stat],
                         label=stat,
                         histtype='stepfilled',  # Fills the histograms
                         edgecolor='black',
                         linewidth=0.5,
                         zorder=zorders.get(stat, 1)  # Get zorder, default to 1
                         )

        hist_ax.set_title(r'$\bf{(g)}$', fontname='Times New Roman', fontsize=16)
        hist_ax.set_xlabel('Score', fontname='Times New Roman', fontsize=16)
        hist_ax.set_ylabel('Number of sites', fontname='Times New Roman', fontsize=16)
        hist_ax.legend(loc='upper center',
                       prop={'family': 'Times New Roman', 'size': 14},
                       frameon=False,
                       ncol=3,  # Changed to 3 columns for 6 items
                       bbox_to_anchor=(0.4, 1.05))  # Move legend above plot to avoid overlap

        hist_ax.set_xlim(0, 1)  # Set x-axis limit to match map range

        # Set font for ticks
        for label in hist_ax.get_xticklabels() + hist_ax.get_yticklabels():
            label.set_fontname('Times New Roman')
            label.set_fontsize(16)

        # --- 6. Save and Show the Figure ---

        # plt.tight_layout()

        if self.write:
            print('\033[1;31mSaving case_4_spatial_distribution...\033[0m')
            plt.savefig('temp/case_4_spatial_distribution.png', dpi=300, bbox_inches='tight')
            plt.savefig('temp/case_4_spatial_distribution.pdf', dpi=300, bbox_inches='tight')
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')

        plt.show()

        return 0


case_4_test = case_4_real_world_data()
case_4_test.two_examples()
case_4_test.radar()
case_4_test.spatial_distribution()