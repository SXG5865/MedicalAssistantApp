import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import difflib
import sys
from tkinter import *
from PIL import Image, ImageTk

#global variables for profile info
profile_info = {
    "gender": None,
    "age": None,
    "medical_history": None
}



#-------------------------------------------------GUI-----------------------------------------------------$

#Navigation functions
def save_profile():
    #save selected gender to profile_info dict. using the val of gender_var
    profile_info["gender"] = gender_var.get()
    #save selected age to profile_info dict. using the val of the age_combobox
    profile_info["age"] = age_combobox.get()
    #save entered medical history to profile_info dict.
    #"1.0" is the starting index (row 1, column 0) of the text box
    #"tk.END" refers to the end of the text box content, allowing the function to capture everything in it
    profile_info["medical_history"] = medical_history_text.get("1.0", tk.END).strip()
    #show a message box w/ a confirmation message
    messagebox.showinfo("Profile Saved", "Your profile information has been saved.")

#displays the homepage by hiding other frames and showing the homepage_frame
def show_profile_page():
    hide_all_frames()
    #fill = "both" means that the widget will stretch both horizontally and vertically to fill the avaliable space
    profile_frame.pack(fill="both", expand=True)
    #expand = True means that the widget will expand to fill any additional space, sharing it with other widgets that also have expand=True

#displays the profile page by hiding other frames and showing the profile_frame
def show_homepage():
    hide_all_frames()
    homepage_frame.pack(fill="both", expand=True)

#displays the profile page by hiding other frames and showing the profile_frame
def show_symptom_page():
    hide_all_frames()
    symptom_frame.pack(fill="both", expand=True)

#displays the condition search page by hiding other frames and showing the condition
def show_conditionSearch_page():
    hide_all_frames()
    condition_search_frame.pack(fill="both", expand=True)

#hides all frames to prepare for showing a specific frame
#used for apps that use multiple frames but only shows one at a time
def hide_all_frames():
    #iterate over the list of frames
    for frame in [homepage_frame, profile_frame, symptom_frame, condition_search_frame]:
        #method that removes the widget (a frame) from the visible layout
        frame.pack_forget() #removes it from the layout, hiding it from view without destroying it

###########################################################################################################
#GUI setup
root = tk.Tk() #creates main app window; starting point for any Tkinter app
root.title("Medical Assistant App") #sets title of app window
root.geometry("500x600") #sets the size of the window

#dict to trafck all frames
windows = {}

##############################################################################################################
#Homepage
#creates a frame to hold all the widgets for the homepage
homepage_frame = tk.Frame(root)
#root is parent widget (displayed in main app window)
#adds a label to the homepage, displays the welcome message
tk.Label(homepage_frame, text="Welcome to the Medical Assistant App", font=("Arial", 16)).pack(pady=20)
# ".pack(pady=20)" places the label in the frame with pack() and adds a vertical padding of 20 pixels above and below (for space)
#adds a button to navigate to the profile page
#width is 30; pack(pady=10) means vertical padding of 10 above and below button
tk.Button(homepage_frame, text="Visit Profile", command=show_profile_page, width=30).pack(pady=10)
#adds a button to navigate to the symptom page
#width is 30; pack(pady=10) means vertical padding of 10 above and below button
tk.Button(homepage_frame, text="Enter My Symptoms", command=show_symptom_page, width=30).pack(pady=10)
#adds a button to navigate to the condition page
#width is 30; pack(pady=10) means vertical padding of 10 above and below button
tk.Button(homepage_frame, text="Search for Information on a Condition", command=show_conditionSearch_page, width=30).pack(pady=10)
#adds a button to end the program
#width is 30; pack(pady=10) means vertical padding of 10 above and below button
tk.Button(homepage_frame, text="Exit", command=root.quit, width=30).pack(pady=10)
# a label for a disclaimer that we are not real medical care professionals! Can change to color red.
#wraplength limits the label's text to 400 pixels. it will wrap to next line if it exceeds
#justify:aligns the text to the center ("center" alignment).
tk.Label(homepage_frame, text="Disclaimer: This is not a verified medical professional.\nIf this is a medical emergency, call 911.", fg="red", wraplength=400, justify="center").pack(pady=20)

