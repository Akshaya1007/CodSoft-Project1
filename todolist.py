import tkinter as tk
from tkinter import messagebox, simpledialog
import os

TASKS_FILE = "tasks.txt"

def create_window():
    window = tk.Tk()
    window.title("To-Do List")
    window.geometry("400x400")
    window.config(bg="lightblue")  # Set the background color of the window
    return window

def add_task():
    task = task_entry.get()
    if task:
        var = tk.BooleanVar()
        task_frame_inner = tk.Frame(task_frame, bg="lightblue")
        chk = tk.Checkbutton(task_frame_inner, text=task, variable=var, bg="lightblue")
        chk.pack(side=tk.LEFT)
        delete_button = tk.Button(task_frame_inner, text="Delete", command=lambda: delete_task(task_frame_inner, task, var), bg="lightblue")
        delete_button.pack(side=tk.RIGHT)
        task_frame_inner.pack(anchor='w', fill=tk.X)
        tasks.append((task, var))
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task(task_frame_inner, task, var):
    task_frame_inner.destroy()
    tasks.remove((task, var))
    save_tasks()

def edit_task():
    for task, var in tasks:
        if var.get():
            new_task = simpledialog.askstring("Edit Task", "Edit the task:", initialvalue=task)
            if new_task:
                var.set(False)
                for widget in task_frame.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for subwidget in widget.winfo_children():
                            if isinstance(subwidget, tk.Checkbutton) and subwidget.cget("text") == task:
                                subwidget.config(text=new_task)
                                break
                tasks[tasks.index((task, var))] = (new_task, var)
            save_tasks()
            break

def save_tasks():
    with open(TASKS_FILE, "w") as file:
        for task, var in tasks:
            file.write(f"{task},{var.get()}\n")

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                task, completed = line.strip().split(",")
                var = tk.BooleanVar(value=completed == "True")
                task_frame_inner = tk.Frame(task_frame, bg="lightblue")
                chk = tk.Checkbutton(task_frame_inner, text=task, variable=var, bg="lightblue")
                chk.pack(side=tk.LEFT)
                delete_button = tk.Button(task_frame_inner, text="Delete", command=lambda: delete_task(task_frame_inner, task, var), bg="lightblue")
                delete_button.pack(side=tk.RIGHT)
                task_frame_inner.pack(anchor='w', fill=tk.X)
                tasks.append((task, var))

def create_widgets(window):
    global task_entry, task_frame, tasks
    
    tasks = []

    task_entry = tk.Entry(window, width=40)
    task_entry.pack(pady=10)
    
    add_task_button = tk.Button(window, text="Add Task", command=add_task)
    add_task_button.pack(pady=5)
    
    edit_task_button = tk.Button(window, text="Edit Task", command=edit_task)
    edit_task_button.pack(pady=5)
    
    task_frame = tk.Frame(window, bg="lightblue")
    task_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    
    load_tasks()

if __name__ == "__main__":
    app_window = create_window()
    create_widgets(app_window)
    app_window.mainloop()
