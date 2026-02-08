"""
This script plots the figure of the Case 1: Error compensation.
"""

from mfm import *
from read_file import *

class case_1_error_compensation():
    def __init__(self, scale=50, write=False, reader=read_file(), mfm_temp=mfm()):
        self.scale = scale
        self.write = write
        self.reader = reader
        self.mfm_temp = mfm_temp


    def error_compensation_data(self):
        """Generating the error compensation data."""

        file = 'data/01013500_05_model_output.txt'
        flow_data = self.reader.read_flow(file)
        # sim = flow_data['sim'].copy()
        obs = flow_data['obs'].copy()
        obs_double = np.concatenate([obs, obs]).copy()

        categories = ['high_low', 'high_good']
        metrics = ['mfm', 'nse', 'kge', 'mkge', 'rmse', 'nrmse', 'alpha', 'beta']
        result = {
            category: {metric: np.zeros(self.scale) for metric in metrics}
            for category in categories
        }

        for j in range(self.scale):
            k = j + 1
            n = len(obs)

            sim_high_low = obs_double.copy()
            sim_high_low[:n] *= (k + 1) / k
            sim_high_low[n:] *= (k - 1) / k

            sim_high_good = obs_double.copy()
            sim_high_good[:n] *= (k + 1) / k

            result['high_low']['mfm'][j] = self.mfm_temp.model_fidelity_metric(sim=sim_high_low, obs=obs_double)['MFM']
            result_standard_metrcs = self.mfm_temp.baseline_metrics(sim=sim_high_low, obs=obs_double)
            result['high_low']['nse'][j] = result_standard_metrcs['NSE']
            result['high_low']['kge'][j] = result_standard_metrcs['KGE']
            result['high_low']['mkge'][j] = result_standard_metrcs['mKGE']
            result['high_low']['rmse'][j] = result_standard_metrcs['RMSE']
            result['high_low']['nrmse'][j] = result_standard_metrcs['NRMSE']
            result['high_low']['alpha'][j] = result_standard_metrcs['alpha']
            result['high_low']['beta'][j] = result_standard_metrcs['beta']

            result['high_good']['mfm'][j] = self.mfm_temp.model_fidelity_metric(sim=sim_high_good, obs=obs_double)['MFM']
            result_standard_metrcs = self.mfm_temp.baseline_metrics(sim=sim_high_good, obs=obs_double)
            result['high_good']['nse'][j] = result_standard_metrcs['NSE']
            result['high_good']['kge'][j] = result_standard_metrcs['KGE']
            result['high_good']['mkge'][j] = result_standard_metrcs['mKGE']
            result['high_good']['rmse'][j] = result_standard_metrcs['RMSE']
            result['high_good']['nrmse'][j] = result_standard_metrcs['NRMSE']
            result['high_good']['alpha'][j] = result_standard_metrcs['alpha']
            result['high_good']['beta'][j] = result_standard_metrcs['beta']

        return result

    def plot_sensitivity(self):
        """Plot error compensation sensitivity curve."""

        result_temp = case_1_error_compensation()
        result = result_temp.error_compensation_data()

        mfm_diff = result['high_good']['mfm'] - result['high_low']['mfm']
        nse_diff = result['high_good']['nse'] - result['high_low']['nse']
        kge_diff = result['high_good']['kge'] - result['high_low']['kge']
        mkge_diff = result['high_good']['mkge'] - result['high_low']['mkge']
        plt.figure(figsize=(8, 4))
        x = np.arange(1, self.scale + 1)
        # x_array = np.arange(1, scale + 1, 9)
        plt.plot(x, mfm_diff, color="#4477AA", label='MFM', lw=3)
        plt.plot(x, nse_diff, color="#EE6677", label='NSE', lw=2, alpha=0.8)
        plt.plot(x, kge_diff, color="#228833", label='KGE', lw=3, linestyle='--', alpha=0.8)
        plt.plot(x, mkge_diff, color="#CCBB44", label='mKGE', lw=3, linestyle=':', alpha=0.8)
        plt.xlabel('Scaling parameter', fontname='Times New Roman', fontsize=18)
        plt.ylabel('BG score - BB score', fontname='Times New Roman', fontsize=18)
        plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        plt.axvline(x=1, color='gray', linestyle='--', alpha=0.5)

        # plt.grid(True)
        plt.legend(frameon=False, ncol=2, prop={'family': 'Times New Roman', 'size': 18})
        plt.xticks(fontname='Times New Roman', fontsize=18)
        plt.yticks(fontname='Times New Roman', fontsize=18)
        plt.tight_layout()
        
        # Save figure
        if self.write:
            print('\033[1;31mSaving case_1_sensitivity...\033[0m')
            plt.savefig("temp/case_1_sensitivity.png", bbox_inches='tight', dpi=300)
            plt.savefig("temp/case_1_sensitivity.pdf", bbox_inches='tight', dpi=300)
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')
        plt.show()

        return 0

    def plot_error_compensation(self):
        """Plot error compensation figure."""

        result_temp = case_1_error_compensation()
        result = result_temp.error_compensation_data()

        metrics = ['MFM', 'NSE', 'KGE', 'mKGE', 'RMSE', 'NRMSE', 'alpha', 'beta']
        metrics_left = metrics[0:4]
        metrics_right = metrics[4:8]

        bb_scores = np.array(
            [result['high_low']['mfm'][3], result['high_low']['nse'][3], result['high_low']['kge'][3],
             result['high_low']['mkge'][3], result['high_low']['rmse'][3], result['high_low']['nrmse'][3],
             result['high_low']['alpha'][3], result['high_low']['beta'][3]])
        print(f"\033[1;31mbb_scores = {bb_scores}\033[0m")
        bg_scores = np.array(
            [result['high_good']['mfm'][3], result['high_good']['nse'][3], result['high_good']['kge'][3],
             result['high_good']['mkge'][3], result['high_good']['rmse'][3], result['high_good']['nrmse'][3],
             result['high_good']['alpha'][3], result['high_good']['beta'][3]])
        print(f"\033[1;31mbg_scores = {bg_scores}\033[0m")

        bb_left = bb_scores[0:4]
        bb_right = bb_scores[4:8]

        bg_left = bg_scores[0:4]
        bg_right = bg_scores[4:8]

        # Generating figure
        fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(8, 3.5), sharey=False)

        # Plot left subplot
        y_pos_left = np.arange(len(metrics_left))[::-1]

        # Draw connecting lines
        for i in range(len(metrics_left)):
            ax_left.plot([bg_left[i], bb_left[i]], [y_pos_left[i], y_pos_left[i]], 'k-', linewidth=1)

        # Draw BG model (white, hollow circle)
        ax_left.scatter(bg_left, y_pos_left, color='black', s=80, edgecolors='black',
                        facecolors='white', zorder=5, label='BG model')
        # Draw BB model (black, solid circle)
        ax_left.scatter(bb_left, y_pos_left, color='black', s=80, zorder=5, label='BB model')


        ax_left.set_yticks(y_pos_left)
        ax_left.set_yticklabels(metrics_left, fontname='Times New Roman', fontsize=14)
        ax_left.set_xlim(0.8, 1.02)
        ax_left.set_title(r'$\bf{(a)}$ Goodness-of-fit', loc='left', fontname='Times New Roman', fontsize=14)

        # Add ideal value line at 1.0
        ax_left.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        ax_left.axvline(x=1, color='gray', linestyle='--', alpha=0.5)

        # Add legend to the left plot
        ax_left.legend(loc='lower left', frameon=False, prop={'family': 'Times New Roman', 'size': 14},
                       bbox_to_anchor=(-0.1, -0.3), ncol=2)

        # Plot right subplot
        y_pos_right = np.arange(len(metrics_right))[::-1]

        # Draw connecting lines
        for i in range(len(metrics_right)):
            ax_right.plot([bg_right[i], bb_right[i]], [y_pos_right[i], y_pos_right[i]], 'k-', linewidth=1)

        # Draw BG model (white, hollow circle)
        ax_right.scatter(bg_right, y_pos_right, color='black', s=80, edgecolors='black',
                         facecolors='white', zorder=5, label='BG model')
        # Draw BB model (black, solid circle)
        ax_right.scatter(bb_right, y_pos_right, color='black', s=80, zorder=5, label='BB model')

        ax_right.set_yticks(y_pos_right)
        ax_right.set_yticklabels(metrics_right, fontname='Times New Roman', fontsize=14)
        ax_right.set_xlim(0.2, 1.2)
        ax_right.set_title(r'$\bf{(b)}$ Error and components', loc='left', fontname='Times New Roman', fontsize=14)

        # Add ideal value lines (0.0 for RMSE/NRMSE, 1.0 for alpha/beta)
        ax_right.axvline(x=0.0, color='gray', linestyle='--', alpha=0.5)
        ax_right.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5)

        for tick in ax_left.get_xticklabels():
            tick.set_fontname('Times New Roman')
            tick.set_fontsize(14)

        for tick in ax_right.get_xticklabels():
            tick.set_fontname('Times New Roman')
            tick.set_fontsize(14)

        plt.tight_layout()

        # Save figure
        if self.write:
            print('\033[1;31mSaving case_1_error_compensation...\033[0m')
            plt.savefig("temp/case_1_error_compensation.png", dpi=300, bbox_inches='tight')
            plt.savefig("temp/case_1_error_compensation.pdf", dpi=300, bbox_inches='tight')
            print('\033[1;31mDone\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')
        plt.show()
        
        return 0


# case_1_test = case_1_error_compensation()
# case_1_test.plot_sensitivity()
# case_1_test.plot_error_compensation()