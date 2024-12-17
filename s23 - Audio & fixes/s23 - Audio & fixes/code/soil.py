import pygame  # Nhập thư viện pygame để sử dụng các chức năng đồ họa
from settings import *  # Nhập các cài đặt từ module settings
from pytmx.util_pygame import load_pygame  # Nhập chức năng load tmx map từ pytmx
from support import *  # Nhập các hỗ trợ từ module support
from random import choice  # Nhập hàm choice từ thư viện random

class SoilTile(pygame.sprite.Sprite):  # Lớp SoilTile đại diện cho các ô đất
    def __init__(self, pos, surf, groups):  # Khởi tạo lớp SoilTile với vị trí, hình ảnh và các nhóm sprite
        super().__init__(groups)  # Thêm đối tượng vào các nhóm sprite
        self.image = surf  # Lưu hình ảnh của ô đất
        self.rect = self.image.get_rect(topleft = pos)  # Lấy hình chữ nhật bao quanh ô đất, đặt ở vị trí pos
        self.z = LAYERS['soil']  # Xác định lớp vẽ (z-index) của ô đất

class WaterTile(pygame.sprite.Sprite):  # Lớp WaterTile đại diện cho các ô nước
    def __init__(self, pos, surf, groups):  # Khởi tạo lớp WaterTile với vị trí, hình ảnh và các nhóm sprite
        super().__init__(groups)  # Thêm đối tượng vào các nhóm sprite
        self.image = surf  # Lưu hình ảnh của ô nước
        self.rect = self.image.get_rect(topleft = pos)  # Lấy hình chữ nhật bao quanh ô nước, đặt ở vị trí pos
        self.z = LAYERS['soil water']  # Xác định lớp vẽ (z-index) của ô nước

class Plant(pygame.sprite.Sprite):  # Lớp Plant đại diện cho cây trồng
    def __init__(self, plant_type, groups, soil, check_watered):  # Khởi tạo cây trồng với loại cây, nhóm sprite, ô đất, và hàm kiểm tra tưới nước
        super().__init__(groups)  # Thêm đối tượng vào các nhóm sprite
        
        # setup
        self.plant_type = plant_type  # Lưu loại cây
        self.frames = import_folder(f'c:/Desktop/KHMT/s3 - import/s3 - import/graphics/fruit/{plant_type}')  # Lấy các hình ảnh của cây
        self.soil = soil  # Lưu đối tượng ô đất
        self.check_watered = check_watered  # Lưu hàm kiểm tra tưới nước

        # plant growing 
        self.age = 0  # Tuổi của cây, bắt đầu từ 0
        self.max_age = len(self.frames) - 1  # Tuổi tối đa của cây là số lượng hình ảnh - 1
        self.grow_speed = GROW_SPEED[plant_type]  # Tốc độ phát triển của cây theo loại
        self.harvestable = False  # Cây có thể thu hoạch được không?

        # sprite setup
        self.image = self.frames[self.age]  # Lấy hình ảnh cây tại tuổi hiện tại
        self.y_offset = -16 if plant_type == 'corn' else -8  # Độ dời hình ảnh theo trục y, tùy theo loại cây
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))  # Vị trí hình ảnh cây dựa vào ô đất
        self.z = LAYERS['ground plant']  # Xác định lớp vẽ (z-index) của cây

    def grow(self):  # Hàm xử lý sự phát triển của cây
        if self.check_watered(self.rect.center):  # Kiểm tra nếu cây đã được tưới nước
            self.age += self.grow_speed  # Tăng tuổi cây theo tốc độ phát triển

            if int(self.age) > 0:  # Nếu cây đã phát triển
                self.z = LAYERS['main']  # Đổi lớp vẽ của cây
                self.hitbox = self.rect.copy().inflate(-26,-self.rect.height * 0.4)  # Cập nhật vùng va chạm của cây

            if self.age >= self.max_age:  # Nếu cây đạt tuổi tối đa
                self.age = self.max_age  # Đặt tuổi cây bằng tuổi tối đa
                self.harvestable = True  # Cây có thể thu hoạch được

            self.image = self.frames[int(self.age)]  # Cập nhật hình ảnh cây theo tuổi
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))  # Cập nhật vị trí cây