############################################################################################################################################################
#Profile Page
profile_frame = tk.Frame(root)
#label for profile information
tk.Label(profile_frame, text="Profile Information", font=("Arial", 16)).pack(pady=20)

######
#SOURCE:https://www.geeksforgeeks.org/light-or-dark-theme-changer-using-tkinter/

#creating a dark and light mode for the app; for light sensitivity
#creating a label for dark and light mode
tk.Label(profile_frame, text="Choose Light Mode or Dark Mode:").pack(anchor="w",padx=20)
#adding light and dark mode images
lightImage = Image.open('images\light mode.png')
darkImage = Image.open('images\dark mode.png')
#RESIZING EACH IMAGE USING PILLOW LIBRARY
#SOURCE: https://www.geeksforgeeks.org/how-to-resize-image-in-python-tkinter/
resize_imageL = lightImage.resize((180,80))
resize_imageD = darkImage.resize((180,80))
light = ImageTk.PhotoImage(resize_imageL)
dark = ImageTk.PhotoImage(resize_imageD)
switch_value = True

# recursive func to apply theme to all widgets
def apply_theme(widget, bg, fg):
    #applies background (bg) and foreground (fg) theme to all children widgets within parent widget
    #bg = background color
    #fg = foreground (text) color
    try:
        #check if widget is button or label. if true, update its background and foreground
        # update basic widget colors
        if isinstance(widget, (Button, Label)):
            widget.config(bg=bg, fg=fg)
        #update radio button widgets (diff from button and label because it becomes diff when selected )
        elif isinstance(widget, tk.Radiobutton):
            widget.config(bg=bg, fg=fg, selectcolor=bg)
        #check if widget is a frame
        #if true, update only its BG color
        elif isinstance(widget, tk.Frame):
            widget.config(bg=bg)

    #print an error message if the widget cannot be added
    except Exception as e:
        print(f"Error applying theme to {widget}: {e}")

    # recursive apply theme to child widgets of current widget
    for child in widget.winfo_children():
        apply_theme(child, bg, fg)




#defining a function to toggle between both themes
def toggle():
    #updates for all windows and frames
    global switch_value #uses the global var to track the current theme state

    if switch_value:
        #set the toggle button to dark mode appearance
        switch.config(image=dark, bg="#26242f",
                      activebackground="#26242f")

        #apply dark mode theme to all frames in all registered windows
        for win, frames in windows.items():
            for frame in frames:
                apply_theme(frame, bg = "#26242f", fg = "white")
        #update the theme state to dark mode
        switch_value = False

    else:
        #set the toggle button to light mode appearance
        switch.config(image=light, bg="white", activebackground="white")

        #apply light mode theme to all frames
        for win, frames in windows.items():
            for frame in frames:
                apply_theme(frame, bg="white", fg = "black")
        #update theme state to light mode
        switch_value = True


#creating a button to toggle between light and dark themes
switch = Button(profile_frame, image=light, bd=0, bg = "white", activebackground = "white", command=toggle)
switch.pack(anchor="w",padx=20)
######END OF LIGHT MODE AND DARK MODE FEATURE

#creates a variable to store the user gender selection
gender_var = tk.StringVar() #Tkiner class used to manage string variables
tk.Label(profile_frame, text="Gender:").pack(anchor="w", padx=20) #variable is linked to gender radio buttons so will auto update
#label texts will display "Gender:" as the label's text
#anchor = "w" aligns the label to the left (west) of the frame
#variable "gender_var" links the button to the variable.
#tristatevalue sent to "x" because the variable value and the tristate value are the same for all 3, which caused them to be auto selected.
#set tristatevalue to "x" so it matches the default value of the associated variable
#source: https://stackoverflow.com/questions/40684739/why-do-tkinters-radio-buttons-all-start-selected-when-using-stringvar-but-not-i
tk.Radiobutton(profile_frame, text="Male", variable=gender_var, value="Male", tristatevalue="x").pack(anchor="w", padx=20)
tk.Radiobutton(profile_frame, text="Female", variable=gender_var, value="Female", tristatevalue="x").pack(anchor="w", padx=20)
tk.Radiobutton(profile_frame, text="Other", variable=gender_var, value="Other", tristatevalue="x").pack(anchor="w", padx=20)

