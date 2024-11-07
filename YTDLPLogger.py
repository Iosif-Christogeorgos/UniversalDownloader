import logging


class YTDLPLogger(logging.Logger):
    def __init__(self, update_ui_callback):
        super().__init__("YTDLPLogger")
        self.update_ui_callback = update_ui_callback  # Function to update UI

    def debug(self, msg):
        if "Merging formats into" in msg:
            self.update_ui_callback("Merging formats...")
        elif "Deleting original file" in msg:
            self.update_ui_callback("Cleaning up temporary files...")
        # Add any other relevant messages you want to capture here

    def warning(self, msg):
        self.update_ui_callback(f"Warning: {msg}")

    def error(self, msg):
        self.update_ui_callback(f"Error: {msg}")
