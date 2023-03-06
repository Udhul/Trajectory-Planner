#__________________________________________________________________________________________________________
#------ Requirements -------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
import PySimpleGUI as sg
import json
import serial
import serial.tools.list_ports



#__________________________________________________________________________________________________________
#------ Definitions --------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
#---Header
FONT_TOP_BLOCK          = 'verdana 16 bold'
FONT_SUB_TOP_BLOCK      = 'verdana 12 bold'
COLOR_TOP_BG            = 'yellow'
PAD_BLOCK_TOP           = (0,0)

#---Footer
PAD_BLOCK_BOTTOM        = (0,0)
COLOR_BOTTOM_BG         = 'black'

#---body
COLOR_BODY_BG           = 'grey'

#---Start window
SIZE_BLOCK_START        = (256,256)
TITLE_START             = 'CNC Trajectory Planner'
SUBTITLE_START          = 'Connect to Controller'
ERROR_NO_PORT           = 'No port found...'
COLOR_BUTTON_REFRESH    = 'teal'
COLOR_BUTTON_CONNECT    = 'dark green'
COLOR_BUTTON_EXIT       = 'dark red'



#__________________________________________________________________________________________________________
#------ Startup Window ------------------------------------------------------------------------------------>
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
def window_start(first_launch:bool=True):
    '''Startup window to connect to the serial port.\n
    Defines and runs the port connection window. \n
    ::param:: first_launch should be False if this function is called from mid-program'''
    #---Top Block
    block_top = [
        [
            sg.Column([
                [sg.Text(TITLE_START, font=FONT_TOP_BLOCK, text_color='black', border_width=5, background_color=COLOR_TOP_BG, justification='c')],
                [sg.Text(SUBTITLE_START, font=FONT_SUB_TOP_BLOCK, text_color='black', border_width=5, background_color=COLOR_TOP_BG, justification='c')]
            ], element_justification='c', background_color=COLOR_TOP_BG, pad=(PAD_BLOCK_TOP), expand_x=True)
        ],
    ]

    #---Bottom Block
    block_bottom = [
        [
            sg.Column([
                #---Navigation buttons
                [
                    sg.Button('Close', expand_x=True, button_color=COLOR_BUTTON_EXIT),
                ],
            ], element_justification='c', background_color=COLOR_BOTTOM_BG, pad=PAD_BLOCK_BOTTOM, expand_x=True)
        ],
    ]


    block_body = [
        # Port selection
        [sg.Text('Select Serial Port:', expand_x=True)],
        # [sg.Listbox(values=[ERROR_NO_PORT], key='start/ports', no_scrollbar=True, select_mode='single', expand_x=True)],
        [sg.Combo([''], default_value='', key='start/ports', expand_x=True, tooltip=' Select Serial Port ')],
        [sg.Button('Refresh Ports', key='start/refresh', expand_x=True, button_color=COLOR_BUTTON_REFRESH)],

        # Separator
        [sg.HorizontalSeparator()],

        # Baud rate
        [sg.Text('Select Baud Rate:', expand_x=True)],
        [sg.Combo(['115200'], default_value='115200', key='start/baudrate', expand_x=True, tooltip=' Select Baud Rate ')],

        # Connect
        [sg.Button('Connect', key='start/connect', button_color=COLOR_BUTTON_CONNECT, expand_x=True)]
    ]


    #---Assemble layout
    layout = [
        [block_top],
        [[sg.Column(block_body, background_color=COLOR_BODY_BG, pad=(0,0), element_justification='c', expand_x=True, expand_y=True)]],
        [block_bottom]
    ]

    #---Define window. Finalize it, so elements can be updated before first window read
    window = sg.Window(TITLE_START, layout, grab_anywhere=True, element_padding=(0,0), keep_on_top=True, no_titlebar=True, finalize=True, background_color=COLOR_BODY_BG)


    #---Refresh ports function (called at start and from refresh button)
    def refresh_ports():
        # Get a list of available serial ports on the system
        ports = serial.tools.list_ports.comports()
        # If no ports are found
        if ports == []: 
            # Set the list index 0 to the error code
            ports = [ERROR_NO_PORT]
            # Disable connect button
            window['start/connect'].update(disabled=True)
        # If ports were found, enable the connect button
        else: window['start/connect'].update(disabled=False)
        # Update the combobox with the list of ports. Set the select value to list index 0
        window['start/ports'].update(values=ports, value=ports[0])


    #---Reset event flags and window values
    refresh_ports()
    proceed = False
    

    #---Window Main Loop
    while True:
        #---Open connect window
        event, values = window.read()

        #---Window close check
        if event == 'Exit' or event == 'Close' or event == sg.WIN_CLOSED:
            break

        #---Refresh click event
        if event == 'start/refresh':
            refresh_ports

        #---Connect click event
        if event == 'start/connect' and values['start/ports'] != ERROR_NO_PORT:
            try: 
                # Try connecting to the selected port
                ser = serial.Serial(port='COM1', baudrate=115200, timeout=1)
                # Set proceed flag, meaning that the window break is not due to Exit
                proceed = True
                break
            # In case the port launch fails:
            except Exception as e: 
                # Show popup with error message 
                # (Normally this will not be shown due to connect button being disabled when there's no port)
                sg.popup(f'Could not connect to the port\nError: {e}', keep_on_top=True, modal=True)

    # Close this connection window
    window.close()
    
    # If proceed (expect main window to launch) and first_launch (main window not already running): 
    if proceed and first_launch: 
        # Open the main window, passing in the serial connection
        window_main(ser)
    # If the connect window is called from the main window, just return the serial connection
    elif proceed: return ser



#__________________________________________________________________________________________________________
#------ Main Window --------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
def window_main(ser=None):
    #---Top Block
    block_top = [
        [
            sg.Column([
                [sg.Text(TITLE_START, font=FONT_TOP_BLOCK, text_color='black', border_width=5, background_color=COLOR_TOP_BG, justification='c')],
                [sg.Text('Main Window', font=FONT_SUB_TOP_BLOCK, text_color='black', border_width=5, background_color=COLOR_TOP_BG, justification='c')],
                []
            ], element_justification='c', background_color=COLOR_TOP_BG, pad=(PAD_BLOCK_TOP), expand_x=True)
        ],
    ]

    #---Bottom Block
    block_bottom = [
        [
            sg.Column([
                #---Navigation buttons
                [
                    sg.Button('Reconnect', key='main/reconnect'),
                    sg.Button('Exit', expand_x=True, button_color=COLOR_BUTTON_EXIT),
                ],
            ], element_justification='c', background_color=COLOR_BOTTOM_BG, pad=PAD_BLOCK_BOTTOM, expand_x=True)
        ],
    ]

    #---Assemble layout
    layout = [
        [block_top],
        [block_bottom]
    ]
    
    #---Define window. Finalize it, so elements can be updated before first window read
    window = sg.Window(TITLE_START, layout, element_padding=(0,0), keep_on_top=True, no_titlebar=True, finalize=True, background_color=COLOR_BODY_BG)

    #---Window Main Loop
    while True:
        #---Open connect window
        event, values = window.read()

        #---Window close check
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        if event == 'main/reconnect':
            ser = window_start(first_launch=False)
#__________________________________________________________________________________________________________
#------ Main loop ----------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
def main():
    window_start()



#__________________________________________________________________________________________________________
#------ Run main loop ------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
if __name__ == '__main__':
    main()