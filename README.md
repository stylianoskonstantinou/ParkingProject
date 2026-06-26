# Parking Management System (Python & Tkinter)

This is a parking management application with a graphical user interface built in Python using Tkinter. The project was developed as part of the Master's Program in Applied Informatics at the University of Thessaly.

## Key Features

- **Parking Space Management:** Manages 20 parking spaces, including 5 long-term and 15 hourly parking spots.
- **Vehicle Entry:** Registers incoming vehicles and automatically returns long-term customers to their assigned parking space.
- **Vehicle Exit:** Calculates parking fees based on the parking duration.
- **Hourly Parking:** Charges €2 per hour (rounded up to the nearest hour).
- **Long-Term Parking:** Supports monthly parking rentals at a fixed cost of €50.
- **Automatic Rental Renewal:** Automatically renews expired long-term rentals and applies the monthly fee.
- **Parking Space Status:** Displays a graphical overview of occupied and available parking spaces.
- **Parked Vehicles List:** Displays all currently parked vehicles and their parking type.
- **Daily Revenue Report:** Shows the total revenue collected during the current day.
- **Best Customer Report:** Displays the customer(s) with the highest total spending.
- **Data Persistence:** Stores and loads parking data using a JSON file.

## Technologies

- Python 3
- Tkinter
- JSON
- Object-Oriented Programming (OOP)

## How to Run

Clone the repository:

```bash
git clone https://github.com/stylianoskonstantinou/ParkingProject
cd ParkingProject
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python ParkingProject.py
```

or

```bash
python3 ParkingProject.py
```

## Project Files

- `ParkingProject.py` – Main application source code.
- `parking_data.json` – Stores parking spaces, transactions and revenue.
- `README.md` – Project documentation.
- `requirements.txt` – Required Python libraries.

## Notes

Tkinter is included with most Python installations.

If it is missing, install it with:

```bash
pip install tk
```

On some Linux distributions:

```bash
sudo apt-get install python3-tk
```

## Author

**Stylianos Konstantinou**

M.Sc. in Applied Informatics  
University of Thessaly

## License

This project is available for educational purposes.