# chatapp.py
import reflex as rx
import os
import asyncio
import main
import config

html = ""
class State(rx.State):
    img: list[str] = []
    _n_tasks:int = 0
    output = ""
    vidDict = {"key":"value"}
    
    
    async def handle_upload(self, files: list[rx.UploadFile]):
        upload_dir = rx.get_upload_dir()

        for file in files:
            if file.filename.lower().endswith('.mp4'):
                upload_data = await file.read()
                outfile = rx.get_upload_dir() / "new_video.mp4"

                # Save the file.
                with outfile.open("wb") as file_object:
                    file_object.write(upload_data)


                # Update the img var.
                self.img.append(file.filename)
                self.output, self.vidDict = main.main()
                return rx.redirect("output")




class ImageState(rx.State):
    image_src: str = "/YCZH.gif"
    async def update_image_src(self):
        while True:

            # Update the image URL here
            self.image_src = "/YCZH_copy.gif"
            # Wait for a few seconds before updating again
            print("Hi")
            await asyncio.sleep(1)
            self.image_src = "/YCZH.gif"
            # Wait for a few seconds before updating again
            await asyncio.sleep(1)



color = "rgb(107,99,246)"


def index():
    """The main view."""
    return rx.center(rx.vstack(
        rx.hstack(
            rx.image(
                src = "/logo.jpg",
                height = "80%",
                width = "auto",
                border_radius = "40px",
                padding = "20px",
                padding_right = "0px",
                align = "center",
            ),
            rx.image(
                src = "/words.jpeg",
                height = "80%",
                width = "auto",
                padding = "20px",
                padding_left = "0px",
                margin_top = "5px",
                align = "center",
            ),
            width = "100%",
            height = "125px",
            bg = "#FAF1E8",
            # red is bg = "#720001",


        ),
        rx.upload(
            rx.vstack(
                rx.text(
                    "UPLOAD VIDEO",
                    font_size = "40px",
                    font_weight = "bold",
                    text_align="center",
                    padding_bottom = "30%",
                    margin = "20px",
                ),
                rx.text(
                    "Drag and drop your .mp4 file here or click to select",
                    font_size="1.25em",  # Adjusts the font size
                    color="rgb(128, 0, 32)",  # Burgundy color for sleek appearance
                    font_weight="bold",  # Makes the text bold
                    text_align="center",  # Centers the text
                    padding="10px",  # Adds some padding around the text
                    border="2px dashed #800020",  # Adds a burgundy border
                    border_radius="8px",  # Rounds the corners of the border
                    margin="20px",  # Adds some margin outside the border
                ),
            ),
        id="upload",
        on_drop = State.handle_upload(rx.upload_files(upload_id="upload")),
        border="2px solid #800020", 
        background_color="#FAF1E8",  
        color="#800020", 
        padding="20px",
        width="auto",
        height="400px",
        margin = "5%",
        border_radius = "25px",
        ),
            align = "center",
            width = "100%",
    
    ),
    #rx.hstack(
     #   rx.button("Click me for status", on_click=rx.window_alert(str(config.PERCENT_COMPLETED) + "%: " + config.CURRENT_STATUS), size = '4', align = "center")
    #)
    
    )

def loading():
    ImageState.update_image_src()
    return rx.center(rx.vstack(
        rx.hstack(
            rx.image(
                src = "/logo.jpg",
                height = "80%",
                width = "auto",
                border_radius = "40px",
                padding = "20px",
                padding_right = "0px",
                align = "center",
            ),
            rx.image(
                src = "/words.jpeg",
                height = "80%",
                width = "auto",
                padding = "20px",
                padding_left = "0px",
                margin_top = "5px",
                align = "center",
            ),
            width = "100%",
            height = "125px",
            bg = "#FAF1E8",
            # red is bg = "#720001",


        ),
        rx.image(
            src = ImageState.image_src,
            align = "center",
        ),
        
        align = "center",
        width = "100%",
    ),
    align = "center",
    width = "100%",
    )


def output():
    return rx.center(rx.vstack(
        rx.hstack(
            rx.image(
                src = "/logo.jpg",
                height = "80%",
                width = "auto",
                border_radius = "40px",
                padding = "20px",
                padding_right = "0px",
                align = "center",
            ),
            rx.image(
                src = "/words.jpeg",
                height = "80%",
                width = "auto",
                padding = "20px",
                padding_left = "0px",
                margin_top = "5px",
                align = "center",
            ),
            width = "100%",
            height = "125px",
            bg = "#FAF1E8",
            # red is bg = "#720001",


        ),
    rx.markdown(State.output)
    ),
    ),


style = {
    "background-color":"#FFFFFF",
}
app = rx.App(style = style)
app.add_page(index)
app.add_page(loading)
app.add_page(output)
