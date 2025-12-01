"""
This script represents how phase affects the standard metrics.
"""

from mfm import *
from read_file import *
from matplotlib.patches import ConnectionPatch

class case_3_phase_error():
    def __init__(self, scale=50, write=False, mfm_temp = mfm()):
        self.scale = scale
        self.write = write
        self.mfm_temp = mfm_temp

    def geometry(self):
        """Plot the phase-corrected error."""
        
        PI = np.pi
        PHASE_SHIFT = PI / 4

        def y_black(x):
            return np.sin(x)

        def y_blue(x):
            return np.sin(x - PHASE_SHIFT) + 1.0

        x = np.linspace(0, 2 * PI, 500)
        y_obs = y_black(x)
        y_sim = y_blue(x)

        fig, ax = plt.subplots(figsize=(8, 3.5))

        ax.plot(x, y_obs, color='#4477AA', lw=3, label='Observation')
        ax.plot(x, y_sim, color='#EE6677', lw=3, label='Simulation')

        annotation_points_x = [PI / 2, PI * 3/2]

        for x_val in annotation_points_x:
            p_black = (x_val, y_black(x_val))
            p_blue_vertical = (x_val, y_blue(x_val))

            x_shifted = x_val + PHASE_SHIFT
            p_blue_shifted = (x_shifted, y_blue(x_shifted))

            p_triangle_corner = (x_shifted, y_black(x_val))

            ax.plot(p_black[0], p_black[1], color='black', marker='o', markersize=6)
            ax.plot(p_blue_vertical[0], p_blue_vertical[1], color='black', marker='o', markersize=6)
            ax.plot(p_blue_shifted[0], p_blue_shifted[1], color='black', marker='o', markersize=6)

            ax.plot([p_black[0], p_blue_vertical[0]],
                    [p_black[1], p_blue_vertical[1]],
                    color="#AA3377", linestyle='--', lw=1.5)

            ax.plot([p_black[0], p_blue_shifted[0]],
                    [p_black[1], p_blue_shifted[1]],
                    color="#AA3377", linestyle='--', lw=1.5)

            ax.plot([p_black[0], p_triangle_corner[0]],
                    [p_black[1], p_triangle_corner[1]],
                    color="#AA3377", linestyle='--', lw=1)
            ax.plot([p_triangle_corner[0], p_blue_shifted[0]],
                    [p_triangle_corner[1], p_blue_shifted[1]],
                    color="#AA3377", linestyle='--', lw=1)

            ax.text(p_black[0], p_black[1] + 0.05, r'$\theta$',
                    color='#000000', fontsize=16, ha='left', va='bottom')

            x_brace_d1 = p_black[0] - 0.15
            con_d1 = ConnectionPatch(xyA=(x_brace_d1, p_black[1]),
                                     xyB=(x_brace_d1, p_blue_vertical[1]),
                                     coordsA='data', coordsB='data',
                                     arrowstyle=f'|-|', lw=1.5, color='#000000', zorder=10)
            ax.add_patch(con_d1)
            ax.text(x_brace_d1 - 0.08, (p_black[1] + p_blue_vertical[1]) / 2, '$d_1$',
                    color='#000000', fontsize=16, ha='right', va='center')

            x_brace_d2 = p_triangle_corner[0] + 0.15
            con_d2 = ConnectionPatch(xyA=(x_brace_d2, p_triangle_corner[1]),
                                     xyB=(x_brace_d2, p_blue_shifted[1]),
                                     coordsA='data', coordsB='data',
                                     arrowstyle=f'|-|', lw=1.5, color='#000000', zorder=10)
            ax.add_patch(con_d2)
            ax.text(x_brace_d2 + 0.08, (p_triangle_corner[1] + p_blue_shifted[1]) / 2, '$d_2$',
                    color='#000000', fontsize=16, ha='left', va='center')

        ax.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax.set_ylabel('Value', fontname='Times New Roman', fontsize=18)
        ax.legend(prop={'family': 'Times New Roman', 'size': 18}, frameon=False, loc='upper left', bbox_to_anchor=(0.1, 0.35))

        ax.set_xticks([0, PI / 2, PI, 3 * PI / 2, 2 * PI])
        ax.set_xticklabels(['0', 'pi/2', 'pi', '3pi/2', '2pi'], fontname='Times New Roman', fontsize=18)
        plt.yticks(fontname='Times New Roman', fontsize=18)
        
        ax.set_ylim(-1.5, 2.5)
        ax.set_xlim(0, 2 * PI)

        # ax.grid(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()

        # Save figure
        if self.write:
            print('\033[1;31mSaving case_3_geometry...\033[0m')
            plt.savefig("temp/case_3_geometry.png", dpi=300, bbox_inches='tight')
            plt.savefig("temp/case_3_geometry.pdf", dpi=300, bbox_inches='tight')
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')

        plt.show()

    def decoupling(self):
        """Decouple phase and error"""
        
        t = np.arange(0, 100)
        t_pi = t * np.pi
        cost = np.cos(t_pi)
        # print('t\t', t)

        # Synthetic data with an extreme event
        obs_extreme = np.abs(cost) * 1
        sim_extreme = np.abs(cost) * 1
        obs_extreme[len(t) - 1] = 2
        sim_extreme[len(t) - 1] = 12

        t_pi = t * np.pi
        cost = np.cos(t_pi)
        # print('cost\t', cost)
        # print('len(cost)\t', len(cost))

        # Synthetic anti-phase data
        obs_anti_phase = cost / 2 + 1
        sim_anti_phase = - cost / 2 + 1

        # Synthetic data with large error
        obs_failure = cost * 0.01 + 1
        sim_failure = cost * 0.01 + 2

        print('\033[1;31mExtreme event case:\033[0m')
        print(self.mfm_temp.model_fidelity_metric(sim_extreme, obs_extreme))
        print("========================")
        print(self.mfm_temp.standard_metrics(sim_extreme, obs_extreme))

        print('\033[1;31mAnti-phase case:\033[0m')
        print(self.mfm_temp.model_fidelity_metric(sim_anti_phase, obs_anti_phase))
        print("========================")
        print(self.mfm_temp.standard_metrics(sim_anti_phase, obs_anti_phase))

        print('\033[1;31mFailure case:\033[0m')
        print(self.mfm_temp.model_fidelity_metric(sim_failure, obs_failure))
        print("========================")
        print(self.mfm_temp.standard_metrics(sim_failure, obs_failure))

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))
        ax1.plot(sim_extreme, color='#4477AA', alpha=0.8, label="Simulation", lw=1.5, zorder=2)
        ax1.plot(obs_extreme, color="#EE6677", alpha=0.8, label="Observation", lw=1.5, zorder=1)
        ax1.set_title(r'$\bf{(a)}$ Extreme event', fontname='Times New Roman', fontsize=18)
        ax1.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax1.set_ylabel('Value', fontname='Times New Roman', fontsize=18)
        ax1.legend(prop={'family': 'Times New Roman', 'size': 18}, frameon=False)

        ax2.plot(sim_anti_phase, color='#4477AA', alpha=0.8, label="Simulation", lw=1.5, zorder=2)
        ax2.plot(obs_anti_phase, color="#EE6677", alpha=0.8, label="Observation", lw=1.5, zorder=1)
        ax2.set_title(r'$\bf{(b)}$ Anti-phase', fontname='Times New Roman', fontsize=18)
        ax2.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax2.set_ylabel('Value', fontname='Times New Roman', fontsize=18)
        # ax2.legend()

        ax3.plot(sim_failure, color='#4477AA', alpha=0.8, label="Simulation", lw=1.5, zorder=2)
        ax3.plot(obs_failure, color="#EE6677", alpha=0.8, label="Observation", lw=1.5, zorder=1)
        ax3.set_title(r'$\bf{(c)}$ Failure', fontname='Times New Roman', fontsize=18)
        ax3.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax3.set_ylabel('Value', fontname='Times New Roman', fontsize=18)
        # ax3.legend()
        for ax in [ax1, ax2, ax3]:
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_fontname('Times New Roman')
                tick.set_fontsize(16)

        plt.tight_layout()
        
        # Save figure
        if self.write:
            print('\033[1;31mSaving case_3_decoupling...\033[0m')
            plt.savefig("temp/case_3_decoupling.png", dpi=300, bbox_inches='tight')  # 保存为高分辨率png
            plt.savefig("temp/case_3_decoupling.pdf", dpi=300, bbox_inches='tight')  # 保存为高分辨率png
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')
        plt.show()

        return 0

    def sensitivity(self):
        """Plot phase sensitivity figure."""

        metrics = ['mfm', 'nse', 'kge', 'mkge', 'rmse', 'nrmse']
        result = {metric: np.zeros(self.scale) for metric in metrics}

        for i in range(self.scale):
            t = np.arange(0, 100)
            t_pi = t * np.pi
            cost = np.cos(t_pi)
            
            obs_sensitivity = cost / (i + 1) + 1
            sim_sensitivity = - cost / (i + 1) + 1

            result['mfm'][i] = self.mfm_temp.model_fidelity_metric(sim_sensitivity, obs_sensitivity)['MFM']
            std_m = self.mfm_temp.standard_metrics(sim_sensitivity, obs_sensitivity)
            result['nse'][i] = std_m['NSE']
            result['kge'][i] = std_m['KGE']
            result['mkge'][i] = std_m['mKGE']
            result['rmse'][i] = std_m['RMSE']
            result['nrmse'][i] = std_m['NRMSE']

        plt.figure(figsize=(8, 3.5))
        plt.plot()
        x = np.arange(1, self.scale + 1)
        plt.plot(x, result['mfm'], color="#4477AA", label='MFM', lw=3)

        plt.plot(x, result['nse'], color="#EE6677", label='NSE', alpha=0.8, lw=2)
        plt.plot(x, result['kge'], color="#228833", label='KGE', alpha=0.8, linestyle='--', lw=3)
        plt.plot(x, result['mkge'], color="#CCBB44", label='mKGE', alpha=0.8, linestyle=':', lw=3)
        plt.plot(x, result['rmse'], color="#66CCEE", label='RMSE', alpha=0.8, linestyle='--', lw=3)
        plt.plot(x, result['nrmse'], color="#AA3377", label='NRMSE', alpha=0.8, linestyle=':', lw=3)
        plt.xlabel('Scaling parameter', fontname='Times New Roman', fontsize=18)
        plt.ylabel('Score', fontname='Times New Roman', fontsize=18)
        plt.axhline(0, color='grey', linestyle='--', alpha=0.5)
        plt.axhline(1, color='grey', linestyle='--', alpha=0.5)
        plt.axvline(1, color='grey', linestyle='--', alpha=0.5)
        plt.legend(prop={'family': 'Times New Roman', 'size': 18}, frameon=False, ncol=3)
        plt.xticks(fontname="Times New Roman", fontsize=16)
        plt.yticks(fontname="Times New Roman", fontsize=16)
        plt.tight_layout()
        
        # Save figure
        if self.write:
            print('\033[1;31mSaving case_3_sensitivity...\033[0m')
            plt.savefig("temp/case_3_sensitivity.png", bbox_inches='tight', dpi=300)
            plt.savefig("temp/case_3_sensitivity.pdf", bbox_inches='tight', dpi=300)
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')
        plt.show()
        
        return 0


# case_3_test = case_3_phase_error()
# case_3_test.geometry()
# case_3_test.decoupling()
# case_3_test.sensitivity()