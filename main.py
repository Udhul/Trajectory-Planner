#__________________________________________________________________________________________________________
#------ Requirements -------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
import PySimpleGUI as sg
import json
import serial
import serial.tools.list_ports
from gcodeparser import GcodeParser
import hashlib


#__________________________________________________________________________________________________________
#------ Definitions --------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
#---Header General
HEADER_FONT_TITLE       = 'verdana 16 bold'
HEADER_FONT_SUBTITLE    = 'verdana 12 bold'
HEADER_COLOR_BG         = 'yellow'
HEADER_PAD              = (0,0)

#---Footer General
FOOTER_PAD              = (0,0)
FOOTER_COLOR_BG         = 'black'

#---Body General
BODY_COLOR_BG           = 'grey'

#---Start window
SIZE_BLOCK_START        = (256,256)
TITLE_START             = 'CNC Trajectory Planner'
SUBTITLE_START          = 'Connect to Controller'
ERROR_NO_PORT           = 'No port found...'
COLOR_BUTTON_REFRESH    = 'teal'
COLOR_BUTTON_CONNECT    = 'dark green'
COLOR_BUTTON_EXIT       = 'dark red'



#__________________________________________________________________________________________________________
#------ G-Code Line Executor ------------------------------------------------------------------------------>
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
class gcode:
    '''Create objects containing gcode, the parsed version, execution methods, and keep track of progress and gcode position'''
    def __init__(self, gcode_path:str) -> None:
        self.path = gcode_path
        self.parsed = self.parse(gcode_path)
        self.hash = self.hash(self.parsed.gcode)

    def parse(self, gcode_path:str):
        '''Parse the loaded gcode using the GcodeParser library. 
        This will split the gcode into liones, commands and parameters'''
        # Try parsing the gcode
        try:
            with open(gcode_path, 'r') as f:
                # Raw string form of the file
                gcode_loaded = f.read()
                # Parsed object format
                gcode_parsed = GcodeParser(gcode_loaded)
                return gcode_parsed
        # If the gcode could not be parsed, print the error (maybe it is a wrong or unsupported file)
        except Exception as e:
            print(f'The chosen file could not be parsed as a G-Code.\nError: {e}')
            # self.parsed becomes 'None' until gcode is successfully loaded and parsed
            return None

    def hash(self, gcode:str):
        '''Get the hashed value of the loaded gcode. 
        Used to Keep object settings if the same code is loaded later'''
        gcode_utf = gcode.encode('utf-8')
        sha1hash = hashlib.sha1()
        sha1hash.update(gcode_utf)
        gcode_hash = sha1hash.hexdigest()
        return gcode_hash

    def run(self, line_no:int):
        self.execute_line(self.parsed, line_no)

    def execute_line(self, line_no:int):
        # print(gcode_parsed.gcode) # Contains the raw loaded gcode
        # print(gcode_parsed.lines[line_no])  # Print parsed gcode lines
        command_type    = self.parsed.lines[line_no].command[0]
        command_number  = self.parsed.lines[line_no].command[1]
        params          = self.parsed.lines[line_no].params
        print('type:  ', command_type)
        print('number:', command_number)
        print('params:', params)
        print('-----------')

        # Machine Op Commands
        if command_type == 'M':
            # Program stop
            if command_number == 0:
                ... 
            # Spindle On CW
            if command_number == 3:
                ... # 
            # Spindle On CCW
            if command_number == 4:
                ... # 
            # Spindle Off
            if command_number == 5:
                ... # 

        # G type Commands
        if command_type == 'G':
            # Rapid Movement
            if command_number == 0:
                ...
            # Cut Movement
            if command_number == 1:
                ...
            # Move to Position 0
            if command_number == 21:
                ...
            # Swtich to Absolute Coordinates
            if command_number == 90:
                ...
            # Swtch to Incremental Coordinates
            if command_number == 91:
                ...

        # Tool change commands. Placeholder. Currently unsupported
        if command_type == 'T':
            ... 



