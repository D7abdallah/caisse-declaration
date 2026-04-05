import tkinter as tk
from tkinter import messagebox
import datetime
import os

# 🎨 الألوان والتنسيق
BG_COLOR = "#ffffff"
PRIMARY = "#4CAF50"      # أخضر
LIGHT = "#E8F5E9"        # أخضر فاتح
BTN_HOVER = "#45a049"    
FOCUS_COLOR = "#2E7D32"  # أخضر داكن للتركيز
DEVELOPER_COLOR = "#757575" # رمادي خفيف

# متغير عالمي لحفظ الرقم الصافي للنسخ
current_total_raw = 0

def validate_input(value):
    return value.isdigit() or value == ""

def get_value(entry):
    return int(entry.get()) if entry.get().isdigit() else 0

def copy_to_clipboard():
    # ننسخ الرقم الصافي فقط (current_total_raw) ليكون مجرد أرقام
    if current_total_raw != 0 or result_var.get() != "":
        root.clipboard_clear()
        root.clipboard_append(str(current_total_raw))
        messagebox.showinfo("Succès", f"Montant copié : {current_total_raw}")
    else:
        messagebox.showwarning("Attention", "Aucun résultat à copier !")

def export_to_file():
    res = result_var.get()
    if not res:
        messagebox.showwarning("Attention", "Faites le calcul avant l'exportation !")
        return
    
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M")
    filename = f"Rapport_Caisse_{date_str}.txt"
    
    # التقرير بالفرنسية وبدون سطر المبرمج
    content = f"""
    === RAPPORT DE CAISSE ===
    Date: {now.strftime('%d/%m/%Y %H:%M:%S')}
    ----------------------------
    2000 DA: {get_value(e2000)}
    1000 DA: {get_value(e1000)}
    500 DA:  {get_value(e500)}
    200 DA:  {get_value(e200)}
    100 DA:  {get_value(e100)}
    50 DA:   {get_value(e50)}
    ----------------------------
    Nombre de caisses: {get_value(ecaisse)}
    ----------------------------
    TOTAL FINAL: {res}
    ============================
    """
    
    try:
        # استخدام encoding utf-8 لضمان التوافق مع كل نسخ ويندوز
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Exportation", f"Rapport enregistré sous :\n{filename}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'enregistrement : {e}")

def calculate():
    global current_total_raw
    total = (
        get_value(e2000) * 2000 +
        get_value(e1000) * 1000 +
        get_value(e500) * 500 +
        get_value(e200) * 200 +
        get_value(e100) * 100 +
        get_value(e50) * 50
    )
    caisses = get_value(ecaisse)
    final_total = total - (caisses * 4000)
    
    # حفظ الرقم الصافي للنسخ
    current_total_raw = final_total
    
    # عرض المبلغ مع الفواصل للجمالية في البرنامج فقط
    result_var.set(f"{final_total:,} DA")

def reset():
    global current_total_raw
    for e in entries:
        e.delete(0, tk.END)
    result_var.set("")
    current_total_raw = 0
    e2000.focus()

def focus_next(event):
    event.widget.tk_focusNext().focus()
    return "break"

def focus_prev(event):
    event.widget.tk_focusPrev().focus()
    return "break"

def on_focus_in_btn(canvas, bg_color):
    for item in canvas.find_all():
        if canvas.type(item) != "text":
            canvas.itemconfig(item, fill=bg_color, outline=bg_color)

def on_focus_out_btn(canvas, bg_color):
    for item in canvas.find_all():
        if canvas.type(item) != "text":
            canvas.itemconfig(item, fill=bg_color, outline=bg_color)