class SoilLayer:  # Lớp SoilLayer quản lý toàn bộ lớp đất, nước, và cây trồng
    def __init__(self, all_sprites, collision_sprites):  # Khởi tạo lớp SoilLayer với các nhóm sprite
        # sprite groups
        self.all_sprites = all_sprites  # Nhóm sprite tất cả các đối tượng
        self.collision_sprites = collision_sprites  # Nhóm sprite các đối tượng có va chạm
        self.soil_sprites = pygame.sprite.Group()  # Nhóm sprite đất
        self.water_sprites = pygame.sprite.Group()  # Nhóm sprite nước
        self.plant_sprites = pygame.sprite.Group()  # Nhóm sprite cây trồng

        # graphics
        self.soil_surfs = import_folder_dict('c:/Desktop/KHMT/s3 - import/s3 - import/graphics/soil/')  # Tạo dictionary chứa các hình ảnh đất
        self.water_surfs = import_folder('c:/Desktop/KHMT/s3 - import/s3 - import/graphics/soil_water')  # Tạo danh sách chứa các hình ảnh nước

        self.create_soil_grid()  # Tạo lưới đất
        self.create_hit_rects()  # Tạo các hình chữ nhật va chạm cho các ô đất

        # sounds
        self.hoe_sound = pygame.mixer.Sound('c:/Desktop/KHMT/s3 - import/s3 - import/audio/hoe.wav')  # Âm thanh cào đất
        self.hoe_sound.set_volume(0.1)  # Cài đặt âm lượng cho âm thanh cào đất

        self.plant_sound = pygame.mixer.Sound('c:/Desktop/KHMT/s3 - import/s3 - import/audio/plant.wav')  # Âm thanh trồng cây
        self.plant_sound.set_volume(0.2)  # Cài đặt âm lượng cho âm thanh trồng cây

    def create_soil_grid(self):  # Hàm tạo lưới đất
        ground = pygame.image.load('c:/Desktop/KHMT/s3 - import/s3 - import/graphics/world/ground.png')  # Tải hình ảnh mặt đất
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE  # Tính số lượng ô đất theo chiều ngang và chiều dọc
        
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]  # Khởi tạo lưới đất
        for x, y, _ in load_pygame('c:/Desktop/KHMT/s3 - import/s3 - import/data/map.tmx').get_layer_by_name('Farmable').tiles():  # Duyệt qua các ô có thể trồng
            self.grid[y][x].append('F')  # Đánh dấu ô có thể trồng cây

    def create_hit_rects(self):  # Hàm tạo các hình chữ nhật va chạm cho các ô đất
        self.hit_rects = []  # Danh sách các hình chữ nhật va chạm
        for index_row, row in enumerate(self.grid):  # Duyệt qua các hàng trong lưới đất
            for index_col, cell in enumerate(row):  # Duyệt qua các cột trong mỗi hàng
                if 'F' in cell:  # Nếu ô có thể trồng cây
                    x = index_col * TILE_SIZE  # Tính toán tọa độ x của ô
                    y = index_row * TILE_SIZE  # Tính toán tọa độ y của ô
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)  # Tạo hình chữ nhật cho ô đất
                    self.hit_rects.append(rect)  # Thêm hình chữ nhật vào danh sách

    def get_hit(self, point):  # Hàm kiểm tra va chạm với một điểm
        for rect in self.hit_rects:  # Duyệt qua tất cả các hình chữ nhật va chạm
            if rect.collidepoint(point):  # Nếu điểm va chạm với hình chữ nhật
                self.hoe_sound.play()  # Phát âm thanh cào đất

                x = rect.x // TILE_SIZE  # Tính toán tọa độ x của ô đất
                y = rect.y // TILE_SIZE  # Tính toán tọa độ y của ô đất

                if 'F' in self.grid[y][x]:  # Nếu ô có thể trồng cây
                    self.grid[y][x].append('X')  # Đánh dấu ô đã được xử lý
                    self.create_soil_tiles()  # Tạo các ô đất mới
                    if self.raining:  # Nếu đang mưa
                        self.water_all()  # Tưới nước cho tất cả cây


    def water(self, target_pos):  # Hàm tưới nước vào vị trí target_pos
        for soil_sprite in self.soil_sprites.sprites():  # Duyệt qua tất cả các sprite đất
            if soil_sprite.rect.collidepoint(target_pos):  # Nếu ô đất va chạm với vị trí target_pos

                x = soil_sprite.rect.x // TILE_SIZE  # Tính tọa độ x của ô đất
                y = soil_sprite.rect.y // TILE_SIZE  # Tính tọa độ y của ô đất
                self.grid[y][x].append('W')  # Đánh dấu ô đất đã được tưới nước

                pos = soil_sprite.rect.topleft  # Lấy vị trí góc trên trái của ô đất
                surf = choice(self.water_surfs)  # Chọn một hình ảnh nước ngẫu nhiên
                WaterTile(pos, surf, [self.all_sprites, self.water_sprites])  # Tạo đối tượng nước tại vị trí ô đất

    def water_all(self):  # Hàm tưới nước cho tất cả các ô đất
        for index_row, row in enumerate(self.grid):  # Duyệt qua các hàng trong lưới đất
            for index_col, cell in enumerate(row):  # Duyệt qua các cột trong mỗi hàng
                if 'X' in cell and 'W' not in cell:  # Nếu ô có thể trồng cây và chưa được tưới nước
                    cell.append('W')  # Đánh dấu ô đất đã được tưới nước
                    x = index_col * TILE_SIZE  # Tính tọa độ x của ô đất
                    y = index_row * TILE_SIZE  # Tính tọa độ y của ô đất
                    WaterTile((x,y), choice(self.water_surfs), [self.all_sprites, self.water_sprites])  # Tạo đối tượng nước cho ô đất

    def remove_water(self):  # Hàm xóa nước khỏi tất cả các ô đất
    # destroy all water sprites
        for sprite in self.water_sprites.sprites():  # Duyệt qua tất cả các sprite nước
            sprite.kill()  # Xóa sprite nước khỏi game

    # clean up the grid
        for row in self.grid:  # Duyệt qua các hàng trong lưới đất
            for cell in row:  # Duyệt qua các cột trong mỗi hàng
                if 'W' in cell:  # Nếu ô đất có nước
                    cell.remove('W')  # Loại bỏ nước khỏi ô đất

    def check_watered(self, pos):  # Hàm kiểm tra ô đất tại vị trí pos có được tưới nước hay không
        x = pos[0] // TILE_SIZE  # Tính tọa độ x của ô đất
        y = pos[1] // TILE_SIZE  # Tính tọa độ y của ô đất
        cell = self.grid[y][x]  # Lấy ô đất tại vị trí (x, y)
        is_watered = 'W' in cell  # Kiểm tra nếu ô đất đã có nước
        return is_watered  # Trả về kết quả kiểm tra

    def plant_seed(self, target_pos, seed):  # Hàm trồng hạt giống vào vị trí target_pos
        for soil_sprite in self.soil_sprites.sprites():  # Duyệt qua tất cả các sprite đất
            if soil_sprite.rect.collidepoint(target_pos):  # Nếu ô đất va chạm với vị trí target_pos
                self.plant_sound.play()  # Phát âm thanh trồng cây

                x = soil_sprite.rect.x // TILE_SIZE  # Tính tọa độ x của ô đất
                y = soil_sprite.rect.y // TILE_SIZE  # Tính tọa độ y của ô đất

                if 'P' not in self.grid[y][x]:  # Nếu ô đất chưa có cây
                    self.grid[y][x].append('P')  # Đánh dấu ô đất đã trồng cây
                    Plant(seed, [self.all_sprites, self.plant_sprites, self.collision_sprites], soil_sprite, self.check_watered)  # Trồng cây mới

    def update_plants(self):  # Hàm cập nhật sự phát triển của các cây trồng
        for plant in self.plant_sprites.sprites():  # Duyệt qua tất cả các cây trồng
            plant.grow()  # Gọi hàm grow() để cây phát triển

    def create_soil_tiles(self):  # Hàm tạo các ô đất từ lưới đất
        self.soil_sprites.empty()  # Dọn sạch các sprite đất cũ
        for index_row, row in enumerate(self.grid):  # Duyệt qua các hàng trong lưới đất
            for index_col, cell in enumerate(row):  # Duyệt qua các cột trong mỗi hàng
                if 'X' in cell:  # Nếu ô đất có thể trồng cây

                # tile options 
                    t = 'X' in self.grid[index_row - 1][index_col]  # Kiểm tra ô đất phía trên
                    b = 'X' in self.grid[index_row + 1][index_col]  # Kiểm tra ô đất phía dưới
                    r = 'X' in row[index_col + 1]  # Kiểm tra ô đất bên phải
                    l = 'X' in row[index_col - 1]  # Kiểm tra ô đất bên trái

                    tile_type = 'o'  # Loại ô đất mặc định

                # all sides
                    if all((t,r,b,l)): tile_type = 'x'  # Nếu có đất ở tất cả các phía

                # horizontal tiles only
                    if l and not any((t,r,b)): tile_type = 'r'  # Nếu chỉ có đất bên trái
                    if r and not any((t,l,b)): tile_type = 'l'  # Nếu chỉ có đất bên phải
                    if r and l and not any((t,b)): tile_type = 'lr'  # Nếu có đất ở bên trái và bên phải

                # vertical only 
                    if t and not any((r,l,b)): tile_type = 'b'  # Nếu chỉ có đất phía trên
                    if b and not any((r,l,t)): tile_type = 't'  # Nếu chỉ có đất phía dưới
                    if b and t and not any((r,l)): tile_type = 'tb'  # Nếu có đất ở phía trên và phía dưới

                # corners 
                    if l and b and not any((t,r)): tile_type = 'tr'  # Nếu có đất ở phía dưới và bên trái
                    if r and b and not any((t,l)): tile_type = 'tl'  # Nếu có đất ở phía dưới và bên phải
                    if l and t and not any((b,r)): tile_type = 'br'  # Nếu có đất ở phía trên và bên trái
                    if r and t and not any((b,l)): tile_type = 'bl'  # Nếu có đất ở phía trên và bên phải

                # T shapes
                    if all((t,b,r)) and not l: tile_type = 'tbr'  # Nếu có đất ở phía trên, dưới, và bên phải
                    if all((t,b,l)) and not r: tile_type = 'tbl'  # Nếu có đất ở phía trên, dưới, và bên trái
                    if all((l,r,t)) and not b: tile_type = 'lrb'  # Nếu có đất ở bên trái, phải, và trên
                    if all((l,r,b)) and not t: tile_type = 'lrt'  # Nếu có đất ở bên trái, phải, và dưới

                    SoilTile(  # Tạo đối tượng SoilTile với các tham số đã xác định
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE),  # Vị trí của ô đất
                        surf = self.soil_surfs[tile_type],  # Hình ảnh ô đất
                        groups = [self.all_sprites, self.soil_sprites])  # Các nhóm sprite
