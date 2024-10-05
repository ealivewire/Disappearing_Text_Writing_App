# PROFESSIONAL PROJECT: Disappearing Text Writing App.

# OBJECTIVE:
# For most writers, a big problem is writing block. That refers to where you can't
# think of what to write and you can't write anything.
# The goal of this application is to help reduce writer's block.
# If user stops typing, after a pre-determined number of seconds the contents of the typing area
# will be cleared.  This should help discourage too much idle time between typing.

# Import necessary library(ies):
from datetime import datetime, timedelta
from time import time
from tkinter import *
from tkinter import messagebox, scrolledtext, END, WORD
import traceback

# Define constants for application default font size as well as window's height and width:
FONT_NAME = "Arial"
WINDOW_HEIGHT = 725
WINDOW_WIDTH = 800

# Define constant for maximum idle time allowed during typing time:
MAX_IDLE_TIME_IN_SECONDS = 5

# Define variable for the GUI (application) window (so that it can be used globally), and make it a Tkinter instance:
window = Tk()

# Define variable for designating application for termination
# (part of mechanism to break typing-test 'while' loop without
# generating additional errors):
application_exited = False

# Define variable for image to be displayed at top of application window:
img = None

# Define variable to track if a test is in progress:
test_in_progress = False

# Define variable for tracking the time in which the last typing was detected:
time_of_last_typing = time()

# Define variable for widgets that must be referenced across functions:
txt_typing_area = scrolledtext.ScrolledText()


# DEFINE FUNCTIONS TO BE USED FOR THIS APPLICATION (LISTED IN ALPHABETICAL ORDER BY FUNCTION NAME):
def handle_window_on_closing():
    """Function which confirms with user if s/he wishes to exit this application"""
    global time_of_last_typing, application_exited

    # Confirm with user if s/he wishes to exit this application:
    if messagebox.askokcancel("Exit?", "Do you want to exit this application?"):
        # Designate application for termination:
        application_exited = True

        # Destroy the application window:
        window.destroy()

        # Exit this application:
        exit()

    else:
        # Capture the current time as the time that typing was last detected (i.e., "timer"
        # restarts upon user confirming that s/he wishes to continue using this application):
        time_of_last_typing = time()


def reset_last_time_typing_detected(event):
    """Function which resets the timer variable which stores the last time that typing has been detected"""
    # NOTE:  Error handling will be deferred to the lone function (window_create_and_config_user_interface)
    #        that references this function via binding to one of the user interface constructs.
    global time_of_last_typing

    # Capture the current time.  This restarts the "timer" which tracks the last time that typing was detected:
    time_of_last_typing = time()


def reset_test_to_beginning():
    """Function which clears the entry widget of its contents and performs supporting functionality"""
    global txt_typing_area, time_of_last_typing

    try:
        # Clear the entry widget of its contents, preparing for subsequent typing by the user:
        txt_typing_area.delete('1.0', END)
        txt_typing_area.insert('1.0', "")

        # Set focus on the entry widget:
        txt_typing_area.focus()

        # Capture the current time.  This restarts the "timer" which tracks the last time that typing was detected:
        time_of_last_typing = time()

        # Update the application window to reflect the updates executed above:
        window.update()

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (reset_test_to_beginning): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("reset_test_to_beginning", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def run_app():
    """Main function used to run this application"""
    global test_in_progress, time_of_last_typing, application_exited

    try:
        # Creates and configure all visible aspects of the application window.  If an error occurs,
        # exit this application:
        if not window_config():
            exit()

        # Indicate that a new test is now in progress (used in the 'while' loop below):
        test_in_progress = True

        # Reset test to beginning-of-test state, preparing for subsequent typing by the user.
        # If an error occurs, exit this application:
        if not reset_test_to_beginning():
            exit()

        # Run the following while loop until user exits the application (by closing the app. window):
        while test_in_progress:
            # If application has been designated for termination, exit this application
            # (mechanism to break this loop without generating additional errors):
            if application_exited:
                exit()

            # Capture the current time:
            time_now = time()

            # Update the application window to reflect changes within the typing area:
            window.update()

            # If the time elapsed between the last typing detection and the current time is greater than/equal to
            # the max seconds of idle time allowed, clear the typing area of all of its contents.  If an error
            # occurs, exit this application:
            if time_now >= time_of_last_typing + MAX_IDLE_TIME_IN_SECONDS:
                if not reset_test_to_beginning():
                    test_in_progress = False
                    exit()

    except SystemExit:  # Exiting application.
        exit()

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (run_app): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("run_app", traceback.format_exc())

        # If window object exists, destroy it:
        try:
            window.destroy()
        except:
            pass

        # Exit this application:
        exit()


def update_system_log(activity, log):
    """Function to update the system log with errors encountered"""
    try:
        # Capture current date/time:
        current_date_time = datetime.now()
        current_date_time_file = current_date_time.strftime("%Y-%m-%d")

        # Update log file.  If log file does not exist, create it:
        with open("log_disapp_txt_wrtg_app_" + current_date_time_file + ".txt", "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d @ %I:%M %p") + ":\n")
            f.write(activity + ": " + log + "\n")

        # Close the log file:
        f.close()

    except:  # An error has occurred.
        messagebox.showinfo("Error", f"Error: System log could not be updated.\n{traceback.format_exc()}")


