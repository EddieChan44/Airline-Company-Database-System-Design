import sqlite3, os, sys
from tabulate import tabulate
from datetime import date

conn = sqlite3.connect('Airline_record.db')  #.db file
#conn = sqlite3.connect(':memory:') #for testing
curs = conn.cursor()
curs.execute("PRAGMA foreign_keys = ON")


# rest tables to default
def reset_tables():
  # clear tables
  curs.execute("""DROP TABLE pilots_flights""")
  curs.execute("""DROP TABLE flights""")
  curs.execute("""DROP TABLE pilots""")
  curs.execute("""DROP TABLE aircrafts""")

  # create tables
  curs.execute("""CREATE TABLE pilots (
                  pilot_id INTEGER PRIMARY KEY,
                  name VARCHAR(30) NOT NULL,
                  date_of_birth DATE NOT NULL,
                  sex VARCHAR(1) NOT NULL,
                  grade VARCHAR(20) NOT NULL,
                  year_of_exp TINYINT NOT NULL
                  );""")

  curs.execute("""CREATE TABLE flights (
                  flight_id VARCHAR(11) PRIMARY KEY,
                  flight_number VARCHAR(10) NOT NULL,
                  departure_date DATE NOT NULL,
                  departure_time TIME NOT NULL,
                  arrival_date DATE NOT NULL,
                  arrival_time TIME NOT NULL,
                  origin VARCHAR(30) NOT NULL,
                  destination VARCHAR(30) NOT NULL,
                  aircraft_id INTEGER,
                  FOREIGN KEY (aircraft_id) REFERENCES aircrafts (aircraft_id) ON DELETE Set Null ON UPDATE CASCADE
                  );""")

  curs.execute("""CREATE TABLE aircrafts (
                  aircraft_id INTEGER PRIMARY KEY,
                  model VARCHAR(20),
                  year_of_service INTEGER,
                  last_maintanance DATE
                  );""")

  curs.execute("""CREATE TABLE pilots_flights (
                  pilot_id INTEGER,
                  flight_id INTEGER,
                  FOREIGN KEY (pilot_id) REFERENCES pilots (pilot_id) ON DELETE CASCADE ON UPDATE CASCADE,
                  FOREIGN KEY (flight_id) REFERENCES flights (flight_id) ON DELETE CASCADE ON UPDATE CASCADE
                  );""")

  # input data (default)
  # pilots
  curs.execute("INSERT or IGNORE INTO pilots VALUES (?,?,?,?,?,?)",
               (1, 'John Smith', '1975-01-01', 'M', 'Captain', 20))
  curs.execute("INSERT or IGNORE INTO pilots VALUES (?,?,?,?,?,?)",
               (2, 'Jane Doe', '1978-01-01', 'F', 'Captain', 18))
  curs.execute("INSERT or IGNORE INTO pilots VALUES (?,?,?,?,?,?)",
               (3, 'Milton Turner', '1979-01-01', 'M', 'Captain', 17))
  curs.execute("INSERT or IGNORE INTO pilots VALUES (?,?,?,?,?,?)",
               (4, 'Geoffrey Robbins', '1980-01-01', 'M', 'Captain', 17))
  curs.execute("INSERT or IGNORE INTO pilots VALUES (?,?,?,?,?,?)",
               (5, 'Lulu Gregory', '1983-01-01', 'F', 'First Officer', 15))
  curs.execute("INSERT or IGNORE INTO pilots VALUES (?,?,?,?,?,?)",
               (6, 'Ellen Gill', '1987-01-01', 'F', 'First Officer', 12))
  curs.execute("INSERT or IGNORE INTO pilots VALUES (?,?,?,?,?,?)",
               (7, 'Rex Allen', '1990-01-01', 'M', 'Second Officer', 7))
  curs.execute("INSERT or IGNORE INTO pilots VALUES (?,?,?,?,?,?)",
               (8, 'Kingsley Holmes', '1995-01-01', 'M', 'Second Officer', 4))
  # aircrafts
  curs.execute("INSERT or IGNORE INTO aircrafts VALUES (?,?,?,?)",
               (1, 'Boeing 747-400', '3', '2022-12-20'))
  curs.execute("INSERT or IGNORE INTO aircrafts VALUES (?,?,?,?)",
               (2, 'Boeing 747-400', '3', '2022-11-20'))
  curs.execute("INSERT or IGNORE INTO aircrafts VALUES (?,?,?,?)",
               (3, 'Boeing 747-400', '3', '2022-10-20'))
  curs.execute("INSERT or IGNORE INTO aircrafts VALUES (?,?,?,?)",
               (4, 'Boeing 747-400', '3', '2022-09-20'))
  # flights
  curs.execute("INSERT or IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?)",
               (20230101001, 'UB123', '2023-01-01', '08:00:00', '2023-01-01',
                '09:20:00', 'London', 'Paris', 1))
  curs.execute("INSERT or IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?)",
               (20230101002, 'UB124', '2023-01-01', '12:00:00', '2023-01-01',
                '13:20:00', 'Paris', 'London', 1))
  curs.execute("INSERT or IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?)",
               (20230101003, 'UB125', '2023-01-01', '08:10:00', '2023-01-01',
                '10:40:00', 'London', 'Madrid', 2))
  curs.execute("INSERT or IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?)",
               (20230101004, 'UB126', '2023-01-01', '12:00:00', '2023-01-01',
                '14:30:00', 'Madrid', 'London', 2))
  curs.execute("INSERT or IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?)",
               (20230102001, 'UB123', '2023-01-02', '08:00:00', '2023-01-02',
                '09:20:00', 'London', 'Paris', 3))
  curs.execute("INSERT or IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?)",
               (20230102002, 'UB124', '2023-01-02', '12:00:00', '2023-01-02',
                '13:20:00', 'Paris', 'London', 3))
  curs.execute("INSERT or IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?)",
               (20230102003, 'UB125', '2023-01-02', '08:10:00', '2023-01-02',
                '10:40:00', 'London', 'Madrid', 4))
  curs.execute("INSERT or IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?)",
               (20230102004, 'UB126', '2023-01-02', '12:00:00', '2023-01-02',
                '14:30:00', 'Madrid', 'London', 4))

  # pilots_flights
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (1, 20230101001))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (5, 20230101001))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (1, 20230101002))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (5, 20230101002))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (2, 20230101003))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (6, 20230101003))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (2, 20230101004))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (6, 20230101004))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (3, 20230102001))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (7, 20230102001))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (3, 20230102002))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (7, 20230102002))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (4, 20230102003))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (8, 20230102003))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (4, 20230102004))
  curs.execute("INSERT or IGNORE INTO pilots_flights VALUES (?,?)",
               (8, 20230101004))

  # commit changes
  conn.commit()


