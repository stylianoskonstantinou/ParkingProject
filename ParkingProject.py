# Εισαγωγή βιβλιοθήκης tkinter για δημιουργία GUI 
import tkinter as tk  # Βασική βιβλιοθήκη για τη δημιουργία παραθύρων 
from tkinter import messagebox, simpledialog, ttk  # Επιπλέον στοιχεία GUI πχ πλαίσια διαλόγου 

# Εισαγωγή βιβλιοθηκών για επεξεργασία δεδομένων JSON, ημερομηνιών και αρχείων
import json  # Βιβλιοθήκη με αρχεία JSON
from datetime import datetime, timedelta  # Βιβλιοθήκες με ημερομηνίες και ώρες
import os  # Βιβλιοθήκη με το σύστημα αρχείων και λειτουργίες συστήματος
import math  # Βιβλιοθήκη για μαθηματικές λειτουργίες και πράξεις


# Δεδομένα για θέσεις πάρκινγκ και συναλλαγές
parking_data = {
    "parking_spots": [  # Λίστα με όλες τις διαθέσιμες θέσεις (20)
        # 5 θέσεις για long term στάθμευση, μη κατειλημμένες
        {"type": "long_term", "occupied": False, "car": None}, 
        {"type": "long_term", "occupied": False, "car": None},  
        {"type": "long_term", "occupied": False, "car": None},  
        {"type": "long_term", "occupied": False, "car": None},  
        {"type": "long_term", "occupied": False, "car": None}, 

        # 15 θέσεις για hourly στάθμευση, μη κατειλημμένες
        {"type": "hourly", "occupied": False, "car": None},  
        {"type": "hourly", "occupied": False, "car": None},  
        {"type": "hourly", "occupied": False, "car": None},  
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None},
        {"type": "hourly", "occupied": False, "car": None}
    ],
    "transactions": [],  # Λίστα για τις συναλλαγές (π.χ. είσοδος/έξοδος αυτοκινήτου)
    "revenue": 0.0  # Αρχικό ποσό εσόδων (0 ευρώ). Θα αυξηθεί με τις συναλλαγές
}

# Δημιουργούμε ένα αρχείο "parking_data.json" αν δεν υπάρχει ήδη
if not os.path.exists('parking_data.json'):  # Έλεγχος αν το αρχείο υπάρχει στον φάκελο
    with open('parking_data.json', 'w', encoding='utf-8') as file:
        json.dump(parking_data, file, indent=4, ensure_ascii=False)  # Δημιουργία και αποθήκευση δεδομένων

# Ανάγνωση του αρχείου JSON με κωδικοποίηση UTF-8
try:
    with open('parking_data.json', 'r', encoding='utf-8') as file:  # Άνοιγμα αρχείου για ανάγνωση
        data = json.load(file)  # Φόρτωση δεδομένων από το αρχείο JSON
except UnicodeDecodeError as e:  # Διαχείριση σφαλμάτων κωδικοποίησης
    print(f"Σφάλμα κατά την ανάγνωση του JSON: {e}")
    exit(1)  # Τερματισμός προγράμματος αν υπάρχει σφάλμα

