import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import pandas as pd
import difflib
import sys
from PIL import Image, ImageTk

#global variables for profile info
profile_info = {
    "gender": None,
    "age": None,
    "medical_history": None
}

#global for condition search
suggestion_label = None
no_match_label = None
condition_label = None

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

#displays the pain assessment page by hiding other frames and showing the pain_assessment_frame
def show_pain_assessment_page():
    hide_all_frames()
    pain_assessment_frame.pack(fill="both", expand=True)
    # Reapply theme to the pain assessment frame
    apply_theme(pain_assessment_frame,
                bg="#26242f" if not switch_value else "white",
                fg="white" if not switch_value else "black")

#hides all frames to prepare for showing a specific frame
#used for apps that use multiple frames but only shows one at a time
def hide_all_frames():
    #iterate over the list of frames
    for frame in [homepage_frame, profile_frame, symptom_frame, condition_search_frame, pain_assessment_frame]:
        #method that removes the widget (a frame) from the visible layout
        frame.pack_forget() #removes it from the layout, hiding it from view without destroying it
###########################################################################################################
#GUI setup
root = tk.Tk() #creates main app window; starting point for any Tkinter app
root.title("Medical Assistant App") #sets title of app window
root.geometry("1024x768") #sets the size of the window
#dict to track all frames
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
disclaimer_label = tk.Label(homepage_frame, text="Disclaimer: This is not a verified medical professional.\nIf this is a medical emergency, call 911.", fg="red", wraplength=400, justify="center")
disclaimer_label.pack(pady=20)

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
lightImage = Image.open('images/light mode.png')
darkImage = Image.open('images/dark mode.png')

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
    # global variables for search condition
    global suggestion_label, no_match_label, condition_label

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

    # ensure the disclaimaer label remains red
    disclaimer_label.config(fg="red")

    #update only if they exist
    if suggestion_label:
        suggestion_label.config(fg="blue")
    if no_match_label:
        no_match_label.config(fg="red")
    if condition_label:
        condition_label.config(fg="green")

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

#################################################################################
# Symptom Page
symptom_frame = tk.Frame(root)

#title label
tk.Label(symptom_frame, text="Symptom Checker", font=("Arial", 16)).pack(pady=20)

#label and entry for symptom, count
tk.Label(symptom_frame, text="How many symptoms would you like to enter? (1-5)", font=("Arial", 12)).pack(pady=20)
symptom_count_val = tk.StringVar() #variable to hold the number of symptopms
symptom_count_entry = tk.Entry(symptom_frame, textvariable=symptom_count_val, width=10)
symptom_count_entry.pack(pady=10)

# Global variables
symptom_texts = [] #list to build text widgets for symptoms
submit_button = None #Reference for submit button
reset_button = None #reference for reset button

def symptom_boxes():
    #dynamically creates text boxes based on the users desired number
    #ensures that the user enters a valid number between 1 and 5
    global symptom_texts, submit_button, reset_button

    try:
        # Validate input
        symptom_count = int(symptom_count_val.get())

        # Check bounds
        if symptom_count < 1 or symptom_count > 5:
            messagebox.showerror("Invalid Number", "Please enter a number between 1 and 5.")
            return

        #disable symptom count entry to prevent changes
        symptom_count_entry.config(state=tk.DISABLED)

        # Clear previous widgets (except for symptom count)
        for widget in symptom_frame.winfo_children():
            if widget not in [symptom_count_entry]:
                widget.destroy()

        # label to prompt users for symptoms
        tk.Label(symptom_frame, text=f"Enter {symptom_count} Symptoms", font=("Arial", 12)).pack(pady=10)

        #create text boxes for symptoms
        symptom_texts = []
        for i in range(symptom_count):
            tk.Label(symptom_frame, text=f"Symptom {i + 1}:").pack()
            symptom_text = tk.Text(symptom_frame, height=2, width=40, wrap=tk.WORD)
            symptom_text.pack(pady=5)
            symptom_texts.append(symptom_text)

        #  add the Submit button for symptoms
        submit_button = tk.Button(symptom_frame,
                                  text="Submit Symptoms",
                                  command=submit_symptoms)
        submit_button.pack(pady=10)

        #add the reset button to reset the entire process
        reset_button = tk.Button(symptom_frame, text = "Reset", command=reset_symptom_page)
        reset_button.pack(pady=10)
        # Back to Homepage Button
        back_button = tk.Button(symptom_frame,
                                text="Back to Homepage",
                                command=show_homepage)
        back_button.pack(pady=10)

        # Reapply theme to the symptom_frame and its children
        apply_theme(symptom_frame, bg="#26242f" if not switch_value else "white",
                    fg="white" if not switch_value else "black")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

