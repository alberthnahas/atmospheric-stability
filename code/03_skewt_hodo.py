import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pandas as pd
import metpy.calc as mpcalc
from metpy.plots import SkewT, Hodograph
from metpy.units import units
from metpy.constants import Rd, g, dry_adiabatic_lapse_rate

# --- 1. CONFIGURATION ---
NC_FILENAME = 'cams_data_kemayoran.nc'
LOCATION_NAME = 'Kemayoran, Jakarta'

# --- 2. DATA LOADING ---
try:
    ds = xr.open_dataset(NC_FILENAME, decode_timedelta=True)
except FileNotFoundError:
    print(f"ERROR: File not found -> '{NC_FILENAME}'")
    exit()

print("--- Data loaded. Processing all forecast periods... ---")

# --- DATA SELECTION & INITIAL TIME SETUP ---
ds_squeezed = ds.squeeze()
p = ds_squeezed['pressure_level'].values * units.hPa

initial_time_pd = pd.to_datetime(str(ds_squeezed.forecast_reference_time.values))
initial_time_str_file = initial_time_pd.strftime('%Y%m%d_%Hz')

OUTPUT_REPORT_FILENAME = f"stability_analysis_report_initial_{initial_time_str_file}.txt"


# --- FILE HANDLING & REPORT HEADER ---
with open(OUTPUT_REPORT_FILENAME, 'w') as report_file:
    report_file.write(f"Atmospheric Stability and Inversion Analysis Report\n")
    report_file.write(f"Location: {LOCATION_NAME}\n")
    report_file.write(f"Source: ECMWF Integrated Forecasting System (IFS)\n")
    report_file.write(f"Initialization Time: {initial_time_pd.strftime('%Y-%m-%d %H:%MZ')}\n\n")

    # (Reference Guides)
    report_file.write("--- Stability Classification Reference ---\n")
    report_file.write("Based on Environmental Lapse Rate (Γ = -dT/dz) in the surface layer.\n\n")
    report_file.write("- Γ < 0    K/km: Absolutely Stable (Inversion) - Strongest trapping\n")
    report_file.write("- 0 to 2   K/km: Extremely Stable - Very strong trapping\n")
    report_file.write("- 2 to 5   K/km: Very Stable - Significant trapping\n")
    report_file.write("- 5 to 8   K/km: Moderately Stable - Some trapping\n")
    report_file.write("- 8 to 9.8 K/km: Weakly Stable - Dispersion becoming favorable\n")
    report_file.write("- Γ >= 9.8 K/km: Neutral/Unstable - Good dispersion\n")
    report_file.write("----------------------------------------\n\n")
    
    # NEW: Boundary Layer Reference Guide
    report_file.write("--- Boundary Layer Analysis Reference ---\n")
    report_file.write("1. Mixing Height: The depth of the layer available for pollutant dilution\n")
    report_file.write("   - < 500 m: Shallow - Very poor dilution - High concentrations likely\n")
    report_file.write("   - 500-1500 m: Moderate - Dilution is limited\n")
    report_file.write("   - > 1500 m: Deep - Good dilution potential\n\n")
    report_file.write("2. Low-Level Jet (LLJ): A peak in wind speed in the lower atmosphere\n")
    report_file.write("   - Can increase surface turbulence and ventilation\n")
    report_file.write("   - Can also transport pollutants from upwind sources over long distances\n")
    report_file.write("----------------------------------------\n\n")

    report_file.write("--- Hodograph Analysis Reference ---\n")
    report_file.write("Provides insights into ventilation and severe weather potential\n\n")
    report_file.write("1. Mean Wind (0-1 km AGL): Indicates surface ventilation potential\n")
    report_file.write("   - < 5 m/s: Poor ventilation, favorable for pollutant trapping\n")
    report_file.write("   - > 5 m/s: Good ventilation, favorable for dispersion\n\n")
    report_file.write("2. Bulk Shear (0-6 km): Indicates potential for thunderstorm organization\n")
    report_file.write("   - < 25 knots: Disorganized, single-cell storms are likely\n")
    report_file.write("   - 25-40 knots: Favorable for organized multicell thunderstorms\n")
    report_file.write("   - > 40 knots: Favorable for supercells (rotating storms)\n")
    report_file.write("----------------------------------------\n\n")
    report_file.write("--- Convective Potential (CAPE/CIN) Reference ---\n")
    report_file.write("CAPE (J/kg): 0-1000 (Marginal), 1000-2500 (Moderate), >2500 (Strong)\n")
    report_file.write("CIN (J/kg): 0 to -25 (Weak Cap), -25 to -100 (Moderate Cap), < -100 (Strong Cap)\n")
    report_file.write("----------------------------------------\n")
    
    # --- MAIN LOOP ---
    for fp_index in range(len(ds_squeezed.forecast_period)):
        
        current_profile = ds_squeezed.isel(forecast_period=fp_index)
        T = current_profile['t'].values * units.K; q = current_profile['q'].values * units('kg/kg')
        u = current_profile['u'].values * units('m/s'); v = current_profile['v'].values * units('m/s')
        
        valid_time_pd = pd.to_datetime(str(current_profile.valid_time.values))
        valid_time_utc_str = valid_time_pd.strftime('%Y-%m-%d %H:%MZ')
        valid_time_wib = valid_time_pd + pd.Timedelta(hours=7)
        valid_time_wib_str = valid_time_wib.strftime('%Y-%m-%d %H:%M WIB')
        lead_time_hours = current_profile.forecast_period.values / np.timedelta64(1, 'h')
        
        # --- CALCULATIONS ---
        Td = mpcalc.dewpoint_from_specific_humidity(p, q)
        prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')
        cape, cin = mpcalc.cape_cin(p, T, Td, prof)
        Tv = mpcalc.virtual_temperature(T, q)
        H_m = np.zeros_like(p.m)
        for i in range(1, len(p)):
            Tv_mean_layer = np.mean(Tv[i-1:i+1])
            layer_thickness = (Rd * Tv_mean_layer / g) * np.log(p[i-1] / p[i])
            H_m[i] = H_m[i-1] + layer_thickness.m
        H = H_m * units.m
        
        theta = mpcalc.potential_temperature(p, T)
        wind_speed = mpcalc.wind_speed(u, v)
        
        # --- PLOTTING ---
        print(f"\nGenerating plot for forecast +{lead_time_hours:.0f}h (Valid: {valid_time_utc_str})...")

        fig = plt.figure(figsize=(20, 10))
        gs = GridSpec(1, 3, width_ratios=[2, 1, 1])
        title_line1 = f"Forecast for {LOCATION_NAME} (Source: ECMWF IFS)"
        title_line2 = f"Valid time: {valid_time_utc_str} or {valid_time_wib_str}"
        fig.suptitle(f"{title_line1}\n{title_line2}", fontsize=16, y=0.98)

        skew = SkewT(fig, rotation=45, subplot=gs[0])
        skew.ax.set_title('Skew-T Log-P')
        skew.plot(p, T, 'r', linewidth=2, label='Temperature'); skew.plot(p, Td, 'g', linewidth=2, label='Dew Point')
        skew.plot_barbs(p, u, v, y_clip_radius=0.03); skew.plot(p, prof, 'k', linestyle='--', label='Parcel Path')
        skew.shade_cin(p, T, prof, alpha=0.2, label=f'CIN: {cin.to("J/kg").m:.0f} J/kg'); skew.shade_cape(p, T, prof, alpha=0.4, label=f'CAPE: {cape.to("J/kg").m:.0f} J/kg')
        skew.plot_dry_adiabats(); skew.plot_moist_adiabats(); skew.plot_mixing_lines()
        skew.ax.set_ylim(1000, 100); skew.ax.set_xlabel('Temperature (°C)'); skew.ax.set_ylabel('Pressure (hPa)')
        skew.ax.legend(loc='upper right')
        
        hodo_ax = fig.add_subplot(gs[1])
        hodo_ax.set_title('Hodograph')
        h = Hodograph(hodo_ax, component_range=80.)
        h.add_grid(increment=20); line = h.plot_colormapped(u, v, H.to('km'), cmap='viridis')
        divider = make_axes_locatable(hodo_ax); cax = divider.append_axes("right", size="5%", pad=0.1)
        fig.colorbar(line, cax=cax, label='Height (km AGL)')
        hodo_ax.set_xlabel('U-Wind (m/s)'); hodo_ax.set_ylabel('V-Wind (m/s)')
        
        profile_ax = fig.add_subplot(gs[2])
        profile_ax.set_title("Vertical Profiles")
        profile_ax.set_ylabel("Height (km AGL)")
        profile_ax.set_ylim(0, 5)
        profile_ax.grid(True, linestyle='--', alpha=0.5)

        color_theta = 'darkorange'
        profile_ax.plot(theta.to('K'), H.to('km'), label='Potential Temp. (θ)', color=color_theta, marker='o', markersize=3)
        profile_ax.set_xlabel("Potential Temperature (K)", color=color_theta)
        profile_ax.tick_params(axis='x', labelcolor=color_theta)
        
        boundary_layer_indices = np.where(H.to('km').m <= 5)[0]
        theta_bl = theta[boundary_layer_indices]
        min_theta, max_theta = np.min(theta_bl).to('K').m, np.max(theta_bl).to('K').m
        padding = 1
        profile_ax.set_xlim(min_theta - padding, max_theta + padding)
        
        wind_ax = profile_ax.twiny()
        color_wind = 'darkblue'
        wind_ax.plot(wind_speed.to('m/s'), H.to('km'), label='Wind Speed', color=color_wind, marker='x', markersize=3, linestyle='--')
        wind_ax.set_xlabel("Wind Speed (m/s)", color=color_wind)
        wind_ax.tick_params(axis='x', labelcolor=color_wind)

        valid_time_str_file = valid_time_pd.strftime('%Y%m%d_%Hz')
        output_plot_filename = f"full_vertical_profile_{LOCATION_NAME.replace(', ', '_').lower()}_initial_{initial_time_str_file}_forecast_{valid_time_str_file}.png"
        
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.savefig(output_plot_filename, dpi=150, bbox_inches='tight'); plt.close(fig)
        print(f"Plot saved as: {output_plot_filename}")

        # --- ANALYSIS REPORT ---
        report_file.write(f"\n\n--- Analysis for Forecast +{lead_time_hours:.0f}h (Valid: {valid_time_utc_str} or {valid_time_wib_str}) ---\n")
        
        report_file.write(f"--- Inversion Analysis ---\n")
        if T[1] > T[0]: report_file.write("Surface-based inversion: Detected\n")
        else: report_file.write("Surface-based inversion: Not Detected\n")
        
        report_file.write(f"--- Surface Layer Stability Analysis ---\n")
        try:
            delta_H = H[1] - H[0]
            if delta_H > 0 * units.m:
                lapse_rate = -((T[1] - T[0]) / delta_H).to('delta_degC/km')
                report_file.write(f"Lapse rate: {lapse_rate:.2f~P}\n")
                if lapse_rate < 0 * units('delta_degC/km'): stability = "Absolutely Stable (Inversion)"; conclusion = "Excellent conditions for trapping pollutants..."
                elif lapse_rate < 2 * units('delta_degC/km'): stability = "Extremely Stable"; conclusion = "Very strong trapping potential"
                elif lapse_rate < 5 * units('delta_degC/km'): stability = "Very Stable"; conclusion = "Significant trapping potential"
                elif lapse_rate < 8 * units('delta_degC/km'): stability = "Moderately Stable"; conclusion = "Some trapping potential"
                elif lapse_rate < 9.8 * units('delta_degC/km'): stability = "Weakly Stable"; conclusion = "Dispersion is favorable"
                else: stability = "Neutral/Unstable"; conclusion = "Good vertical dispersion"
                report_file.write(f"Stability Condition: {stability}\n"); report_file.write(f"Conclusion: {conclusion}\n")
            else: report_file.write("Could not calculate lapse rate\n")
        except Exception as e: report_file.write(f"Could not perform stability analysis: {e}\n")

        # NEW: Boundary Layer Analysis Section
        report_file.write(f"--- Boundary Layer Analysis ---\n")
        try:
            # Estimate Mixing Height
            theta_sfc = theta[0]
            # Find first level where theta is 2K greater than surface theta (common threshold)
            mixing_indices = np.where(theta > theta_sfc + 2 * units.delta_degC)[0]
            if mixing_indices.size > 0:
                mixing_height = H[mixing_indices[0]]
                report_file.write(f"Estimated Mixing Height: {mixing_height.to('m'):.0f~P}\n")
            else:
                report_file.write("Estimated Mixing Height: Very deep or not well-defined\n")

            # Detect Low-Level Jet (below 3km)
            llj_indices = np.where(H.to('km').m < 3)[0]
            if len(llj_indices) > 2:
                ws_ll = wind_speed[llj_indices]
                llj_idx = np.argmax(ws_ll)
                llj_speed = ws_ll[llj_idx]
                if llj_speed > 12 * units('m/s'): # Common speed threshold for an LLJ
                    llj_height = H[llj_indices[llj_idx]]
                    report_file.write(f"Low-Level Jet: Detected at ~{llj_height.to('m'):.0f~P} with speed {llj_speed:.1f~P}\n")
                else:
                    report_file.write("Low-Level Jet: Not Detected\n")
            else:
                report_file.write("Low-Level Jet: Not enough data below 3km to analyze\n")
        except Exception as e:
            report_file.write(f"Could not perform Boundary Layer analysis: {e}\n")
        
        report_file.write(f"--- Hodograph Analysis ---\n")
        try:
            low_level_indices = np.where(H.m <= 1000)[0]
            if len(low_level_indices) > 1:
                mean_wind_speed = np.sqrt(np.mean(u[low_level_indices])**2 + np.mean(v[low_level_indices])**2)
                report_file.write(f"Mean Wind (0-1 km): {mean_wind_speed:.2f~P}\n")
                if mean_wind_speed < 5 * units('m/s'): report_file.write("  - Ventilation: Poor - Favorable for trapping\n")
                else: report_file.write("  - Ventilation: Good - Favorable for dispersion\n")
            u_sfc, v_sfc = u[0].m, v[0].m
            u_6km = np.interp(6000, H.m, u.m); v_6km = np.interp(6000, H.m, v.m)
            shear_mag = mpcalc.wind_speed((u_6km - u_sfc) * units('m/s'), (v_6km - v_sfc) * units('m/s'))
            report_file.write(f"Bulk Shear (0-6 km): {shear_mag.to('knots'):.2f~P}\n")
            if shear_mag < 25 * units.knots: report_file.write("  - Storm Potential: Disorganized, single-cell storms\n")
            elif shear_mag < 40 * units.knots: report_file.write("  - Storm Potential: Favorable for multicell storms\n")
            else: report_file.write("  - Storm Potential: Favorable for supercells\n")
        except Exception as e: report_file.write(f"Could not perform hodograph analysis: {e}\n")

        report_file.write(f"--- Convective Potential Analysis ---\n")
        report_file.write(f"CAPE: {cape:.0f~P} | CIN: {cin:.0f~P}\n")
        if cape < 100 * units('J/kg'): cape_conclusion = "Essentially no instability"
        elif cape < 1000 * units('J/kg'): cape_conclusion = "Marginal instability"
        elif cape < 2500 * units('J/kg'): cape_conclusion = "Moderate instability"
        else: cape_conclusion = "Strong/Extreme instability"
        report_file.write(f"  - Instability Level: {cape_conclusion}\n")
        if cin > -25 * units('J/kg'): cin_conclusion = "Weak cap - Storms can initiate easily"
        elif cin > -100 * units('J/kg'): cin_conclusion = "Moderate cap - Requires strong forcing to break"
        else: cin_conclusion = "Strong cap - Convection is unlikely"
        report_file.write(f"  - Capping Strength: {cin_conclusion}\n")
        if cape < 100 * units('J/kg'): final_conclusion = "No thunderstorm potential"
        elif cin > -25 * units('J/kg'): final_conclusion = "Thunderstorms are possible if lift is present"
        else: final_conclusion = "Storms are unlikely, but could be severe if cap breaks"
        report_file.write(f"  - Overall Conclusion: {final_conclusion}\n")
        
        report_file.write("----------------------------------------------------------------------\n")

print(f"\nAll plots generated and analysis complete.")
print(f"Full report saved to: {OUTPUT_REPORT_FILENAME}")
