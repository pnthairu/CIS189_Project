# Start Program
"""
Program: ticket_counter.py
Author: Paul Thairu
Last date modified: 07/31/2020

This program is for counting remaining ticket for sale and the number
of customers who have bought the ticket in any given concert

The program also shows the percentage progress of the tickets sold up to 100%

With the program once all tickets have been sold the database is reset to sell tickets
for another concert

"""
import tkinter
import tkinter.ttk
import tkinter.messagebox
import sqlite3

# Constants for program execution
TOTAL_TICKETS = 100   # total tickets for the concert
MAX_TICKETS_PER_BUYER = 6  # Maximum ticket each customer can buy
DATABASE_FILE = 'tickets_database.db'

# Method to buy tickets, activated when "Purchase" button is clicked
def set_tickets_to_buy():
    global tickets_remaining, customers, tickets_remaining_label, customers_label, progress_bar, conn
    num_tickets = tickets_entry.get()  # user input for the number of tickets
    # Check if input is numeric
    if num_tickets.isdigit():
        num_tickets = int(num_tickets)
        # Check if number of tickets is greater than MAX_TICKETS_PER_BUYER
        if (num_tickets > MAX_TICKETS_PER_BUYER):
            tkinter.messagebox.showinfo("Error", "You can't buy more than " + str(MAX_TICKETS_PER_BUYER) + " tickets.")
        # Check if number of tickets is less than 1
        elif (num_tickets < 1):
            tkinter.messagebox.showinfo("Error", "You can't buy less than 1 ticket.")
        # Check if event is sold out
        elif tickets_remaining == 0:
            tkinter.messagebox.showinfo("Error", "Event sold out!")
        # Check if number of tickets exceeds tickets remaining
        elif (num_tickets > tickets_remaining):
            tkinter.messagebox.showinfo("Error", "There are " + str(tickets_remaining) + " tickets remaining.\nYou cannot buy more than " + str(tickets_remaining) + " tickets.")
        # Otherwise, successfully process ticket purchase
        else:
            tickets_remaining -= num_tickets
            customers += 1
            tickets_remaining_label.config(text="Tickets remaining:  " + str(tickets_remaining))
            customers_label.config(text="Number of customers:  " + str(customers))
            progress_bar.config(value=TOTAL_TICKETS-tickets_remaining)
            conn.execute("INSERT INTO tasks (id, tickets) \
                          VALUES (" + str(customers) + ", " + str(num_tickets) + ")");
            conn.commit()
    else:
        tkinter.messagebox.showinfo("Error", "Please enter numeric input.")

# Method to reset database, activated when "Reset database" button is clicked
def reset_database():
    global tickets_remaining, customers, tickets_remaining_label, customers_label, progress_bar, conn
    tickets_remaining = TOTAL_TICKETS
    customers = 0
    tickets_remaining_label.config(text="Tickets remaining:  " + str(tickets_remaining))
    customers_label.config(text="Number of customers:  " + str(customers))
    progress_bar.config(value=TOTAL_TICKETS-tickets_remaining)
    conn.execute("DELETE FROM tasks");
    conn.commit()


# SQL command to initialize table
sql_create_table = """CREATE TABLE IF NOT EXISTS tasks (
                          id integer PRIMARY KEY,
                          tickets integer
                      );"""

# Initialize SQL connection
conn = sqlite3.connect(DATABASE_FILE)
conn.execute(sql_create_table)

# Establish program variables from reading SQL database
tickets_remaining = TOTAL_TICKETS
customers = 0
cursor = conn.execute("SELECT id, tickets from tasks")
for row in cursor:
    tickets = row[1]
    tickets_remaining -= row[1]
    customers += 1

# Construct GUI
root = tkinter.Tk()
root.title("Ticket Manager")
root.geometry("400x400")

# Define tickets entry label
tickets_entry_label = tkinter.Label(root, text="Enter how many tickets you'd like to purchase (1-6): ")
tickets_entry_label.grid(row=0, column=0, pady=10, padx=10, ipadx=40)

# Define tickets entry
tickets_entry = tkinter.Entry(root, width=2)
tickets_entry.insert(0, "1")
tickets_entry.grid(row=1, column=0, pady=10, padx=10, ipadx=20)

# Define purchase button
purchase_button = tkinter.Button(root, text="Purchase", command=set_tickets_to_buy)
purchase_button.grid(row=2, column=0, columnspan=1, pady=10, padx=5, ipadx=40)

# Define progress bar
progress_bar = tkinter.ttk.Progressbar(root, length=TOTAL_TICKETS, value=TOTAL_TICKETS-tickets_remaining)
progress_bar.grid(row=3, column=0, columnspan=1, pady=10, padx=5, ipadx=40)

# Define tickets remaining label
tickets_remaining_label = tkinter.Label(root, text="Tickets remaining:  " + str(tickets_remaining))
tickets_remaining_label.grid(row=4, column=0)

# Define customers label
customers_label = tkinter.Label(root, text="Number of customers:  " + str(customers))
customers_label.grid(row=5, column=0)

# Define reset database button
reset_database_button = tkinter.Button(root, text="Reset database", command=reset_database)
reset_database_button.grid(row=6, column=0, columnspan=1, pady=10, padx=5, ipadx=40)

# Run database
root.mainloop()

# Terminate SQL connection
conn.close()

