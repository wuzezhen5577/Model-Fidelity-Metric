"""
This script plot the hyperparameter sensitivity of MFM
"""

from mfm import *
from read_file import *

class case_5_sensitivity():
    def __init__(self, write=False):
        self.write = write

    def sensitivity(self):
        """Plot the sensitivity of MFM"""

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(8, 8))

        # Sensitivity of p
        result_p_test = []
        with open('data/case_5_sensitivity_p.txt', 'r') as f:
            for line in f:
                line = np.array(line.strip().split('\t'), dtype=float)
                result_p_test.append(line)
        result_p_test = np.array(result_p_test)

        boxprops = dict(facecolor="#f7e79c", color='black')
        medianprops = dict(color="black", linewidth=2)
        ax1.boxplot(result_p_test, patch_artist=True, boxprops=boxprops, medianprops=medianprops)

        ax1.set_ylabel('MFM', fontname='Times New Roman', fontsize=18)
        ax1.set_xlabel(r'$\bf{(a)}$ $p$', fontname='Times New Roman', fontsize=18)

        x_ticks = np.arange(1, len(result_p_test.T) + 1)
        x_labels = [f'{i / 10 + 0.9:.1f}' for i in x_ticks]
        ax1.set_xticks(x_ticks, x_labels, fontname='Times New Roman', fontsize=18)
        ax1.grid(False)

        # Sensitivity of bins_suse
        result_bins_suse_test = []
        with open('data/case_5_sensitivity_bins_suse.txt', 'r') as f:
            for line in f:
                line = np.array(line.strip().split('\t'), dtype=float)
                result_bins_suse_test.append(line)
        result_bins_suse_test = np.array(result_bins_suse_test)

        boxprops = dict(facecolor="#f1b27a", color='black')
        medianprops = dict(color="black", linewidth=2)
        ax2.boxplot(result_bins_suse_test, patch_artist=True, boxprops=boxprops, medianprops=medianprops)

        ax2.set_ylabel('MFM', fontname='Times New Roman', fontsize=18)
        ax2.set_xlabel(r'$\bf{(b)}$ $n_{\text{SUSE}}$', fontname='Times New Roman', fontsize=18)

        x_ticks = np.arange(1, len(result_bins_suse_test.T) + 1)
        x_labels = [f'{i * 5:.0f}' for i in x_ticks]
        ax2.set_xticks(x_ticks, x_labels, fontname='Times New Roman', fontsize=18)
        ax2.grid(False)

        # Sensitivity of bins_phi
        result_bins_phi_test = []
        with open('data/case_5_sensitivity_bins_phi.txt', 'r') as f:
            for line in f:
                line = np.array(line.strip().split('\t'), dtype=float)
                result_bins_phi_test.append(line)
        result_bins_phi_test = np.array(result_bins_phi_test)

        boxprops = dict(facecolor="#7ea6c5", color='black')
        medianprops = dict(color="black", linewidth=2)
        ax3.boxplot(result_bins_phi_test, patch_artist=True, boxprops=boxprops, medianprops=medianprops)

        ax3.set_ylabel('MFM', fontname='Times New Roman', fontsize=18)
        ax3.set_xlabel(r'$\bf{(c)}$ $n_{\text{PHI}}$', fontname='Times New Roman', fontsize=18)

        x_ticks = np.arange(1, len(result_bins_suse_test.T) + 1)
        x_labels = [f'{i * 5:.0f}' for i in x_ticks]
        ax3.set_xticks(x_ticks, x_labels, fontname='Times New Roman', fontsize=18)
        ax3.grid(False)

        # Sensitivity of c
        result_c_test = []
        with open('data/case_5_sensitivity_c.txt', 'r') as f:
            for line in f:
                line = np.array(line.strip().split('\t'), dtype=float)
                result_c_test.append(line)
        result_c_test = np.array(result_c_test)

        boxprops = dict(facecolor="#c9d9b7", color='black')
        medianprops = dict(color="black", linewidth=2)
        ax4.boxplot(result_c_test, patch_artist=True, boxprops=boxprops, medianprops=medianprops)

        ax4.set_ylabel('MFM', fontname='Times New Roman', fontsize=18)
        ax4.set_xlabel(r'$\bf{(d)}$ $c$', fontname='Times New Roman', fontsize=18)

        x_ticks = np.arange(1, len(result_c_test.T) + 1)
        x_labels = [f'{i + 1:.1f}' for i in x_ticks]
        ax4.set_xticks(x_ticks, x_labels, fontname='Times New Roman', fontsize=18)
        ax4.grid(False)

        for ax in [ax1, ax2, ax3, ax4]:
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_fontname('Times New Roman')
                tick.set_fontsize(18)

        plt.tight_layout()

        # Save figure
        if self.write:
            print('\033[1;31mSaving case_5_sensitivity...\033[0m')
            fig.savefig("temp/case_5_sensitivity.png", dpi=300, bbox_inches='tight')
            fig.savefig("temp/case_5_sensitivity.pdf", dpi=300, bbox_inches='tight')
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')
        plt.show()

        return 0

# case_5_test = case_5_sensitivity()
# case_5_test.sensitivity()