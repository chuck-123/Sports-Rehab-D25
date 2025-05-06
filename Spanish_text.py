import tkinter as tk
from tkinter import ttk
import random
import time
import csv
import os 
from tkinter import messagebox
import datetime 
import serial

#connect to arduino
ser = serial.Serial('COM7', baudrate = 9600, timeout = 1)

# Varialbles and placeholdes
Flash_win = 0
Order_win = 0

Flash_Lose = 0
Order_Lose = 0

list_order = ""

Flash_num_blinks = 5
Flash_level = 5
Order_level = 5

FH1 = 0
FH2 = 0
FH3 = 0
FH4 = 0

rand_order_hoop_list = [1,2,3,4]

def main_exit_game():
        if messagebox.askyesno("Exit Game", "Are you sure you want to exit?"):
            root.destroy()

def flasher_game():
    global FH1,FH2,FH3,FH4
    FH1 =0
    FH2 =0
    FH3 =0
    FH4 =0

    hoop1_counter.config(text = FH1)
    hoop2_counter.config(text = FH2)
    hoop3_counter.config(text = FH3)
    hoop4_counter.config(text = FH4)
    Fscore_Value.config(text="0")

    current_time = time.time()
    end_time = current_time + 60

    list = ["a","b","c","d"]
    if select_patient_combo.get() == "":
        messagebox.showinfo("showinfo","No user selected")
    else:
        while end_time>time.time():
            Flasher(random.choice(list))
            value = str(FH1+2*FH2+2*FH3+FH4)
            Fscore_Value.config(text =str(FH1+2*FH2+2*FH3+FH4))
        save_user_data()

def Flasher_PointChange(outcome):
    global FH1,FH2,FH3,FH4
    if outcome == "H1+":
        FH1 = FH1 +1
        hoop1_counter.config(text = str(FH1))
    if outcome == "H2+":
        FH2 = FH2 +1
        hoop2_counter.config(text = str(FH2))
    if outcome == "H3+":
        FH3 = FH3 +1
        hoop3_counter.config(text = str(FH3))
    if outcome == "H4+":
        FH4 = FH4 +1
        hoop4_counter.config(text = str(FH4))
        

    
# input from button, updates difficulty settings
def settings(Change):
    global Flash_num_blinks, Flash_level, Order_level
                
            
    if Change == "FL+" and Flash_level <= 10 and Flash_level >= 1:
        if Flash_level == 10:
            Flash_level = 10
        else:
            Flash_level = Flash_level + 1
        flasher_level_value.config(text=str(Flash_level))

        ser.write("f".encode('ascii'))
        print(Flash_level)
        value = Flash_level-1
        ser.write(str(value).encode('ascii'))

    if Change == "FL-" and Flash_level <= 10 and Flash_level >= 1:
        if Flash_level == 1:
            Flash_level = 1
        else:
            Flash_level = Flash_level - 1
        flasher_level_value.config(text=str(Flash_level))

        ser.write("f".encode('ascii'))
        print(Flash_level)
        value = Flash_level-1
        ser.write(str(value).encode('ascii'))
            
    if Change == "OL+" and Order_level <= 10 and Order_level >= 1:
        if Order_level == 10:
            Order_level = 10
        else:
            Order_level = Order_level + 1
        order_level_value.config(text=str(Order_level))
        
        ser.write("f".encode('ascii'))
        print(Order_level)
        value = Order_level-1
        ser.write(str(value).encode('ascii'))
            
    if Change == "OL-" and Order_level <= 10 and Order_level >= 1:
        if Order_level == 1:
            Order_level = 1
        else:
            Order_level = Order_level - 1
        order_level_value.config(text=str(Order_level))

        ser.write("f".encode('ascii'))
        print(Order_level)
        value = Order_level-1
        ser.write(str(value).encode('ascii'))


