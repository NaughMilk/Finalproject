import pygame  # Nhập thư viện pygame cho lập trình game
from settings import *  # Nhập các cài đặt từ file settings.py
from player import Player  # Nhập lớp Player từ file player.py
from overlay import Overlay  # Nhập lớp Overlay từ file overlay.py
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle  # Nhập các sprite từ file sprites.py
from pytmx.util_pygame import load_pygame  # Nhập hàm load_pygame từ pytmx để tải bản đồ Tiled
from support import *  # Nhập các hỗ trợ từ file support.py
from transition import Transition  # Nhập lớp Transition từ file transition.py
from soil import SoilLayer  # Nhập lớp SoilLayer từ file soil.py
from sky import Rain, Sky  # Nhập các lớp Rain và Sky từ file sky.py
from random import randint  # Nhập hàm randint để tạo số ngẫu nhiên
from menu import Menu  # Nhập lớp Menu từ file menu.py


class Level:
    def __init__(self):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()  # Lấy đối tượng surface của cửa sổ hiển thị

        # Sprite groups
        self.all_sprites = CameraGroup()  # Nhóm tất cả sprite và camera
        self.collision_sprites = pygame.sprite.Group()  # Nhóm sprite va chạm
        self.tree_sprites = pygame.sprite.Group()  # Nhóm cây
        self.interaction_sprites = pygame.sprite.Group()  # Nhóm tương tác

        # Soil layer
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)  # Khởi tạo lớp đất
        self.setup()  # Gọi phương thức setup() để thiết lập ban đầu
        self.overlay = Overlay(self.player)  # Khởi tạo overlay (màn hình phụ)
        self.transition = Transition(self.reset, self.player)  # Khởi tạo transition (hiệu ứng chuyển cảnh)

        # Sky
        self.rain = Rain(self.all_sprites)  # Khởi tạo mưa
        self.raining = randint(0, 10) > 7  # Tạo mưa ngẫu nhiên
        self.soil_layer.raining = self.raining  # Cập nhật trạng thái mưa trong lớp đất
        self.sky = Sky()  # Khởi tạo bầu trời

        # Shop
        self.menu = Menu(self.player, self.toggle_shop)  # Khởi tạo menu cửa hàng
        self.shop_active = False  # Biến trạng thái cửa hàng

        # Music
        self.success = pygame.mixer.Sound('c:/Desktop/KHMT/s3 - import/s3 - import/audio/success.wav')  # Âm thanh thành công
        self.success.set_volume(0.3)  # Cài đặt âm lượng âm thanh thành công
        self.music = pygame.mixer.Sound('c:/Desktop/KHMT/s3 - import/s3 - import/audio/music.mp3')  # Âm nhạc nền
        self.music.play(loops=-1)  # Chạy nhạc nền liên tục

        # Day/Night and Weather
        self.time_of_day = "Day"  # Cài đặt thời gian ban đầu là ban ngày
        self.is_raining = False  # Cài đặt trạng thái mưa ban đầu

        # Danh sách nội dung
        self.facts = [  # Danh sách các sự kiện/câu nói trong game
            "Press H to view the game guide.",
            "You can change the weather with buttons in the left corner.",
            "Planting trees helps increase income quickly!",
            "Press S to open the shop.",
            "Rain will help trees grow faster.",
            "Take care of trees to harvest fruits!",
            "You can slept at night - just 'enter' the bed"
        ]
        self.current_fact = self.facts[0]  # Nội dung ban đầu được hiển thị
        self.fact_timer = pygame.time.get_ticks()  # Bộ đếm thời gian cho việc thay đổi nội dung

    def update_fact(self):
        """Cập nhật nội dung mỗi 10 giây."""
        current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại
        if current_time - self.fact_timer > 10000:  # Kiểm tra thời gian qua 10 giây
            self.fact_timer = current_time  # Cập nhật lại bộ đếm thời gian
            # Chuyển sang nội dung tiếp theo
            current_index = self.facts.index(self.current_fact)  # Lấy chỉ số của nội dung hiện tại
            next_index = (current_index + 1) % len(self.facts)  # Chuyển đến nội dung kế tiếp (lặp lại nếu hết)
            self.current_fact = self.facts[next_index]  # Cập nhật nội dung hiện tại

    def display_fact(self):
        """Display the current fact with white text and black outline."""
        font = pygame.font.Font('c:/Desktop/KHMT/s3 - import/s3 - import/font/LycheeSoda.ttf', 30)  # Tạo font chữ
    
    # Render the main text (white)
        fact_surface_main = font.render(self.current_fact, True, "White")  # Vẽ chữ chính màu trắng
    
    # Render the outline text (black)
        fact_surface_outline = font.render(self.current_fact, True, "Black")  # Vẽ viền chữ màu đen
        fact_rect = fact_surface_main.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() - 50))  # Định vị trí chữ

    # Draw the outline by placing black text around the white text
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Các vị trí offset để vẽ viền
        for dx, dy in offsets:
            outline_rect = fact_rect.move(dx, dy)  # Di chuyển chữ viền
            self.display_surface.blit(fact_surface_outline, outline_rect)  # Vẽ viền lên màn hình
    
    # Draw the main text (white) on top
        self.display_surface.blit(fact_surface_main, fact_rect)  # Vẽ chữ chính lên màn hình



    def setup(self):
        tmx_data = load_pygame('c:/Desktop/KHMT/s3 - import/s3 - import/data/map.tmx')  # Tải dữ liệu bản đồ từ file tmx

    # House
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:  # Lặp qua các lớp "HouseFloor" và "HouseFurnitureBottom"
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():  # Lấy thông tin các ô trong lớp
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])  # Vẽ các ô

        for layer in ['HouseWalls', 'HouseFurnitureTop']:  # Lặp qua các lớp "HouseWalls" và "HouseFurnitureTop"
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():  # Lấy thông tin các ô trong lớp
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)  # Vẽ các ô

    # Fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():  # Lặp qua các ô trong lớp "Fence"
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])  # Vẽ hàng rào

    # Water
        water_frames = import_folder('c:/Desktop/KHMT/s3 - import/s3 - import/graphics/water')  # Nhập các frame nước
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():  # Lặp qua các ô trong lớp "Water"
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)  # Vẽ nước

    # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):  # Lặp qua các đối tượng cây trong lớp "Trees"
            Tree(
                pos=(obj.x, obj.y),  # Vị trí cây
                surf=obj.image,  # Hình ảnh cây
                groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],  # Nhóm cây vào các nhóm sprite
                name=obj.name,  # Tên cây
                player_add=self.player_add,  # Gọi phương thức player_add khi thu hoạch
            )

    # Wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):  # Lặp qua các đối tượng hoa dại trong lớp "Decoration"
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])  # Vẽ hoa dại

    # Collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():  # Lặp qua các ô trong lớp "Collision"
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)  # Vẽ các ô va chạm

    # Player
        for obj in tmx_data.get_layer_by_name('Player'):  # Lặp qua các đối tượng trong lớp "Player"
            if obj.name == 'Start':  # Nếu đối tượng là "Start"
                self.player = Player(
                    pos=(obj.x, obj.y),  # Vị trí của người chơi
                    group=self.all_sprites,  # Nhóm người chơi
                    collision_sprites=self.collision_sprites,  # Nhóm va chạm
                    tree_sprites=self.tree_sprites,  # Nhóm cây
                    interaction=self.interaction_sprites,  # Nhóm tương tác
                    soil_layer=self.soil_layer,  # Lớp đất
                    toggle_shop=self.toggle_shop,  # Gọi phương thức toggle_shop khi mở cửa hàng
                )

            if obj.name == 'Bed':  # Nếu đối tượng là "Bed" (giường)
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)  # Tạo tương tác giường

            if obj.name == 'Trader':  # Nếu đối tượng là "Trader" (thương nhân)
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)  # Tạo tương tác với thương nhân

        Generic(
            pos=(0, 0),  # Vị trí đối tượng
            surf=pygame.image.load('c:/Desktop/KHMT/s3 - import/s3 - import/graphics/world/ground.png').convert_alpha(),  # Tải hình nền
            groups=self.all_sprites,  # Nhóm sprite
            z=LAYERS['ground'],  # Đặt lớp z cho đối tượng nền
        )

    def player_add(self, item):
        self.player.item_inventory[item] += 1  # Thêm vật phẩm vào kho của người chơi
        self.success.play()  # Phát âm thanh thành công khi thêm vật phẩm

    def toggle_shop(self):
        self.shop_active = not self.shop_active  # Bật/tắt cửa hàng

    def reset(self):
        """Reset game state after sleep."""
        # Plants
        self.soil_layer.update_plants()  # Cập nhật cây trồng

    # Soil
        self.soil_layer.remove_water()  # Xóa nước trong đất
        self.raining = randint(0, 10) > 7  # Tạo mưa ngẫu nhiên
        self.soil_layer.raining = self.raining  # Cập nhật trạng thái mưa trong đất
        if self.raining:
            self.soil_layer.water_all()  # Cung cấp nước cho tất cả cây trồng nếu có mưa

    # Apples on the trees
        for tree in self.tree_sprites.sprites():  # Lặp qua các cây
            for apple in tree.apple_sprites.sprites():  # Lặp qua các quả táo trên cây
                apple.kill()  # Xóa quả táo cũ
            tree.create_fruit()  # Tạo quả mới

    # Sky
        self.sky.start_color = [255, 255, 255]  # Đặt màu sắc bầu trời khi reset


    def set_time_of_day(self, time_of_day):
        """Change time of day (Day/Night)."""
        self.time_of_day = time_of_day  # Lưu thời gian trong ngày
        if time_of_day == "Day":
            self.sky.start_color = [255, 255, 255]  # Màu sáng cho ban ngày
        elif time_of_day == "Night":
            self.sky.start_color = [60, 80, 80]  # Màu tối cho ban đêm

    def toggle_weather(self):
        """Toggle rain."""
        self.is_raining = not self.is_raining  # Đảo trạng thái mưa
        self.raining = self.is_raining  # Đồng bộ trạng thái mưa
        self.soil_layer.raining = self.raining  # Cập nhật trạng thái mưa cho lớp đất
        if self.raining:
            self.rain.update()  # Hiển thị mưa nếu trời mưa

    def plant_collision(self):
        """Xử lý va chạm của cây với người chơi."""
        if self.soil_layer.plant_sprites:  # Kiểm tra nếu có cây trong lớp đất
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):  # Nếu cây có thể thu hoạch và va chạm với người chơi
                    self.player_add(plant.plant_type)  # Thêm vật phẩm vào inventory người chơi
                    plant.kill()  # Xóa cây
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, z=LAYERS['main'])  # Tạo hiệu ứng hạt giống
                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')  # Xóa cây khỏi lưới đất

    def run(self, dt):
        """Main game loop logic."""
    # Drawing logic
        self.display_surface.fill('black')  # Làm mới màn hình với màu đen
        self.all_sprites.custom_draw(self.player)  # Vẽ tất cả sprite lên màn hình

    # Updates
        if self.shop_active:
            self.menu.update()  # Cập nhật menu nếu cửa hàng mở
        else:
            self.all_sprites.update(dt)  # Cập nhật tất cả sprite nếu cửa hàng đóng
            self.plant_collision()  # Kiểm tra va chạm cây với người chơi

    # Weather
        self.overlay.display()  # Hiển thị lớp phủ thời tiết
        if self.raining and not self.shop_active:
            self.rain.update()  # Cập nhật mưa nếu trời mưa và không có cửa hàng mở
        self.sky.display(dt)  # Hiển thị bầu trời

    # Hiển thị nội dung ngắn
        self.update_fact()  # Cập nhật thông tin ngắn
        self.display_fact()  # Hiển thị thông tin ngắn

    # Transition overlay
        if self.player.sleep:
            self.transition.play()  # Phát hiệu ứng chuyển cảnh nếu người chơi đang ngủ

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()  # Lấy bề mặt hiển thị
        self.offset = pygame.math.Vector2()  # Khởi tạo offset camera

    def custom_draw(self, player):
        """Custom camera logic để theo dõi người chơi."""
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2  # Tính toán offset theo trục X
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2  # Tính toán offset theo trục Y

        for layer in LAYERS.values():  # Duyệt qua các lớp
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):  # Sắp xếp sprite theo chiều dọc
                if sprite.z == layer:  # Kiểm tra lớp sprite
                    offset_rect = sprite.rect.copy()  # Tạo bản sao của rect
                    offset_rect.center -= self.offset  # Áp dụng offset
                    self.display_surface.blit(sprite.image, offset_rect)  # Vẽ sprite lên màn hình