def rounded_button(parent, text, command, bg, fg, radius=10, width=120):
    height = 40
    canvas = tk.Canvas(parent, width=width, height=height,
                       bg=BG_COLOR, highlightthickness=0, takefocus=1)
    
    canvas.create_arc((0, 0, radius*2, radius*2), start=90, extent=90, fill=bg, outline=bg)
    canvas.create_arc((width-radius*2, 0, width, radius*2), start=0, extent=90, fill=bg, outline=bg)
    canvas.create_arc((0, height-radius*2, radius*2, height), start=180, extent=90, fill=bg, outline=bg)
    canvas.create_arc((width-radius*2, height-radius*2, width, height), start=270, extent=90, fill=bg, outline=bg)
    canvas.create_rectangle(radius, 0, width-radius, height, fill=bg, outline=bg)
    canvas.create_rectangle(0, radius, width, height-radius, fill=bg, outline=bg)
    canvas.create_text(width/2, height/2, text=text, fill=fg, font=("Helvetica", 10, "bold"))

    canvas.bind("<Button-1>", lambda e: command())
    canvas.bind("<Return>", lambda e: command())
    canvas.bind("<FocusIn>", lambda e: on_focus_in_btn(canvas, FOCUS_COLOR))
    canvas.bind("<FocusOut>", lambda e: on_focus_out_btn(canvas, bg))
    return canvas

# إنشاء النافذة
root = tk.Tk()
root.title("Caisse Pro")
root.geometry("380x630")
root.configure(bg=BG_COLOR)

vcmd = (root.register(validate_input), '%P')
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(main_frame, text="CAISSE DÉCLARATION", font=("Helvetica", 16, "bold"),
         bg=BG_COLOR, fg=PRIMARY).pack(pady=10)

def create_input(label_text, is_last=False):
    row = tk.Frame(main_frame, bg=BG_COLOR)
    row.pack(pady=4)
    tk.Label(row, text=label_text, font=("Helvetica", 11), bg=BG_COLOR, width=12, anchor="w").pack(side="left")
    entry = tk.Entry(row, font=("Helvetica", 12), width=10, justify="center", bg=LIGHT, relief="flat", validate="key", validatecommand=vcmd)
    entry.pack(side="right", ipady=3)
    if is_last:
        entry.bind("<Return>", lambda e: btn_calc.focus_set())
        entry.bind("<Down>", lambda e: btn_calc.focus_set())
    else:
        entry.bind("<Return>", focus_next)
        entry.bind("<Down>", focus_next)
    entry.bind("<Up>", focus_prev)
    return entry

# الحقول
e2000 = create_input("2000 DA")
e1000 = create_input("1000 DA")
e500 = create_input("500 DA")
e200 = create_input("200 DA")
e100 = create_input("100 DA")
e50 = create_input("50 DA")
ecaisse = create_input("Nbr caisse", is_last=True)

entries = [e2000, e1000, e500, e200, e100, e50, ecaisse]

# الأزرار الرئيسية
btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
btn_frame.pack(pady=15)

btn_calc = rounded_button(btn_frame, "Calculer", calculate, PRIMARY, "white")
btn_calc.pack(side="left", padx=5)

btn_reset = rounded_button(btn_frame, "Reset", reset, "#cccccc", "black")
btn_reset.pack(side="left", padx=5)

# منطقة النتيجة
result_frame = tk.Frame(main_frame, bg=BG_COLOR)
result_frame.pack(pady=5)

result_var = tk.StringVar()
tk.Label(result_frame, textvariable=result_var, font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg="black").pack()

# أزرار الإجراءات
action_frame = tk.Frame(main_frame, bg=BG_COLOR)
action_frame.pack(pady=10)

btn_copy = rounded_button(action_frame, "Copy Result", copy_to_clipboard, "#2196F3", "white", width=100)
btn_copy.pack(side="left", padx=5)

btn_export = rounded_button(action_frame, "Export Report", export_to_file, "#607D8B", "white", width=100)
btn_export.pack(side="left", padx=5)

# توقيع المبرمج (يظهر في التطبيق فقط)
developer_label = tk.Label(main_frame, text="Dahamna", font=("Helvetica", 9),
                          bg=BG_COLOR, fg=DEVELOPER_COLOR)
developer_label.pack(pady=(20, 5))

root.after(100, lambda: e2000.focus())
root.resizable(False, False)
root.mainloop()