# selects random order for single player game
def randOrder(Listorder,attempts):
    global list_order
    print(attempts)
    list_order = ""
    
    # Order for memory game, updates ui and flashes lights
    if select_patient_combo.get()=="":
        messagebox.showinfo("showinfo","No user selected")
    else:
        for i in Listorder:
            list_order += str(i)
            time.sleep(1)
            
            answer_entry.config(state="normal")
            answer_entry.delete(1.0, tk.END)  
            answer_entry.insert(tk.END, list_order)
            answer_entry.config(state="disabled")
            root.update()  
            
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(str(i).encode('ascii'))
            time.sleep(1)  
        
        print("Sequence to remember:", list_order)
        
        root.update()
        
        
        correct_inputs = 0
        
        # For each expected number in the sequence
        for expected in list_order:
            # Tell Arduino we're ready for input mode - send this before EACH button press
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write("5".encode('ascii'))  # Activate button-listening mode for this button press
            
            answer_entry.config(state="normal")
            answer_entry.delete(1.0, tk.END)  
            answer_entry.insert(tk.END, list_order)
            answer_entry.config(state="disabled")
            
            while True:
                try:
                    if ser.in_waiting > 0:
                        response = ser.readline()
                        if response:
                            response_str = str(response, 'UTF-8').strip()
                            print(f"Received from Arduino: '{response_str}'")
                            
                            if response_str:
                                if response_str == expected:  # Correct Hoop
                                    correct_inputs += 1

                                    answer_entry.config(state="normal")
                                    answer_entry.delete(1.0, tk.END)
                                    answer_entry.insert(tk.END, f"Correct! {correct_inputs}/{len(list_order)}")
                                    answer_entry.config(state="disabled")
                                    root.update()

                                    time.sleep(0.5) 

                                    break  
                                else:  # Incorrect Hoop
                                    answer_entry.config(state="normal")
                                    answer_entry.delete(1.0, tk.END)
                                    answer_entry.insert(tk.END, f"Wrong! Expected {expected}, got {response_str}")
                                    answer_entry.config(state="disabled")
                                    root.update()

                                    randOrder(Listorder,attempts+1)
                                    return list_order 
                    
                    
                    root.update_idletasks()
                    root.update()
                    time.sleep(0.1)
                    
                except Exception as e:
                    print("Error reading from serial:")
                
    
    # if it gets through the loop add a point
    if correct_inputs == len(list_order):
        answer_entry.config(state="normal")
        answer_entry.delete(1.0, tk.END)
        answer_entry.insert(tk.END, "Success! All correct")
        answer_entry.config(state="disabled")
        print("Correct order in this many attempts: ", attempts)
        save_user_data_order(attempts)
    
    return list_order
      
# FLasher game
def Flasher(Trgt):
    #input target to ui
    Selected_Target = ""
    if Trgt == "a":
        Selected_Target = "Hoop 1"
    if Trgt == "b":
        Selected_Target = "Hoop 2"
    if Trgt == "c":
        Selected_Target = "Hoop 3"
    if Trgt == "d":
        Selected_Target = "Hoop 4"

    answer_entry.config(state="normal")
    answer_entry.delete(1.0, tk.END)  
    answer_entry.insert(tk.END, Selected_Target)
    answer_entry.config(state="disabled")

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    ser.write(Trgt.encode('ascii'))
    response = b''

    #wait for arduino's response and assign the correct point values
    while True:
        try:
            if ser.in_waiting > 0:
                response = ser.readline()
                if response:  
                    response_str = str(response, 'UTF-8').strip()
                    print(f"Received from Arduino: '{response_str}'")
                    if response_str:  
                        Flasher_PointChange(response_str)
                        break  
            
        
            root.update_idletasks()
            root.update()
            
            
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error reading from serial: {e}")
    
    