#label for age
tk.Label(profile_frame, text="Age:").pack(anchor="w", padx=20, pady=10)
#adds a combobox for selecting age. values specifies the list of options (ages 1 to 100)
age_combobox = ttk.Combobox(profile_frame, values=[str(i) for i in range(1, 101)]) # generates a list of strings represents numbers 1 thru 100
#places the age combobox in the frame; 40 pixels of horizontal padding
age_combobox.pack(anchor="w", padx=40)
#adds a label to prompt the user to enter their medical history
#padx = 20; 20 pixels of horizontal padding
#pady = 10; 10 pixels of vertical padding above and yellow
tk.Label(profile_frame, text="Medical History:").pack(anchor="w", padx=20, pady=10)
#adds a multi-line text box for entering medical history
#height = sets text box height to 5 lines
#width = sets text box width to 40 chars.
medical_history_text = tk.Text(profile_frame, height=5, width=40)
#places the medical history text box in the frame; 40 horizontal padding left and right
medical_history_text.pack(padx=40)
#adds a button to save the user's profile information
#command = links button to save_profile func
tk.Button(profile_frame, text="Save Profile", command=save_profile).pack(pady=10)
#command = show_homepage; goes back to homepage
tk.Button(profile_frame, text="Back to Homepage", command=show_homepage).pack(pady=10)

# Symptom Page
symptom_frame = tk.Frame(root)
tk.Label(symptom_frame, text="Enter Your Symptoms", font=("Arial", 16)).pack(pady=20)

# Create a frame for symptom input
symptom_input_frame = tk.Frame(symptom_frame) #subframe to organize symptom entry and its scrollbar
symptom_input_frame.pack(pady=10)

# Symptom Entry with Scrollbar
#adds multi-line textbox
symptom_text = tk.Text(symptom_input_frame, height=5, width=40, wrap=tk.WORD)
symptom_text.pack(side=tk.LEFT, padx=5)

# Scrollbar for symptom text
symptom_scrollbar = tk.Scrollbar(symptom_input_frame, command=symptom_text.yview)
symptom_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
symptom_text.config(yscrollcommand=symptom_scrollbar.set)


# Back to Homepage Button
back_button = tk.Button(symptom_frame, text="Back to Homepage", command=show_homepage)
back_button.pack()

#Condition Search Page
condition_search_frame = tk.Frame(root)
tk.Label(condition_search_frame, text="Search for a Medical Condition", font=("Arial", 16)).pack(pady=20)
condition_entry = tk.Entry(condition_search_frame, width=40)
condition_entry.pack(pady=10)

#register all the frames (FOR LIGHT MODE AND DARK MODE!!)
windows[root] = [profile_frame, homepage_frame, condition_search_frame, symptom_frame]

##########################################################################################################
#ConditionGraph Class
class ConditionGraph:

    def __init__(self):
        self.graph = {
            'conditions': {},
            'symptoms': {}
        }

    def load_data(self, file_path):
        """Load data from a CSV file and categorize conditions and symptoms."""
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return
        except ValueError:
            print(f"Error: Cannot read the file, please ensure it's a valid CSV file.")
            return

        df.columns = df.columns.str.strip()
        required_columns = ['Condition']
        symptom_columns = [col for col in df.columns if col.lower().startswith('symptom')]

        if not symptom_columns or 'Condition' not in df.columns:
            print(f"Error: Missing necessary columns (Symptom columns or Condition) in the CSV file.")
            return

        for _, row in df.iterrows():
            condition = row['Condition'].strip().lower()

            if condition not in self.graph['conditions']:
                self.graph['conditions'][condition] = []

            for col in symptom_columns:
                symptom = row[col].strip().lower()
                if pd.notna(symptom):
                    if symptom not in self.graph['symptoms']:
                        self.graph['symptoms'][symptom] = []

                    if symptom not in self.graph['conditions'][condition]:
                        self.graph['conditions'][condition].append(symptom)

                    if condition not in self.graph['symptoms'][symptom]:
                        self.graph['symptoms'][symptom].append(condition)

    def match_symptoms_to_conditions(self, symptoms):
        """Match the symptoms entered by the user to corresponding conditions."""
        matched_conditions = set()

        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if symptom_lower in self.graph['symptoms']:
                matched_conditions.update(self.graph['symptoms'][symptom_lower])

        return matched_conditions

    def suggest_correction(self, user_input, valid_list):
        """Suggest corrections for user input using difflib."""
        suggestions = difflib.get_close_matches(user_input.lower(), valid_list, n=1, cutoff=0.8)
        return suggestions[0] if suggestions else None


