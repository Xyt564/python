import socket
import threading
import customtkinter as ctk
from tkinter import messagebox

# ---------------- Port Scanning Logic ---------------- #

def scan_port(host, port, text_widget, progress_bar, total_ports, progress_var):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            text_widget.insert("end", f"[+] Port {port} is OPEN\n")
            text_widget.see("end")
        sock.close()
    except Exception as e:
        pass
    finally:
        # update progress
        progress_var[0] += 1
        progress_bar.set(progress_var[0] / total_ports)


def start_scan(host, start_port, end_port, text_widget, progress_bar):
    text_widget.delete("1.0", "end")  # clear old results

    try:
        start_port, end_port = int(start_port), int(end_port)
    except ValueError:
        messagebox.showerror("Error", "Ports must be numbers!")
        return

    if start_port < 0 or end_port > 65535 or start_port > end_port:
        messagebox.showerror("Error", "Invalid port range!")
        return

    text_widget.insert("end", f"Scanning {host} from port {start_port} to {end_port}...\n\n")

    total_ports = end_port - start_port + 1
    progress_var = [0]  # mutable integer so threads can update

    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(
            target=scan_port,
            args=(host, port, text_widget, progress_bar, total_ports, progress_var)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish in background
    def wait_for_completion():
        for t in threads:
            t.join()
        text_widget.insert("end", "\n--- Scan Complete ---\n")
        text_widget.see("end")

    threading.Thread(target=wait_for_completion, daemon=True).start()


# ---------------- GUI Setup ---------------- #

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Python Port Scanner")
    app.geometry("600x500")

    # Host input
    host_label = ctk.CTkLabel(app, text="Target Host:")
    host_label.pack(pady=5)
    host_entry = ctk.CTkEntry(app, width=300)
    host_entry.insert(0, "scanme.nmap.org")  # default target
    host_entry.pack(pady=5)

    # Port range input
    port_frame = ctk.CTkFrame(app)
    port_frame.pack(pady=10)

    start_port_label = ctk.CTkLabel(port_frame, text="Start Port:")
    start_port_label.grid(row=0, column=0, padx=5)
    start_port_entry = ctk.CTkEntry(port_frame, width=100)
    start_port_entry.insert(0, "20")
    start_port_entry.grid(row=0, column=1, padx=5)

    end_port_label = ctk.CTkLabel(port_frame, text="End Port:")
    end_port_label.grid(row=0, column=2, padx=5)
    end_port_entry = ctk.CTkEntry(port_frame, width=100)
    end_port_entry.insert(0, "1000")
    end_port_entry.grid(row=0, column=3, padx=5)

    # Results box (scrollable)
    result_box = ctk.CTkTextbox(app, width=500, height=250)
    result_box.pack(pady=10)

    # Progress bar
    progress_bar = ctk.CTkProgressBar(app, width=400)
    progress_bar.set(0)
    progress_bar.pack(pady=10)

    # Scan button
    scan_button = ctk.CTkButton(
        app, text="Start Scan",
        command=lambda: start_scan(
            host_entry.get(),
            start_port_entry.get(),
            end_port_entry.get(),
            result_box,
            progress_bar
        )
    )
    scan_button.pack(pady=10)

    app.mainloop()


if __name__ == "__main__":
    main()
