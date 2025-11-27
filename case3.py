from mfm import *
from read_file import *
from matplotlib.patches import ConnectionPatch

class case_3_phase_error():
    def __init__(self, scale=50, write=False, mfm_temp = mfm()):
        self.scale = scale
        self.write = write
        self.mfm_temp = mfm_temp

    def geometry(self):

        # --- 1. 设置全局字体和样式 (符合科学论文规范) ---
        # 使用 'serif' 字体 (例如 Times New Roman)，并设置合适的字号
        # plt.rcParams.update({
        #     'font.family': 'serif',
        #     'font.serif': ['Times New Roman'],
        #     'font.size': 14,
        #     'axes.labelsize': 16,
        #     'xtick.labelsize': 14,
        #     'ytick.labelsize': 14,
        #     'legend.fontsize': 14,
        #     'axes.linewidth': 1.5,
        #     'grid.linestyle': ':',
        #     'grid.alpha': 0.6
        # })

        # --- 2. 定义函数和数据 ---
        PI = np.pi
        PHASE_SHIFT = PI / 4

        def y_black(x):
            """黑色波: "observation" """
            return np.sin(x)

        def y_blue(x):
            """蓝色波: "simulation"
            1. 相位差 pi/4
            2. 比黑色波 "高" 1
            """
            return np.sin(x - PHASE_SHIFT) + 1.0

        # 生成 x 轴数据
        x = np.linspace(0, 2 * PI, 500)
        y_obs = y_black(x)
        y_sim = y_blue(x)

        # --- 3. 创建画布和坐标系 ---
        fig, ax = plt.subplots(figsize=(8, 3.5))

        # --- 4. 绘制两条正弦波 ---
        ax.plot(x, y_obs, color='#4477AA', lw=3, label='Observation')
        ax.plot(x, y_sim, color='#EE6677', lw=3, label='Simulation')

        # --- 5. 循环绘制两个标注点 (pi/2 和 pi) ---
        annotation_points_x = [PI / 2, PI * 3/2]
        brace_width = 7.0  # 标注d1, d2的卷括号宽度

        for x_val in annotation_points_x:
            # --- 计算所有关键点坐标 ---
            # 黑色波上的点
            p_black = (x_val, y_black(x_val))

            # 蓝色波上对应的垂直点 (d1的终点)
            p_blue_vertical = (x_val, y_blue(x_val))

            # 蓝色波上相位偏移的点
            x_shifted = x_val + PHASE_SHIFT
            p_blue_shifted = (x_shifted, y_blue(x_shifted))

            # 构成三角形的直角顶点
            p_triangle_corner = (x_shifted, y_black(x_val))

            # --- 绘制关键点 ---
            ax.plot(p_black[0], p_black[1], color='black', marker='o', markersize=6)  # 黑色圆点
            ax.plot(p_blue_vertical[0], p_blue_vertical[1], color='black', marker='o', markersize=6)  # 蓝色垂直点
            ax.plot(p_blue_shifted[0], p_blue_shifted[1], color='black', marker='o', markersize=6)  # 蓝色相位点

            # --- 2&6: 绘制 d1 (垂直连线) ---
            ax.plot([p_black[0], p_blue_vertical[0]],
                    [p_black[1], p_blue_vertical[1]],
                    color="#AA3377", linestyle='--', lw=1.5)

            # --- 3&4: 绘制对角线和三角形 ---
            # 3. 对角线 (黑色点 -> 蓝色相位点)
            ax.plot([p_black[0], p_blue_shifted[0]],
                    [p_black[1], p_blue_shifted[1]],
                    color="#AA3377", linestyle='--', lw=1.5)

            # 4. 三角形的另外两条边 (水平 + 垂直)
            ax.plot([p_black[0], p_triangle_corner[0]],
                    [p_black[1], p_triangle_corner[1]],
                    color="#AA3377", linestyle='--', lw=1)  # 水平边
            ax.plot([p_triangle_corner[0], p_blue_shifted[0]],
                    [p_triangle_corner[1], p_blue_shifted[1]],
                    color="#AA3377", linestyle='--', lw=1)  # 垂直边 (d2)

            # --- 5: 标注角度 theta ---
            # 在p_black点右侧标注
            ax.text(p_black[0], p_black[1] + 0.05, r'$\theta$',
                    color='#000000', fontsize=16, ha='left', va='bottom')


            # --- 6: 标注 d1 和 d2 (使用卷括号) ---
            # 标注 d1
            x_brace_d1 = p_black[0] - 0.15  # 放在 d1 左侧
            con_d1 = ConnectionPatch(xyA=(x_brace_d1, p_black[1]),
                                     xyB=(x_brace_d1, p_blue_vertical[1]),
                                     coordsA='data', coordsB='data',
                                     arrowstyle=f'|-|', lw=1.5, color='#000000', zorder=10)
            ax.add_patch(con_d1)
            ax.text(x_brace_d1 - 0.08, (p_black[1] + p_blue_vertical[1]) / 2, '$d_1$',
                    color='#000000', fontsize=16, ha='right', va='center')

            # 标注 d2 (d2 是三角形的垂直边)
            x_brace_d2 = p_triangle_corner[0] + 0.15  # 放在 d2 右侧
            con_d2 = ConnectionPatch(xyA=(x_brace_d2, p_triangle_corner[1]),
                                     xyB=(x_brace_d2, p_blue_shifted[1]),
                                     coordsA='data', coordsB='data',
                                     arrowstyle=f'|-|', lw=1.5, color='#000000', zorder=10)
            ax.add_patch(con_d2)
            ax.text(x_brace_d2 + 0.08, (p_triangle_corner[1] + p_blue_shifted[1]) / 2, '$d_2$',
                    color='#000000', fontsize=16, ha='left', va='center')

        # --- 7. 美化和清理图表 ---
        ax.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax.set_ylabel('Value', fontname='Times New Roman', fontsize=18)
        ax.legend(prop={'family': 'Times New Roman', 'size': 18}, frameon=False, loc='upper left', bbox_to_anchor=(0.1, 0.35))

        # 设置x轴刻度为pi的倍数
        ax.set_xticks([0, PI / 2, PI, 3 * PI / 2, 2 * PI])
        ax.set_xticklabels(['0', 'pi/2', 'pi', '3pi/2', '2pi'], fontname='Times New Roman', fontsize=18)
        plt.yticks(fontname='Times New Roman', fontsize=18)
        # 设置y轴范围
        ax.set_ylim(-1.5, 2.5)
        ax.set_xlim(0, 2 * PI)

        # 添加网格
        # ax.grid(True)

        # 移除顶部和右侧的边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # 确保布局紧凑
        plt.tight_layout()

        # --- 8. 显示或保存图片 ---
        if self.write:
            print('\033[1;31mSaving case_3_phase_error_geometry...\033[0m')
            plt.savefig("temp/case_3_phase_error_geometry.png", dpi=300, bbox_inches='tight')  # 保存为高分辨率png
            plt.savefig("temp/case_3_phase_error_geometry.pdf", dpi=300, bbox_inches='tight')  # 保存为高分辨率png
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')

        plt.show()

    def decoupling(self):
        t = np.arange(0, 100)
        t_pi = t * np.pi
        cost = np.cos(t_pi)
        # print('t\t', t)

        # 1 号实验：KGE、NSE 在恒定或低流量下不可靠-RMSE、NRMSE 相等
        obs_extreme = np.abs(cost) * 1
        sim_extreme = np.abs(cost) * 1
        # RMSE 不变参数
        obs_extreme[len(t) - 1] = 2
        sim_extreme[len(t) - 1] = 12

        t_pi = t * np.pi
        cost = np.cos(t_pi)
        # print('cost\t', cost)
        # print('len(cost)\t', len(cost))

        # 2 号实验：KGE、NSE 在相位差下不可靠-RMSE、NRMSE 相等下，无法区分好坏
        obs_anti_phase = cost / 2 + 1
        sim_anti_phase = - cost / 2 + 1

        # 2 号实验：RMSE、NRMSE 相等下，无法区分好坏
        obs_failure = cost * 0.01 + 1
        sim_failure = cost * 0.01 + 2
        # print(sim_anti_phase)

        print('\033[1;31mExtreme event case\033[0m')
        print(self.mfm_temp.model_fidelity_metric(sim_extreme, obs_extreme))
        print("========================")
        print(self.mfm_temp.standard_metrics(sim_extreme, obs_extreme))

        print('\033[1;31mAnti-phase case\033[0m')
        print(self.mfm_temp.model_fidelity_metric(sim_anti_phase, obs_anti_phase))
        print("========================")
        print(self.mfm_temp.standard_metrics(sim_anti_phase, obs_anti_phase))

        print('\033[1;31mFailure case\033[0m')
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
        ax2.set_title(r'$\bf{(b)}$ Reverse phase', fontname='Times New Roman', fontsize=18)
        ax2.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax2.set_ylabel('Value', fontname='Times New Roman', fontsize=18)
        # ax2.legend()

        ax3.plot(sim_failure, color='#4477AA', alpha=0.8, label="Simulation", lw=1.5, zorder=2)
        ax3.plot(obs_failure, color="#EE6677", alpha=0.8, label="Observation", lw=1.5, zorder=1)
        ax3.set_title(r'$\bf{(c)}$ Simulation failure', fontname='Times New Roman', fontsize=18)
        ax3.set_xlabel('Time', fontname='Times New Roman', fontsize=18)
        ax3.set_ylabel('Value', fontname='Times New Roman', fontsize=18)
        # ax3.legend()
        for ax in [ax1, ax2, ax3]:
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_fontname('Times New Roman')
                tick.set_fontsize(16)

        plt.tight_layout()
        if self.write:
            print('\033[1;31mSaving phase_error_decoupling...\033[0m')
            plt.savefig("temp/case_3_phase_error_decoupling.png", dpi=300, bbox_inches='tight')  # 保存为高分辨率png
            plt.savefig("temp/case_3_phase_error_decoupling.pdf", dpi=300, bbox_inches='tight')  # 保存为高分辨率png
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')

        plt.show()

        return 0

    def sensitivity(self):

        metrics = ['mfm', 'nse', 'kge', 'mkge', 'rmse', 'nrmse']

        # 创建嵌套字典：如 result['high_low']['mfm'] = np.zeros(scale)
        result = {metric: np.zeros(self.scale) for metric in metrics}

        for i in range(self.scale):
            t = np.arange(0, 100)
            t_pi = t * np.pi
            cost = np.cos(t_pi)
            # 2 号实验：KGE、NSE 在相位差下不可靠-RMSE、NRMSE 相等下，无法区分好坏
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
        # 从 1 开始
        x = np.arange(1, self.scale + 1)
        plt.plot(x, result['mfm'], color="#4477AA", label='MFM', lw=3)
        # plt.plot(mfm_no_phase_phase_sensitivity, color='brown', label='MFM without phase penalty', alpha=0.7, marker='x')

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

        if self.write:
            print('\033[1;31mSaving phase_error_decoupling...\033[0m')
            plt.savefig("temp/case3_phase_sensitivity.png", bbox_inches='tight', dpi=300)
            plt.savefig("temp/case3_phase_sensitivity.pdf", bbox_inches='tight', dpi=300)
            print('\033[1;31mDone.\033[0m')
        else:
            print('\033[1;31mFigure will not be saved.\033[0m')

        plt.show()
        return 0


case_3_test = case_3_phase_error()
case_3_test.geometry()
case_3_test.decoupling()
case_3_test.sensitivity()