# user programme
# print pilots list
def print_pilots():
  print("PILOT TABLE")
  curs.execute("SELECT * FROM pilots")
  data = curs.fetchall()
  data.insert(0, list(map(lambda x: x[0], curs.description)))
  print(tabulate(data, headers='firstrow', tablefmt='fancy_grid'))
  return 0


# print flights list
def print_flights():
  print("FLIGHT TABLE")
  curs.execute("SELECT * FROM flights")
  data = curs.fetchall()
  data.insert(0, list(map(lambda x: x[0], curs.description)))
  print(tabulate(data, headers='firstrow', tablefmt='fancy_grid'))
  return 0


# print aircrafts list
def print_aircrafts():
  print("AIRCRAFT TABLE")
  curs.execute("SELECT * FROM aircrafts")
  data = curs.fetchall()
  data.insert(0, list(map(lambda x: x[0], curs.description)))
  print(tabulate(data, headers='firstrow', tablefmt='fancy_grid'))
  return 0


# print pilots_flights list
def print_pilots_flights():
  print("PILOTS_FLIGHTS TABLE")
  curs.execute("SELECT * FROM pilots_flights")
  data = curs.fetchall()
  data.insert(0, list(map(lambda x: x[0], curs.description)))
  print(tabulate(data, headers='firstrow', tablefmt='fancy_grid'))
  return 0