def load_patients():
    patients = []
    try:
        os.chdir('C:/Users/daviz/OneDrive/Documents/Sports Rehab')
        with open('User_List.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row: 
                    patients.append(row[0])
    
    except Exception as e:
        print(f"Error reading CSV: {e}")
    
    # Update User List
    select_patient_combo['values'] = patients

#add patient to User_List.CSV 
def add_a_patient():
    os.chdir('C:/Users/daviz/OneDrive/Documents/Sports Rehab') 
    data = patient_name_entry.get()
    if data.strip(): 
        print(data)
        
        try:
            with open('User_List.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([data])
                file.flush()  
        except Exception as e:
            print(f"Error writing to CSV: {e}")
        
        patient_name_entry.delete(0, tk.END)
        
        load_patients()
#exports data to csv file
def save_user_data():
    if select_patient_combo.get() == "":
        messagebox.showinfo("showinfo","No user selected")
    else:
       
        saved_data = [select_patient_combo.get(),"Flasher",FH1,FH2,FH3,FH4,FH1+2*FH2+2*FH3+FH4,Flash_level,datetime.datetime.now()]
        try:
            with open('User_Data.csv','a',newline = '') as file2:
                writer2 = csv.writer(file2)
                writer2.writerow(saved_data)
                file2.flush()
        except Exception as e2:
            print(f"Error writing to csv: {e2}")
        
        
        patient_name_entry.delete(0, tk.END)

def save_user_data_order(attempts):
    if select_patient_combo.get() == "":
        messagebox.showinfo("showinfo","No user selected")
    else:
       
        saved_data = [select_patient_combo.get(),"Memory",attempts,Order_level,datetime.datetime.now()]
        try:
            with open('User_Data.csv','a',newline = '') as file2:
                writer2 = csv.writer(file2)
                writer2.writerow(saved_data)
                file2.flush()
        except Exception as e2:
            print(f"Error writing to csv: {e2}")
        
        
        patient_name_entry.delete(0, tk.END)
# Placeholder variables for multiplayer game
P1_score = 0
P2_score = 0


#Multyplayer game
def create_multiplayer_game():
    
    BW = 0 #Blue Win
    BL = 0# Blue loss
    RW = 0#Red win
    RL = 0#Red loss
    RH1 = 0# Red hoop 1 
    RH2 = 0# Red hoop 2
    RH3 = 0
    RH4 = 0
    BH1 = 0
    BH2 = 0
    BH3 = 0
    BH4 = 0
    GP = 0# Games Played

    def MPointChange():
        global P1_score, P2_score
        P1_score =RH1+RH2*2+RH3*2+RH4
        score1_value.config(text=str(P1_score))
        
        P2_score = BH1+BH2*2+BH3*2+BH4
        score2_value.config(text=str(P2_score))

    def load_patients():
        patients = []
        try:
            os.chdir('C:/Users/daviz/OneDrive/Documents/Sports Rehab')
            with open('User_List.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        patients.append(row[0])
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error reading CSV: {e}")

        player1_dropdown['values'] = patients
        player2_dropdown['values'] = patients

    def pointdispo(dispo, RLL, RS):
        nonlocal BW, BL, RW, RL, RH1, RH2, RH3, RH4, BH1, BH2, BH3, BH4, GP
        
        if dispo[0] == "B":
            BW += 1
            RL += 1
            GP += 1

            games_played_entry.config(state="normal")
            games_played_entry.delete(0, tk.END)
            games_played_entry.insert(0, str(GP))
            games_played_entry.config(state="readonly")

            p2_wins_entry.config(state="normal")
            p2_wins_entry.delete(0, tk.END)
            p2_wins_entry.insert(0, str(BW))
            p2_wins_entry.config(state="readonly")

            p1_losses_entry.config(state="normal")
            p1_losses_entry.delete(0, tk.END)
            p1_losses_entry.insert(0, str(RL))
            p1_losses_entry.config(state="readonly")
            
        if dispo[0] == "R":
            RW += 1
            BL += 1
            GP += 1
            
            games_played_entry.config(state="normal")
            games_played_entry.delete(0, tk.END)
            games_played_entry.insert(0, str(GP))
            games_played_entry.config(state="readonly")

            p1_wins_entry.config(state="normal")
            p1_wins_entry.delete(0, tk.END)
            p1_wins_entry.insert(0, str(RW))
            p1_wins_entry.config(state="readonly")

            p2_losses_entry.config(state="normal")
            p2_losses_entry.delete(0, tk.END)
            p2_losses_entry.insert(0, str(BL))
            p2_losses_entry.config(state="readonly")
        
        if dispo[1] == '1':
            if RLL[0] == 1:
                RH1 += 1
                p1_entry1.delete(0, tk.END)
                p1_entry1.insert(0, str(RH1))
            if RLL[0] == 4:
                RH4 += 1
                p1_entry4.delete(0, tk.END)
                p1_entry4.insert(0, str(RH4))

        if dispo[2] == '1':
            if RS[0] == 2:
                RH2 += 1
                p1_entry2.delete(0, tk.END)
                p1_entry2.insert(0, str(RH2))
            if RS[0] == 3:
                RH3 += 1
                p1_entry3.delete(0, tk.END)
                p1_entry3.insert(0, str(RH3))

        if dispo[3] == '1':
            if RS[1] == 2:
                BH2 += 1
                p2_entry2.delete(0, tk.END)
                p2_entry2.insert(0, str(BH2))
            if RS[1] == 3:
                BH3 += 1
                p2_entry3.delete(0, tk.END)
                p2_entry3.insert(0, str(BH3))
        
        if dispo[4] == '1':
            if RLL[1] == 1:
                BH1 += 1
                p2_entry1.delete(0, tk.END)
                p2_entry1.insert(0, str(BH1))
            if RLL[1] == 4:
                BH4 += 1
                p2_entry4.delete(0, tk.END)
                p2_entry4.insert(0, str(BH4))
        MPointChange()
     # saves csv data   | if both users are selected and if they have played a game, they can save the data
    def save_user_data():
        os.chdir('C:/Users/daviz/OneDrive/Documents/Sports Rehab') 
        if player1_dropdown.get() == "" or player2_dropdown.get() == "":
            messagebox.showinfo("showinfo","No user selected")
        else:
            proceed1 = messagebox.askyesno("showinfo","Are you sure you have the correct user and want to save")
            if proceed1:
                saved_data = [player1_dropdown.get(),GP,RW,RL,RH1,RH2,RH3,RH4,P1_score,player2_dropdown.get(),GP,BW,BL,BH1,BH2,BH3,BH4,datetime.datetime.now()]
            try:
                with open('Multi-Data.csv','a',newline = '') as file2:
                    writer2 = csv.writer(file2)
                    writer2.writerow(saved_data)
                    file2.flush()
            except Exception as e2:
                    print(f"Error writing to csv: {e2}")
            
            
            player1_dropdown.delete(0, tk.END)
            player1_dropdown.delete(0, tk.END)

# selects the hoops 
    def change_colors():
        hoop1 = 1
        hoop2 = 2
        hoop3 = 3
        hoop4 = 4

        #first entry of Random_order_ is for the red hoop, second is for the blue hoop
        random_order_small = random.sample([hoop2, hoop3], 2)
        random_order_large = random.sample([hoop1, hoop4], 2)

        print(random_order_small)
        print(random_order_large)

        #used change the color of the hoop
        hoop_to_circle = {
            1: p1_outer_circles[0],
            2: p1_outer_circles[1],
            3: p2_outer_circles[0],
            4: p2_outer_circles[1],
        }
        canvas.itemconfig(hoop_to_circle[random_order_small[0]], fill="red")
        canvas.itemconfig(hoop_to_circle[random_order_large[0]], fill="red")
        canvas.itemconfig(hoop_to_circle[random_order_small[1]], fill="blue")
        canvas.itemconfig(hoop_to_circle[random_order_large[1]], fill="blue")

        #initates multiplayer game in arduino
        ser.write("m".encode('ascii'))
        
        ser.write(str(random_order_small[0]).encode('ascii'))
        print(random_order_small[0])
        time.sleep(0.1)
        ser.write(str(random_order_large[0]).encode('ascii'))
        print(random_order_large[0])
        time.sleep(0.1)
        ser.write(str(random_order_small[1]).encode('ascii'))
        print(random_order_small[1])
        
        ser.write(str(random_order_large[1]).encode('ascii'))
        print(random_order_large[1])
        
        #get arduinos response and update ui
        while True:
            try:
                if ser.in_waiting > 0:
                    response = ser.readline()
                    if response:
                        response_str = str(response, 'UTF-8').strip()
                        print(f"Received from Arduino: '{response_str}'")
                        if response_str:
                            pointdispo(response_str, random_order_large, random_order_small)
                            break
                window.update_idletasks()
                window.update()
                time.sleep(0.1)
            except Exception as e:
                print(f"Error reading from serial: {e}")

    window = tk.Tk()
    window.title("Multiplayer Game")
    window.geometry("750x750")

    def exit_game():
        if messagebox.askyesno("Exit Game", "Are you sure you want to exit?"):
            window.destroy()

# multiplayer ui

    
    main_frame = tk.Frame(window, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    
    title_label = tk.Label(main_frame, text="Guerras de Aro", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
    
    exit_button = tk.Button(main_frame, text="Salida", command=exit_game)
    exit_button.grid(row=0, column=4, sticky="e")
    
    # Player selection section
    player1_label = tk.Label(main_frame, text="Jugadora Rojo", font=("Arial", 12))
    player1_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
    
    player1_var = tk.StringVar()
    player1_dropdown = ttk.Combobox(main_frame, textvariable=player1_var, width=20, state="readonly")
    player1_dropdown.grid(row=2, column=0, sticky="w", padx=(0, 20))
    
    player2_label = tk.Label(main_frame, text="Jugadora Azul", font=("Arial", 12))
    player2_label.grid(row=1, column=3, sticky="w", pady=(0, 5))
    
    player2_var = tk.StringVar()
    player2_dropdown = ttk.Combobox(main_frame, textvariable=player2_var, width=20, state="readonly")
    player2_dropdown.grid(row=2, column=3, sticky="w")
    
    #Hoops
    canvas = tk.Canvas(main_frame, width=700, height=200, bg="light gray")
    canvas.grid(row=3, column=0, columnspan=5, pady=20)
    
    p1_outer_circles = []
    p1_inner_circles = []
    
    p1_outer_circles.append(canvas.create_oval(50, 30, 130, 110, width=2))
    p1_inner_circles.append(canvas.create_oval(60, 40, 120, 100, width=2, fill="white"))
    canvas.create_text(90, 70, text="Aro 1", font=("Arial", 10))
    
    p1_outer_circles.append(canvas.create_oval(170, 30, 250, 110, width=2))
    p1_inner_circles.append(canvas.create_oval(180, 40, 240, 100, width=2, fill="white"))
    canvas.create_text(210, 70, text="Aro 2", font=("Arial", 10))
    
    p2_outer_circles = []
    p2_inner_circles = []
    
    p2_outer_circles.append(canvas.create_oval(450, 30, 530, 110, width=2))
    p2_inner_circles.append(canvas.create_oval(460, 40, 520, 100, width=2, fill="white"))
    canvas.create_text(490, 70, text="Aro 3", font=("Arial", 10))
    
    p2_outer_circles.append(canvas.create_oval(570, 30, 650, 110, width=2))
    p2_inner_circles.append(canvas.create_oval(580, 40, 640, 100, width=2, fill="white"))
    canvas.create_text(610, 70, text="Aro 4", font=("Arial", 10))
    
    p1_entries = []
    
    tk.Label(main_frame, text="Aro 1").grid(row=4, column=0, sticky="w")
    p1_entry1 = tk.Entry(main_frame, width=5)
    p1_entry1.grid(row=4, column=0, sticky="e", padx=(50, 0))
    p1_entries.append(p1_entry1)
    
    tk.Label(main_frame, text="Aro 2").grid(row=5, column=0, sticky="w")
    p1_entry2 = tk.Entry(main_frame, width=5)
    p1_entry2.grid(row=5, column=0, sticky="e", padx=(50, 0))
    p1_entries.append(p1_entry2)
    
    tk.Label(main_frame, text="Aro 3").grid(row=6, column=0, sticky="w")
    p1_entry3 = tk.Entry(main_frame, width=5)
    p1_entry3.grid(row=6, column=0, sticky="e", padx=(50, 0))
    p1_entries.append(p1_entry3)
    
    tk.Label(main_frame, text="Aro 4").grid(row=7, column=0, sticky="w")
    p1_entry4 = tk.Entry(main_frame, width=5)
    p1_entry4.grid(row=7, column=0, sticky="e", padx=(50, 0))
    p1_entries.append(p1_entry4)
    
    p2_entries = []
    
    tk.Label(main_frame, text="Aro 1").grid(row=4, column=3, sticky="w")
    p2_entry1 = tk.Entry(main_frame, width=5)
    p2_entry1.grid(row=4, column=3, sticky="e", padx=(50, 0))
    p2_entries.append(p2_entry1)
    
    tk.Label(main_frame, text="Aro 2").grid(row=5, column=3, sticky="w")
    p2_entry2 = tk.Entry(main_frame, width=5)
    p2_entry2.grid(row=5, column=3, sticky="e", padx=(50, 0))
    p2_entries.append(p2_entry2)
    
    tk.Label(main_frame, text="Aro 3").grid(row=6, column=3, sticky="w")
    p2_entry3 = tk.Entry(main_frame, width=5)
    p2_entry3.grid(row=6, column=3, sticky="e", padx=(50, 0))
    p2_entries.append(p2_entry3)
    
    tk.Label(main_frame, text="Aro 4").grid(row=7, column=3, sticky="w")
    p2_entry4 = tk.Entry(main_frame, width=5)
    p2_entry4.grid(row=7, column=3, sticky="e", padx=(50, 0))
    p2_entries.append(p2_entry4)
    
    # Player score 1 is red 2 is blue
    score1_label = tk.Label(main_frame, text="Puntaje", font=("Arial", 12))
    score1_label.grid(row=8, column=0, sticky="w", pady=(20, 5))
    
    score1_frame = tk.Frame(main_frame, highlightbackground="black", highlightthickness=1)
    score1_frame.grid(row=9, column=0, sticky="w")
    score1_value = tk.Label(score1_frame, text=str(P1_score), font=("Arial", 14), width=8)
    score1_value.pack(pady=5)
    
    score2_label = tk.Label(main_frame, text="Puntaje", font=("Arial", 12))
    score2_label.grid(row=8, column=3, sticky="w", pady=(20, 5))
    
    score2_frame = tk.Frame(main_frame, highlightbackground="black", highlightthickness=1)
    score2_frame.grid(row=9, column=3, sticky="w")
    score2_value = tk.Label(score2_frame, text=str(P2_score), font=("Arial", 14), width=8)
    score2_value.pack(pady=5)
    
    # Start button
    change_colors_button = tk.Button(main_frame, text="Nueva Ronda", command=change_colors)
    change_colors_button.grid(row=5, column=1, columnspan=2, pady=20)
    
    tk.Label(main_frame, text="Juegos Jugados:", font=("Arial", 12)).grid(row=10, column=1, columnspan=2, pady=(20, 0))
    games_played_entry = tk.Entry(main_frame, width=5, state="readonly", justify="center")
    games_played_entry.grid(row=11, column=1, columnspan=2, pady=(5, 0))
    
    # Wins and losses
    tk.Label(main_frame, text="Victorias:", font=("Arial", 10)).grid(row=12, column=0, sticky="w")
    p1_wins_entry = tk.Entry(main_frame, width=5, state="readonly")
    p1_wins_entry.grid(row=12, column=0, sticky="e", padx=(50, 0))
    
    tk.Label(main_frame, text="Pérdidas:", font=("Arial", 10)).grid(row=13, column=0, sticky="w")
    p1_losses_entry = tk.Entry(main_frame, width=5, state="readonly")
    p1_losses_entry.grid(row=13, column=0, sticky="e", padx=(50, 0))
    
    tk.Label(main_frame, text="Victorias:", font=("Arial", 10)).grid(row=12, column=3, sticky="w")
    p2_wins_entry = tk.Entry(main_frame, width=5, state="readonly")
    p2_wins_entry.grid(row=12, column=3, sticky="e", padx=(50, 0))
    
    tk.Label(main_frame, text="Pérdidas:", font=("Arial", 10)).grid(row=13, column=3, sticky="w")
    p2_losses_entry = tk.Entry(main_frame, width=5, state="readonly")
    p2_losses_entry.grid(row=13, column=3, sticky="e", padx=(50, 0))
    
    #Save button
    save_button = tk.Button(main_frame, text="Guardar", command= lambda: save_user_data())
    save_button.grid(row=14, column=1, columnspan=2, pady=(20, 40))
    
    load_patients()
    window.mainloop()

hoopLetters = ["a","b","c","d"]

#Main UI
root = tk.Tk()
root.title("MMHS")

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# Flasher label and buttons
flashing_label = tk.Label(main_frame, text="Parpadeo Rápido", font=("Arial", 14))
flashing_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

hoop_frame = tk.Frame(main_frame)
hoop_frame.grid(row=1, column=0, columnspan=7, sticky="w", pady=(0, 10))

random_btn = tk.Button(hoop_frame, text="Comenzar", command = lambda: flasher_game())
random_btn.pack(side="left", padx=2)

Fscore_Label = tk.Label(hoop_frame, text="Puntaje: ")
Fscore_Label.pack(side="left", padx=2)

Fscore_Value = tk.Label(hoop_frame, text="0")
Fscore_Value.pack(side="left", padx=2)



hoop_frame.update()  

hoop1_label = tk.Label(main_frame, text="Aro 1")
hoop1_label.grid(row=2, column=0, sticky="w")

hoop1_frame = tk.Frame(main_frame)
hoop1_frame.grid(row=2, column=0, sticky="e", padx=(50, 0))

hoop1_counter = tk.Label(hoop1_frame, text=str(Flash_win), width=2)
hoop1_counter.pack(side="left")

hoop3_label = tk.Label(main_frame, text="Aro 3")
hoop3_label.grid(row=2, column=1, sticky="w")

hoop3_frame = tk.Frame(main_frame)
hoop3_frame.grid(row=2, column=1, sticky="e", padx=(50, 0))

hoop3_counter = tk.Label(hoop3_frame, text=str(FH3), width=2)
hoop3_counter.pack(side="left")


# Flasher Level
flasher_level_label = tk.Label(main_frame, text="Nivel")
flasher_level_label.grid(row=2, column=3, sticky="e", padx=(15, 0))

flasher_level_minus = tk.Button(main_frame, text="-", width=2, command= lambda: settings("FL-"))
flasher_level_minus.grid(row=2, column=4)

flasher_level_value = tk.Label(main_frame, text=str(Flash_level), width=2)
flasher_level_value.grid(row=2, column=5)

flasher_level_plus = tk.Button(main_frame, text="+", width=2,command= lambda: settings("FL+"))
flasher_level_plus.grid(row=2, column=6)


hoop2_label = tk.Label(main_frame, text="Aro 2")
hoop2_label.grid(row=3, column=0, sticky="w")

hoop2_frame = tk.Frame(main_frame)
hoop2_frame.grid(row=3, column=0, sticky="e", padx=(50, 0))

hoop2_counter = tk.Label(hoop2_frame, text=str(Flash_Lose), width=2)
hoop2_counter.pack(side="left")


hoop4_label = tk.Label(main_frame, text="Aro 4")
hoop4_label.grid(row=3, column=1, sticky="w")

hoop4_frame = tk.Frame(main_frame)
hoop4_frame.grid(row=3, column=1, sticky="e", padx=(50, 0))

hoop4_counter = tk.Label(hoop4_frame, text=str(FH4), width=2)
hoop4_counter.pack(side="left")


# Order Title and start 
order_label = tk.Label(main_frame, text="Secuencia", font=("Arial", 14))
order_label.grid(row=4, column=0, sticky="w", pady=(10, 5))

start_order_btn = tk.Button(main_frame, text="Comenzar - Order", command = lambda: randOrder(random.sample(rand_order_hoop_list,4),1))
start_order_btn.grid(row=4, column=1, sticky="w")

# Games Won for Order
games_won_label2 = tk.Label(main_frame, text="Attempts")
games_won_label2.grid(row=5, column=0, sticky="w")

games_won_frame2 = tk.Frame(main_frame)
games_won_frame2.grid(row=5, column=1, sticky="w")

games_won_count2 = tk.Label(games_won_frame2, text=str(Order_win))
games_won_count2.pack(side="left")


# Level setting for Order
order_level_label = tk.Label(main_frame, text="Nivel:")
order_level_label.grid(row=5, column=3, sticky="e", padx=(15, 0))

order_level_minus = tk.Button(main_frame, text="-", width=2, command= lambda: settings("OL-"))
order_level_minus.grid(row=5, column=4)

order_level_value = tk.Label(main_frame, text=str(Order_level), width=2)
order_level_value.grid(row=5, column=5)

order_level_plus = tk.Button(main_frame, text="+", width=2,command= lambda: settings("OL+"))
order_level_plus.grid(row=5, column=6)

Multi_label = tk.Label(main_frame, text="Guerras de Aro", font=("Arial", 14))
Multi_label.grid(row=7, column=0, sticky="w", pady=(10, 5))

start_Multi_btn = tk.Button(main_frame, text="Comenzar",command= lambda: create_multiplayer_game())
start_Multi_btn.grid(row=7, column=1, sticky="w")


answer_frame = tk.Frame(main_frame)
answer_frame.grid(row=10, column=0, columnspan=10, sticky="w", pady=(30, 5))

answer_label = tk.Label(answer_frame, text="Respuesta", font=("Arial", 14))
answer_label.grid(row=0, column=0, sticky="nw")

answer_entry = tk.Text(answer_frame, width=30, height=3)
answer_entry.insert(tk.END, list_order)  
answer_entry.config(state="disabled")     
answer_entry.grid(row=0, column=1, sticky="w", padx=(5, 0))

user_selection_label = tk.Label(main_frame, text="Selección de Usuario", font=("Arial", 14))
user_selection_label.grid(row=11, column=0, sticky="w", pady=(20, 5))

save_data_btn = tk.Button(main_frame, text="Guardar Datos", command = lambda: save_user_data())
save_data_btn.grid(row=12, column=0, columnspan=2, sticky="w", pady=(5, 5))

select_patient_label = tk.Label(main_frame, text="Seleccionar usuario")
select_patient_label.grid(row=13, column=0, sticky="w")

select_patient_combo = ttk.Combobox(main_frame, width=38, state="readonly")
select_patient_combo.grid(row=13, column=1, columnspan=3, sticky="w")

patient_name_label = tk.Label(main_frame, text="Nombre de usuario:")
patient_name_label.grid(row=14, column=0, sticky="w")

patient_name_entry = tk.Entry(main_frame, width=40)
patient_name_entry.grid(row=14, column=1, columnspan=3, sticky="w")

add_patient_btn = tk.Button(main_frame, text="Agregar un Nuevo Paciente", command=lambda: add_a_patient())
add_patient_btn.grid(row=15, column=0, columnspan=2, sticky="w", pady=(5, 0))

exit_btn = tk.Button(main_frame, text="Salida", command=lambda: main_exit_game())
exit_btn.grid(row=16, column=0, columnspan=2, sticky="w", pady=(5, 0))

load_patients()

root.mainloop()