dangerous_symptoms = [
    "Coughing Blood",
    "Chest Pain",
    "Slurred Speech",
    "Paralysis",
    "Unexplained Weight Loss",
    "Severe Shortness of Breath",
    "Stiff Neck with Fever",
    "Irregular Heartbeat",
    "Persistent High Fever"
]

def submit_symptoms():
    # Collect and process symptoms from text boxes and matches to condition
    #NOTE: global declares a variable in the global scope, which means it can be accessed and modified inside functions
    global symptom_texts

    #collect symptoms from text boxes
    #"1.0", tk.END
    #"1.0" -> Refers to the starting position of the text in TEXT widget.
    #"1" means first line, "0" means character index (column 0) on that line. means very beginning
    #tk.END refers to the end of the text in the widget.
    #"1.0", tk.END essentially extracts all text from the widget
    symptoms = [text.get("1.0", tk.END).strip().lower() for text in symptom_texts]
    #list comprehension; used to filter our empty entries from a list
    #"symptom for symptom in symptoms" iterates each item in symptom list
    #if symptom condition ensures that only non empty entries are included in the list
    symptoms = [symptom for symptom in symptoms if symptom]  # Remove empty entries

    integrate_dangerous_symptoms_check(symptoms)

    if not symptoms:
        messagebox.showwarning("No Symptoms", "Please enter at least one symptom.")
        return

    # Find conditions that have ALL symptoms
    matched_conditions = set()
    unmatched_symptoms = []
    suggested_symptoms = {}  # Dictionary to track suggested corrections

    # First pass: check for exact matches
    for condition, condition_symptoms in condition_graph.graph['conditions'].items():
        # Check if ALL user symptoms are in the condition's symptoms
        if all(symptom in condition_symptoms for symptom in symptoms):
            matched_conditions.add(condition)

    # If no exact matches, try to find suggestions
    if not matched_conditions:
        # Check for symptoms in the graph
        for symptom in symptoms:
            if symptom not in condition_graph.graph['symptoms']:
                # Try to find a close match for unmatched symptoms
                suggestion = condition_graph.suggest_correction(symptom, list(condition_graph.graph['symptoms'].keys()))
                if suggestion:
                    # If a suggestion is found, store it
                    suggested_symptoms[symptom] = suggestion
                else:
                    unmatched_symptoms.append(symptom)

        # Recheck with suggested symptoms
        if not unmatched_symptoms:
            for condition, condition_symptoms in condition_graph.graph['conditions'].items():
                if all(symptom in condition_symptoms for symptom in symptoms):
                    matched_conditions.add(condition)

    # Clear previous result labels
    for widget in symptom_frame.winfo_children():
        if isinstance(widget, tk.Label) and "symptom" not in widget.cget("text").lower():
            widget.destroy()

    # Display results
    if matched_conditions:
        tk.Label(symptom_frame,
                 text=f"Conditions with ALL symptoms:\n{', '.join(matched_conditions)}",
                 fg="green",
                 wraplength=400,
                 justify=tk.LEFT).pack(pady=10)

    # Display suggestions for mistyped symptoms
    if suggested_symptoms:
        suggestion_text = "Did you mean:\n"
        for original, suggestion in suggested_symptoms.items():
            suggestion_text += f"- '{original}' → '{suggestion}'\n"

        tk.Label(symptom_frame,
                 text=suggestion_text,
                 fg="blue",
                 wraplength=400,
                 justify=tk.LEFT).pack(pady=5)

    # Display unmatched symptoms
    if unmatched_symptoms:
        tk.Label(symptom_frame,
                 text=f"Unmatched Symptoms:\n{', '.join(unmatched_symptoms)}",
                 fg="red",
                 wraplength=400,
                 justify=tk.LEFT).pack(pady=5)

    # If no conditions found and no suggestions
    if not matched_conditions and not suggested_symptoms:
        tk.Label(symptom_frame,
                 text="No conditions found matching all symptoms.",
                 fg="red",
                 wraplength=400,
                 justify=tk.LEFT).pack(pady=10)