def window_center_screen():
    """Function which centers the application window on the computer screen"""
    try:
        # Capture the desired width and height for the window:
        w = WINDOW_WIDTH # width of tkinter window
        h = WINDOW_HEIGHT  # height of tkinter window

        # Capture the computer screen's width and height:
        screen_width = window.winfo_screenwidth()  # Width of the screen
        screen_height = window.winfo_screenheight()  # Height of the screen

        # Calculate starting X and Y coordinates for the application window:
        x = (screen_width / 2) - (w / 2)
        y = (screen_height / 2) - (h / 2)

        # Center the application window based on the aforementioned constructs:
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (window_center_screen): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("window_center_screen", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def window_config():
    """Function which creates and configures all visible aspects of the application window"""
    try:
        # Create and configure application window.  If an error occurs, return
        # failed-execution indication to the calling function:
        if not window_create_and_config():
            return False

        # Create and configure user interface.  If an error occurs, return failed-execution
        # indication to the calling function:
        if not window_create_and_config_user_interface():
            return False

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (window_config): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("window_config", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def window_create_and_config():
    """Function to create and configure the GUI (application) window"""
    global img

    try:
        # Create and configure the application window:
        window.title("My Disappearing Text Writing App.")
        window.minsize(width=800, height=725)
        window.config(padx=45, pady=0,bg='skyblue')
        window.resizable(0, 0)  # Prevents window from being resized.
        window.attributes("-toolwindow", 1)  # Removes the minimize and maximize buttons from the application window.

        # Center the application window on the computer screen.  If an error occurs, return failed-execution
        # indication to the calling function:
        if not window_center_screen():
            return False

        # Prepare the application to handle the event of user attempting to close the application window:
        window.protocol("WM_DELETE_WINDOW", handle_window_on_closing)

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (window_create_and_config): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("window_create_and_config", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def window_create_and_config_user_interface():
    """Function which creates and configures items comprising the user interface, including the canvas (which overlays on top of the app. window), labels, and textbox for the typing area"""
    global txt_typing_area, img

    try:
        # Create and configure canvas which overlays on top of window:
        canvas = Canvas(window)
        img = PhotoImage(file="keyboard.png")
        canvas.config(height=img.height(), width=WINDOW_WIDTH, bg='skyblue', highlightthickness=0)
        canvas.create_image(345,54, image=img)
        canvas.grid(column=1, row=2, columnspan=6, padx=0, pady=10)
        canvas.update()

        # Create and configure the introductory header text (labels):
        label_intro = Label(text=f"WELCOME TO MY DISAPPEARING TEXT WRITING APPLICATION!", height=3, bg='skyblue', fg='black', padx=0, pady=0, font=(FONT_NAME,16, "bold"))
        label_intro.grid(column=1, row=0, columnspan=5)

        label_problem_at_hand = Label(text=f"For most writers, a big problem is writing block. That refers to\nwhere you can't think of what to write and you can't write anything.\n\nThe goal of this application is to help reduce writer's block.\n\nIf you stop typing, after {MAX_IDLE_TIME_IN_SECONDS} seconds the contents of the typing area below will be cleared.", height=6, bg='skyblue', fg='black', padx=0, pady=0, font=(FONT_NAME,12, "bold"))
        label_problem_at_hand.grid(column=1, row=1, columnspan=5)

        # Create and configure the header text (label) immediately above the typing area:
        label_typing_area = Label(text="Please type your contents below.", height=2, bg='skyblue', fg='navy', padx=0, pady=0, font=(FONT_NAME,16, "bold"))
        label_typing_area.grid(column=0, row=3, columnspan=6)

        # Create and configure the scrolled text widget which will house the typing area:
        txt_typing_area = scrolledtext.ScrolledText(window, wrap = WORD, width = 62, height = 15, font=(FONT_NAME,14,"normal"))
        txt_typing_area.grid(column=0, row=4, columnspan=6, pady=0)

        # Bind any key-press event in the typing area to the function which will reset the timer variable which
        # stores the last time that typing has been detected:
        txt_typing_area.bind("<KeyPress>", reset_last_time_typing_detected)

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (window_create_and_config_user_interface): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("window_create_and_config_user_interface", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


# Run this application:
run_app()

# Keep application window open until user closes it:
window.mainloop()

if __name__ == '__main__':
    run_app()
