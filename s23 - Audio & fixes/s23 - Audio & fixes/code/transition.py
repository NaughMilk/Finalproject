import pygame  # Nhập thư viện pygame
from settings import *  # Nhập các thiết lập từ file settings.py

class Transition:
	def __init__(self, reset, player):
		
		# setup
		self.display_surface = pygame.display.get_surface()  # Lấy đối tượng surface của cửa sổ hiển thị
		self.reset = reset  # Gán hàm reset cho thuộc tính của lớp
		self.player = player  # Gán đối tượng người chơi

		# overlay image
		self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Tạo một surface với kích thước bằng màn hình
		self.color = 255  # Giá trị màu ban đầu (màu trắng)
		self.speed = -2  # Tốc độ thay đổi màu

	def play(self):
		self.color += self.speed  # Thay đổi giá trị màu dựa vào tốc độ
		if self.color <= 0:  # Nếu giá trị màu nhỏ hơn hoặc bằng 0
			self.speed *= -1  # Đảo ngược tốc độ
			self.color = 0  # Đặt giá trị màu bằng 0
			self.reset()  # Gọi hàm reset
		if self.color > 255:  # Nếu giá trị màu lớn hơn 255
			self.color = 255  # Đặt giá trị màu bằng 255
			self.player.sleep = False  # Đặt trạng thái ngủ của người chơi thành False
			self.speed = -2  # Đặt lại tốc độ thành -2

		self.image.fill((self.color, self.color, self.color))  # Điền màu cho surface
		self.display_surface.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Vẽ surface lên màn hình với hiệu ứng đặc biệt