#resets the symptom page, clears all text boxes and asks the user for a new num of symptoms
def reset_symptom_page():

    global symptom_texts, submit_button, reset_button, symptom_count_entry

    #clear all widgets
    for widget in symptom_frame.winfo_children():
        widget.destroy()

    #reinitialize the page
    # title label
    tk.Label(symptom_frame, text="Symptom Checker", font=("Arial", 16)).pack(pady=20)
    # label and entry for symptom, count
    tk.Label(symptom_frame, text="How many symptoms would you like to enter? (1-5)", font=("Arial", 12)).pack(pady=20)

    #recreate symptom count entry widget
    symptom_count_val.set("") #reset the stringVar for the entry
    symptom_count_entry = tk.Entry(symptom_frame, textvariable=symptom_count_val, width=10)
    symptom_count_entry.pack(pady=10)

    #add gen symptom boxes button again
    generate_boxes_button = tk.Button(symptom_frame, text="Enter Symptoms", command=symptom_boxes)
    generate_boxes_button.pack(pady=10)

    # Back to Homepage Button
    back_button = tk.Button(symptom_frame,
                            text="Back to Homepage",
                            command=show_homepage)
    back_button.pack(pady=10)
    #reset global variables
    symptom_texts = []
    submit_button = None
    reset_button = None
    # Reapply theme to the symptom_frame and its children
    apply_theme(symptom_frame, bg="#26242f" if not switch_value else "white",
                    fg="white" if not switch_value else "black")
#button to generate symptom boxes
generate_boxes_button = tk.Button(symptom_frame, text = "Enter Symptoms", command = symptom_boxes)
generate_boxes_button.pack(pady=10)

# Back to Homepage Button
back_button = tk.Button(symptom_frame,
                        text="Back to Homepage",
                        command=show_homepage)
back_button.pack(pady=10)


################################################################################
#Condition Search Page
condition_search_frame = tk.Frame(root)
tk.Label(condition_search_frame, text="Search for a Medical Condition", font=("Arial", 16)).pack(pady=20)
condition_entry = tk.Entry(condition_search_frame, width=40)
condition_entry.pack(pady=10)

def search_condition():
    # global variables for search condition
    global suggestion_label, no_match_label, condition_label

    # Clear any previous result labels
    for widget in condition_search_frame.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("text") not in ["Search for a Medical Condition"]:
            widget.destroy()

    search_term = condition_entry.get().strip().lower()

    #reset globals
    suggestion_label = None
    no_match_label = None
    condition_label = None

    # Try to find an exact or suggested match
    if search_term in condition_graph.graph['conditions']:
        # Exact match found
        matched_condition = search_term
        symptoms = condition_graph.graph['conditions'][matched_condition]

        # Create labels for condition and symptoms
        condition_label = tk.Label(condition_search_frame,
                                   text=f"Condition Found: {matched_condition.capitalize()}", fg = "green",
                                   font=("Arial", 12, "bold"),
                                   wraplength=400)
        condition_label.pack(pady=10)

        symptoms_label = tk.Label(condition_search_frame,
                                  text=f"Symptoms: {', '.join(symptoms)}",
                                  wraplength=400,
                                  justify=tk.LEFT)
        symptoms_label.pack(pady=5)

    else:
        # Try to find a suggestion
        suggested_condition = condition_graph.suggest_correction(search_term,
                                                                 list(condition_graph.graph['conditions'].keys()))

        if suggested_condition:
            # Suggestion found
            symptoms = condition_graph.graph['conditions'][suggested_condition]

            # Create labels for suggested condition and symptoms
            suggestion_label = tk.Label(condition_search_frame,
                                        text=f"Did you mean: {suggested_condition.capitalize()}?",
                                        fg="blue",
                                        font=("Arial", 12, "bold"),
                                        wraplength=400)
            suggestion_label.pack(pady=10)

            symptoms_label = tk.Label(condition_search_frame,
                                      text=f"Symptoms for {suggested_condition.capitalize()}:\n{', '.join(symptoms)}",
                                      wraplength=400,
                                      justify=tk.LEFT)
            symptoms_label.pack(pady=5)

        else:
            # No match found
            no_match_label = tk.Label(condition_search_frame,
                                      text=f"No condition found for '{search_term}'.",
                                      fg="red",
                                      wraplength=400)
            no_match_label.pack(pady=10)

    # Reapply theme to the symptom_frame and its children
    apply_theme(condition_search_frame, bg="#26242f" if not switch_value else "white",
                    fg="white" if not switch_value else "black")

