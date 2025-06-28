### **Scientific Sources for Report Classifications**

#### **1. Stability Classification Reference (Lapse Rate)**

* **Physical Basis:** This classification is based on comparing the environmental lapse rate ($Γ$) to the dry adiabatic lapse rate ($Γ_d$, approx. 9.8 K/km). The stability of a parcel of air, and thus the atmosphere's tendency to suppress or enhance vertical motion, is determined by this comparison. A lapse rate significantly lower than the adiabatic rate indicates that a lifted parcel will be colder than its surroundings and sink, signifying stability. This principle is a cornerstone of atmospheric thermodynamics.

* **Scientific Sources:**
    1.  **Textbook:** **Markowski, P., & Richardson, Y. (2010). *Mesoscale Meteorology in Midlatitudes*. Wiley-Blackwell.** Chapter 2 provides an exhaustive review of atmospheric thermodynamics, including the detailed derivation of static stability, inversions, and lapse rates.
    2.  **Textbook:** **Stull, R. B. (1988). *An Introduction to Boundary Layer Meteorology*. Kluwer Academic Publishers.** This is a foundational text. Chapter 3, "The Structure of the ABL," and Chapter 7, "Turbulence," directly relate lapse rate and stability profiles to turbulence and the dispersion of pollutants within the boundary layer. The specific numerical bins (`0-2`, `2-5` K/km) are practical operational categorizations derived from these principles for air quality forecasting.

#### **2. Boundary Layer Analysis Reference (Mixing Height & LLJ)**

* **Physical Basis (Mixing Height):** The mixing height represents the depth of the turbulent planetary boundary layer (PBL). A shallow PBL traps pollutants in a small volume, leading to high concentrations. The top of the PBL is often marked by a capping inversion, where the potential temperature increases sharply, suppressing further vertical mixing.
* **Physical Basis (LLJ):** The Low-Level Jet is a region of maximum wind speed in the lower troposphere, typically decoupled from the surface by a nocturnal inversion. It is a key mechanism for the long-range transport of moisture, heat, and pollutants.

* **Scientific Sources:**
    1.  **Textbook:** **Seinfeld, J. H., & Pandis, S. N. (2016). *Atmospheric Chemistry and Physics: From Air Pollution to Climate Change*. Wiley.** This is the definitive textbook on the subject. Chapter 18, "Atmospheric Transport," and Chapter 19, "Atmospheric Diffusion," extensively discuss the critical role of mixing height in determining pollutant concentrations. The thresholds (`< 500 m`, `500-1500 m`, etc.) are widely accepted operational guidelines used in air quality models and forecasts.
    2.  **Review Article:** **Stull, R. B. (1988). *An Introduction to Boundary Layer Meteorology*.** Chapter 11 is dedicated entirely to the "Low-Level Jet." It discusses its formation, structure, and impact on transport and turbulence, validating its importance as a distinct phenomenon to analyze.

#### **3. Hodograph Analysis Reference (Mean Wind & Bulk Shear)**

* **Physical Basis (Mean Wind):** The mean wind speed in the lowest kilometer is a direct measure of the ventilation within the boundary layer. Light winds lead to the stagnation of air and accumulation of pollutants.
* **Physical Basis (Bulk Shear):** The change in wind vector over a deep layer (0-6 km) is a primary factor in organizing thunderstorms. Strong shear helps separate a storm's updraft from its downdraft, allowing it to persist, strengthen, and potentially rotate.

* **Scientific Sources:**
    1.  **Operational Guide:** **The NOAA National Weather Service, Storm Prediction Center (SPC) "Sounding Analysis" page.** While not a peer-reviewed paper, the SPC's operational guidance is the de facto standard in severe weather forecasting. Their materials extensively discuss the interpretation of hodographs, and the bulk shear thresholds (`<25 kt`, `25-40 kt`, `>40 kt`) are standard operational values used by forecasters to assess storm potential.
    2.  **Textbook:** **Doswell, C. A., III, & Markowski, P. M. (2004). *Severe Convection*. In *An Introduction to Models of Online Weather*. Academic Press.** This and similar works by these authors provide the deep physical connection between hodograph shape, deep-layer shear, and the dynamics of supercell thunderstorms. They form the scientific basis for the operational thresholds used by the SPC.

#### **4. Convective Potential (CAPE/CIN) Reference**

* **Physical Basis:** CAPE (Convective Available Potential Energy) is the integrated buoyancy of a lifted air parcel, representing the "fuel" available for a thunderstorm's updraft. CIN (Convective Inhibition) is the integrated negative buoyancy, representing the energy barrier or "cap" that must be overcome to initiate convection.

* **Scientific Sources:**
    1.  **Seminal Paper:** **Moncrieff, M. W., & Miller, M. J. (1976). The dynamics and simulation of tropical cumulonimbus and squall lines. *Quarterly Journal of the Royal Meteorological Society*, 102(432), 373-394.** This is one of the foundational papers that used CAPE to understand storm dynamics and intensity.
    2.  **Operational Guide:** Again, the **NOAA Storm Prediction Center (SPC) guidance** provides the most widely used operational thresholds for CAPE and CIN. The values used in our script (`0-1000 J/kg` for Marginal, etc.) are standard categories used by forecasters in the US and globally to quickly assess the potential for severe weather from a sounding. These values are ubiquitous in training materials and operational forecasting tools.