#Instantiate ConditionGraph and load data
condition_graph = ConditionGraph()
condition_graph.load_data('database/FinalProjectDatabase.csv')  # Ensure correct file path




###################################--SYMPTOM MATCHER--#######################################################
def submit_symptoms():
    # Clear any previous result labels
    for widget in symptom_frame.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button)) and widget not in [submit_button, back_button,
                                                                        symptom_text, symptom_scrollbar] and \
                not widget.cget("text").startswith(("Enter Your Symptoms", "Submit Symptoms", "Back to Homepage")):
            widget.destroy()

    # Get symptoms and process them
    symptoms = symptom_text.get("1.0", tk.END).strip().split("\n")

    # List of all valid symptoms from the graph
    valid_symptoms = list(condition_graph.graph['symptoms'].keys())

    # Track matched conditions and symptoms that need correction
    matched_conditions = set()
    suggestions = {}

    for symptom in symptoms:
        symptom_lower = symptom.lower().strip()
        if symptom_lower in condition_graph.graph['symptoms']:
            # Direct match found
            matched_conditions.update(condition_graph.graph['symptoms'][symptom_lower])
        else:
            # Try to find a suggestion
            suggestion = condition_graph.suggest_correction(symptom_lower, valid_symptoms)
            if suggestion:
                # If a suggestion is found
                suggestions[symptom] = suggestion
                matched_conditions.update(condition_graph.graph['symptoms'][suggestion])

    # Create result labels dynamically
    if matched_conditions:
        # Conditions matched label
        conditions_label = tk.Label(symptom_frame,
                                    text=f"Conditions associated with the symptoms:\n{', '.join(matched_conditions)}",
                                    wraplength=400,
                                    justify=tk.LEFT)
        conditions_label.pack(pady=10)

        # Suggestions label (if any)
        if suggestions:
            suggestion_text = "Symptom Suggestions:\n" + \
                              "\n".join([f"'{orig}' -> '{sugg}'" for orig, sugg in suggestions.items()])
            suggestions_label = tk.Label(symptom_frame,
                                         text=suggestion_text,
                                         fg="blue",
                                         wraplength=400,
                                         justify=tk.LEFT)
            suggestions_label.pack(pady=5)

    elif suggestions:
        # Only suggestions found
        suggestion_text = "No exact matches found. Did you mean:\n" + \
                          "\n".join([f"'{orig}' -> '{sugg}'" for orig, sugg in suggestions.items()])
        suggestions_label = tk.Label(symptom_frame,
                                     text=suggestion_text,
                                     fg="blue",
                                     wraplength=400,
                                     justify=tk.LEFT)
        suggestions_label.pack(pady=10)

    else:
        # No matches at all
        no_match_label = tk.Label(symptom_frame,
                                  text="No conditions matched the symptoms entered.",
                                  fg="red",
                                  wraplength=400,
                                  justify=tk.LEFT)
        no_match_label.pack(pady=10)

def search_condition():
    search_term = condition_entry.get().strip().lower()
    suggested_condition = condition_graph.suggest_correction(search_term, list(condition_graph.graph['conditions'].keys()))
    if suggested_condition:
        messagebox.showinfo("Condition Found", f"Found: {suggested_condition}")
        symptoms = condition_graph.graph['conditions'][suggested_condition]
        messagebox.showinfo("Symptoms", f"Symptoms: {', '.join(symptoms)}")
    else:
        messagebox.showinfo("Condition Not Found", f"No condition found for '{search_term}'.")

tk.Button(condition_search_frame, text="Search", command=search_condition).pack(pady=10)
tk.Button(condition_search_frame, text="Back to Homepage", command=show_homepage).pack()

# Submit Symptoms Button
submit_button = tk.Button(symptom_frame, text="Submit Symptoms", command=submit_symptoms)
submit_button.pack(pady=10)


#Show Homepage by default
show_homepage()

#Start tkinter main loop
root.mainloop()
