### CLEAR WORKSPACE ###
rm(list = ls())
gc()

# Get yesterday's date in YYYY-MM-DD format
today <- format(Sys.Date(), "%Y-%m-%d")

# Create and print the date line for the Python request dictionary.
# The print() function also returns the string, which is then used in writeLines.
date_line <- print(paste0('    "date": ["', today, '/', today, '"],'))

# Open the output file for writing the Python script.
# Note: The filename is kept as per the original script, but the content it generates has changed.
fout <- file("02_download_meteo.py")

# Write the new Python script content to the file
writeLines(c(
  '#!/usr/bin/env python',
  '',
  'import cdsapi',
  '',
  'dataset = "cams-global-atmospheric-composition-forecasts"',
  'request = {',
  '    "pressure_level": [',
  '        "1", "2", "3",',
  '        "5", "7", "10",',
  '        "20", "30", "50",',
  '        "70", "100", "150",',
  '        "200", "250", "300",',
  '        "400", "500", "600",',
  '        "700", "800", "850",',
  '        "900", "925", "950",',
  '        "1000"',
  '    ],',
  date_line,
  '    "time": ["00:00"],',
  '    "leadtime_hour": [',
  '        "0",',
  '        "6",',
  '        "12",',
  '        "18",',
  '        "24",',
  '        "30",',
  '        "36",',
  '        "42",',
  '        "48",',
  '        "54",',
  '        "60",',
  '        "66",',
  '        "72",',
  '        "78",',
  '        "84",',
  '        "90",',
  '        "96"',
  '    ],',
  '    "type": ["forecast"],',
  '    "data_format": "netcdf_zip",',
  '    "variable": [',
  '        "specific_humidity",',
  '        "temperature",',
  '        "u_component_of_wind",',
  '        "v_component_of_wind"',
  '    ],',
  '    "area": [-6.1, 106.8, -6.2, 106.9]',
  '}',
  '',
  'client = cdsapi.Client()',
  'client.retrieve(dataset, request).download()'
),
fout)

# Close the file connection for good practice
close(fout)