#__________________________________________________________________________________________________________
#------ Startup Window ------------------------------------------------------------------------------------>
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
def window_start(first_launch:bool=True):
    '''Startup window to connect to the serial port.\n
    Defines and runs the port connection window. \n
    ::param:: first_launch should be False if this function is called from mid-program'''
    #---Top Block
    block_header = [
        [
            sg.Column([
                [sg.Text(TITLE_START, font=HEADER_FONT_TITLE, text_color='black', border_width=5, background_color=HEADER_COLOR_BG, justification='c')],
                [sg.Text(SUBTITLE_START, font=HEADER_FONT_SUBTITLE, text_color='black', border_width=5, background_color=HEADER_COLOR_BG, justification='c')]
            ], element_justification='c', background_color=HEADER_COLOR_BG, pad=(HEADER_PAD), expand_x=True)
        ],
    ]

    #---Bottom Block
    block_footer = [
        [
            sg.Column([
                #---Navigation buttons
                [
                    sg.Button('Close', expand_x=True, button_color=COLOR_BUTTON_EXIT),
                ],
            ], element_justification='c', background_color=FOOTER_COLOR_BG, pad=FOOTER_PAD, expand_x=True)
        ],
    ]

    #---Body Block
    block_body = [
        # Port selection
        [sg.Text('Select Serial Port:', expand_x=True)],
        # [sg.Listbox(values=[ERROR_NO_PORT], key='start/ports', no_scrollbar=True, select_mode='single', expand_x=True)],
        [sg.Combo([''], default_value='', key='start/ports', expand_x=True, tooltip=' Select Serial Port ')],
        [sg.Button('Refresh Ports', key='start/refresh', expand_x=True, button_color=COLOR_BUTTON_REFRESH)],

        # Separator
        [sg.HorizontalSeparator()],

        # Baud rate (Fixed for now)
        [sg.Text('Select Baud Rate:', expand_x=True)],
        [sg.Combo(['115200'], default_value='115200', key='start/baudrate', expand_x=True, tooltip=' Select Baud Rate ')],

        # Connect
        [sg.Button('Connect', key='start/connect', button_color=COLOR_BUTTON_CONNECT, expand_x=True)]
    ]


    #---Assemble layout
    layout = [
        [block_header],
        [[sg.Column(block_body, background_color=BODY_COLOR_BG, pad=(0,0), element_justification='c', expand_x=True, expand_y=True)]],
        [block_footer]
    ]

    #---Define window. Finalize it, so elements can be updated before first window read
    window = sg.Window(TITLE_START, layout, grab_anywhere=True, element_padding=(0,0), keep_on_top=True, no_titlebar=True, finalize=True, background_color=BODY_COLOR_BG)


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
                ser = serial.Serial(port=values['start/ports'], baudrate=values['start/baudrate'], timeout=1)
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
    block_header = [
        [
            sg.Column([
                [sg.Text(TITLE_START, font=HEADER_FONT_TITLE, text_color='black', border_width=5, background_color=HEADER_COLOR_BG, justification='c')],
                [sg.Text('Main Window', font=HEADER_FONT_SUBTITLE, text_color='black', border_width=5, background_color=HEADER_COLOR_BG, justification='c')],
                []
            ], element_justification='c', background_color=HEADER_COLOR_BG, pad=(HEADER_PAD), expand_x=True)
        ],
    ]

    #---Body Block
    block_body = [
        [
            #---Left Column
            sg.Column([
                [sg.Text('Here goes left column elements')]
            ], 
            background_color='red', pad=(0,0), expand_x=True
            ),
    
            #---Right Column
            sg.Column([
                [sg.Text('Here goes right column elements')]
            ], 
            background_color='blue', pad=(0,0), expand_x=True
            ),
        ]
    ]

    #---Bottom Block
    block_footer = [
        [
            sg.Column([
                #---Navigation buttons
                [
                    sg.Button('Reconnect', key='main/reconnect'),
                    sg.Button('Settings', key='main/settings'),
                    sg.Button('Load G-Code', key='main/load_gcode_button'),
                    sg.Input('', key='load_gcode_input'),
                    sg.Button('Exit', expand_x=True, button_color=COLOR_BUTTON_EXIT),
                ],
            ], element_justification='c', background_color=FOOTER_COLOR_BG, pad=FOOTER_PAD, expand_x=True)
        ],
    ]

    #---Assemble layout
    layout = [
        [block_header],
        [block_body],
        [block_footer]
    ]
    
    #---Define window. Finalize it, so elements can be updated before first window read
    window = sg.Window(TITLE_START, layout, element_padding=(0,0), keep_on_top=True, no_titlebar=True, finalize=True, background_color=BODY_COLOR_BG)

    #---Window Main Loop
    while True:
        #---Open connect window
        event, values = window.read()

        #---Window close check
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        if event == 'main/reconnect':
            ser = window_start(first_launch=False)

        if event == 'main/load_gcode_button':
            # Get the gcode path from the file browse popup
            gcode_path = sg.popup_get_file(message='Load G-code', title='Load G-code', default_extension='.nc', keep_on_top=True)
            # sg.FileBrowse(button_text='Select G-Code', target='load_gcode_input')

            gcode_loaded = gcode(gcode_path)

            # Test run through the first 50 lines
            for line in range(50):
                gcode_loaded.run(line)



#__________________________________________________________________________________________________________
#------ Main loop ----------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
def main():
    window_main()



#__________________________________________________________________________________________________________
#------ Run main loop ------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
if __name__ == '__main__':
    main()