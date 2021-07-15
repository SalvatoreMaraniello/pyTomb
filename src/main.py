'''
Tombola Manager
'''

import os
import yaml 
import random 
import numpy as np 
import cowsay 
import art 

from colorama import init
init()
from colorama import Fore, Back, Style

colors_dict = {
    'LIGHTBLACK_EX': ['CYAN', 'GREEN', 'RED',  'WHITE', 'YELLOW'],
    'LIGHTBLUE_EX': ['WHITE'],
    'LIGHTCYAN_EX': ['BLACK', 'BLUE', 'MAGENTA', 'RED'],
    'LIGHTGREEN_EX': ['BLACK', 'MAGENTA' ],
    'LIGHTMAGENTA_EX': ['WHITE'],
    'LIGHTRED_EX': ['WHITE'],
    'LIGHTWHITE_EX': ['BLACK', 'BLUE', 'MAGENTA', 'RED' ],
    'LIGHTYELLOW_EX': ['BLACK', 'BLUE', 'MAGENTA', 'RED' ],
}

# mgs = 'Test message'
# for back,avail in colors_dict.items():
#     for fore in avail:
#         print( f'{back}:{fore}: ' + getattr(Back,back) + ' ' + getattr(Fore,fore) + mgs)
#         print(Style.RESET_ALL)

np.set_printoptions(linewidth=200)

### retrieve some settings
_src_dir = os.sep.join(__file__.split(os.sep)[:-1])
_numbers_yaml = 'numbers.yaml'
_version = '0.0'


class TombolaEngine():

    def __init__(self):
        self._version = _version

        self.available_numbers = yaml.safe_load( open( os.path.join(_src_dir,_numbers_yaml),'r') )
        self.extracted_numbers = dict()

        self.num_extracted = 0
        self.num_history = []
        self.num_available = len(self.available_numbers)
        assert self.num_available==90, 'You fucked up something in `numbers.yaml`'

        self.game_is_on = True
        self.Tabellone = np.zeros( (9,10), dtype=np.int8 )
        self.prices = dict(
            ambo = False, 
            terno = False, 
            quaterna = False, 
            cinquina = False, 
            tombola = False
        )

        # print(1*'\n')


        print(Style.BRIGHT)
        print(Back.BLUE)
        print(Fore.WHITE)
        art.tprint( 'T o m b o l a  ! ! !' )
        print(f'Tombola engine v{self._version:s} started!')
        print(Style.RESET_ALL)

    def end_game(self):
        self.game_is_on = False
        print(2 * '\n')
        art.tprint('G a m e   is   O v e r ! ! !')


    def get_status(self):
        print(2 * '\n')
        print('Numbers extracted: {self.num_extracted:.2d}')
        print('Numbers remaining: {self.num_available:.2d}')
        

    def extract_number(self):
        '''Extract a new number'''

        new_number = random.choice(list(self.available_numbers.keys()))
        desc = self.available_numbers.pop(new_number)

        self.num_history.append(new_number)
        self.extracted_numbers[new_number] = desc

        self.num_extracted += 1
        self.num_available -= 1

        # # set random color
        # print( Back.LIGHTBLUE_EX )
        # print( Style.BRIGHT)
        # print( getattr(Fore, random.choice( [ k for k in Fore.__dict__.keys() if 'BLUE' not in k] ) ) )
        # self.cowsay_fun( f'{new_number}' + 2*'\n' + f'{desc:s}' )
        # print(Style.RESET_ALL)

        desc = desc[:desc.find('(')]
        self.print_render(f'{new_number}' + 2*'\n' + f'{desc:s}')

        self.tomboliere_manager(new_number)

        # ToDo
        # check wins


    def print_render( self, msg: str):

        # set random color
        print(Style.RESET_ALL)
        print( Style.BRIGHT)

        # set random background
        available_back_colors = [k for k in colors_dict.keys()]
        back_color = random.choice( available_back_colors )
        print( getattr(Back, back_color) )

        # set fore color
        available_fore_colors = colors_dict[back_color]
        print( getattr(Fore, random.choice( available_fore_colors ) ) )

        # pick random animation 
        available_funs = [ k for k,it in cowsay.__dict__.items() if ('_' not in k and callable(it)) ]
        print_fun = getattr( cowsay, random.choice( available_funs ) )

        print_fun( msg )
        print(Style.RESET_ALL)

    
    def view_tabellone(self):
        # print(self.Tabellone)

        # ticks = list(ii+1 for ii in range(10))
        # quad = 3
        # header = quad*' '
        # for num in ticks:
        #     tick = str(num)
        #     tick = (quad-len(tick))*' ' + tick
        #     if num==6:
        #         tick = ' |' + tick[1:]
        #     header += tick
        # print(header)

        print(Style.BRIGHT)
        print(Back.BLUE)
        row = Fore.WHITE + 45*'-' + '\n'

        for num in range(1,91):
            
            if num in self.extracted_numbers.keys():
                row+=Fore.YELLOW
            else:
                row+=Fore.CYAN
            row+='  %.2d'%num

            if num%5==0 and num%10!=0:
                row += Fore.WHITE + '  |'

            if num%10==0:
                row += '\n'

            if num%30==0:
                row += Fore.WHITE + 45*'-' + '\n'

        print(row)
        print(Style.RESET_ALL)



    def tomboliere_manager(self, new_number):
        '''
        Keep track of progress and check if tomboliere has won a prise!
        '''
        pass 

        # Position in tablellone
        row, col = (new_number-1)//10, (new_number-1)%10
        self.Tabellone[row,col] = 1






cmd_dict = dict(
    # h = dict(
    #     desc = 'Get help',
    #     cmd = None,
    # ),
    
    n = dict(cmd='extract_number', desc='Extract a new number'),
    q = dict(cmd='end_game', desc='Terminate Game'),
    t = dict(cmd='view_tabellone', desc='Visualise tabellone'),

)

def GameManager():

    T = TombolaEngine()

    while T.game_is_on:
        cmd = input('\nNext action (press h for help): ')

        if cmd=='':
            cmd='n'
        if cmd=='h':
            print(1*'\n' + 'List commands:')
            for key, item in cmd_dict.items():
                print(f'''{key}: {item['desc']}''')
            continue
        if cmd not in cmd_dict.keys():
            print('Input not valid!')
            continue
                
        # make move
        getattr(T, cmd_dict[cmd]['cmd'])()
    
    return T



class Cartella():
    def __init__(self):
        '''
        Initialise cartella with random numbers
        '''

        avail = list(range(1,91))
        self.vals = []


        for ii in range(3):
            row = []
            for jj in range(5):

                num = random.choice(avail)
                row.append( avail.pop(num-1) )
            
            self.vals.append(row)
        






if __name__ == '__main__':
    T = GameManager()
    # C = Cartella()