tk.Button(condition_search_frame, text="Search", command=search_condition).pack(pady=10)
tk.Button(condition_search_frame, text="Back to Homepage", command=show_homepage).pack()
################################################################################
#Pain Assessment Page
pain_assessment_frame = tk.Frame(root)
tk.Label(pain_assessment_frame, text="Pain Level Assessment", font=("Arial", 16)).pack(pady=20)

# Pain Level Description Label
pain_description_label = tk.Label(pain_assessment_frame,
                                  text="Rate your pain on a scale of 1-10\n"
                                       "1-3: Mild Discomfort\n"
                                       "4-7: Significant Pain\n"
                                       "8-10: Severe Pain",
                                  justify=tk.LEFT,
                                  wraplength=400)
pain_description_label.pack(pady=10)

# Pain Level Entry
tk.Label(pain_assessment_frame, text="Enter your current pain level (1-10):").pack()
pain_entry = tk.Entry(pain_assessment_frame, width=10)
pain_entry.pack(pady=10)

def show_pain_alert():
    try:
        pain_level = int(pain_entry.get())
        message, severity = alert_system(pain_level)

        # Clear previous alert labels
        for widget in pain_assessment_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget not in [
                pain_description_label,
                pain_assessment_frame.winfo_children()[0]  # Keep the title label
            ]:
                widget.destroy()

        # Create a new label for the alert
        if severity == "low":
            alert_label = tk.Label(pain_assessment_frame,
                                   text=message,
                                   fg="green",
                                   wraplength=400,
                                   justify=tk.LEFT)
        elif severity == "moderate":
            alert_label = tk.Label(pain_assessment_frame,
                                   text=message,
                                   fg="orange",
                                   wraplength=400,
                                   justify=tk.LEFT)
        else:  # severe
            alert_label = tk.Label(pain_assessment_frame,
                                   text=message,
                                   fg="red",
                                   wraplength=400,
                                   justify=tk.LEFT)

        alert_label.pack(pady=10)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number between 1 and 10")

def alert_system(pain_level):
    """
    Generates an alert message based on the user's reported pain level.

    Args:
        pain_level (int): Pain level on a scale of 1-10

    Returns:
        tuple: A tuple containing a message and a severity level
    """
    # Validate input
    if not isinstance(pain_level, int) or pain_level < 1 or pain_level > 10:
        return "Invalid pain level. Please enter a number between 1 and 10.", "error"

    # Pain level categories and corresponding messages
    if 1 <= pain_level <= 3:
        return (
            "Low Pain Level Alert:\n"
            "You appear to be experiencing minimal discomfort. "
            "Monitor your symptoms carefully. "
            "If pain persists or worsens, consult a medical professional.",
            "low"
        )

    elif 4 <= pain_level <= 7:
        return (
            "Moderate Pain Level Alert:\n"
            "You are experiencing significant pain. "
            "We recommend scheduling an appointment with your doctor "
            "or visiting a hospital for a thorough medical evaluation.",
            "moderate"
        )

    else:  # 8-10 pain level
        return (
            "SEVERE PAIN ALERT:\n"
            "YOU ARE EXPERIENCING EXTREMELY HIGH PAIN LEVELS. "
            "IMMEDIATE MEDICAL ATTENTION IS CRITICAL. "
            "CALL EMERGENCY SERVICES (911) OR GO TO THE NEAREST EMERGENCY ROOM IMMEDIATELY.",
            "severe"
        )

