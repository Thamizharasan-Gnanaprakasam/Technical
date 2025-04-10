import time

from kivy.config import Config


Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.core.window import Window
from kivy.core.audio import Sound, SoundLoader
from kivy.app import App
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
import random
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file("menu.kv")


class MainWidget(RelativeLayout):
    from user_actions import is_desktop, keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up
    from transforms import transform, transform_perspective, transform_2D

    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    vertical_lines = []
    NB_V_LINES = 8
    VL_SPACING= .20

    horizontal_lines=[]
    NB_H_LINES = 15
    HL_SPACING = .2

    current_offset_y = 0
    SPEED=.8

    current_offset_x = 0
    current_speed_x = 0
    SPEED_X = 3

    NO_TILES = 16
    tiles = []
    tiles_coordinates = []
    ti_x = 1
    ti_y = 2

    current_y_loop = 0

    ship = None
    SHIP_WIDTH = .1
    SHIP_HEIGHT = 0.035
    SHIP_BASE_Y = 0.04

    ship_coordinates = [(0,0),(0,0),(0,0)]
    game_over_state = False
    game_start_state = False

    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("START")
    score_txt = StringProperty("Score: 0")

    sound_begin = None
    sound_galaxy = None
    sound_gameover_impact = None
    sound_gameover_voice = None
    sound_music1 = None
    sound_restart = None
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.init_sound()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_game()

        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down=self.on_keyboard_down)
            self.keyboard.bind(on_key_up=self.on_keyboard_up)

        self.sound_galaxy.play()
        Clock.schedule_interval(self.update, .5 / 60)


    def init_sound(self):
        self.sound_begin = SoundLoader.load("audio/begin.wav")
        self.sound_galaxy = SoundLoader.load("audio/galaxy.wav")
        self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")
        self.sound_gameover_voice = SoundLoader.load("audio/gameover_voice.wav")
        self.sound_music1 = SoundLoader.load("audio/music1.wav")
        self.sound_restart = SoundLoader.load("audio/restart.wav")

        self.sound_music1.volume = 1
        self.sound_begin.volume = .25
        self.sound_galaxy.volume = .25
        self.sound_gameover_voice.volume = .25
        self.sound_restart.volume = .25
        self.sound_gameover_impact.volume = .6

    def reset_game(self):
        self.current_offset_y = 0
        self.current_offset_x = 0
        self.current_speed_x = 0
        self.current_y_loop = 0
        self.tiles_coordinates = []
        self.pre_tile_fill_coordinate()
        self.generate_tiles_coordinates()
        self.game_over_state = False
        self.game_start_state = False

    def init_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.NO_TILES):
                self.tiles.append(Quad())

    def init_ship(self):
        with self.canvas:
            Color(0,0,0)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width/2
        base_y = self.SHIP_BASE_Y * self.height
        ship_half_width = self.SHIP_WIDTH * self.width/2
        ship_height = self.SHIP_HEIGHT * self.height

        self.ship_coordinates[0] = (center_x-ship_half_width,base_y)
        self.ship_coordinates[1] = (center_x , base_y+ship_height)
        self.ship_coordinates[2] = (center_x + ship_half_width, base_y)


        x1,y1 = self.transform(*self.ship_coordinates[0])
        x2,y2 = self.transform(*self.ship_coordinates[1])
        x3,y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points= [x1,y1,x2,y2,x3,y3]

    def check_ship_collision(self):
        for i in range(len(self.tiles_coordinates)):
            ti_x,ti_y = self.tiles_coordinates[i]

            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tail(ti_x,ti_y):
                return True
        return False

    def check_ship_collision_with_tail(self,ti_x,ti_y):
        xmin, ymin = self.get_tile_cooridnates(ti_x, ti_y)
        xmax, ymax = self.get_tile_cooridnates(ti_x + 1, ti_y + 1)
        for i in range(len(self.ship_coordinates)):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False


    def pre_tile_fill_coordinate(self):
        last_x = 0
        last_y = 0
        for i in range(10):
            self.tiles_coordinates.append((last_x, last_y))
            last_y+=1

    def generate_tiles_coordinates(self):
        last_x = 0
        last_y = 0
        for i in range(len(self.tiles_coordinates) -1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_x = self.tiles_coordinates[-1][0]
            last_y = self.tiles_coordinates[-1][1] + 1
        for i in range(len(self.tiles_coordinates),self.NO_TILES):
            r = random.randint(0,2)
            # 0 => Stright
            # 1 => Right
            # 2 => Left
            self.tiles_coordinates.append((last_x,last_y))
            start_index = -int(self.NB_V_LINES / 2) + 1
            end_index = start_index + self.NB_V_LINES - 1
            if last_x <= start_index:
                r = 1
            if end_index <= last_x:
                r = 2

            if r == 1:
                last_x +=1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            elif r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y +=1

    def update_tiles(self):
        for i in range(self.NO_TILES):
            tile_coordinate = self.tiles_coordinates[i]
            tile = self.tiles[i]
            xmin, ymin = self.get_tile_cooridnates(tile_coordinate[0],tile_coordinate[1])
            xmax, ymax = self.get_tile_cooridnates(tile_coordinate[0]+1,tile_coordinate[1]+1)

            # 2  3
            #
            # 1  4
            x1,y1 = self.transform(xmin,ymin)
            x2,y2 = self.transform(xmin,ymax)
            x3,y3 = self.transform(xmax,ymax)
            x4,y4 = self.transform(xmax,ymin)
            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]


    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            #self.line = Line(points=[100, 0, 100, 100])
            for i in range(self.NB_V_LINES):
                self.vertical_lines.append(Line())

    def get_line_x_from_index(self,index):
        #4 lines => -1, 0, 1, 2
        v_central_x = self.perspective_point_x
        if (self.NB_V_LINES % 2 == 0):
            offset = index - .5
        else:
            offset = index
        spacing = self.VL_SPACING * self.width

        line_x = v_central_x + offset * spacing + self.current_offset_x
        return line_x

    def get_tile_cooridnates(self,ti_x,ti_y):
        ti_y -= self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x,y




    def update_vertical_lines(self):
        start_index = -int(self.NB_V_LINES/2) +1
        for i in range(start_index,start_index+self.NB_V_LINES):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x,0)
            x2, y2 = self.transform(line_x,self.height)
            self.vertical_lines[i].points = [x1,y1,x2,y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)
            #self.line = Line(points=[100, 0, 100, 100])
            for i in range(self.NB_H_LINES):
                self.horizontal_lines.append(Line())

    def get_line_y_from_index(self, index):
        spacing = self.HL_SPACING * self.height
        line_y = index * spacing - self.current_offset_y
        return line_y

    def update_horizontal_lines(self):
        start_index = -int(self.NB_V_LINES/2 ) + 1
        end_index = start_index+self.NB_V_LINES -1

        min_x = self.get_line_x_from_index(start_index)
        max_x = self.get_line_x_from_index(end_index)


        for i in range(self.NB_H_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(min_x,line_y)
            x2, y2 = self.transform(max_x,line_y)
            self.horizontal_lines[i].points = [x1,y1,x2,y2]



    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()
        if not self.game_over_state and self.game_start_state:
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor
            h_spacing = self.HL_SPACING * self.height

            while self.current_offset_y >= h_spacing:
                self.current_offset_y -= h_spacing
                self.current_y_loop += 1
                self.generate_tiles_coordinates()
            speed_x = self.current_speed_x * self.width /100
            self.current_offset_x += speed_x*time_factor
            self.score_txt = "SCORE: " + str(self.current_y_loop)

        if not self.check_ship_collision() and not self.game_over_state:
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            time.sleep(3)
            self.sound_gameover_voice.play()
            self.game_over_state = True
            self.menu_widget.opacity = 1
            self.menu_title = "G  A  M  E   O  V  E  R"
            self.menu_button_title="RESTART"
            print("Game Over")

    def on_button_press(self):
        self.reset_game()
        if self.menu_button_title == "START":
            self.sound_begin.play()
        elif self.menu_button_title == "RESTART":
            self.sound_restart.play()
        self.sound_music1.play()
        self.game_start_state = True
        self.menu_widget.opacity = 0




class GalaxyApp(App):
    pass

GalaxyApp().run()