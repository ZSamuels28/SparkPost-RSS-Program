import PySimpleGUI as sg


def build_window(template_ids, recipient_ids):
    # Creates the layout of the GUI
    layout = [
        [
            sg.Text(
                "Enter RSS URL:",
                auto_size_text=True,
            ),
            sg.InputText(key="rss-url"),
            sg.Button("Read RSS", key="read_rss"),
        ],
        [
            sg.Text(
                "How many RSS items to send?",
                auto_size_text=True,
            ),
            sg.InputText(
                key="rss-number",
                size=(2, 1),
            ),
        ],
        [
            sg.Text(
                "Enter Campaign ID:",
                auto_size_text=True,
            ),
            sg.InputText(
                size=(30, 1),
                key="campaign_id",
            ),
        ],
        [
            sg.Text(
                "Choose Template",
                auto_size_text=True,
            ),
            sg.Combo(
                template_ids,
                auto_size_text=True,
                enable_events=True,
                readonly=True,
                key="template_id",
            ),
        ],
        [
            sg.Text(
                "Choose Recipient List",
                auto_size_text=True,
            ),
            sg.Combo(
                recipient_ids,
                default_value=recipient_ids[0],
                auto_size_text=True,
                readonly=True,
                key="recipient_id",
            ),
            sg.Text(
                "Filter Elements: ",
                size=(26, 1),
                justification="right",
            ),
            sg.Input(
                size=(18, 1),
                enable_events=True,
                key="filter",
            ),
        ],
        [
            sg.Multiline(
                size=(50, 20),
                sbar_arrow_width=15,
                enable_events=True,
                key="template",
            ),
            sg.Listbox(
                values=[],
                sbar_arrow_width=15,
                size=(30, 19),
                enable_events=True,
                key="rss_elements",
            ),
        ],
        [
            sg.Button("Send", key="send"),
            sg.Button("Update Template", key="update_template"),
            sg.Button("Close", key="close"),
        ],
    ]

    window = sg.Window(
        "SparkPost RSS Tranmission",
        layout,
        finalize=True,
        font="Any 16",
    )  # Define the window to be shown with the above objects

    return window


# Gets the center of the window to be used for pop-ups
def center_of_window(window):
    x = window.current_size_accurate()[0] / 2
    y = window.current_size_accurate()[1] / 2
    center = (window.current_location()[0] + x - 110, window.current_location()[1] + y)
    return center
