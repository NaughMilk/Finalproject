import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop):
        super().__init__(group)

        self.import_assets()  # Import tài nguyên (hình ảnh động) cho nhân vật
        self.status = 'down_idle'  # Mặc định trạng thái ban đầu của nhân vật là đứng yên nhìn xuống
        self.frame_index = 0  # Chỉ số khung hình hiện tại (được sử dụng để hiển thị hoạt ảnh)

        # general setup
        self.image = self.animations[self.status][self.frame_index]  # Lấy hình ảnh từ bộ hoạt ảnh theo trạng thái và chỉ số khung hình
        self.rect = self.image.get_rect(center = pos)  # Tạo hình chữ nhật của nhân vật, đặt ở vị trí ban đầu
        self.z = LAYERS['main']  # Thiết lập thứ tự lớp của nhân vật để hiển thị đúng vị trí

        # movement attributes
        self.direction = pygame.math.Vector2()  # Định nghĩa vector chỉ hướng của nhân vật
        self.pos = pygame.math.Vector2(self.rect.center)  # Vị trí trung tâm của nhân vật
        self.speed = 200  # Tốc độ di chuyển của nhân vật

        # collision
        self.hitbox = self.rect.copy().inflate((-126,-70))  # Tạo một hitbox nhỏ hơn hình chữ nhật của nhân vật
        self.collision_sprites = collision_sprites  # Các đối tượng va chạm mà nhân vật có thể gặp phải

        # timers 
        self.timers = {
            'tool use': Timer(350,self.use_tool),  # Bộ đếm thời gian cho việc sử dụng công cụ (350ms)
            'tool switch': Timer(200),  # Bộ đếm thời gian cho việc chuyển công cụ (200ms)
            'seed use': Timer(350,self.use_seed),  # Bộ đếm thời gian cho việc sử dụng hạt giống (350ms)
            'seed switch': Timer(200),  # Bộ đếm thời gian cho việc chuyển hạt giống (200ms)
        }

        # tools 
        self.tools = ['hoe','axe','water']  # Các công cụ có sẵn mà nhân vật có thể sử dụng
        self.tool_index = 0  # Chỉ số công cụ đang được chọn
        self.selected_tool = self.tools[self.tool_index]  # Công cụ được chọn hiện tại

        # seeds 
        self.seeds = ['corn', 'tomato']  # Các loại hạt giống có sẵn
        self.seed_index = 0  # Chỉ số hạt giống đang được chọn
        self.selected_seed = self.seeds[self.seed_index]  # Hạt giống được chọn hiện tại

        # inventory
        self.item_inventory = {
            'wood':   20,  # Số lượng gỗ
            'apple':  20,  # Số lượng táo
            'corn':   20,  # Số lượng bắp
            'tomato': 20  # Số lượng cà chua
        }
        self.seed_inventory = {
            'corn': 5,  # Số lượng hạt giống bắp
            'tomato': 5  # Số lượng hạt giống cà chua
        }
        self.money = 200  # Số tiền trong túi

        # interaction
        self.tree_sprites = tree_sprites  # Các cây trong trò chơi mà nhân vật có thể tương tác
        self.interaction = interaction  # Thông tin về các tương tác khác trong trò chơi
        self.sleep = False  # Trạng thái ngủ của nhân vật (mặc định là không ngủ)
        self.soil_layer = soil_layer  # Lớp đất mà nhân vật có thể tương tác với
        self.toggle_shop = toggle_shop  # Biến để bật/tắt cửa hàng

        # sound
        self.watering = pygame.mixer.Sound('c:/Desktop/KHMT/s3 - import/s3 - import/audio/water.mp3')  # Âm thanh tưới cây
        self.watering.set_volume(0.2)  # Đặt âm lượng cho âm thanh tưới cây

    def use_tool(self):
        if self.selected_tool == 'hoe':  # Nếu công cụ chọn là cuốc
            self.soil_layer.get_hit(self.target_pos)  # Tác động lên đất (cày đất)
        
        if self.selected_tool == 'axe':  # Nếu công cụ chọn là rìu
            for tree in self.tree_sprites.sprites():  # Duyệt qua các cây trong trò chơi
                if tree.rect.collidepoint(self.target_pos):  # Kiểm tra nếu rìu va chạm với cây
                    tree.damage()  # Gây sát thương cho cây (chặt cây)
        
        if self.selected_tool == 'water':  # Nếu công cụ chọn là vòi tưới
            self.soil_layer.water(self.target_pos)  # Tưới cây ở vị trí target
            self.watering.play()  # Phát âm thanh tưới cây

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]  # Tính toán vị trí mục tiêu dựa trên trạng thái hiện tại của nhân vật

    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0:  # Kiểm tra nếu còn hạt giống
            self.soil_layer.plant_seed(self.target_pos, self.selected_seed)  # Cấy hạt giống vào đất
            self.seed_inventory[self.selected_seed] -= 1  # Giảm số lượng hạt giống đã sử dụng

    def import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],  # Khởi tạo từ điển chứa các danh sách hoạt ảnh cho các hướng
                           'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
                           'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
                           'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
                           'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

        for animation in self.animations.keys():  # Duyệt qua các hoạt ảnh có sẵn
            full_path = 'c:/Desktop/KHMT/s3 - import/s3 - import/graphics/character/' + animation  # Tạo đường dẫn đầy đủ đến thư mục chứa hình ảnh hoạt ảnh
            self.animations[animation] = import_folder(full_path)  # Nhập các hình ảnh từ thư mục đã chỉ định và lưu vào từ điển


    def animate(self, dt):
        self.frame_index += 4 * dt  # Tăng chỉ số khung hình, tốc độ thay đổi khung hình phụ thuộc vào thời gian (dt)
        if self.frame_index >= len(self.animations[self.status]):  # Kiểm tra nếu chỉ số khung hình vượt qua số lượng khung hình trong hoạt ảnh
            self.frame_index = 0  # Nếu vượt quá, reset lại chỉ số khung hình về 0

        self.image = self.animations[self.status][int(self.frame_index)]  # Lấy khung hình từ bộ hoạt ảnh theo trạng thái và chỉ số khung hình

    def input(self):
        keys = pygame.key.get_pressed()  # Lấy trạng thái của tất cả các phím được nhấn

        if not self.timers['tool use'].active and not self.sleep:  # Kiểm tra nếu không có công cụ nào đang được sử dụng và nhân vật không ngủ
    # directions 
            if keys[pygame.K_UP]:  # Nếu phím mũi tên lên được nhấn
                self.direction.y = -1  # Di chuyển nhân vật lên
                self.status = 'up'  # Cập nhật trạng thái là "up"
            elif keys[pygame.K_DOWN]:  # Nếu phím mũi tên xuống được nhấn
                self.direction.y = 1  # Di chuyển nhân vật xuống
                self.status = 'down'  # Cập nhật trạng thái là "down"
            else:
                self.direction.y = 0  # Nếu không có phím mũi tên nào được nhấn, không di chuyển theo chiều dọc

            if keys[pygame.K_RIGHT]:  # Nếu phím mũi tên phải được nhấn
                self.direction.x = 1  # Di chuyển nhân vật sang phải
                self.status = 'right'  # Cập nhật trạng thái là "right"
            elif keys[pygame.K_LEFT]:  # Nếu phím mũi tên trái được nhấn
                self.direction.x = -1  # Di chuyển nhân vật sang trái
                self.status = 'left'  # Cập nhật trạng thái là "left"
            else:
                self.direction.x = 0  # Nếu không có phím mũi tên nào được nhấn, không di chuyển theo chiều ngang

            # tool use
            if keys[pygame.K_SPACE]:  # Nếu phím cách (SPACE) được nhấn
                self.timers['tool use'].activate()  # Kích hoạt bộ đếm thời gian cho việc sử dụng công cụ
                self.direction = pygame.math.Vector2()  # Reset lại hướng di chuyển
                self.frame_index = 0  # Reset lại chỉ số khung hình

        # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:  # Nếu phím Q được nhấn và bộ đếm thời gian chuyển công cụ không hoạt động
                self.timers['tool switch'].activate()  # Kích hoạt bộ đếm thời gian chuyển công cụ
                self.tool_index += 1  # Chuyển sang công cụ tiếp theo
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0  # Nếu vượt qua danh sách công cụ, quay lại công cụ đầu tiên
                self.selected_tool = self.tools[self.tool_index]  # Cập nhật công cụ được chọn

        # seed use
            if keys[pygame.K_LCTRL]:  # Nếu phím CTRL trái được nhấn
                self.timers['seed use'].activate()  # Kích hoạt bộ đếm thời gian cho việc sử dụng hạt giống
                self.direction = pygame.math.Vector2()  # Reset lại hướng di chuyển
                self.frame_index = 0  # Reset lại chỉ số khung hình

        # change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:  # Nếu phím E được nhấn và bộ đếm thời gian chuyển hạt giống không hoạt động
                self.timers['seed switch'].activate()  # Kích hoạt bộ đếm thời gian chuyển hạt giống
                self.seed_index += 1  # Chuyển sang hạt giống tiếp theo
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0  # Nếu vượt qua danh sách hạt giống, quay lại hạt giống đầu tiên
                self.selected_seed = self.seeds[self.seed_index]  # Cập nhật hạt giống được chọn

            if keys[pygame.K_RETURN]:  # Nếu phím Enter được nhấn
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)  # Kiểm tra va chạm với các đối tượng có thể tương tác
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':  # Nếu va chạm với đối tượng "Trader" (người bán)
                        self.toggle_shop()  # Mở cửa hàng
                    else:
                        self.status = 'left_idle'  # Cập nhật trạng thái là "left_idle"
                        self.sleep = True  # Đặt trạng thái ngủ thành True

    def get_status(self):
    # idle
        if self.direction.magnitude() == 0:  # Nếu không có hướng di chuyển (magnitude bằng 0)
            self.status = self.status.split('_')[0] + '_idle'  # Cập nhật trạng thái thành "idle" (đứng yên)

    # tool use
        if self.timers['tool use'].active:  # Nếu công cụ đang được sử dụng
            self.status = self.status.split('_')[0] + '_' + self.selected_tool  # Cập nhật trạng thái thành công cụ đang được sử dụng

    def update_timers(self):
        for timer in self.timers.values():  # Duyệt qua tất cả các bộ đếm thời gian
            timer.update()  # Cập nhật các bộ đếm thời gian

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():  # Duyệt qua tất cả các đối tượng va chạm
            if hasattr(sprite, 'hitbox'):  # Kiểm tra nếu đối tượng có thuộc tính 'hitbox'
                if sprite.hitbox.colliderect(self.hitbox):  # Kiểm tra nếu hitbox của đối tượng va chạm với hitbox của nhân vật
                    if direction == 'horizontal':  # Nếu va chạm theo chiều ngang
                        if self.direction.x > 0:  # Nếu di chuyển sang phải
                            self.hitbox.right = sprite.hitbox.left  # Đặt hitbox nhân vật chạm vào hitbox của đối tượng
                        if self.direction.x < 0:  # Nếu di chuyển sang trái
                            self.hitbox.left = sprite.hitbox.right  # Đặt hitbox nhân vật chạm vào hitbox của đối tượng
                        self.rect.centerx = self.hitbox.centerx  # Cập nhật vị trí của nhân vật theo hitbox
                        self.pos.x = self.hitbox.centerx  # Cập nhật vị trí x của nhân vật

                    if direction == 'vertical':  # Nếu va chạm theo chiều dọc
                        if self.direction.y > 0:  # Nếu di chuyển xuống
                            self.hitbox.bottom = sprite.hitbox.top  # Đặt hitbox nhân vật chạm vào hitbox của đối tượng
                        if self.direction.y < 0:  # Nếu di chuyển lên
                            self.hitbox.top = sprite.hitbox.bottom  # Đặt hitbox nhân vật chạm vào hitbox của đối tượng
                        self.rect.centery = self.hitbox.centery  # Cập nhật vị trí của nhân vật theo hitbox
                        self.pos.y = self.hitbox.centery  # Cập nhật vị trí y của nhân vật

    def move(self, dt):
    # normalizing a vector 
        if self.direction.magnitude() > 0:  # Nếu có hướng di chuyển
            self.direction = self.direction.normalize()  # Chuẩn hóa vector (đảm bảo tốc độ di chuyển không thay đổi)

    # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt  # Di chuyển theo chiều ngang
        self.hitbox.centerx = round(self.pos.x)  # Cập nhật vị trí hitbox
        self.rect.centerx = self.hitbox.centerx  # Cập nhật vị trí của nhân vật
        self.collision('horizontal')  # Kiểm tra va chạm theo chiều ngang

    # vertical movement
        self.pos.y += self.direction.y * self.speed * dt  # Di chuyển theo chiều dọc
        self.hitbox.centery = round(self.pos.y)  # Cập nhật vị trí hitbox
        self.rect.centery = self.hitbox.centery  # Cập nhật vị trí của nhân vật
        self.collision('vertical')  # Kiểm tra va chạm theo chiều dọc

    def update(self, dt):
        self.input()  # Xử lý đầu vào từ người chơi (di chuyển, sử dụng công cụ, v.v.)
        self.get_status()  # Cập nhật trạng thái của nhân vật
        self.update_timers()  # Cập nhật các bộ đếm thời gian
        self.get_target_pos()  # Tính toán vị trí mục tiêu để tương tác với công cụ

        self.move(dt)  # Di chuyển nhân vật
        self.animate(dt)  # Cập nhật hoạt ảnh của nhân vật