# insert function
def insert(table):
  os.system('clear')
  # insert to pilots table
  if table == 1:
    print_pilots()
    curs.execute(
        "INSERT INTO pilots (pilot_id, name, date_of_birth, sex, grade, year_of_exp) VALUES (?, ?, ?, ?, ?, ?)",
        array)
    os.system('clear')
    print_pilots()
    input("Press Enter to return to insert interface...")
    insert_interface(0)
  # insert to flights table
  elif table == 2:
    print_flights()
    array = [
        input("flight_id: "),
        input("flight_number: "),
        input("departure_date: "),
        input("departure_time: "),
        input("arrival_date: "),
        input("arrival_time: "),
        input("origin: "),
        input("destination: "),
        input("aircraft_id: ")
    ]
    curs.execute(
        "INSERT INTO flights (flight_id, flight_number, departure_date, departure_time, arrival_date, arrival_time, origin, destination, aircraft_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        array)
    print("atleast 2 pilots are required for a flight")
    first_pilot = input("Enter first pilot_id: ")
    secone_pilot = input("Enter second pilot_id: ")
    third_pilot = input(
        "Enter third pilot_id (enter 0 if third pilot does not exist): ")
    if int(third_pilot) == 0:
      pilot = [first_pilot, secone_pilot]
      curs.execute(
          "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
          (pilot[0], array[0]))
      curs.execute(
          "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
          (pilot[1], array[0]))
    else:
      forth_pilot = input(
          "Enter forth pilot_id (enter 0 if third pilot does not exist): ")
      if int(forth_pilot) == 0:
        pilot = [first_pilot, secone_pilot, third_pilot]
        curs.execute(
            "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
            (pilot[0], array[0]))
        curs.execute(
            "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
            (pilot[1], array[0]))
        curs.execute(
            "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
            (pilot[2], array[0]))
      else:
        pilot = [first_pilot, secone_pilot, third_pilot, forth_pilot]
        curs.execute(
            "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
            (pilot[0], array[0]))
        curs.execute(
            "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
            (pilot[1], array[0]))
        curs.execute(
            "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
            (pilot[2], array[0]))
        curs.execute(
            "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
            (pilot[3], array[0]))

    os.system('clear')
    print_flights()
    print_pilots_flights()
    input("Press Enter to return to insert interface...")
    insert_interface(0)

  # insert to aircrafts table
  elif table == 3:
    print_aircrafts()
    array = [
        input("aircraft_id: "),
        input("model: "),
        input("year_of_service: "),
        input("last_maintanance: ")
    ]
    curs.execute(
        "INSERT INTO pilots (aircraft_id, model, year_of_service, last_maintanance) VALUES (?, ?, ?, ?)",
        array)
    os.system('clear')
    print_aircrafts()
    input("Press Enter to return to insert interface...")
    insert_interface(0)

  # insert to pilots_flights table
  elif table == 4:
    print_pilots_flights()
    array = [input("pilot_id: "), input("flight_id: ")]
    curs.execute(
        "INSERT INTO pilots_flights (pilot_id, flight_id) VALUES (?, ?)",
        array)
    os.system('clear')
    print_pilots_flights()
    input("Press Enter to return to insert interface...")
    insert_interface(0)

  conn.commit()  # commit changes
  return 0


# search function
def search(table):
  os.system('clear')

  # search pilots table
  if table == 1:
    print_pilots()
    print(
        "Pilot ID - 1\nName - 2\nDate of birth - 3\nSex - 4\nGrade - 5\nYear of experience (bigger or equal to) - 6\nYear of experience (smaller or equal to) - 7\nReturn to search menu - 0"
    )
    column = input("\nEnter the number of column name you want to search: ")
    if int(column) not in [0, 1, 2, 3, 4, 5, 6, 7]:
      print("Error! Try again!")
      search(table)
    elif int(column) == 0:
      search_interface
    else:
      info = input("Enter the information you want to search: ")
      if column == '1':
        curs.execute("SELECT * FROM pilots WHERE pilot_id = ?", (info, ))
      elif column == '2':
        curs.execute("SELECT * FROM pilots WHERE name LIKE '%'||?||'%'",
                     (info, ))
      elif column == '3':
        curs.execute(
            "SELECT * FROM pilots WHERE date_of_birth LIKE '%'||?||'%'",
            (info, ))
      elif column == '4':
        curs.execute("SELECT * FROM pilots WHERE sex LIKE '%'||?||'%'",
                     (info, ))
      elif column == '5':
        curs.execute("SELECT * FROM pilots WHERE grade LIKE '%'||?||'%'",
                     (info, ))
      elif column == '6':
        curs.execute("SELECT * FROM pilots WHERE year_of_exp >= ?", (info, ))
      elif column == '7':
        curs.execute("SELECT * FROM pilots WHERE year_of_exp <= ?", (info, ))

  # search flights table
  if table == 2:
    print_flights()
    print(
        "Flight ID - 1\nFlight number - 2\nDeparture date - 3\nDeparture time - 4\nArrival date - 5\nArrival time - 6\nOrigin & Destination - 7\nAircraft ID - 8\nReturn to search menu - 0"
    )
    column = input("\nEnter the number of column name you want to search: ")
    if int(column) not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
      print("Error! Try again!")
      search(table)  # reset for incorrect input
    elif int(column) == 0:
      search_interface
    else:
      info = input("Enter the information you want to search: ")
      if column == '1':
        curs.execute("SELECT * FROM flights WHERE flight_id = ?", (info, ))
      elif column == '2':
        curs.execute(
            "SELECT * FROM flights WHERE flight_number LIKE '%'||?||'%'",
            (info, ))
      elif column == '3':
        curs.execute("SELECT * FROM flights WHERE departure_date = ?",
                     (info, ))
      elif column == '4':
        curs.execute(
            "SELECT * FROM flights WHERE departure_time LIKE '%'||?||'%'",
            (info, ))
      elif column == '5':
        curs.execute(
            "SELECT * FROM flights WHERE arrival_date LIKE '%'||?||'%'",
            (info, ))
      elif column == '6':
        curs.execute(
            "SELECT * FROM flights WHERE arrival_time LIKE '%'||?||'%'",
            (info, ))
      elif column == '7':
        info2 = input("Enter the second information you want to search: ")
        curs.execute(
            "SELECT * FROM flights WHERE origin LIKE '%'||?||'%' AND destination LIKE '%'||?||'%'",
            (
                info,
                info2,
            ))
      elif column == '8':
        curs.execute("SELECT * FROM flights WHERE aircraft_id = ?", (info, ))

  # search aircrafts table
  if table == 3:
    print_aircrafts()
    print(
        "Aircraft ID - 1\nModel - 2\nYear of service (longer or equal) - 3\nYear of service (shorter or equal) - 4\nLast maintanance - 5\nReturn to search menu - 0"
    )
    column = input("\nEnter the number of column name you want to search: ")
    if int(column) not in [0, 1, 2, 3, 4, 5]:
      print("Error! Try again!")
      search(table)
    elif int(column) == 0:
      search_interface(0)  #return to search interface
    else:
      info = input("Enter the information you want to search: ")
      if column == '1':
        curs.execute("SELECT * FROM aircrafts WHERE aircraft_id = ?", (info, ))
      elif column == '2':
        curs.execute("SELECT * FROM aircrafts WHERE model LIKE '%'||?||'%'",
                     (info, ))
      elif column == '3':
        curs.execute("SELECT * FROM aircrafts WHERE year_of_service >= ?",
                     (info, ))
      elif column == '4':
        curs.execute("SELECT * FROM aircrafts WHERE year_of_service <= ?",
                     (info, ))
      elif column == '5':
        curs.execute(
            "SELECT * FROM aircrafts WHERE last_maintanance LIKE '%'||?||'%'",
            (info, ))

  # search pilots-flights table
  if table == 4:
    print_pilots_flights()
    print("Pilot ID - 1\nFlight ID - 2\nReturn to search menu - 0")
    column = input("\nEnter the number of column name you want to search: ")
    if int(column) not in [0, 1, 2]:  # reset for incorrect input
      print("Error! Try again!")
      search(table)
    elif int(column) == 0:  # return to search interface
      search_interface
    else:
      info = input("Enter the information you want to search: ")
      if column == '1':
        curs.execute("SELECT * FROM pilots_flights WHERE pilot_id = ?",
                     (info, ))
      elif column == '2':
        curs.execute(
            "SELECT * FROM pilots_flights WHERE flight_id LIKE '%'||?||'%'",
            (info, ))

  # print the selected data and return to search menu
  data = curs.fetchall()
  data.insert(0, list(map(lambda x: x[0], curs.description)))
  os.system('clear')
  print(tabulate(data, headers='firstrow', tablefmt='fancy_grid'))
  input("Press Enter to return to search interface...")
  search_interface(0)

  return 0


# update function
def update(table):
  os.system('clear')
  # update pilots table
  if table == 1:
    print_pilots()
    id = input(
        "Enter the pilot's ID you want to update: ")  # row id for change
    attribute = input("Enter the attribute you want to update (1 to 6): ")
    if int(attribute) not in [1, 2, 3, 4, 5, 6]:  # reset for incorrect input
      print("Error! Try again!")
      update(table)
    elif int(attribute) == 1:
      att = input("Enter the new pilot's ID: "
                  )  # new input to the chosed attribute of the chosen row
      curs.execute("UPDATE pilots SET pilot_id = ? WHERE pilot_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 2:
      att = input("Enter the new pilot's name: ")
      curs.execute("UPDATE pilots SET name = ? WHERE pilot_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 3:
      att = input("Enter the new pilot's date of birth: ")
      curs.execute("UPDATE pilots SET date_of_birth = ? WHERE pilot_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 4:
      att = input("Enter the new pilot's sex: ")
      curs.execute("UPDATE pilots SET sex = ? WHERE pilot_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 5:
      att = input("Enter the new pilot's grade: ")
      curs.execute("UPDATE pilots SET grade = ? WHERE pilot_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 6:
      att = input("Enter the new pilot's flight ID: ")
      curs.execute("UPDATE pilots SET year_of_exp = ? WHERE pilot_id = ?", (
          att,
          id,
      ))
    os.system('clear')
    # print relevent tables
    print_pilots()
    print_flights()
    print_pilots_flights()

  # update flights table
  if table == 2:
    print_flights()
    id = input("Enter the flight's ID you want to update: ")
    attribute = input("Enter the attribute you want to update (1 to 9): ")
    if int(attribute) not in [1, 2, 3, 4, 5, 6, 7, 8,
                              9]:  # reset for incorrect input
      print("Error! Try again!")
      update(table)
    elif int(attribute) == 1:
      att = input("Enter the new flight's ID: ")
      curs.execute("UPDATE flights SET flight_id = ? WHERE flight_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 2:
      att = input("Enter the new flight's flight number: ")
      curs.execute("UPDATE flights SET flight_number = ? WHERE flight_id = ?",
                   (
                       att,
                       id,
                   ))
    elif int(attribute) == 3:
      att = input("Enter the new flight's departure date: ")
      curs.execute("UPDATE flights SET departure_date = ? WHERE flight_id = ?",
                   (
                       att,
                       id,
                   ))
    elif int(attribute) == 4:
      att = input("Enter the new flight's departure time: ")
      curs.execute("UPDATE flights SET departure_time = ? WHERE flight_id = ?",
                   (
                       att,
                       id,
                   ))
    elif int(attribute) == 5:
      att = input("Enter the new flight's arrival date: ")
      curs.execute("UPDATE flights SET arrival_date = ? WHERE flight_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 6:
      att = input("Enter the new flight's arrival time: ")
      curs.execute("UPDATE flights SET arrival_time = ? WHERE flight_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 7:
      att = input("Enter the new flight's origin: ")
      curs.execute("UPDATE flights SET origin = ? WHERE flight_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 8:
      att = input("Enter the new flight's destination: ")
      curs.execute("UPDATE flights SET destination = ? WHERE flight_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 9:
      att = input("Enter the new flight's aircraft ID: ")
      curs.execute("UPDATE flights SET aircraft_id = ? WHERE flight_id = ?", (
          att,
          id,
      ))
    os.system('clear')
    print_flights()
    print_aircrafts()

  if table == 3:
    print_aircrafts()
    id = input("Enter the aircraft's ID you want to update: ")
    attribute = input("Enter the attribute you want to update (1 to 4): ")
    if int(attribute) not in [1, 2, 3, 4]:  #reset for incorrect input
      print("Error! Try again!")
      update(table)
    elif int(attribute) == 1:
      att = input("Enter the new aircraft's ID: ")
      curs.execute(
          "UPDATE aircrafts SET aircraft_id = ? WHERE aircraft_id = ?", (
              att,
              id,
          ))
    elif int(attribute) == 2:
      att = input("Enter the new aircraft's model: ")
      curs.execute("UPDATE aircrafts SET model = ? WHERE aircraft_id = ?", (
          att,
          id,
      ))
    elif int(attribute) == 3:
      att = input("Enter the new aircraft's year of service: ")
      curs.execute(
          "UPDATE aircrafts SET year_of_service = ? WHERE aircraft_id = ?", (
              att,
              id,
          ))
    elif int(attribute) == 4:
      mode = input(
          "Enter the mode of update (update to today - 0 or update manually - random keys): "
      )
      if int(mode) == 0:  # auto update the last maintanance date to today
        today = date.today()
        curs.execute(
            "UPDATE aircrafts SET last_maintanance = ? WHERE aircraft_id = ?",
            (
                str(today),
                id,
            ))
      else:
        att = input("Enter the new aircraft's last maintanance: ")
        curs.execute(
            "UPDATE aircrafts SET last_maintanance = ? WHERE aircraft_id = ?",
            (
                att,
                id,
            ))
    os.system('clear')
    print_aircrafts()
    print_flights()

  if table == 4:
    print_pilotsflights()
    id = input("Enter the pilot's ID you want to update: ")
    attribute = input("Enter the attribute you want to update (1 to 4): ")
    if int(attribute) not in [1, 2]:  #reset for incorrect input
      print("Error! Try again!")
      update(table)
    elif int(attribute) == 1:
      att = input("Enter the new pilot's ID: ")
      curs.execute("UPDATE pilotsflights SET pilot_id = ? WHERE pilot_id = ?",
                   (
                       att,
                       id,
                   ))
    elif int(attribute) == 2:
      att = input("Enter the new pilot's flight ID: ")
      curs.execute("UPDATE pilotsflights SET flight_id = ? WHERE pilot_id = ?",
                   (
                       att,
                       id,
                   ))
    os.system('clear')
    print_pilotsflights()
    print_pilots()
    print_flights()

  conn.commit()  # commit changes
  # return to update menu after update
  input("Press Enter to return to update interface...")
  update_interface(0)

  return 0


# delete function (delete whole row)
def delete(table):
  print("Select the table you want to delete from: ")
  os.system('clear')
  # selected pilots table
  if table == 1:
    print_pilots()
    id = input("Enter the pilot's ID you want to delete: "
               )  # select the row by pilot's ID
    curs.execute("DELETE FROM pilots WHERE pilot_id = ?", (id, ))
    os.system('clear')
    # print related tables
    print_pilots()
    print_flights()
    print_pilots_flights()

  # selected flights table
  if table == 2:
    print_flights()
    id = input("Enter the flight's ID you want to delete: "
               )  # select the row by flight's ID
    curs.execute("DELETE FROM flights WHERE flight_id = ?", (id, ))
    os.system('clear')
    print_flights()
    print_aircrafts()

  # selected aircrafts table
  if table == 3:
    print_aircrafts()
    id = input("Enter the aircraft's ID you want to delete: "
               )  #select the row by aircraft's ID
    curs.execute("DELETE FROM aircrafts WHERE aircraft_id = ?", (id, ))
    os.system('clear')
    print_aircrafts()
    print_flights()

  #selected pilots_flights table
  if table == 4:
    print_pilotsflights()
    p_id = input(
        "Enter the pilot-flight record you want to delete (pilot_id): "
    )  # first select the row by pilot's ID
    f_id = input(
        "Enter the pilot-flight record you want to delete (flight_id): "
    )  # second select the row by flight's ID
    os.system('clear')
    print_pilotsflights()
    print_pilots()
    print_flights()

  conn.commit()  # commit changes
  # return to delete menu after delete
  input("Press Enter to return to delete interface...")
  delete_interface(0)

  return 0


# main interface
def interface(error):
  os.system('clear')
  script = "Welcome to Flight Management System\nPlease select the function you want to use\nInsert data - 1\nSearch data - 2\nUpdate data - 3\nDelete data - 4\nTo show the sex of pilots that having higher than a number - 5\nView tables by order - 6\nReset tables - 7\n"
  input_script = "\nPlease input the number of the function you want to use: "
  error_script = "Wrong input, please try again"
  print(script)
  if error == 1:
    print(error_script)  #only print when there is an error input
  print(input_script)
  choice = int(input())
  while choice not in [1, 2, 3, 4, 5, 6, 7]:
    os.system('clear')
    interface(1)
  if choice == 1:
    insert_interface(0)  # insert function
  if choice == 2:
    search_interface(0)  # search function
  if choice == 3:
    update_interface(0)  # update function
  if choice == 4:
    delete_interface(0)  # delete function
  if choice == 5:
    count_interface(0)  # count function
  if choice == 6:
    order_interface(0)  # order function (sorting)
  if choice == 7:
    reset_tables()  # reset .db file to the default tables and data
    # print default tables and data
    print_pilots()
    print_flights()
    print_aircrafts()
    print_pilots_flights()
    print("Tables have been reset")
    input("Press Enter to return to main interface..."
          )  # return to the main interface
    interface(0)

  return 0


# insert interface
def insert_interface(error):
  os.system('clear')
  script = "Insert data\nPlease select the table you want to insert data into\nPilots - 1\nFlights - 2\nAircrafts - 3\nPilots_flight -4\nReturn to main interface - 5\n "
  input_script = "\nPlease input the number of the table you want to insert: "
  error_script = "Wrong input, please try again"
  print(script)
  if error == 1:
    print(error_script)  # print when there is an wrong input
  print(input_script)
  choice = int(input())
  if choice not in [1, 2, 3, 4, 5]:
    insert_interface(1)
  elif choice == 5:  #return to main interface
    interface(0)
  else:
    insert(choice)


#search interface
def search_interface(error):
  os.system('clear')
  script = "Search data\nPlease select the table you want to search\nPilots - 1\nFlights - 2\nAircrafts - 3\nPilots_flight -4\nReturn to main interface - 5\n "
  input_script = "\nPlease input the number of the table you want to insert: "
  error_script = "Wrong input, please try again"
  print(script)
  if error == 1:
    print(error_script)
  print(input_script)
  choice = int(input())
  if choice not in [1, 2, 3, 4, 5]:
    search_interface(1)
  elif choice == 5:
    interface(0)
  else:
    search(choice)


#update interface
def update_interface(error):
  os.system('clear')
  # print tables for preview
  print_pilots()
  print_flights()
  print_aircrafts()
  print_pilots_flights()
  script = "Update data\nPlease select the table you want to update data into\nPilots - 1\nFlights - 2\nAircrafts - 3\nPilots_flight -4\nReturn to main interface - 5\n "
  input_script = "\nPlease input the number of the table you want to update: "
  error_script = "Wrong input, please try again"
  print(script)
  if error == 1:
    print(error_script)
  print(input_script)
  choice = int(input())
  if choice not in [1, 2, 3, 4, 5]:
    search_interface(1)
  elif choice == 5:
    interface(0)
  else:
    update(choice)


#delete interface
def delete_interface(error):
  os.system('clear')
  # print tables for preview
  print_pilots()
  print_flights()
  print_aircrafts()
  print_pilots_flights()
  script = "Update data\nPlease select the table you want to update data into\nPilots - 1\nFlights - 2\nAircrafts - 3\nPilots_flight -4\nReturn to main interface - 5\n "
  input_script = "\nPlease input the number of the table you want to delete: "
  error_script = "Wrong input, please try again"
  print(script)
  if error == 1:
    print(error_script)
  print(input_script)
  choice = int(input())
  if choice not in [1, 2, 3, 4, 5]:
    search_interface(1)
  elif choice == 5:
    interface(0)
  else:
    delete(choice)


#count interface
def count_interface(error):
  os.system('clear')
  script = "Please insert the number of the sex of pilots that more or equal to: "
  error_script = "Wrong input, please try again"
  print(script)
  if error == 1:
    print(error_script)
  choice = input()
  if choice.isdigit() == False:
    count_interface(1)
  else:
    curs.execute(
        "SELECT sex, COUNT(*) FROM pilots GROUP BY sex HAVING COUNT(*) >= ?",
        (int(choice), )
    )  # look for the sex of pilots that equals or higher than the input number

    #print the table with the sex match the criteria and
    data = curs.fetchall()
    data.insert(0, list(map(lambda x: x[0], curs.description)))
    os.system('clear')
    print(tabulate(data, headers='firstrow', tablefmt='fancy_grid'))
    input("Press Enter to return to main interface..."
          )  #return to main interface
    interface(0)


#order interface
def order_interface(error):
  os.system('clear')
  print(
      "View data in order\nPlease select the table you want to view\nPilots - 1\nFlights - 2\nAircrafts - 3\nReturn to main interface - 0\n "
  )
  input_script = "\nPlease input the number of the table you want to delete: "
  error_script = "Wrong input, please try again"
  if error == 1:
    print(error_script)
  print(input_script)
  choice = int(input())  # select the table by number
  if choice not in [1, 2, 3, 4]:
    order_interface(1)
  elif choice == 4:
    interface(0)
  else:
    # sort for pilots table
    if int(choice) == 1:
      os.system('clear')
      print_pilots()
      print(
          "Please select the attribute you want to sort in order\nName - 1\nDate of birth - 2\nSex - 3\nGrade - 4\nYear of experience - 5"
      )
      att = int(
          input(
              "Please input the number of the attribute you want to sort in order: "
          ))
      if int(att) not in [1, 2, 3, 4, 5]:
        order_interface(1)
      else:
        if int(att) == 1:
          att = "name"
        elif int(att) == 2:
          att = "date_of_birth"
        elif int(att) == 3:
          att = "sex"
        elif int(att) == 4:
          att = "grade"
        elif int(att) == 5:
          att = "year_of_experience"
        ad = input(
            "Please input ascending or descending order\nAscending - A\nDescending - D\n: "
        )  # choose sorting by ascending or descending order
        if ad not in ['A', 'D']:
          order_interface(1)  # reset for error input
        else:
          if ad == 'A':
            ad = "ASC"
          else:
            ad = "DESC"
      curs.execute("SELECT * FROM pilots ORDER BY " + att + " " +
                   ad)  # select the sorted table

  # sort for flights table
  if int(choice) == 2:
    os.system('clear')
    print_flights()
    print(
        "Please select the attribute you want to sort in order\nFlight number - 1\nDeparture date - 2\nDeparture time - 3\nArrival date - 4\nArrival time - 5\nOrigin - 6\nDestination - 7\nAircraft ID - 8"
    )
    att = int(
        input(
            "Please input the number of the attribute you want to sort in order: "
        ))
    if int(att) not in [1, 2, 3, 4, 5, 6, 7, 8]:
      order_interface(1)
    else:
      if int(att) == 1:
        att = "flight_number"
      elif int(att) == 2:
        att = "departure_date"
      elif int(att) == 3:
        att = "departure_time"
      elif int(att) == 4:
        att = "arrival_date"
      elif int(att) == 5:
        att = "arrival_time"
      elif int(att) == 6:
        att = "origin"
      elif int(att) == 7:
        att = "destination"
      elif int(att) == 8:
        att = "aircraft_id"
      ad = input(
          "Please input ascending or descending order\nAscending - A\nDescending - D\n: "
      )
      if ad not in ['A', 'D']:
        order_interface(1)
      else:
        if ad == 'A':
          ad = "ASC"
        else:
          ad = "DESC"
    curs.execute("SELECT * FROM flights ORDER BY " + att + " " +
                 ad)  # select the sorted table

  # sort for aircrafts table
  if int(choice) == 3:
    os.system('clear')
    print_aircrafts()
    print(
        "Please select the attribute you want to sort in order\nModel - 1\nYear of service - 2\nLast maintanance - 3\n"
    )
    att = int(
        input(
            "Please input the number of the attribute you want to sort in order: "
        ))
    if int(att) not in [1, 2, 3]:
      order_interface(1)
    else:
      if int(att) == 1:
        att = "model"
      elif int(att) == 2:
        att = "year_of_service"
      elif int(att) == 3:
        att = "last_maintanance"
      ad = input(
          "Please input ascending or descending order\nAscending - A\nDescending - D\n: "
      )
      if ad not in ['A', 'D']:
        order_interface(1)
      else:
        if ad == 'A':
          ad = "ASC"
        else:
          ad = "DESC"
  curs.execute("SELECT * FROM pilots ORDER BY " + att + " " +
               ad)  # select the sorted table

  # print the select sorted table
  data = curs.fetchall()
  data.insert(0, list(map(lambda x: x[0], curs.description)))
  print(tabulate(data, headers='firstrow', tablefmt='fancy_grid'))
  input("Press Enter to return to insert interface...")
  insert_interface(0)


# run main interface
interface(0)

conn.commit()

conn.close()
