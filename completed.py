import pandas as rd
import pickle
from sklearn.metrics import accuracy_score
import customtkinter as ctk
from PIL import Image
import threading
from tkinter import messagebox

# Configuration for CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class DiabetesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Diabetes Prediction System")
        self.geometry("900x700")
        
        # Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (Left)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MediPredict", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Prediction", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                               command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # Main Content Area (Right)
        self.main_scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Patient Data Input")
        self.main_scrollable_frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=20, pady=20)
        self.main_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.main_scrollable_frame.grid_columnconfigure(1, weight=1)

        # Model Loading
        self.model = None
        self.load_and_train_model()

        # Input Fields with typical ranges (Pima Indians Diabetes Dataset constraints)
        self.fields = [
            ("Pregnancies", "Preg", "0 - 20"),
            ("Glucose", "Gluco", "50 - 200 mg/dL"),
            ("Blood Pressure", "BP", "40 - 140 mm Hg"),
            ("Skin Thickness", "skinTH", "5 - 100 mm"),
            ("Insulin", "Insulin", "0 - 900 mu U/ml"),
            ("BMI", "BMI", "10 - 60"),
            ("Diabetes Pedigree", "Pedigreefunc", "0.0 - 2.5"),
            ("Age", "Age", "21 - 100")
        ]
        self.entries = {}

        for i, (label_text, key, range_hint) in enumerate(self.fields):
            # Label with range hint
            full_label = f"{label_text} ({range_hint})"
            label = ctk.CTkLabel(self.main_scrollable_frame, text=full_label, anchor="w", text_color=("gray60", "gray40"))
            label.grid(row=i, column=0, padx=20, pady=(10, 0), sticky="w")
            
            entry = ctk.CTkEntry(self.main_scrollable_frame, placeholder_text=f"e.g., {range_hint.split()[0]}")
            entry.grid(row=i, column=1, padx=20, pady=(10, 0), sticky="ew")
            self.entries[key] = entry

        # Buttons
        self.predict_button = ctk.CTkButton(self.main_scrollable_frame, text="Generate Prediction", command=self.predict_event, height=40)
        self.predict_button.grid(row=len(self.fields), column=0, padx=(20, 10), pady=30, sticky="ew")

        self.reset_button = ctk.CTkButton(self.main_scrollable_frame, text="Reset Fields", command=self.reset_event, height=40, fg_color="gray", hover_color="#555555")
        self.reset_button.grid(row=len(self.fields), column=1, padx=(10, 20), pady=30, sticky="ew")

        # Result Area
        self.result_frame = ctk.CTkFrame(self.main_scrollable_frame, fg_color="transparent")
        self.result_frame.grid(row=len(self.fields)+1, column=0, columnspan=2, sticky="ew")
        
        self.result_label = ctk.CTkLabel(self.result_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_label.pack(pady=10)

        self.advice_button = ctk.CTkButton(self.result_frame, text="View Recommendations", command=self.show_advice, state="disabled")
        self.advice_button.pack(pady=10)
        
        self.prediction_result = None # Store result for advice

    def load_and_train_model(self):
        try:
            df = rd.read_csv("diabetes2.csv")
            X = df.drop('Outcome', axis=1)
            y = df[['Outcome']]
            
            # Save feature names
            self.feature_names = X.columns.tolist()
            print(f"Model trained on features: {self.feature_names}")
            
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LogisticRegression
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
            lr = LogisticRegression(max_iter=1000)
            self.model = lr.fit(X_train, y_train.values.ravel())
            
            y_pred = lr.predict(X_test)
            acc = accuracy_score(y_pred, y_test)
            print(f"Model trained. Accuracy: {acc}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load/train model: {e}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def sidebar_button_event(self):
        print("Sidebar button click")

    def reset_event(self):
        for _, key, _ in self.fields:
            self.entries[key].delete(0, 'end')
        self.result_label.configure(text="")
        self.advice_button.configure(state="disabled", text="View Recommendations", fg_color=["#3B8ED0", "#1F6AA5"])
        self.prediction_result = None

    def predict_event(self):
        if not self.model:
            messagebox.showerror("Error", "Model not loaded.")
            return

        import pandas as pd
        data = {}
        try:
            # Collect data using internal keys
            temp_data = {}
            for _, key, _ in self.fields:
                val = self.entries[key].get()
                if not val.strip():
                     messagebox.showwarning("Missing Input", f"Please enter a value for {key}")
                     return
                temp_data[key] = float(val)
            
            # Map temp_data (keys) to model feature_names (CSV columns)
            # Assumption: The order of self.fields matches the order of self.feature_names?
            # self.fields order: Pregnancies, Glucose, BP, Skin, Insulin, BMI, Pedigree, Age
            # diabetes2.csv standard order: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
            
            # Let's rely on index since we can't be 100% sure of CSV header names vs our keys without mapping logic
            # Be safer: Check length match and construct list
            
            if len(self.feature_names) != len(self.fields):
                raise ValueError("Feature count mismatch between model and UI.")

            # Create dataframe with correct column names from model
            final_data = {}
            for i, feature_name in enumerate(self.feature_names):
                # We assume the UI fields are defined in the same order as CSV columns. 
                # This is standard for this dataset.
                ui_key = self.fields[i][1] # Get key from fields list at index i
                final_data[feature_name] = [temp_data[ui_key]]
            
            # DataFrame for prediction
            input_df = pd.DataFrame(final_data)
            
            output = self.model.predict(input_df)[0]
            self.prediction_result = output
            
            if output == 1:
                self.result_label.configure(text="Result: High Risk of Diabetes", text_color="#e74c3c") # Red
                self.advice_button.configure(text="View Diet Plan", state="normal", fg_color="#e74c3c", hover_color="#c0392b")
            else:
                self.result_label.configure(text="Result: Low Risk of Diabetes", text_color="#2ecc71") # Green
                self.advice_button.configure(text="View Health Tips", state="normal", fg_color="#2ecc71", hover_color="#27ae60")
                
        except ValueError as ve:
            print(f"Validation Error: {ve}")
            messagebox.showerror("Invalid Input", f"Please ensure all fields contain valid numbers.\nDetails: {ve}")
        except Exception as e:
            print(f"Prediction Error: {e}")
            messagebox.showerror("Error", f"An error occurred during prediction:\n{e}")

    def show_advice(self):
        if self.prediction_result is None:
            return
            
        # Check if window already exists and is open
        if hasattr(self, 'advice_window') and self.advice_window is not None and self.advice_window.winfo_exists():
            self.advice_window.lift()
            self.advice_window.focus()
            return

        self.advice_window = ctk.CTkToplevel(self)
        self.advice_window.geometry("500x400")
        self.advice_window.title("Recommendations")
        
        # Bring to front
        self.advice_window.lift()
        self.advice_window.attributes('-topmost', True)
        self.advice_window.after(100, lambda: self.advice_window.attributes('-topmost', False)) # Use after instead of after_idle for better stability
        
        textbox = ctk.CTkTextbox(self.advice_window, width=460, height=360)
        textbox.pack(padx=20, pady=20)
        
        if self.prediction_result == 1:
            title = "DIET PLAN FOR DIABETIC MANAGEMENT\n\n"
            content = """Nutrient Distribution:
• Carbohydrates (50%): Whole grains, vegetables, fruits, legumes. Avoid refined sugar.
• Proteins (25%): Lean meat, poultry, fish, eggs, tofu, beans.
• Fats (25%): Avocados, nuts, seeds, olive oil.

Recommended Foods:
• Leafy greens (Spinach, Kale)
• Fatty fish (Salmon, Mackerel)
• Berries and citrus fruits
• Whole grains (Quinoa, Brown Rice)
            """
        else:
            title = "HEALTH TIPS FOR PREVENTION\n\n"
            content = """Prevention Strategies:
1. Physical Activity
   - Aim for at least 150 minutes of moderate aerobic activity per week.
   
2. Healthy Eating
   - Focus on fiber-rich foods.
   - Limit sugary drinks and processed snacks.
   
3. Regular Checkups
   - Monitor glucose levels and blood pressure periodically.
   - Maintain a healthy weight.
            """
            
        textbox.insert("0.0", title + content)
        textbox.configure(state="disabled")

if __name__ == "__main__":
    app = DiabetesApp()
    app.mainloop()
