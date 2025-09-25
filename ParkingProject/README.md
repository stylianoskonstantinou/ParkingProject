# Parking Management GUI (Python)

This is a parking management application with a graphical user interface built in Python using Tkinter. It was developed as a master's project at the University of Thessaly.

## Detailed Description of Features

The application includes:

- Management of parking spaces: The system manages 20 spaces, 5 of which are for long-term parking and 15 for hourly. Each space has a status (occupied or free).
- Vehicle entry: The user can enter a car for either hourly or long-term parking. If a car already has a long-term parking space, it returns to it.
- Vehicle exit: Records the exit of a car and calculates the charge based on the parking duration. Hourly spots are charged €2 per hour (rounded up). Long-term spots have a monthly fee of €50.
- Space rental: There is an option to rent a long-term parking space for one month at a flat rate of €50.
- Saving & Loading data: All data are saved in a JSON file (`parking_data.json`) and loaded on startup.
- Viewing space status: The user can graphically see which spaces are occupied or free, with different colors for each type of space.
- List of parked cars: A list appears with license plates and whether they are hourly or permanent customers.
- Cash register for the day: Displays the total collections for the current day.
- Best customer: Shows the customer(s) who paid the most.
- Renewal management: Automatically renews expired long-term rentals with the applicable charge.

## Execution Instructions

1. Ensure that you have Python 3.8+ installed.
2. Install Tkinter (if not already available):

   ```
   pip install tk
   ```

   On some Linux systems, you might need:

   ```
   sudo apt-get install python3-tk
   ```

3. Download all project files (ParkingProject.py, parking_data.json, README.md, requirements.txt) from the repository.
4. If required, install the application's dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Run the application using the command:

   ```
   python ParkingProject.py
   ```

   or

   ```
   python3 ParkingProject.py
   ```

## Program Files

- ParkingProject.py: Main application code.
- parking_data.json: Data storage file.
- README.md: This file.
- requirements.txt: Required libraries for the application.

## Author

Stylianos Konstantinou  
Postgraduate student in Applied Informatics, Department of Electrical and Computer Engineering, University of Thessaly.


