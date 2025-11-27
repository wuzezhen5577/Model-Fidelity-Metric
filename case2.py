from mfm import *
from read_file import *

class case_2_low_variability():
    def __init__(self, scale=51, write=False, mfm_temp=mfm()):
        self.scale = scale
        self.write = write
        self.mfm_temp = mfm_temp

    def low_variability(self):
        t = np.arange(0, 100)
        # print('t\t', t)
        t_pi = t * np.pi
        cost = np.cos(t_pi)
        # mfm_temp = mfm()

        # 0 号实验：KGE、NSE 在恒定或低流量下不可靠
        obs_anti_phase = np.abs(cost) * 1
        sim_anti_phase = np.abs(cost) * 1
        obs_anti_phase[len(t) - 1] = 0.99
        sim_anti_phase[len(t) - 1] = 1.01

        # 1 号实验：KGE、NSE 在恒定或低流量下不可靠-RMSE、NRMSE 相等
        obs_in_phase = np.abs(cost) * 1
        sim_in_phase = np.abs(cost) * 1
        # RMSE 不变参数
        obs_in_phase[len(t) - 1] = 1.03
        sim_in_phase[len(t) - 1] = 1.01

        # print(sim_t2)
        print('\033[1;31mAnti-phase case:\033[0m')
        print('MFM with phase penalty:')
        print(self.mfm_temp.model_fidelity_metric(sim_anti_phase, obs_anti_phase, phase=True))
        print("========================")
        print('MFM without phase penalty:')
        print(self.mfm_temp.model_fidelity_metric(sim_anti_phase, obs_anti_phase, phase=False))
        print("========================")
        std_m = self.mfm_temp.standard_metrics(sim_anti_phase, obs_anti_phase, plot=False)
        print(std_m)

        print('\033[1;31mIn-phase case:\033[0m')
        print(self.mfm_temp.model_fidelity_metric(sim_in_phase, obs_in_phase))
        print("========================")
        std_m = self.mfm_temp.standard_metrics(sim_in_phase, obs_in_phase)
        print(std_m)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5))

        ax1.plot(sim_anti_phase, color="#4477AA", alpha=0.8, lw=3, label="Simulation")
        ax1.plot(obs_anti_phase, color="#EE6677", alpha=0.8, lw=3, label="Observation")
        ax1.set_ylabel('Value', fontname='Times New Roman', fontsize=18)
        ax1.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax1.set_title(r'$\bf{(a)}$ Runoff data with a small outlier, different phase.', fontname='Times New Roman',
                      fontsize=18)

        ax2.plot(sim_in_phase, color="#4477AA", alpha=0.8, lw=3, label="Simulation")
        ax2.plot(obs_in_phase, color="#EE6677", alpha=0.8, lw=3, label="Observation")
        ax2.set_ylabel('Value', fontname='Times New Roman', fontsize=18)
        ax2.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax2.set_title(r'$\bf{(b)}$ Runoff data with an extreme event, same phase.', fontname='Times New Roman',
                      fontsize=18)
        ax2.legend(frameon=False, prop={'family': 'Times New Roman', 'size': 18})
        for ax in [ax1, ax2]:
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_fontname('Times New Roman')
                tick.set_fontsize(16)  # 可选：统一字号
        plt.tight_layout()
        if self.write:
            print('\033[1;31mSaving case_2_low_variability...\033[0m')
            plt.savefig("temp/case2_extreme_events.png", bbox_inches='tight', dpi=300)
            plt.savefig("temp/case2_extreme_events.pdf", bbox_inches='tight', dpi=300)
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')
        plt.show()

        return 0

    def low_variability_sensitivity(self):
        t = np.arange(0, 100)
        # print('t\t', t)
        t_pi = t * np.pi
        cost = np.cos(t_pi)

        categories = ['anti_phase', 'in_phase']
        metrics = ['mfm', 'nse', 'kge', 'mkge', 'rmse', 'nrmse']

        # 创建嵌套字典：如 result['high_low']['mfm'] = np.zeros(scale)
        result = {
            category: {metric: np.zeros(self.scale) for metric in metrics}
            for category in categories
        }



        for i in range(self.scale):
            obs_anti_phase = np.abs(cost)
            sim_anti_phase = np.abs(cost)
            obs_anti_phase[len(t) - 1] = 0.99 - i / 100
            sim_anti_phase[len(t) - 1] = 1.01 + i / 100

            obs_in_phase = np.abs(cost)
            sim_in_phase = np.abs(cost)
            obs_in_phase[len(t) - 1] = 1.03 + i / 100
            sim_in_phase[len(t) - 1] = 1.01 + i / 100

            result['anti_phase']['mfm'][i] = self.mfm_temp.model_fidelity_metric(sim_anti_phase, obs_anti_phase, phase=True)['MFM']
            result_standard_metrcs = self.mfm_temp.standard_metrics(sim_anti_phase, obs_anti_phase)
            result['anti_phase']['nse'][i] = result_standard_metrcs['NSE']
            result['anti_phase']['kge'][i] = result_standard_metrcs['KGE']
            result['anti_phase']['mkge'][i] = result_standard_metrcs['mKGE']
            result['anti_phase']['rmse'][i] = result_standard_metrcs['RMSE']
            result['anti_phase']['nrmse'][i] = result_standard_metrcs['NRMSE']

            result['in_phase']['mfm'][i] = self.mfm_temp.model_fidelity_metric(sim_in_phase, obs_in_phase, p=1, phase=True)['MFM']
            result_standard_metrcs = self.mfm_temp.standard_metrics(sim_in_phase, obs_in_phase)
            result['in_phase']['nse'][i] = result_standard_metrcs['NSE']
            result['in_phase']['kge'][i] = result_standard_metrcs['KGE']
            result['in_phase']['mkge'][i] = result_standard_metrcs['mKGE']
            result['in_phase']['rmse'][i] = result_standard_metrcs['RMSE']
            result['in_phase']['nrmse'][i] = result_standard_metrcs['NRMSE']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.plot(result['anti_phase']['mfm'], color="#4477AA", label='MFM', lw=3)
        ax1.plot(result['anti_phase']['nse'], color="#EE6677", label='NSE', alpha=0.8, lw=2)
        ax1.plot(result['anti_phase']['kge'], color="#228833", label='KGE', alpha=0.8, linestyle='--', lw=3)
        ax1.plot(result['anti_phase']['mkge'], color="#CCBB44", label='mKGE', alpha=0.8, linestyle=':', lw=3)
        ax1.plot(result['anti_phase']['rmse'], color="#66CCEE", label='RMSE', alpha=0.8, linestyle='--', lw=3)
        ax1.plot(result['anti_phase']['nrmse'], color="#AA3377", label='NRMSE', alpha=0.8, linestyle=':', lw=3)
        ax1.axhline(y=0, color='grey', linestyle='--', alpha=0.5)
        ax1.axhline(y=1.0, color='grey', linestyle='--', alpha=0.5)
        ax1.axvline(x=0, color='grey', linestyle='--', alpha=0.5)
        ax1.set_xlabel('Scaling parameter', fontname='Times New Roman', fontsize=18)
        ax1.set_ylabel('Score', fontname='Times New Roman', fontsize=18)
        # ax1.legend()
        ax1.set_title(r'$\bf{(a)}$', fontname='Times New Roman', fontsize=18)

        ax2.plot(result['in_phase']['mfm'], color="#4477AA", label='MFM', lw=3)
        ax2.plot(result['in_phase']['nse'], color="#EE6677", label='NSE', alpha=0.8, lw=2)
        ax2.plot(result['in_phase']['kge'], color="#228833", label='KGE', alpha=0.8, linestyle='--', lw=3)
        ax2.plot(result['in_phase']['mkge'], color="#CCBB44", label='mKGE', alpha=0.8, linestyle=':', lw=3)
        ax2.plot(result['in_phase']['rmse'], color="#66CCEE", label='RMSE', alpha=0.8, linestyle='--', lw=3)
        ax2.plot(result['in_phase']['nrmse'], color="#AA3377", label='NRMSE', alpha=0.8, linestyle=':', lw=3)
        ax2.axhline(y=0, color='grey', linestyle='--', alpha=0.5)
        ax2.axhline(y=1.0, color='grey', linestyle='--', alpha=0.5)
        ax2.axvline(x=0, color='grey', linestyle='--', alpha=0.5)
        ax2.set_xlabel('Scaling parameter', fontname='Times New Roman', fontsize=18)
        ax2.set_ylabel('Score', fontname='Times New Roman', fontsize=18)
        ax2.legend(frameon=False, ncol=2, prop={'family': 'Times New Roman', 'size': 14}, bbox_to_anchor=(0.2, 0.2))
        ax2.set_title(r'$\bf{(b)}$', fontname='Times New Roman', fontsize=18)

        for ax in [ax1, ax2]:
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_fontname('Times New Roman')
                tick.set_fontsize(16)  # 可选：统一字号

        plt.tight_layout()

        if self.write:
            print('\033[1;31mSaving case_2_low_variability_sensitivity...\033[0m')
            plt.savefig("temp/case_2_low_variability_sensitivity.png", bbox_inches='tight', dpi=300)
            plt.savefig("temp/case_2_low_variability_sensitivity.pdf", bbox_inches='tight', dpi=300)
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')
        plt.show()

        print(result)

        return 0

case_2_test = case_2_low_variability()
case_2_test.low_variability()
case_2_test.low_variability_sensitivity()