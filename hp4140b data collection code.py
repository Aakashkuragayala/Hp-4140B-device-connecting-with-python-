import pyvisa
import time
import csv
import traceback

# Replace 'GPIB0::10::INSTR' with your HP 4140B's GPIB address
instrument_address = 'GPIB0::17::17::INSTR'

# Initialize VISA resource manager
rm = pyvisa.ResourceManager()
rm.timeout = 5000  # Set timeout to 100 seconds (adjust as needed)

try:
    # Open a connection to the instrument
    instrument = rm.open_resource(instrument_address, write_termination='\n', read_termination='\n')

    # Configure instrument settings (customize these for your measurements)
    instrument.write("VOLT:RANG 02")  # Set voltage range to 10V
    instrument.write("CURR:RANG 1E-6")  # Set current range to 1µA

    # Create a CSV file to save the data
    filename = "hp4140b_data.csv"
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ['Time', 'Measurement']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(10):  # Perform 10 measurements
            # Measure voltage and current
            instrument.write("MEAS?")
            measurement_str = instrument.read()

            # Get the current time
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Write the measurement and time to the CSV file
            writer.writerow({'Time': timestamp, 'Measurement': measurement_str})

            # Wait for 0.1 seconds before taking the next measurement
            time.sleep(0.1)

except pyvisa.errors.VisaIOError as e:
    print(f"Measurement failed with error: {e}")
    traceback.print_exc()

finally:
    # Close the instrument connection
    instrument.close()
