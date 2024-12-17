import pygame  # Nhập thư viện pygame để sử dụng các chức năng đồ họa
from settings import *  # Nhập các cài đặt từ module settings

class Overlay:  # Lớp Overlay hiển thị các công cụ và hạt giống của người chơi
	def __init__(self, player):  # Khởi tạo lớp Overlay với đối tượng player

		# general setup
		self.display_surface = pygame.display.get_surface()  # Lấy bề mặt hiển thị hiện tại của pygame
		self.player = player  # Lưu đối tượng người chơi

		# imports
		overlay_path = 'c:/Desktop/KHMT/s3 - import/s3 - import/graphics/overlay/'  # Đường dẫn tới thư mục overlay
		# Tạo một dictionary chứa các hình ảnh công cụ, mỗi công cụ có một hình ảnh tương ứng
		self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}  
		# Tạo một dictionary chứa các hình ảnh hạt giống, mỗi hạt giống có một hình ảnh tương ứng
		self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}  

	def display(self):  # Hàm hiển thị các công cụ và hạt giống

		# tool
		tool_surf = self.tools_surf[self.player.selected_tool]  # Lấy hình ảnh công cụ đã chọn
		tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])  # Lấy vị trí công cụ theo định nghĩa trong OVERLAY_POSITIONS
		self.display_surface.blit(tool_surf, tool_rect)  # Vẽ công cụ lên màn hình

		# seeds
		seed_surf = self.seeds_surf[self.player.selected_seed]  # Lấy hình ảnh hạt giống đã chọn
		seed_rect = seed_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])  # Lấy vị trí hạt giống theo định nghĩa trong OVERLAY_POSITIONS
		self.display_surface.blit(seed_surf, seed_rect)  # Vẽ hạt giống lên màn hình