most_dangerous_symptoms = [
    "Coughing Blood",
    "Chest Pain",
    "Slurred Speech",
    "Paralysis",
    "Unexplained Weight Loss",
    "Severe Shortness of Breath",
    "Stiff Neck with Fever",
    "Irregular Heartbeat",
    "Persistent High Fever"
]

def check_dangerous_symptoms(symptoms, dangerous_symptoms):
    """
    Check if any of the user's symptoms are in the list of dangerous symptoms.

    Args:
        symptoms (list): List of symptoms entered by the user
        dangerous_symptoms (list): List of medically critical symptoms

    Returns:
        list: List of detected dangerous symptoms
    """
    # Normalize symptoms for comparison
    symptoms_lower = [str(symptom).lower().strip() for symptom in symptoms]
    dangerous_symptoms_lower = [str(symptom).lower().strip() for symptom in dangerous_symptoms]

    # Find intersection of symptoms
    detected_dangerous_symptoms = [
        symptom for symptom in symptoms_lower
        if any(symptom == dangerous_symptom in symptom for dangerous_symptom in dangerous_symptoms_lower)
    ]

    return detected_dangerous_symptoms

def show_dangerous_symptoms_alert(dangerous_symptoms):
    """
    Create a popup window for dangerous symptoms alert.

    Args:
        dangerous_symptoms (list): List of detected dangerous symptoms
    """
    # Create a top-level window for the alert
    alert_window = tk.Toplevel(root)
    alert_window.title("CRITICAL MEDICAL ALERT")
    alert_window.geometry("600x600")
    alert_window.configure(bg='red')

    # Create a bold, large font
    alert_font = ("Arial", 14, "bold")

    # Alert title
    tk.Label(alert_window,
             text="MEDICAL EMERGENCY ALERT",
             font=("Arial", 18, "bold"),
             fg='white',
             bg='red').pack(pady=10)

    # Dangerous symptoms message
    symptoms_text = "Dangerous Symptoms Detected:\n" + "\n".join(dangerous_symptoms)
    tk.Label(alert_window,
             text=symptoms_text,
             font=alert_font,
             fg='white',
             bg='red',
             wraplength=350).pack(pady=10)

    # Emergency instructions
    tk.Label(alert_window,
             text="CALL EMERGENCY SERVICES (911) IMMEDIATELY",
             font=("Arial", 16, "bold"),
             fg='yellow',
             bg='red').pack(pady=10)

    # Close button
    tk.Button(alert_window,
              text="Close Alert",
              command=alert_window.destroy,
              bg='white',
              fg='red').pack(pady=10)


def integrate_dangerous_symptoms_check(symptoms):
    """
    Integrate dangerous symptoms check into symptom submission process.

    Args:
        symptoms (list): List of symptoms entered by the user
    """

    # Debug: print input symptoms
    print("Checking symptoms:", symptoms)

    # Check for dangerous symptoms
    dangerous_symptoms = check_dangerous_symptoms(symptoms, most_dangerous_symptoms)

    # Debug: print detected dangerous symptoms
    print("Detected dangerous symptoms:", dangerous_symptoms)

    # If dangerous symptoms are found, show alert
    if dangerous_symptoms:
        show_dangerous_symptoms_alert(dangerous_symptoms)

        # Trigger pain assessment page
        show_pain_assessment_page()

# Check Pain Level Button
check_pain_button = tk.Button(pain_assessment_frame,
                              text="Check Pain Level",
                              command=show_pain_alert)
check_pain_button.pack(pady=10)

# Back to Homepage Button
back_to_homepage_button = tk.Button(pain_assessment_frame,
                                    text="Back to Homepage",
                                    command=show_homepage)
back_to_homepage_button.pack(pady=10)

#register all the frames (FOR LIGHT MODE AND DARK MODE!!)
windows[root] = [profile_frame, homepage_frame, condition_search_frame, symptom_frame, pain_assessment_frame]
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

#Show Homepage by default
show_homepage()

#Start tkinter main loop
root.mainloop()