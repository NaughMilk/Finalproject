import pygame  # Nhập thư viện pygame để sử dụng các chức năng đồ họa
from settings import *  # Nhập các cài đặt từ module settings
from support import import_folder  # Nhập hàm import_folder từ module support
from sprites import Generic  # Nhập lớp Generic từ module sprites
from random import randint, choice  # Nhập các hàm randint và choice từ module random

class Sky:
    def __init__(self):  # Hàm khởi tạo của lớp Sky
        self.display_surface = pygame.display.get_surface()  # Lấy bề mặt hiển thị hiện tại của pygame
        self.full_surf = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))  # Tạo một surface đầy đủ có kích thước màn hình
        self.start_color = [255,255,255]  # Màu bắt đầu của bầu trời (màu trắng)
        self.end_color = (38,101,189)  # Màu kết thúc của bầu trời (màu xanh dương)

    def display(self, dt):  # Hàm hiển thị bầu trời
        for index, value in enumerate(self.end_color):  # Duyệt qua từng giá trị màu kết thúc
            if self.start_color[index] > value:  # Nếu màu bắt đầu lớn hơn màu kết thúc
                self.start_color[index] -= 2 * dt  # Giảm màu bắt đầu theo thời gian (dt)

        self.full_surf.fill(self.start_color)  # Làm đầy surface với màu bắt đầu
        self.display_surface.blit(self.full_surf, (0,0), special_flags = pygame.BLEND_RGBA_MULT)  # Vẽ bầu trời lên bề mặt hiển thị

class Drop(Generic):
    def __init__(self, surf, pos, moving, groups, z):  # Khởi tạo rơi giọt nước
        super().__init__(pos, surf, groups, z)  # Khởi tạo lớp cha Generic
        self.lifetime = randint(400,500)  # Thời gian sống ngẫu nhiên của giọt nước (400-500ms)
        self.start_time = pygame.time.get_ticks()  # Lấy thời gian bắt đầu từ lúc pygame bắt đầu chạy

        # Moving setup
        self.moving = moving  # Kiểm tra xem giọt nước có chuyển động không
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)  # Khởi tạo vị trí giọt nước
            self.direction = pygame.math.Vector2(-2,4)  # Hướng di chuyển của giọt nước
            self.speed = randint(200,250)  # Tốc độ ngẫu nhiên của giọt nước

    def update(self, dt):  # Cập nhật vị trí giọt nước
        if self.moving:  # Nếu giọt nước đang di chuyển
            self.pos += self.direction * self.speed * dt  # Cập nhật vị trí giọt nước
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))  # Cập nhật vị trí của hình chữ nhật chứa giọt nước

        # Kiểm tra thời gian sống
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:  # Nếu thời gian sống đã hết
            self.kill()  # Xóa giọt nước

class Rain:
    def __init__(self, all_sprites):  # Khởi tạo lớp Rain
        self.all_sprites = all_sprites  # Danh sách tất cả các sprite
        self.rain_drops = import_folder('c:/Desktop/KHMT/s3 - import/s3 - import/graphics/rain/drops/')  # Nhập các hình ảnh giọt nước
        self.rain_floor = import_folder('c:/Desktop/KHMT/s3 - import/s3 - import/graphics/rain/floor/')  # Nhập các hình ảnh mặt đất khi giọt nước rơi xuống
        self.floor_w, self.floor_h = pygame.image.load('c:/Desktop/KHMT/s3 - import/s3 - import/graphics/world/ground.png').get_size()  # Lấy kích thước mặt đất

    def create_floor(self):  # Tạo mặt đất cho giọt nước rơi
        Drop(  # Tạo giọt nước rơi xuống đất
            surf = choice(self.rain_floor),  # Chọn ngẫu nhiên một hình ảnh mặt đất
            pos = (randint(0,self.floor_w),randint(0,self.floor_h)),  # Vị trí ngẫu nhiên trên mặt đất
            moving = False,  # Giọt nước không di chuyển
            groups = self.all_sprites,  # Thêm vào nhóm sprite
            z = LAYERS['rain floor'])  # Đặt lớp z cho giọt nước

    def create_drops(self):  # Tạo giọt nước đang rơi
        Drop(  # Tạo giọt nước
            surf = choice(self.rain_drops),  # Chọn ngẫu nhiên một hình ảnh giọt nước
            pos = (randint(0,self.floor_w),randint(0,self.floor_h)),  # Vị trí ngẫu nhiên trên màn hình
            moving = True,  # Giọt nước sẽ di chuyển
            groups = self.all_sprites,  # Thêm vào nhóm sprite
            z = LAYERS['rain drops'])  # Đặt lớp z cho giọt nước

    def update(self):  # Cập nhật quá trình tạo giọt nước
        self.create_floor()  # Tạo mặt đất cho giọt nước
        self.create_drops()  # Tạo các giọt nước đang rơi