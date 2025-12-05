"""
Introducing the Model Fidelity Metric (MFM) for robust and diagnostic hydrological evaluation

This script calculates MFM, standard metrics (i.e., NSE, KGE, mKGE), and error benchmarks (RMSE, NRMSE).

Author: Zezhen Wu
Version: 1.0.0
Date: December 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class mfm:
    def __init__(self):
        self.name= 'mfm'
        self.date = 'December 2025'
        self.author = 'Zezhen Wu / wuzezhen5577@163.com'

        np.seterr(all='ignore')

    # def _validate_inputs(self, sim, obs):

    def model_fidelity_metric(self, sim, obs, p=1, bins_suse=10, bins_phi=10, c=4, phase=True):
        """Calculate MFM"""

        def PHI_component(sim, obs, bins_phi):
            """Calculate Percentage of Histogram Intersection"""
            if len(sim) == 0 or len(obs) == 0:
                return np.nan
            bin_min = min(np.min(sim), np.min(obs))
            bin_max = max(np.max(sim), np.max(obs))
            if bin_min == bin_max:
                return 1.0  # Perfect match if all values are the same
            bin_edges = np.linspace(bin_min, bin_max, bins_phi + 1)
            hist_sim, _ = np.histogram(sim, bins=bin_edges, density=False)
            hist_obs, _ = np.histogram(obs, bins=bin_edges, density=False)
            min_sum = np.sum(np.minimum(hist_sim, hist_obs))
            obs_total = np.sum(hist_obs)
            if obs_total == 0:
                return np.nan
            return min_sum / obs_total

        def SUSE_component(sim, obs, bins_suse):
            """Calculate Scaled and Unscaled Shannon Entropy differences"""
            if len(sim) == 0 or len(obs) == 0:
                return np.nan

            # Scaled case
            min_val = min(sim.min(), obs.min())
            max_val = max(sim.max(), obs.max())
            if min_val == max_val:
                return 0.0  # No entropy difference if all values are the same
            bin_edges_scaled = np.linspace(min_val, max_val, bins_suse + 1)

            hist_sim_s, _ = np.histogram(sim, bins=bin_edges_scaled, density=False)
            hist_obs_s, _ = np.histogram(obs, bins=bin_edges_scaled, density=False)

            total_s_sim = np.sum(hist_sim_s)
            total_s_obs = np.sum(hist_obs_s)

            p_sim_s = hist_sim_s / total_s_sim if total_s_sim > 0 else np.zeros_like(hist_sim_s)
            p_obs_s = hist_obs_s / total_s_obs if total_s_obs > 0 else np.zeros_like(hist_obs_s)

            def entropy(p):
                p = p[p > 0]
                return -np.sum(p * np.log(p)) if len(p) > 0 else 0.0

            Hs = abs(entropy(p_sim_s) - entropy(p_obs_s))

            # Unscaled case
            if sim.min() == sim.max():
                Hu_sim = 0.0
            else:
                bin_edges_u_sim = np.linspace(sim.min(), sim.max(), bins_suse + 1)
                hist_sim_u, _ = np.histogram(sim, bins=bin_edges_u_sim, density=False)
                p_sim_u = hist_sim_u / np.sum(hist_sim_u) if np.sum(hist_sim_u) > 0 else np.zeros_like(hist_sim_u)
                Hu_sim = entropy(p_sim_u)

            if obs.min() == obs.max():
                Hu_obs = 0.0
            else:
                bin_edges_u_obs = np.linspace(obs.min(), obs.max(), bins_suse + 1)
                hist_obs_u, _ = np.histogram(obs, bins=bin_edges_u_obs, density=False)
                p_obs_u = hist_obs_u / np.sum(hist_obs_u) if np.sum(hist_obs_u) > 0 else np.zeros_like(hist_obs_u)
                Hu_obs = entropy(p_obs_u)

            Hu = abs(Hu_sim - Hu_obs)

            return max(Hs, Hu)

        def PPF_component(sim, obs):
            """Calculate phase difference using Fast Fourier Transform"""
            N = len(obs)
            if N != len(sim) or N < 3:
                return 0.0

            fft_obs = np.fft.fft(obs)
            fft_sim = np.fft.fft(sim)

            freqs = np.fft.fftfreq(N, d=1.0)

            # Find dominant frequency
            if N // 2 < 1:
                return 0.0

            if len(sim) > 365:
                dominant_freq_idx = max(np.argmax(np.abs(fft_obs[1:N // 2 + 1])), 33) + 1
            else:
                dominant_freq_idx = np.argmax(np.abs(fft_obs[1:N // 2 + 1])) + 1

            # Calculate phase difference
            phase_obs = np.angle(fft_obs)
            phase_sim = np.angle(fft_sim)
            phase_difference_rad = phase_sim[dominant_freq_idx] - phase_obs[dominant_freq_idx]
            phase_difference_rad = (phase_difference_rad + np.pi) % (2 * np.pi) - np.pi

            return phase_difference_rad


        def MFM_calculation(sim, obs):
            """Calculate MFM for a single time series"""
            # Remove NaN values
            mask = np.isfinite(sim) & np.isfinite(obs)
            sim_clean = sim[mask]
            obs_clean = obs[mask]

            if len(sim_clean) < 3 or len(obs_clean) < 3:
                return np.nan

            if np.mean(obs_clean) == 0:
                return np.nan

            # Calculate components
            # 1. Normalized error with phase penalty
            nmaep = np.power(np.mean(np.power(np.abs(sim_clean - obs_clean), p)), 1 / p) / np.mean(obs_clean)

            if phase:
                phase_difference_rad = PPF_component(sim_clean, obs_clean)
                phase_penalty_factor = np.cos(phase_difference_rad / c)
                normalized_error = phase_penalty_factor * np.exp(-nmaep)
            else:
                normalized_error = np.exp(-nmaep)

            # 2. Variability capture
            suse = SUSE_component(sim_clean, obs_clean, bins_suse)
            if np.isnan(suse):
                return np.nan
            variability_capture = np.exp(-suse)

            # 3. Distribution similarity
            distribution_similarity = PHI_component(sim_clean, obs_clean, bins_phi)
            if np.isnan(distribution_similarity):
                return np.nan

            # Calculate MFM
            mfm_value = 1 - (np.sqrt(
                ((1 - normalized_error) ** 2 +
                (1 - variability_capture) ** 2 +
                (1 - distribution_similarity) ** 2) / 3
            ))

            return pd.Series({'MFM':float(mfm_value),
                      'PPF':float(phase_penalty_factor) if phase else np.nan,
                      'exp(- NMAEp)':float(np.exp(- nmaep)),
                      'omega':float(normalized_error),
                      'varphi':float(variability_capture),
                      'eta':float(distribution_similarity)
                      })

        result = MFM_calculation(sim, obs)
        return result

    def standard_metrics(self, sim, obs, plot=False):
        """Calculating Nash-Sutcliffe Efficiency (NSE), Kling-Gupta Efficiency (KGE), modified KGE (mKGE), RMSE, and NRMSE"""

        meanSim = np.nanmean(sim)
        meanObs = np.nanmean(obs)
        varSim = np.nanvar(sim)
        varObs = np.nanvar(obs)
        rProd = np.corrcoef(sim, obs)[0, 1]
        xBeta = meanSim / meanObs
        yBeta = (meanObs - meanSim) / np.sqrt(varObs)
        alpha = np.sqrt(varSim) / np.sqrt(varObs)

        nse = 2 * alpha * rProd - yBeta ** 2 - alpha ** 2
        kge = 1 - np.sqrt((xBeta - 1) ** 2 + (alpha - 1) ** 2 + (rProd - 1) ** 2)
        mkge = 1 - np.sqrt((xBeta - 1) ** 2 + (alpha / xBeta - 1) ** 2 + (rProd - 1) ** 2)
        rmse = np.sqrt(np.mean((sim - obs) ** 2))
        nrmse = rmse / np.mean(obs)
        mae = np.mean(np.abs(sim - obs))
        nmae = mae / np.mean(obs)

        # print('NSE\t',nse)
        # print('KGE\t',kge)
        # print('mKGE\t',mkge)
        # print('RMSE\t',rmse)
        # print('NRMSE\t',nrmse)
        # print('MAE\t',mae)
        # print('NMAE\t',nmae)
        # print('NRMSE\t',nrmse)
        # print('Alpha\t',alpha)
        # print('Beta\t',xBeta)
        # print('mean_Obs\t',meanObs)
        # print('std_Obs\t',varObs)

        if plot:
            plt.figure(figsize=(12, 5))
            plt.plot(sim, color='#4477AA', alpha=0.7, linestyle='--', label="Simulation", zorder=2)
            plt.plot(obs, color="#EE6677", alpha=0.7, label="Observation", zorder=1)
            # plt.grid(True)
            plt.ylabel('Value')
            plt.xlabel('Time')
            plt.legend(frameon=False)
            # plt.xticks(fontsize=14)
            # plt.yticks(fontsize=14)
            # plt.title('Runoff data')
            # plt.legend(fontsize=10)
            plt.show()

        return pd.Series({
            'NSE': float(nse),
            'KGE': float(kge),
            'mKGE': float(mkge),
            'RMSE': float(rmse),
            'NRMSE': float(nrmse),
            'MAE': float(mae),
            'NMAE': float(nmae),
            'alpha': float(alpha),
            'beta': float(xBeta),
            'rprod': float(rProd),
            'meanObs': float(meanObs)
        })