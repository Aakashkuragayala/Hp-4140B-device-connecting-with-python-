import csv

def extract_current_voltage(measurement_str):
    """Extracts the current and voltage values from a measurement string.

    Args:
        measurement_str: A string containing the measurement data.

    Returns:
        A tuple of two strings, containing the current and voltage values as strings.
    """
    # Split the measurement string using a comma as the separator.
    parts = measurement_str.split(",")

    if len(parts) == 2:
        # Extract the first part as current (skipping the first two characters)
        current_str = parts[0][2:]

        # Extract the second part as voltage (remove 'A' and leading/trailing whitespace)
        voltage_str = parts[1].replace("A", "").strip()

        return current_str, voltage_str
    else:
        raise ValueError("Invalid measurement string format")

# Create lists to store the current and voltage values as strings
current_values = []
voltage_values = []

# Open the CSV file containing the measurement data.
with open("hp4140b_data.csv", mode='r', newline='') as csv_file:
    # Create a CSV reader object.
    reader = csv.DictReader(csv_file)

    # Iterate over the rows in the CSV file.
    for row in reader:
        # Extract the current and voltage values from the measurement string.
        current, voltage = extract_current_voltage(row['Measurement'])

        # Append the values to their respective lists
        current_values.append(current)
        voltage_values.append(voltage)

# Now you have two lists: current_values and voltage_values containing the current and voltage values as strings.

# Write the current and voltage values to a new CSV file.
output_filename = "current_voltage_values.csv"
with open(output_filename, mode='w', newline='') as output_csv_file:
    fieldnames = ['Current', 'Voltage']
    writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Write the values to the CSV file
    for current, voltage in zip(current_values, voltage_values):
        writer.writerow({'Current': current, 'Voltage': voltage})

print(f"Current and voltage values saved to {output_filename}")
