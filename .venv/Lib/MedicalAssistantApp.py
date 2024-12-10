import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import difflib
import sys

#global variables for profile info
profile_info = {
    "gender": None,
    "age": None,
    "medical_history": None
}

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

#Navigation functions
def save_profile():
    profile_info["gender"] = gender_var.get()
    profile_info["age"] = age_combobox.get()
    profile_info["medical_history"] = medical_history_text.get("1.0", tk.END).strip()
    messagebox.showinfo("Profile Saved", "Your profile information has been saved.")

def show_profile_page():
    hide_all_frames()
    profile_frame.pack(fill="both", expand=True)

def show_homepage():
    hide_all_frames()
    homepage_frame.pack(fill="both", expand=True)

def show_symptom_page():
    hide_all_frames()
    symptom_frame.pack(fill="both", expand=True)

def show_conditionSearch_page():
    hide_all_frames()
    condition_search_frame.pack(fill="both", expand=True)

def hide_all_frames():
    for frame in [homepage_frame, profile_frame, symptom_frame, condition_search_frame]:
        frame.pack_forget()

#GUI setup
root = tk.Tk()
root.title("Medical Assistant App")
root.geometry("500x400")

#Homepage
homepage_frame = tk.Frame(root)
tk.Label(homepage_frame, text="Welcome to the Medical Assistant App", font=("Arial", 16)).pack(pady=20)
tk.Button(homepage_frame, text="Visit Profile", command=show_profile_page, width=30).pack(pady=10)
tk.Button(homepage_frame, text="Enter My Symptoms", command=show_symptom_page, width=30).pack(pady=10)
tk.Button(homepage_frame, text="Search for Information on a Condition", command=show_conditionSearch_page, width=30).pack(pady=10)
tk.Button(homepage_frame, text="Exit", command=root.quit, width=30).pack(pady=10)
tk.Label(homepage_frame, text="Disclaimer: This is not a verified medical professional.\nIf this is a medical emergency, call 911.", fg="red", wraplength=400, justify="center").pack(pady=20)

#Profile Page
profile_frame = tk.Frame(root)
tk.Label(profile_frame, text="Profile Information", font=("Arial", 16)).pack(pady=20)
gender_var = tk.StringVar()
tk.Label(profile_frame, text="Gender:").pack(anchor="w", padx=20)
tk.Radiobutton(profile_frame, text="Male", variable=gender_var, value="Male").pack(anchor="w", padx=20)
tk.Radiobutton(profile_frame, text="Female", variable=gender_var, value="Female").pack(anchor="w", padx=20)
tk.Radiobutton(profile_frame, text="Other", variable=gender_var, value="Other").pack(anchor="w", padx=20)
tk.Label(profile_frame, text="Age:").pack(anchor="w", padx=20, pady=10)
age_combobox = ttk.Combobox(profile_frame, values=[str(i) for i in range(1, 101)])
age_combobox.pack(anchor="w", padx=40)
tk.Label(profile_frame, text="Medical History:").pack(anchor="w", padx=20, pady=10)
medical_history_text = tk.Text(profile_frame, height=5, width=40)
medical_history_text.pack(padx=40)
tk.Button(profile_frame, text="Save Profile", command=save_profile).pack(pady=10)
tk.Button(profile_frame, text="Back to Homepage", command=show_homepage).pack(pady=10)

# Symptom Page
symptom_frame = tk.Frame(root)
tk.Label(symptom_frame, text="Enter Your Symptoms", font=("Arial", 16)).pack(pady=20)

# Create a frame for symptom input
symptom_input_frame = tk.Frame(symptom_frame)
symptom_input_frame.pack(pady=10)

# Symptom Entry with Scrollbar
symptom_text = tk.Text(symptom_input_frame, height=5, width=40, wrap=tk.WORD)
symptom_text.pack(side=tk.LEFT, padx=5)

# Scrollbar for symptom text
symptom_scrollbar = tk.Scrollbar(symptom_input_frame, command=symptom_text.yview)
symptom_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
symptom_text.config(yscrollcommand=symptom_scrollbar.set)


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


# Submit Symptoms Button
submit_button = tk.Button(symptom_frame, text="Submit Symptoms", command=submit_symptoms)
submit_button.pack(pady=10)

# Back to Homepage Button
back_button = tk.Button(symptom_frame, text="Back to Homepage", command=show_homepage)
back_button.pack()

#Condition Search Page
condition_search_frame = tk.Frame(root)
tk.Label(condition_search_frame, text="Search for a Medical Condition", font=("Arial", 16)).pack(pady=20)
condition_entry = tk.Entry(condition_search_frame, width=40)
condition_entry.pack(pady=10)

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

#Show Homepage by default
show_homepage()

#Start tkinter main loop
root.mainloop()