# Επαναποθήκευση για να εξασφαλίσουμε τη σωστή μορφοποίηση
with open('parking_data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)  # Επαναποθήκευση δεδομένων στο αρχείο

print("Το αρχείο JSON δημιουργήθηκε/ενημερώθηκε με επιτυχία!")  # Μήνυμα επιτυχίας


class Manager:
    def __init__(self):
        # Δημιουργούμε 5 θέσεις για long term parking
        self.parking_spots = [{"type": "long_term", "occupied": False, "car": None} for _ in range(5)]
        # Προσθέτουμε 15 θέσεις για hourly parking
        self.parking_spots += [{"type": "hourly", "occupied": False, "car": None} for _ in range(15)]
        
        # Αρχικοποίηση λίστας συναλλαγών
        self.transactions = []
        
        # Αρχικοποίηση εσόδων στα 0 ευρώ
        self.revenue = 0.0
        
        # Κλήση της συνάρτησης για ανανέωση μακροχρόνιας στάθμευσης κατά το φόρτωμα της εφαρμογής (σε περίπτωση που περάσει ένας μήνας)
        self.check_long_term_renewals()
        
        # Φόρτωση δεδομένων από το αρχείο JSON, αν υπάρχει
        self.load_data()


    def load_data(self):
        """
        Φορτώνει δεδομένα από το αρχείο "parking_data.json".
        Αν το αρχείο δεν υπάρχει, δημιουργείται νέο αρχείο με την τρέχουσα δομή.
        """
        try:
            # Προσπαθούμε να διαβάσουμε τα δεδομένα από το αρχείο "parking_data.json"
            with open("parking_data.json", "r") as file:
                data = json.load(file)  # Φόρτωση δεδομένων JSON
                # Ενημέρωση των θέσεων πάρκινγκ από τα δεδομένα του αρχείου
                self.parking_spots = data["parking_spots"]
                # Ενημέρωση της λίστας συναλλαγών από τα δεδομένα του αρχείου
                self.transactions = data["transactions"]
                # Ενημέρωση των συνολικών εσόδων από τα δεδομένα του αρχείου
                self.revenue = data["revenue"]
        except FileNotFoundError:
            # Αν το αρχείο δεν υπάρχει, το δημιουργούμε καλώντας την `save_data`
            self.save_data()
        except json.JSONDecodeError:
            # Αν υπάρχει πρόβλημα στη μορφή του αρχείου JSON, εμφανίζουμε μήνυμα σφάλματος
            print("Σφάλμα στην ανάγνωση των δεδομένων από το αρχείο.")
        except Exception as e:
            # Γενική διαχείριση σφαλμάτων (για κάθε περίπτωση)
            print(f"Σφάλμα κατά την φόρτωση των δεδομένων: {e}")


    def save_data(self):
        """
        Αποθηκεύει τα δεδομένα (θέσεις πάρκινγκ, συναλλαγές, έσοδα) στο αρχείο "parking_data.json".
        """
        try:
            # Ετοιμάζουμε ένα λεξικό με όλα τα δεδομένα που θέλουμε να αποθηκεύσουμε
            data = {
                "parking_spots": self.parking_spots,  # Θέσεις πάρκινγκ
                "transactions": self.transactions,  # Συναλλαγές
                "revenue": self.revenue,  # Συνολικά έσοδα
            }
            # Ανοίγουμε το αρχείο "parking_data.json" για εγγραφή και αποθηκεύουμε τα δεδομένα
            with open("parking_data.json", "w", encoding="utf-8") as file:
                # Χρησιμοποιούμε json.dump για να έχουν όμορφο format τα δεδομένα 
                json.dump(data, file, indent=4, ensure_ascii=False)  
                # indent=4 για να έχουμε όμορφη δομή στο JSON και ensure_ascii=False για υποστήριξη UTF-8
        except Exception as e:
            # Σε περίπτωση σφάλματος κατά την αποθήκευση, το εκτυπώνουμε
            print(f"Σφάλμα κατά την αποθήκευση των δεδομένων: {e}")


    def show_best_customers(self):
        """
        Εμφανίζει τον καλύτερο πελάτη ή τους καλύτερους πελάτες σε περίπτωση ισοβαθμίας με βάση τα χρήματα που έχουν πληρώσει.
        Δημιουργείται παράθυρο με τις πληροφορίες.
        """
        customer_revenue = {}  # Λεξικό για να κρατάμε τα έσοδα των πελατών

        # Υπολογισμός εσόδων για κάθε πελάτη από τις συναλλαγές
        for transactions in self.transactions:
            if "cost" in transactions:  # Ελέγχει αν υπάρχει κόστος στη συναλλαγή
                license_plate = transactions["license_plate"]
                cost = transactions["cost"]

                # Αν η πινακίδα δεν υπάρχει στο λεξικό, κάνουμε εγγραφή
                if license_plate not in customer_revenue:
                    customer_revenue[license_plate] = {'revenue': 0.0, 'name': None}
                customer_revenue[license_plate]['revenue'] += cost  # Προσθέτουμε το κόστος στα συνολικά έσοδα

                # Ψάχνουμε να βρούμε το όνομα του ιδιοκτήτη για την πινακίδα
                for spot in self.parking_spots:
                    if spot["occupied"] and spot["car"] and spot["car"]["license_plate"] == license_plate:
                        customer_revenue[license_plate]['name'] = spot["car"].get("owner_name", "Άγνωστο")
                        break  # Σταματάμε όταν βρούμε το όνομα

        if customer_revenue:  # Αν έχουμε δεδομένα πελατών
            # Βρίσκουμε τα περισσότερα έσοδα από όλους τους πελάτες
            max_revenue = max(customer_revenue[l_p]['revenue'] for l_p in customer_revenue)

            # Βρίσκουμε τους πελάτες με τα περισσότερα έσοδα
            best_customers = [
                (l_p, customer_revenue[l_p]['name'])
                for l_p, data in customer_revenue.items() if data['revenue'] == max_revenue
            ]

            # Δημιουργία νέου παραθύρου για εμφάνιση δεδομένων
            window = tk.Toplevel()  # Δημιουργία νέου παραθύρου για την εμφάνιση των καλύτερων πελατών
            window.title("Καλύτεροι Πελάτες")  # Ορισμός τίτλου παραθύρου
            window.config(bg="#f7f7f7")  # Ορισμός χρώματος φόντου παραθύρου

            # Ετικέτα τίτλου
            tk.Label(
                window,
                text="Καλύτεροι Πελάτες",
                font=("Helvetica", 20, "bold"),  # Χρησιμοποιούμε γραμματοσειρά Helvetica, μέγεθος 16, bold
                bg="#f7f7f7"  # Το χρώμα φόντου της ετικέτας είναι το ίδιο με το παράθυρο
            ).pack(pady=10)  # Προσθήκη padding πάνω και κάτω από την ετικέτα

            if len(best_customers) == 1:  # Αν υπάρχει μόνο ένας καλύτερος πελάτης
                license_plate, name = best_customers[0]
                tk.Label(
                    window,
                    text=f"Ο καλύτερος πελάτης είναι:",  # Κείμενο που εμφανίζεται αν υπάρχει μόνο ένας καλύτερος πελάτης
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                # Εμφάνιση λεπτομερειών του πελάτη
                tk.Label(
                    window,
                    text=f"Όνομα: {name}\nΑρ. Κυκλοφορίας: {license_plate}\nΈσοδα: {max_revenue}€",  # Εμφανίζει το όνομα, αριθμό κυκλοφορίας και έσοδα
                    font=("Arial", 12),
                    bg="#f7f7f7"
                ).pack(pady=10)
            else:  # Αν υπάρχουν πολλοί καλύτεροι πελάτες
                tk.Label(
                    window,
                    text=f"Οι καλύτεροι πελάτες είναι ({len(best_customers)} συνολικά):",  # Εμφανίζει τον αριθμό των καλύτερων πελατών
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                # Δημιουργία πλαισίου για τη λίστα πελατών
                frame = tk.Frame(window, bg="#f7f7f7")  # Δημιουργούμε ένα πλαίσιο για τη λίστα πελατών
                frame.pack(pady=10)

                # Εμφάνιση όλων των καλύτερων πελατών
                for l_p, name in best_customers:
                    tk.Label(
                        frame,
                        text=f"{name} (Αρ. Κυκλοφορίας: {l_p})",  # Εμφανίζει το όνομα και τον αριθμό κυκλοφορίας κάθε πελάτη
                        font=("Arial", 12),
                        bg="#f7f7f7"
                    ).pack(anchor="w", padx=10)  # Προσθήκη padding αριστερά και δεξιά από την ετικέτα

                # Εμφάνιση του ποσού που πλήρωσε κάθε καλύτερος πελάτης
                tk.Label(
                    window,
                    text=f"Κάθε ένας πλήρωσε: {max_revenue}€",  # Εμφανίζει το ποσό που πλήρωσε κάθε καλύτερος πελάτης
                    font=("Arial", 12, "bold"),
                    bg="#f7f7f7"
                ).pack(pady=10)

            # Κουμπί για κλείσιμο του παραθύρου
            tk.Button(
                window,
                text="Κλείσιμο",  # Κείμενο του κουμπιού
                font=("Arial", 12),
                command=window.destroy  # Εντολή για κλείσιμο του παραθύρου όταν πατηθεί το κουμπί
            ).pack(pady=10)
        else:  # Αν δεν υπάρχουν καταχωρήσεις πελατών
            messagebox.showinfo("Καλύτερος Πελάτης", "Δεν υπάρχουν καταχωρήσεις πελατών.")  # Εμφάνιση μηνύματος ότι δεν υπάρχουν πελάτες



    def check_long_term_renewals(self):
        """
        Ελέγχει αν έχουν λήξει οι μηνιαίες (μακροχρόνιες) θέσεις.
        Αν κάποια έχει ξεπεράσει την ημερομηνία λήξης, ανανεώνει για +1 μήνα
        και χρεώνει αυτόματα 50€.
        """
        now = datetime.now()  # Σημερινή ημερομηνία/ώρα

        for spot in self.parking_spots:
            # Θέλουμε μόνο κατειλημμένες μακροχρόνιες θέσεις
            if spot["occupied"] and spot["type"] == "long_term":
                # Διαβάζουμε την ημερομηνία λήξης της ενοικίασης
                rental_end_str = spot["car"]["rental_end"]
                rental_end = datetime.fromisoformat(rental_end_str)

                # Αν η τρέχουσα ημερομηνία/ώρα έχει ξεπεράσει την ημερομηνία λήξης
                if now >= rental_end:
                    # Ορίζουμε νέες ημερομηνίες (από σήμερα + 30 μέρες)
                    new_start = now
                    new_end = new_start + timedelta(days=30)

                    # Ανανεώνουμε τις ημερομηνίες στο spot["car"]
                    spot["car"]["rental_start"] = new_start.isoformat()
                    spot["car"]["rental_end"] = new_end.isoformat()

                    # Χρεώνουμε 50€ για την ανανέωση της ενοικίασης
                    cost = 50
                    self.revenue += cost  # Προσθέτουμε το κόστος στα συνολικά έσοδα

                    # Προσθέτουμε συναλλαγή τύπου "rental_renewal" στη λίστα συναλλαγών
                    self.transactions.append({
                        "type": "rental_renewal",
                        "license_plate": spot["car"]["license_plate"],
                        "owner_name": spot["car"]["owner_name"],
                        "time": new_start.isoformat(),  # Πότε έγινε η ανανέωση
                        "cost": cost  # Κόστος ανανέωσης
                    })

                    # Αποθηκεύουμε τα ενημερωμένα δεδομένα στο αρχείο JSON
                    self.save_data()



    def show_daily_revenue(self):
        """
        Εμφανίζει τις συνολικές εισπράξεις της ημέρας αναλυτικά,
        μόνο για τις συναλλαγές που έγιναν σήμερα (ημέρα πληρωμής).
        """
        self.check_long_term_renewals()  # Ελέγχουμε και ανανεώνουμε μακροχρόνιες θέσεις αν χρειάζεται
        
        # Παίρνουμε τη σημερινή ημερομηνία
        today = datetime.now().date()  # Σημερινή ημερομηνία χωρίς ώρα

        # Φιλτράρουμε τις σημερινές συναλλαγές που έχουν κόστος
        daily_transactions = []  # Λίστα για αποθήκευση σημερινών συναλλαγών
        for transaction in self.transactions:
            if "cost" in transaction:  # Έχει κόστος
                # Μετατρέπουμε την ώρα της συναλλαγής από string σε datetime
                transaction_time = datetime.fromisoformat(transaction["time"])
                # Συγκρίνουμε μόνο την ημερομηνία (όχι ώρα)
                if transaction_time.date() == today:
                    daily_transactions.append(transaction)  # Προσθέτουμε τη συναλλαγή στη λίστα

        # Υπολογισμός συνολικών εσόδων της ημέρας 
        total_revenue = sum(t["cost"] for t in daily_transactions)  # Συνολικά έσοδα της ημέρας

        # Δημιουργία παραθύρου
        window = tk.Toplevel()  
        window.title("Ταμείο Ημέρας")  # Ορισμός τίτλου παραθύρου
        window.config(bg="#f7f7f7")  # Ορισμός χρώματος φόντου παραθύρου

        # Τίτλος
        tk.Label(
            window,
            text="Ταμείο Ημέρας",
            font=("Helvetica", 20, "bold"),  # Γραμματοσειρά: Helvetica, μέγεθος: 16, στυλ: bold
            bg="#f7f7f7"
        ).pack(pady=10)  # Προσθήκη απόστασης πάνω και κάτω από την ετικέτα

        # Εμφάνιση συνολικών εσόδων της ημέρας
        tk.Label(
            window,
            text="Οι συνολικές εισπράξεις της ημέρας είναι:",
            font=("Arial", 14),
            bg="#f7f7f7"
        ).pack(pady=5)

        tk.Label(
            window,
            text=f"{total_revenue:.2f}€",  # Εμφάνιση συνολικών εσόδων με δύο δεκαδικά ψηφία
            font=("Arial", 18, "bold"),
            bg="#f7f7f7",
            fg="green"
        ).pack(pady=10)

        # Αναλυτική παρουσίαση μόνο των σημερινών συναλλαγών
        tk.Label(
            window,
            text="Αναλυτική Παρουσίαση Συναλλαγών Σήμερα",
            font=("Helvetica", 14, "bold"),
            bg="#f7f7f7"
        ).pack(pady=10)

        # Δημιουργία πλαισίου για εμφάνιση των συναλλαγών
        transaction_frame = tk.Frame(window, bg="#f7f7f7")
        transaction_frame.pack(fill="both", expand=True, padx=10, pady=5)

        if daily_transactions:
            for transaction in daily_transactions:
                # Μετατρέπουμε ξανά την ημερομηνία/ώρα για πιο όμορφη εμφάνιση
                time_str = datetime.fromisoformat(transaction["time"]).strftime('%d/%m/%Y %H:%M:%S')
                license_plate = transaction["license_plate"]
                cost = transaction["cost"]

                tk.Label(
                    transaction_frame,
                    text=f"{time_str} | {license_plate} | {cost:.2f}€",  # Εμφάνιση λεπτομερειών συναλλαγής
                    font=("Arial", 12),
                    bg="#f7f7f7"
                ).pack(anchor="w", pady=2)
        else:
            # Εάν δεν υπάρχει καμία σημερινή συναλλαγή
            tk.Label(
                transaction_frame,
                text="Δεν πραγματοποιήθηκαν πληρωμές σήμερα.",  # Μήνυμα αν δεν υπάρχουν συναλλαγές σήμερα
                font=("Arial", 12, "bold"),
                bg="#f7f7f7",
                fg="red"
            ).pack(anchor="w", pady=2)

        # Κουμπί για κλείσιμο του παραθύρου
        tk.Button(
            window,
            text="Κλείσιμο",
            font=("Arial", 12),
            command=window.destroy  # Εντολή για κλείσιμο του παραθύρου όταν πατηθεί το κουμπί
        ).pack(pady=10)


    def enter_car(self, license_plate):
        """Εισάγει ένα αυτοκίνητο για ωριαία στάθμευση εκτός αν είναι μόνιμος όπου γυρίζει στη θέση του"""
        
        # Έλεγχος αν το αυτοκίνητο βρίσκεται ήδη σε μακροχρόνια θέση για να επιστρέψει εκεί
        for i, spot in enumerate(self.parking_spots):
            if spot["occupied"] and spot["car"]["license_plate"] == license_plate:
                # Αν το αυτοκίνητο βρίσκεται σε μακροχρόνια θέση και είναι προσωρινά κενό
                if spot["type"] == "long_term" and spot.get("temporarily_vacant"):
                    spot["temporarily_vacant"] = False  # Επαναφορά της θέσης στο κανονικό της καθεστώς

                    # Δημιουργία παραθύρου επιτυχίας
                    window = tk.Toplevel()
                    window.title("Επιτυχής Επιστροφή")
                    window.config(bg="#f7f7f7")

                    tk.Label(
                        window,
                        text="Επιτυχής Επιστροφή Αυτοκινήτου",
                        font=("Helvetica", 20, "bold"),
                        bg="#f7f7f7"
                    ).pack(pady=10)

                    tk.Label(
                        window,
                        text=f"Αρ. Κυκλοφορίας: {license_plate}",
                        font=("Arial", 14),
                        bg="#f7f7f7"
                    ).pack(pady=5)

                    tk.Label(
                        window,
                        text=f"Αριθμός Θέσης: {i + 1}",  # Παρουσιάζουμε τη θέση του αυτοκινήτου
                        font=("Arial", 14),
                        bg="#f7f7f7"
                    ).pack(pady=5)

                    tk.Label(
                        window,
                        text="Το αυτοκίνητο επιστρέφει στην μακροχρόνια θέση του.",
                        font=("Arial", 12, "italic"),
                        bg="#f7f7f7",
                        fg="blue"
                    ).pack(pady=5)

                    # Κουμπί για κλείσιμο του παραθύρου
                    tk.Button(
                        window,
                        text="ΟΚ",
                        font=("Arial", 12),
                        command=window.destroy
                    ).pack(pady=10)

                    self.save_data()  # Αποθήκευση των δεδομένων
                    return  # Επιστρέφουμε αφού βρούμε το αυτοκίνητο

        # Αν δεν βρεθεί το αυτοκίνητο στην μακροχρόνια θέση, αναζητούμε ωριαία θέση
        for i, spot in enumerate(self.parking_spots):
            if not spot["occupied"] and spot["type"] == "hourly":
                # Καταγραφή της ώρας εισόδου του αυτοκινήτου
                entry_time = datetime.now()
                spot["occupied"] = True  # Ορίζουμε τη θέση ως κατειλημμένη
                spot["car"] = {
                    "license_plate": license_plate,  # Αριθμός πινακίδας
                    "entry_time": entry_time.isoformat()  # Ώρα εισόδου
                }

                # Δημιουργία παραθύρου επιτυχίας για ωριαία στάθμευση
                window = tk.Toplevel()
                window.title("Επιτυχής Στάθμευση")
                window.config(bg="#f7f7f7")

                tk.Label(
                    window,
                    text="Επιτυχής Στάθμευση Αυτοκινήτου",
                    font=("Helvetica", 16, "bold"),
                    bg="#f7f7f7"
                ).pack(pady=10)

                tk.Label(
                    window,
                    text=f"Αρ. Κυκλοφορίας: {license_plate}",
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                tk.Label(
                    window,
                    text=f"Αριθμός Θέσης: {i + 1}",  # Παρουσιάζουμε τη θέση του αυτοκινήτου
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                tk.Label(
                    window,
                    text="Το αυτοκίνητο στάθμευσε ωριαία στη θέση.",
                    font=("Arial", 12, "italic"),
                    bg="#f7f7f7",
                    fg="green"
                ).pack(pady=5)

                # Κουμπί για κλείσιμο του παραθύρου
                tk.Button(
                    window,
                    text="ΟΚ",
                    font=("Arial", 12),
                    command=window.destroy
                ).pack(pady=10)

                self.save_data()  # Αποθήκευση των δεδομένων
                return  # Επιστρέφουμε αφού βρούμε διαθέσιμη θέση για στάθμευση

        # Αν δεν βρεθεί διαθέσιμη θέση για στάθμευση, εμφανίζεται μήνυμα αποτυχίας
        fail_window = tk.Toplevel()
        fail_window.title("Αποτυχία Στάθμευσης")
        fail_window.config(bg="#f7f7f7")

        tk.Label(
            fail_window,
            text="Δεν υπάρχουν διαθέσιμες θέσεις στάθμευσης.",
            font=("Arial", 14, "bold"),
            bg="#f7f7f7",
            fg="red"  # Χρωματισμός του κειμένου σε κόκκινο για αποτυχία
        ).pack(pady=20)

        # Κουμπί κλεισίματος παραθύρου αποτυχίας
        tk.Button(
            fail_window,
            text="ΟΚ",
            font=("Arial", 12),
            command=fail_window.destroy  # Κλείσιμο του παραθύρου
        ).pack(pady=10)


    def exit_car(self, license_plate):
        """Καταγράφει την έξοδο ενός αυτοκινήτου."""

        # Αναζητούμε το αυτοκίνητο στο χώρο στάθμευσης
        for i, spot in enumerate(self.parking_spots):
            if spot["occupied"] and spot["car"]["license_plate"] == license_plate:
                
                # Αν το αυτοκίνητο βρίσκεται σε μακροχρόνια θέση
                if spot["type"] == "long_term":
                    # Επαναφορά της θέσης σε προσωρινή κενή κατάσταση για μακροχρόνια στάθμευση
                    spot["temporarily_vacant"] = True

                    # Δημιουργία παραθύρου επιτυχίας για μακροχρόνια στάθμευση
                    window = tk.Toplevel()
                    window.title("Επιτυχής Έξοδος")
                    window.config(bg="#f7f7f7")

                    tk.Label(
                        window,
                        text="Προσωρινή Έξοδος Αυτοκινήτου",
                        font=("Helvetica", 20, "bold"),
                        bg="#f7f7f7"
                    ).pack(pady=10)

                    tk.Label(
                        window,
                        text=f"Αρ. Κυκλοφορίας: {license_plate}",
                        font=("Arial", 14),
                        bg="#f7f7f7"
                    ).pack(pady=5)

                    tk.Label(
                        window,
                        text=f"Αριθμός Θέσης: {i + 1}",
                        font=("Arial", 14),
                        bg="#f7f7f7"
                    ).pack(pady=5)

                    tk.Label(
                        window,
                        text="Το αυτοκίνητο έχει δικαίωμα να επιστρέψει στη θέση του.",
                        font=("Arial", 12, "italic"),
                        bg="#f7f7f7",
                        fg="blue"
                    ).pack(pady=5)

                    # Κουμπί για κλείσιμο του παραθύρου
                    tk.Button(
                        window,
                        text="ΟΚ",
                        font=("Arial", 12),
                        command=window.destroy
                    ).pack(pady=10)

                    self.save_data()  # Αποθήκευση των δεδομένων
                    return

                # Αν το αυτοκίνητο βρίσκεται σε ωριαία θέση, υπολογίζουμε τη χρέωση
                entry_time = datetime.fromisoformat(spot["car"]["entry_time"])
                duration = datetime.now() - entry_time
                hours = duration.total_seconds() / 3600  # Υπολογισμός διάρκειας στάθμευσης σε ώρες
                rounded_hours = math.ceil(hours)  # Στρογγυλοποίηση σε ακέραιες ώρες
                cost = max(rounded_hours * 2, 2.0)  # Υπολογισμός κόστους, ελάχιστο 2€

                self.revenue += cost  # Προσθήκη του κόστους στις συνολικές εισπράξεις
                self.transactions.append({
                    "type": "exit",  # Καταγραφή συναλλαγής εξόδου
                    "license_plate": license_plate,
                    "time": datetime.now().isoformat(),
                    "cost": cost
                })

                # Απελευθέρωση της θέσης
                spot["occupied"] = False
                spot["car"] = None

                # Δημιουργία παραθύρου επιτυχίας για ωριαία στάθμευση
                window = tk.Toplevel()
                window.title("Επιτυχής Έξοδος")
                window.config(bg="#f7f7f7")

                tk.Label(
                    window,
                    text="Επιτυχής Έξοδος Αυτοκινήτου",
                    font=("Helvetica", 16, "bold"),
                    bg="#f7f7f7"
                ).pack(pady=10)

                tk.Label(
                    window,
                    text=f"Αρ. Κυκλοφορίας: {license_plate}",
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                tk.Label(
                    window,
                    text=f"Χρέωση: {cost:.2f}€",
                    font=("Arial", 14, "bold"),
                    bg="#f7f7f7",
                    fg="green"
                ).pack(pady=5)

                tk.Label(
                    window,
                    text=f"Διάρκεια Στάθμευσης: {rounded_hours} ώρες",
                    font=("Arial", 12),
                    bg="#f7f7f7"
                ).pack(pady=5)

                # Κουμπί για κλείσιμο του παραθύρου
                tk.Button(
                    window,
                    text="ΟΚ",
                    font=("Arial", 12),
                    command=window.destroy
                ).pack(pady=10)

                self.save_data()  # Αποθήκευση των δεδομένων
                return

        # Αν δεν βρεθεί το αυτοκίνητο στο χώρο στάθμευσης, δημιουργούμε παράθυρο αποτυχίας
        fail_window = tk.Toplevel()
        fail_window.title("Αποτυχία")
        fail_window.config(bg="#f7f7f7")

        tk.Label(
            fail_window,
            text="Δεν βρέθηκε το αυτοκίνητο στο χώρο στάθμευσης.",
            font=("Arial", 14, "bold"),
            bg="#f7f7f7",
            fg="red"  # Χρωματισμός σε κόκκινο για την αποτυχία
        ).pack(pady=20)

        # Κουμπί κλεισίματος παραθύρου αποτυχίας
        tk.Button(
            fail_window,
            text="ΟΚ",
            font=("Arial", 12),
            command=fail_window.destroy  # Κλείσιμο του παραθύρου
        ).pack(pady=10)


    def rent_spot(self, license_plate, owner_name):
        """Καταγράφει την ενοικίαση θέσης για μακροχρόνια στάθμευση."""

        # Εξετάζουμε αν υπάρχουν διαθέσιμες θέσεις για μακροχρόνια στάθμευση
        for i, spot in enumerate(self.parking_spots):
            if not spot["occupied"] and spot["type"] == "long_term":
                # Ορίζουμε την ημερομηνία έναρξης και λήξης της ενοικίασης (30 μέρες)
                rental_start = datetime.now()
                rental_end = rental_start + timedelta(days=30)
                
                # Καταχωρούμε το αυτοκίνητο στην θέση και ενημερώνουμε τις πληροφορίες
                spot["occupied"] = True
                spot["car"] = {
                    "license_plate": license_plate,
                    "owner_name": owner_name,
                    "rental_start": rental_start.isoformat(),
                    "rental_end": rental_end.isoformat()
                }
                
                # Προσθέτουμε το κόστος ενοικίασης στα έσοδα (50€)
                self.revenue += 50
                
                # Καταγράφουμε τη συναλλαγή
                self.transactions.append({
                    "type": "rental",  # Τύπος συναλλαγής
                    "license_plate": license_plate,
                    "owner_name": owner_name,
                    "time": rental_start.isoformat(),  # Ώρα ενοικίασης
                    "cost": 50  # Κόστος ενοικίασης
                })

                # Δημιουργία παραθύρου επιτυχίας
                window = tk.Toplevel()
                window.title("Επιτυχής Ενοικίαση")
                window.config(bg="#f7f7f7")

                # Εμφάνιση πληροφοριών για την ενοικίαση
                tk.Label(
                    window,
                    text="Επιτυχής Ενοικίαση Θέσης",
                    font=("Helvetica", 20, "bold"),
                    bg="#f7f7f7"
                ).pack(pady=10)

                tk.Label(
                    window,
                    text=f"Θέση νούμερο: {i + 1}",  # Αριθμός θέσης
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                tk.Label(
                    window,
                    text=f"Αρ. Κυκλοφορίας: {license_plate}",  # Αριθμός κυκλοφορίας του αυτοκινήτου
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                tk.Label(
                    window,
                    text=f"Ονοματεπώνυμο Ιδιοκτήτη: {owner_name}",  # Ονοματεπώνυμο του ιδιοκτήτη
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                tk.Label(
                    window,
                    text=f"Ημερομηνία Έναρξης: {rental_start.strftime('%d/%m/%Y')}",  # Ημερομηνία έναρξης ενοικίασης
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                tk.Label(
                    window,
                    text=f"Ημερομηνία Λήξης: {rental_end.strftime('%d/%m/%Y')}",  # Ημερομηνία λήξης ενοικίασης
                    font=("Arial", 14),
                    bg="#f7f7f7"
                ).pack(pady=5)

                tk.Label(
                    window,
                    text=f"Χρέωση: 50€",  # Κόστος ενοικίασης
                    font=("Arial", 14, "bold"),
                    bg="#f7f7f7",
                    fg="green"
                ).pack(pady=10)

                # Κουμπί για να κλείσει το παράθυρο
                tk.Button(
                    window,
                    text="ΟΚ",
                    font=("Arial", 12),
                    command=window.destroy
                ).pack(pady=10)

                # Αποθήκευση των δεδομένων
                self.save_data()
                return  # Επιστροφή μετά την επιτυχή ενοικίαση

        # Αν δεν βρέθηκε διαθέσιμη θέση, δημιουργούμε παράθυρο αποτυχίας
        fail_window = tk.Toplevel()
        fail_window.title("Αποτυχία")
        fail_window.config(bg="#f7f7f7")

        # Εμφάνιση μηνύματος αποτυχίας
        tk.Label(
            fail_window,
            text="Δεν υπάρχουν διαθέσιμες θέσεις για μακροχρόνια στάθμευση.",
            font=("Arial", 14, "bold"),
            bg="#f7f7f7",
            fg="red"  # Χρωματισμός σε κόκκινο για την αποτυχία
        ).pack(pady=20)

        # Κουμπί κλεισίματος παραθύρου αποτυχίας
        tk.Button(
            fail_window,
            text="ΟΚ",
            font=("Arial", 12),
            command=fail_window.destroy  # Κλείσιμο του παραθύρου
        ).pack(pady=10)


    def show_parking_status(self):
        """Εμφανίζει την κατάσταση των θέσεων στάθμευσης με γραφικά."""
        
        # Δημιουργία νέου παραθύρου για την προβολή της κατάστασης των θέσεων στάθμευσης
        window = tk.Toplevel()
        window.title("Προβολή Θέσεων Στάθμευσης")
        window.config(bg="#f7f7f7")  # Ορισμός χρώματος φόντου του παραθύρου

        # Δημιουργία ενός καμβά για την εμφάνιση των θέσεων στάθμευσης
        canvas = tk.Canvas(window, width=500, height=350, bg="#e5e5e5", bd=0, highlightthickness=0)
        canvas.pack(padx=20, pady=20)

        # Ορισμός διαστάσεων για κάθε θέση στάθμευσης
        spot_width = 70
        spot_height = 50
        margin = 15
        rows = 5  # Αριθμός σειρών
        columns = 5  # Αριθμός στηλών

        # Για κάθε θέση στάθμευσης, υπολογίζουμε την θέση της στον καμβά
        for i, spot in enumerate(self.parking_spots):
            row = i // columns  # Υπολογισμός της γραμμής στην οποία βρίσκεται η θέση
            col = i % columns  # Υπολογισμός της στήλης στην οποία βρίσκεται η θέση
            
            # Υπολογισμός των συντεταγμένων για την τοποθέτηση του ορθογωνίου
            x1 = col * (spot_width + margin) + margin
            y1 = row * (spot_height + margin) + margin
            x2 = x1 + spot_width
            y2 = y1 + spot_height

            # Χρώμα της θέσης βάσει του τύπου (μακροχρόνια ή ωριαία)
            if spot["type"] == "long_term":
                fill_color = "#006400"  # Μακροχρόνια θέση (πράσινο)
            else:
                fill_color = "blue"  # Ωριαία θέση (μπλε)

            # Αν η θέση είναι κατειλημμένη, τοποθετούμε το νούμερο κυκλοφορίας στο κέντρο της θέσης
            if spot["occupied"]:
                car_plate = spot["car"]["license_plate"]
                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black", width=2)  # Δημιουργία του ορθογωνίου για τη θέση
                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=car_plate, fill="black", font=("Arial", 10, "bold"))  # Εμφάνιση του αριθμού κυκλοφορίας

            else:
                # Αν η θέση είναι ελεύθερη, χρησιμοποιούμε διαφορετικό χρώμα για να την εμφανίσουμε
                if spot["type"] == "long_term":
                    free_color = "#98FB98"  # Ελεύθερη μακροχρόνια θέση (ανοιχτό πράσινο)
                else:
                    free_color = "#B0E0E6"  # Ελεύθερη ωριαία θέση (ανοιχτό μπλε)

                canvas.create_rectangle(x1, y1, x2, y2, fill=free_color, outline="black", width=2)  # Δημιουργία ορθογωνίου για την ελεύθερη θέση
                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="Ελεύθερη", fill="black", font=("Arial", 10, "italic"))  # Κείμενο "Ελεύθερη" στο κέντρο

        # Δημιουργία τίτλου για την οθόνη της κατάστασης θέσεων
        title_label = tk.Label(window, text="Κατάσταση Θέσεων Στάθμευσης", font=("Helvetica", 14, "bold"), bg="#f7f7f7")
        title_label.pack(pady=10)

        # Δημιουργία ενός πλαισίου για την εμφάνιση επιπλέον πληροφοριών
        info_frame = tk.Frame(window, bg="#f7f7f7")
        info_frame.pack(pady=20)

        # Δημιουργία ετικετών (labels) που εξηγούν τα χρώματα των θέσεων
        label_long_term = tk.Label(info_frame, text="Πράσινο: Μακροχρόνια Θέση", bg="#f7f7f7", font=("Arial", 10))
        label_long_term.grid(row=0, column=0, sticky="w", padx=5)

        label_hourly = tk.Label(info_frame, text="Μπλε: Ωριαία Θέση", bg="#f7f7f7", font=("Arial", 10))
        label_hourly.grid(row=1, column=0, sticky="w", padx=5)

        label_free_long_term = tk.Label(info_frame, text="Ανοιχτό Πράσινο: Ελεύθερη Μακροχρόνια Θέση", bg="#f7f7f7", font=("Arial", 10))
        label_free_long_term.grid(row=2, column=0, sticky="w", padx=5)

        label_free_hourly = tk.Label(info_frame, text="Ανοιχτό Μπλε: Ελεύθερη Ωριαία Θέση", bg="#f7f7f7", font=("Arial", 10))
        label_free_hourly.grid(row=3, column=0, sticky="w", padx=5)

        # Ενεργοποιούμε τον κύκλο του παραθύρου για να παραμείνει ανοιχτό
        window.mainloop()

    def list_parked_cars(self):
        """Εμφανίζει μια λίστα με τα παρκαρισμένα αυτοκίνητα και αν είναι μόνιμοι ή ωριαίοι πελάτες."""

        # Δημιουργία νέου παραθύρου για την προβολή των παρκαρισμένων αυτοκινήτων
        window = tk.Toplevel()
        window.title("Παρκαρισμένα Αυτοκίνητα")
        window.config(bg="#f7f7f7")  # Ορισμός χρώματος φόντου του παραθύρου

        # Δημιουργία καμβά για την εμφάνιση των στοιχείων των παρκαρισμένων αυτοκινήτων
        canvas = tk.Canvas(window, width=500, height=350, bg="#e5e5e5", bd=0, highlightthickness=0)
        canvas.pack(padx=20, pady=20)

        # Λίστα για τα κείμενα εμφάνισης (πινακίδα + info)
        parked_cars_info = []

        # Ελέγχουμε κάθε θέση στάθμευσης: αν είναι κατειλημμένη, φτιάχνουμε το κείμενο που θα εμφανίζεται
        for spot in self.parking_spots:
            if spot["occupied"]:
                license_plate = spot["car"]["license_plate"]

                # Έλεγχος αν είναι μακροχρόνια θέση 
                if spot["type"] == "long_term":
                    text_label = f"{license_plate} (Μόνιμος)"
                else:
                    text_label = f"{license_plate} (Ωριαίος)"

                parked_cars_info.append(text_label)

        # Αν υπάρχουν παρκαρισμένα αυτοκίνητα, τα εμφανίζουμε στον καμβά
        if parked_cars_info:
            for i, info_text in enumerate(parked_cars_info):
                y_position = 20 + i * 30  # Σε κάθε γραμμή δείχνουμε και μια πινακίδα
                canvas.create_text(
                    10, y_position,
                    anchor="w",
                    text=info_text,
                    fill="black",
                    font=("Arial", 12, "bold")
                )
        else:
            # Αν δεν υπάρχουν παρκαρισμένα αυτοκίνητα, εμφανίζουμε σχετικό μήνυμα
            canvas.create_text(
                10, 20,
                anchor="w",
                text="Δεν υπάρχουν παρκαρισμένα αυτοκίνητα.",
                fill="black",
                font=("Arial", 12)
            )

        # Δημιουργία τίτλου για το παράθυρο
        title_label = tk.Label(
            window,
            text="Λίστα Παρκαρισμένων Αυτοκινήτων",
            font=("Helvetica", 14, "bold"),
            bg="#f7f7f7"
        )
        title_label.pack(pady=10)

        # Παραμένει ανοιχτό το παράθυρο
        window.mainloop()


    def list_free_spots(self):
        """Εμφανίζει μόνο τις ελεύθερες θέσεις με γραφικά."""
        
        # Δημιουργία νέου παραθύρου για την προβολή των ελεύθερων θέσεων
        window = tk.Toplevel()
        window.title("Ελεύθερες Θέσεις")
        window.config(bg="#f7f7f7")  # Ορισμός χρώματος φόντου του παραθύρου

        # Δημιουργία καμβά για την εμφάνιση των ελεύθερων θέσεων
        canvas = tk.Canvas(window, width=500, height=350, bg="#e5e5e5", bd=0, highlightthickness=0)
        canvas.pack(padx=20, pady=20)

        # Ορισμός διαστάσεων για τις θέσεις και απόσταση μεταξύ τους
        spot_width = 70
        spot_height = 50
        margin = 15
        rows = 5  # Αριθμός σειρών
        columns = 5  # Αριθμός στηλών

        # Σχεδιάζουμε τις θέσεις
        for i, spot in enumerate(self.parking_spots):
            row = i // columns  # Υπολογισμός σειράς
            col = i % columns  # Υπολογισμός στήλης
            x1 = col * (spot_width + margin) + margin  # Υπολογισμός του x1 για το πάνω αριστερό γωνία
            y1 = row * (spot_height + margin) + margin  # Υπολογισμός του y1 για το πάνω αριστερό γωνία
            x2 = x1 + spot_width  # Υπολογισμός του x2 για το κάτω δεξιά γωνία
            y2 = y1 + spot_height  # Υπολογισμός του y2 για το κάτω δεξιά γωνία

            # Αν η θέση είναι κατειλημμένη, δεν την εμφανίζουμε 
            if spot["occupied"]:
                continue  # Αν είναι κατειλημμένη, παραλείπουμε αυτή τη θέση και προχωράμε στην επόμενη
            else:
                # Αν η θέση είναι ελεύθερη, καθορίζουμε το χρώμα ανάλογα με τον τύπο της θέσης (μακροχρόνια ή ωριαία)
                if spot["type"] == "long_term":
                    fill_color = "#98FB98"  # Ανοιχτό πράσινο για τις ελεύθερες μακροχρόνιες θέσεις
                else:
                    fill_color = "#ADD8E6"  # Ανοιχτό μπλε για τις ελεύθερες ωριαίες θέσεις

                # Σχεδίαση του ορθογωνίου που αντιστοιχεί στην ελεύθερη θέση
                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black", width=2)
                # Δημιουργία κειμένου με τον αριθμό της θέσης στο κέντρο του ορθογωνίου
                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"Θέση {i+1}", fill="black", font=("Arial", 10, "italic"))

        # Δημιουργία τίτλου για το παράθυρο
        title_label = tk.Label(window, text="Ελεύθερες Θέσεις", font=("Helvetica", 14, "bold"), bg="#f7f7f7")
        title_label.pack(pady=10)

        # Δημιουργία ενός πλαισίου για την αναφορά των χρωμάτων
        info_frame = tk.Frame(window, bg="#f7f7f7")
        info_frame.pack(pady=20)

        # Δημιουργία ετικετών για να εξηγήσουμε τα χρώματα και τον τύπο των θέσεων
        label_free_long_term = tk.Label(info_frame, text="Ανοιχτό Πράσινο: Ελεύθερη Μακροχρόνια Θέση", bg="#f7f7f7", font=("Arial", 10))
        label_free_long_term.grid(row=2, column=0, sticky="w", padx=5)

        label_free_hourly = tk.Label(info_frame, text="Ανοιχτό Μπλε: Ελεύθερη Ωριαία Θέση", bg="#f7f7f7", font=("Arial", 10))
        label_free_hourly.grid(row=3, column=0, sticky="w", padx=5)

        # Εμφάνιση του παραθύρου
        window.mainloop()


def main():
    # Δημιουργία κύριου παραθύρου της εφαρμογής
    root = tk.Tk()
    root.title("Parking Volos")  # Ορισμός τίτλου παραθύρου
    root.geometry("400x500")  # Ορισμός μεγέθους παραθύρου (400x500)
    root.config(bg="#f0f0f0")  # Ρύθμιση χρώματος φόντου του παραθύρου σε ανοιχτό γκρι

    # Δημιουργία ενός αντικειμένου για τη διαχείριση του χώρου στάθμευσης
    parking_manager = Manager()

    # Δημιουργία ενός πλαισίου για το μενού που θα περιλαμβάνει τα κουμπιά
    menu_frame = ttk.Frame(root, padding="20")  # Πλαίσιο με padding 20 για την καλύτερη εμφάνιση
    menu_frame.pack(fill="both", expand=True)  # Το πλαίσιο θα επεκταθεί για να γεμίσει το παράθυρο

    # Προσθήκη του τίτλου στο επάνω μέρος του παραθύρου με στυλ και γραμματοσειρά
    title_label = ttk.Label(
        menu_frame, 
        text="Parking Volos", 
        font=("Helvetica", 28, "bold"), 
        foreground="navy",  # Χρώμα κειμένου
        background="#f0f0f0",  # Χρώμα φόντου
        anchor="center"
    )
    title_label.pack(pady=20)  # Προσθήκη απόστασης γύρω από την ετικέτα
    # Δημιουργία των κουμπιών για τις διάφορες λειτουργίες του συστήματος
    ttk.Button(menu_frame, text="Εισερχόμενο Αυτοκίνητο", command=lambda: enter_car(parking_manager)).pack(fill="x", pady=5)
    # Κουμπί για την καταχώρηση εισερχόμενου αυτοκινήτου, που καλεί τη συνάρτηση enter_car
    ttk.Button(menu_frame, text="Εξερχόμενο Αυτοκίνητο", command=lambda: exit_car(parking_manager)).pack(fill="x", pady=5)
    # Κουμπί για την καταχώρηση εξερχόμενου αυτοκινήτου, που καλεί τη συνάρτηση exit_car
    ttk.Button(menu_frame, text="Ενοικίαση Θέσης", command=lambda: rent_spot(parking_manager)).pack(fill="x", pady=5)
    # Κουμπί για την ενοικίαση θέσης, που καλεί τη συνάρτηση rent_spot
    ttk.Button(menu_frame, text="Προβολή Θέσεων Στάθμευσης", command=parking_manager.show_parking_status).pack(fill="x", pady=5)
    # Κουμπί για την προβολή της κατάστασης των θέσεων στάθμευσης, που καλεί τη συνάρτηση show_parking_status του manager
    ttk.Button(menu_frame, text="Ταμείο Ημέρας", command=parking_manager.show_daily_revenue).pack(fill="x", pady=5)
    # Κουμπί για την εμφάνιση των εσόδων της ημέρας, που καλεί τη συνάρτηση show_daily_revenue του manager
    ttk.Button(menu_frame, text="Λίστα Παρκαρισμένων Αυτοκινήτων", command=parking_manager.list_parked_cars).pack(fill="x", pady=5)
    # Κουμπί για την προβολή των παρκαρισμένων αυτοκινήτων, που καλεί τη συνάρτηση list_parked_cars του manager
    ttk.Button(menu_frame, text="Λίστα Ελεύθερων Θέσεων", command=parking_manager.list_free_spots).pack(fill="x", pady=5)
    # Κουμπί για την προβολή των ελεύθερων θέσεων, που καλεί τη συνάρτηση list_free_spots του manager
    ttk.Button(menu_frame, text="Καλύτερος Πελάτης", command=parking_manager.show_best_customers).pack(fill="x", pady=5)
    # Κουμπί για την εμφάνιση του καλύτερου πελάτη, που καλεί τη συνάρτηση show_best_customers του manager

    # Δημιουργία κουμπιού εξόδου από το πρόγραμμα
    exit_button = ttk.Button(menu_frame, text="Έξοδος", command=root.quit)
    exit_button.pack(fill="x", pady=10)  # Το κουμπί εξόδου με απόσταση γύρω του

    # Εμφάνιση του παραθύρου και εκκίνηση του loop του tkinter
    root.mainloop()


def enter_car(manager):
    # Εισαγωγή αριθμού κυκλοφορίας για το εισερχόμενο αυτοκίνητο
    license_plate = simpledialog.askstring("Εισερχόμενο Αυτοκίνητο", "Πληκτρολογήστε τον αριθμό κυκλοφορίας:")
    if license_plate:
        manager.enter_car(license_plate)  # Καλεί τη συνάρτηση enter_car του manager με τον αριθμό κυκλοφορίας


def exit_car(manager):
    # Εισαγωγή αριθμού κυκλοφορίας για το εξερχόμενο αυτοκίνητο
    license_plate = simpledialog.askstring("Εξερχόμενο Αυτοκίνητο", "Πληκτρολογήστε τον αριθμό κυκλοφορίας:")
    if license_plate:
        manager.exit_car(license_plate)  # Καλεί τη συνάρτηση exit_car του manager με τον αριθμό κυκλοφορίας


def rent_spot(manager):
    # Εισαγωγή αριθμού κυκλοφορίας για το αυτοκίνητο και ονόματος ιδιοκτήτη για την ενοικίαση θέσης
    license_plate = simpledialog.askstring("Ενοικίαση Θέσης", "Πληκτρολογήστε τον αριθμό κυκλοφορίας:")
    owner_name = simpledialog.askstring("Ενοικίαση Θέσης", "Πληκτρολογήστε το όνομα του ιδιοκτήτη:")
    if license_plate and owner_name:
        manager.rent_spot(license_plate, owner_name)  # Καλεί τη συνάρτηση rent_spot του manager με τις πληροφορίες του αυτοκινήτου


# Εκκίνηση της κύριας συνάρτησης όταν το πρόγραμμα εκτελείται
if __name__ == "__main__":
    main()
