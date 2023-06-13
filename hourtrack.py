import tkinter as tk
import time
import pickle

class TaskTracker:
    def __init__(self):
        self.tasks = {}
        self.active_tasks = {}
        self.start_times = {}
        self.load_data()

        self.root = tk.Tk()
        self.root.title("Task Tracker")
        self.root.geometry("400x300")  # Set the window size (width x height)

        self.buttons_frame = tk.Frame(self.root) 
        self.buttons_frame.pack()

        self.task_entry = tk.Entry(self.buttons_frame)
        self.task_entry.pack()

        self.add_button = tk.Button(self.buttons_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.buttons_frame, text="Save Data", command=self.save_data)
        self.save_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self.buttons_frame, text="Load Data", command=self.load_data)
        self.load_button.pack(side=tk.LEFT)

        self.task_labels = {}
        self.delete_buttons = {}
        self.update_gui()
        self.root.mainloop()

    def add_task(self):
        task_name = self.task_entry.get()
        if task_name not in self.tasks:
            self.tasks[task_name] = 0
            self.start_times[task_name] = time.time()
            self.active_tasks[task_name] = False
            self.create_task_button(task_name)
            self.task_entry.delete(0, tk.END)

    def create_task_button(self, task_name):
        def toggle_task(task):
            self.active_tasks[task] = not self.active_tasks[task]
            if self.active_tasks[task]:
                self.start_times[task] = time.time()
            else:
                elapsed_time = time.time() - self.start_times[task]
                self.tasks[task] += elapsed_time
            self.update_gui()

        def delete_task(task):
            del self.tasks[task]
            del self.start_times[task]
            del self.active_tasks[task]
            self.update_gui()

        task_frame = tk.Frame(self.root)
        task_frame.pack()

        task_label = tk.Label(task_frame, text=task_name)
        task_label.pack(side=tk.LEFT)
        self.task_labels[task_name] = task_label

        task_button = tk.Button(task_frame, text="Start", command=lambda: toggle_task(task_name))
        task_button.pack(side=tk.LEFT)

        delete_button = tk.Button(task_frame, text="Delete", command=lambda: delete_task(task_name))
        delete_button.pack(side=tk.LEFT)
        self.delete_buttons[task_name] = delete_button

    def update_gui(self):
        for widget in self.root.winfo_children():
            if widget not in [self.buttons_frame, self.task_entry, self.add_button, self.save_button, self.load_button]:
                widget.pack_forget()

        for task_name in self.tasks:
            task_frame = tk.Frame(self.root)
            task_frame.pack()

            task_label = tk.Label(task_frame, text=task_name)
            task_label.pack(side=tk.LEFT)
            self.task_labels[task_name] = task_label

            task_button = tk.Button(task_frame, text="Start", command=lambda name=task_name: self.toggle_task(name))
            task_button.pack(side=tk.LEFT)

            delete_button = tk.Button(task_frame, text="Delete", command=lambda name=task_name: self.delete_task(name))
            delete_button.pack(side=tk.LEFT)
            self.delete_buttons[task_name] = delete_button

            if self.active_tasks[task_name]:
                task_button.config(relief=tk.SUNKEN, text="Stop", bg='salmon')
            else:
                task_button.config(relief=tk.RAISED, text="Start", bg='pale green')

        self.update_counters()

    def update_counters(self):
        for task_name, task_label in self.task_labels.items():
            if task_name in self.active_tasks:
                if self.active_tasks[task_name]:
                    elapsed_time = time.time() - self.start_times[task_name] + self.tasks[task_name]
                    hours = int(elapsed_time // 3600)
                    minutes = int((elapsed_time % 3600) // 60)
                    seconds = int(elapsed_time % 60)
                    counter_text = f"{task_name} {hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    elapsed_time = self.tasks[task_name]
                    hours = int(elapsed_time // 3600)
                    minutes = int((elapsed_time % 3600) // 60)
                    seconds = int(elapsed_time % 60)
                    counter_text = f"{task_name} Total: {hours:02d}:{minutes:02d}:{seconds:02d}"

            task_label.config(text=counter_text)

        self.root.after(1000, self.update_counters)

    def save_data(self):
        data = (self.tasks, self.start_times, self.active_tasks)
        with open("task_data.pickle", "wb") as file:
            pickle.dump(data, file)

    def load_data(self):
        try:
            with open("task_data.pickle", "rb") as file:
                data = pickle.load(file)
                self.tasks, self.start_times, self.active_tasks = data
        except FileNotFoundError:
            pass

    def toggle_task(self, task_name):
        self.active_tasks[task_name] = not self.active_tasks[task_name]
        if self.active_tasks[task_name]:
            self.start_times[task_name] = time.time()
        else:
            elapsed_time = time.time() - self.start_times[task_name]
            self.tasks[task_name] += elapsed_time
        self.update_gui()

    def delete_task(self, task_name):
        del self.tasks[task_name]
        del self.start_times[task_name]
        del self.active_tasks[task_name]
        del self.task_labels[task_name]
        self.update_gui()

if __name__ == "__main__":
    TaskTracker()