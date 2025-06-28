## Atmospheric Stability Analysis from ECMWF IFS Data

### Overview

This project provides a comprehensive workflow for downloading atmospheric forecast data, generating analytical plots (Skew-T Log-P and Hodograph), and producing a detailed atmospheric stability report from a single point (the codes are generated for [Kemayoran, Jakarta](https://maps.app.goo.gl/oxvD5d5QV9Y7BBV9A)). The analysis is based on forecast data from the European Centre for Medium-Range Weather Forecasts (ECMWF) Integrated Forecasting System (IFS), obtained via the Copernicus Atmosphere Monitoring Service (CAMS).

The process is divided into three main steps:

1.  **Generate Download Script:** An R script dynamically creates a Python script to download meteorological data for the previous day.
2.  **Download Data:** The generated Python script fetches the specified forecast data.
3.  **Analyze and Plot:** A final Python script processes the downloaded data to create Skew-T plots, Hodographs, and a comprehensive stability analysis text report for each forecast lead time.


### Data Source

The meteorological data is sourced from the **CAMS global atmospheric composition forecasts** dataset.

  * **Website:** [https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts](https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts)

#### How to Access the Data

Accessing the data is free but requires setting up an API key.

1.  **Create an Account:** Register for a free account on the [Copernicus Atmosphere Data Store (ADS) portal](https://www.google.com/search?q=https://ads.atmosphere.copernicus.eu/user/register).

2.  **Install the CDS API Client:** Install the necessary Python library to interact with the service.

    ```bash
    pip install cdsapi
    ```

3.  **Set Up Your API Key:**

      * Log in to the ADS website and navigate to your user profile page to find your **UID** and **API Key**.
      * Create a file named `.cdsapirc` in your home directory (e.g., `C:\Users\<username>` on Windows or `/home/<username>` on Linux/macOS).
      * Add your credentials to the file in the following format:

    <!-- end list -->

    ```
    url: https://ads.atmosphere.copernicus.eu/api/v2
    key: {UID}:{API-KEY}
    ```



### Prerequisites

  * **R:** Required to run the first script. No special packages are needed.
  * **Python 3:** Required for data download and analysis.
  * **Python Libraries:** You can install all required libraries with pip:
    ```bash
    pip install cdsapi xarray netcdf4 matplotlib numpy pandas metpy
    ```



### Workflow/Usage

Follow these steps in order to run the full analysis.

#### Step 1: Generate the Python Download Script

Run the R script to create the Python download script. This will automatically set the date in the request to the previous day.

```bash
Rscript code/01_generate_python.R
```

This command will create/overwrite the `code/02_download_meteo.py` file.

#### Step 2: Download the Meteorological Data

Execute the newly generated Python script to download the forecast data.

```bash
python code/02_download_meteo.py
```

This will download a `netcdf_zip` file into your project's root directory.

#### Step 3: Prepare the Data File

The analysis script expects a specific file name. You must:

1.  **Unzip** the downloaded `netcdf_zip` file to extract the `.nc` (NetCDF) file.
2.  **Rename** the extracted `.nc` file to `cams_data_kemayoran.nc`.
3.  Ensure this file is located in the **same directory** as the `03_skewt_hodo.py` script.

#### Step 4: Run the Analysis and Generate Outputs

Execute the main analysis script. This will read the `cams_data_kemayoran.nc` file and generate the outputs.

```bash
python code/03_skewt_hodo.py
```


### Outputs

The final script produces two types of outputs for each forecast time step:

1.  **Image Files (`.png`):** A plot containing the Skew-T Log-P diagram, parcel path, and a Hodograph.

      * **Filename example:** `skewt_hodograph_kemayoran_jakarta_initial_20231026_00z_forecast_20231027_12z.png`

2.  **Text Report (`.txt`):** A detailed report containing analysis on:

      * Surface-based inversions
      * Surface layer stability and lapse rate
      * Hodograph analysis (low-level ventilation and bulk shear)
      * Convective potential (CAPE and CIN)
      * **Filename example:** `stability_analysis_report_initial_20231026_00z.txt`

### File repository

The final products are kept in the following link, archived by date of production:
* **Website:** [https://cews.bmkg.go.id/tempatirk/Atmospheric_Stability/](https://cews.bmkg.go.id/tempatirk/Atmospheric_Stability/)
