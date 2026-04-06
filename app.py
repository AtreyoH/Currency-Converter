#Python Project Currency Converter

import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk
import re


class RealTimeCurrencyConverter():
    def __init__(self,url):
            self.data = requests.get(url).json()
            self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        if from_currency not in self.currencies:
            raise ValueError("Invalid from_currency")

        elif to_currency not in self.currencies:
            raise ValueError("Invalid to_currency")

        initial_amount = amount 
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
  
        # limiting the precision to 6 decimal places 
        amount = round(amount * self.currencies[to_currency], 6) 
        return amount

class App(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title('Currency Converter')
        self.currency_converter = converter

        self.bg_color = "#0B2A6F"
        self.bg_top_color = "#1D4ED8"
        self.bg_mid_color = "#1E40AF"
        self.bg_bottom_color = "#0F2C7A"
        self.card_color = "#EFF6FF"
        self.button_color = "#2563EB"
        self.button_hover_color = "#1E40AF"
        self.text_dark = "#0F172A"
        self.configure(background=self.bg_color)
        self.geometry("700x440")
        self.resizable(False, False)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure(
            "Blue.TCombobox",
            fieldbackground="#FFFFFF",
            background="#FFFFFF",
            foreground=self.text_dark,
            bordercolor="#BFDBFE",
            arrowsize=16
        )

        # Decorative full-window background.
        self.header_canvas = tk.Canvas(
            self,
            width=700,
            height=440,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.header_canvas.place(x=0, y=0)
        self.header_canvas.create_rectangle(0, 0, 700, 145, fill=self.bg_top_color, outline="")
        self.header_canvas.create_rectangle(0, 145, 700, 290, fill=self.bg_mid_color, outline="")
        self.header_canvas.create_rectangle(0, 290, 700, 440, fill=self.bg_bottom_color, outline="")

        # Soft glowing circles for depth.
        self.header_canvas.create_oval(-90, -70, 220, 220, fill="#3B82F6", outline="")
        self.header_canvas.create_oval(490, -120, 820, 230, fill="#60A5FA", outline="")
        self.header_canvas.create_oval(540, 270, 760, 470, fill="#1D4ED8", outline="")
        self.header_canvas.create_oval(-80, 300, 180, 520, fill="#1E3A8A", outline="")
        self.header_canvas.create_text(
            350,
            58,
            text="Real Time Currency Converter",
            fill="white",
            font=("Segoe UI", 24, "bold")
        )
        self.header_canvas.create_text(
            350,
            98,
            text="Fast conversion with live exchange rates",
            fill="#DBEAFE",
            font=("Segoe UI", 11, "normal")
        )

        # Main card.
        self.card_frame = tk.Frame(
            self,
            bg=self.card_color,
            relief=tk.FLAT,
            bd=0,
            highlightbackground="#BFDBFE",
            highlightthickness=2
        )
        self.card_frame.place(x=50, y=138, width=600, height=265)

        self.rate_label = Label(
            self.card_frame,
            text=f"1 USD = {self.currency_converter.convert('USD','INR',1)} INR",
            bg=self.card_color,
            fg="#1E3A8A",
            font=("Segoe UI", 11, "bold")
        )
        self.rate_label.place(x=22, y=16)

        self.date_label = Label(
            self.card_frame,
            text=f"Updated: {self.currency_converter.data['date']}",
            bg=self.card_color,
            fg="#334155",
            font=("Segoe UI", 10, "normal")
        )
        self.date_label.place(x=22, y=44)

        self.left_col_x = 26
        self.right_col_x = 406
        self.control_width = 170
        self.control_height = 34

        self.from_label = Label(
            self.card_frame,
            text="From",
            bg=self.card_color,
            fg=self.text_dark,
            font=("Segoe UI", 10, "bold")
        )
        self.from_label.place(x=self.left_col_x, y=85, width=self.control_width)

        self.to_label = Label(
            self.card_frame,
            text="To",
            bg=self.card_color,
            fg=self.text_dark,
            font=("Segoe UI", 10, "bold")
        )
        self.to_label.place(x=self.right_col_x, y=85, width=self.control_width)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(
            self.card_frame,
            bd=3,
            relief=tk.RIDGE,
            justify=tk.CENTER,
            bg="#FFFFFF",
            fg=self.text_dark,
            font=("Segoe UI", 12, "bold"),
            validate='key',
            validatecommand=valid
        )
        self.converted_amount_field_label = Label(
            self.card_frame,
            text='Converted value',
            fg='#64748B',
            bg='#FFFFFF',
            relief=tk.RIDGE,
            justify=tk.CENTER,
            width=17,
            borderwidth=3,
            font=("Segoe UI", 12, "bold")
        )

        # dropdown
        self.from_currency_variable = StringVar(self.card_frame)
        self.from_currency_variable.set("INR") # default value
        self.to_currency_variable = StringVar(self.card_frame)
        self.to_currency_variable.set("USD") # default value

        font = ("Segoe UI", 11, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(
            self.card_frame,
            textvariable=self.from_currency_variable,
            values=list(self.currency_converter.currencies.keys()),
            font=font,
            state='readonly',
            width=12,
            justify=tk.CENTER,
            style="Blue.TCombobox"
        )
        self.to_currency_dropdown = ttk.Combobox(
            self.card_frame,
            textvariable=self.to_currency_variable,
            values=list(self.currency_converter.currencies.keys()),
            font=font,
            state='readonly',
            width=12,
            justify=tk.CENTER,
            style="Blue.TCombobox"
        )

        # placing
        self.from_currency_dropdown.place(
            x=self.left_col_x,
            y=112,
            width=self.control_width,
            height=self.control_height
        )
        self.amount_field.place(
            x=self.left_col_x,
            y=150,
            width=self.control_width,
            height=self.control_height
        )
        self.to_currency_dropdown.place(
            x=self.right_col_x,
            y=112,
            width=self.control_width,
            height=self.control_height
        )
        self.converted_amount_field_label.place(
            x=self.right_col_x,
            y=150,
            width=self.control_width,
            height=self.control_height
        )
        
        # Convert button
        self.convert_button = Button(
            self.card_frame,
            text="Convert",
            fg="white",
            bg=self.button_color,
            activebackground=self.button_hover_color,
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.perform
        )
        self.convert_button.config(font=('Segoe UI', 11, 'bold'))
        self.convert_button.place(x=248, y=128, width=104, height=42)
        self.convert_button.bind("<Enter>", lambda event: self.convert_button.config(bg=self.button_hover_color))
        self.convert_button.bind("<Leave>", lambda event: self.convert_button.config(bg=self.button_color))

    def perform(self):
        if self.amount_field.get().strip() == "":
            self.converted_amount_field_label.config(text="Enter amount", fg="#DC2626")
            return

        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 6)

        self.converted_amount_field_label.config(text=str(converted_amount), fg=self.text_dark)
    
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)

    App(converter)
    mainloop()
