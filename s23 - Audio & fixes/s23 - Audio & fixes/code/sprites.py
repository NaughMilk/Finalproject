import pygame  # Thư viện hỗ trợ lập trình game
from settings import *  # Nhập các thiết lập từ tệp settings
from random import randint, choice  # Hàm random: randint để tạo số ngẫu nhiên, choice để chọn ngẫu nhiên phần tử từ danh sách
from timer import Timer  # Nhập lớp Timer (giả sử là lớp hỗ trợ tính thời gian)


class Generic(pygame.sprite.Sprite):  # Lớp cơ bản cho các đối tượng game, kế thừa từ pygame.sprite.Sprite
	def __init__(self, pos, surf, groups, z = LAYERS['main']):  # Khởi tạo lớp với vị trí, bề mặt, nhóm, và lớp đồ họa
		super().__init__(groups)  # Đăng ký đối tượng vào nhóm sprite
		self.image = surf  # Đặt hình ảnh của sprite
		self.rect = self.image.get_rect(topleft = pos)  # Tạo hình chữ nhật với góc trên cùng bên trái là 'pos'
		self.z = z  # Lớp đồ họa (ưu tiên vẽ)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)  # Thu nhỏ hitbox để phát hiện va chạm


class Interaction(Generic):  # Lớp dành cho các đối tượng tương tác, kế thừa từ `Generic`
	def __init__(self, pos, size, groups, name):
		surf = pygame.Surface(size)  # Tạo bề mặt với kích thước `size`
		super().__init__(pos, surf, groups)  # Gọi hàm khởi tạo lớp cha
		self.name = name  # Đặt tên cho đối tượng


class Water(Generic):  # Lớp dành cho đối tượng nước, kế thừa từ `Generic`
	def __init__(self, pos, frames, groups):
		self.frames = frames  # Lưu trữ các khung hình để tạo hoạt ảnh
		self.frame_index = 0  # Bắt đầu từ khung hình đầu tiên
		super().__init__(  # Gọi hàm khởi tạo lớp cha
				pos = pos, 
				surf = self.frames[self.frame_index],  # Khung hình ban đầu
				groups = groups, 
				z = LAYERS['water'])  # Lớp đồ họa là 'water'

	def animate(self,dt):  # Hàm tạo hoạt ảnh
		self.frame_index += 5 * dt  # Tăng chỉ số khung hình dựa trên thời gian
		if self.frame_index >= len(self.frames):  # Nếu vượt quá số khung hình, quay lại đầu
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]  # Cập nhật khung hình hiện tại

	def update(self,dt):  # Hàm cập nhật đối tượng
		self.animate(dt)  # Gọi hàm tạo hoạt ảnh


class WildFlower(Generic):  # Lớp dành cho hoa dại, kế thừa từ `Generic`
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)  # Gọi hàm khởi tạo lớp cha
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height * 0.9)  # Thu nhỏ hitbox theo kích thước hoa


class Particle(Generic):  # Lớp dành cho các hạt hiệu ứng, kế thừa từ `Generic`
	def __init__(self, pos, surf, groups, z, duration = 200):
		super().__init__(pos, surf, groups, z)  # Gọi hàm khởi tạo lớp cha
		self.start_time = pygame.time.get_ticks()  # Lấy thời điểm bắt đầu hiệu ứng
		self.duration = duration  # Thời lượng hiệu ứng

		# Tạo bề mặt trắng từ mặt nạ
		mask_surf = pygame.mask.from_surface(self.image)  # Tạo mặt nạ từ bề mặt hiện tại
		new_surf = mask_surf.to_surface()  # Chuyển mặt nạ thành bề mặt mới
		new_surf.set_colorkey((0,0,0))  # Xóa màu đen khỏi bề mặt
		self.image = new_surf  # Cập nhật hình ảnh

	def update(self,dt):  # Hàm cập nhật hiệu ứng
		current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại
		if current_time - self.start_time > self.duration:  # Nếu đã hết thời gian hiệu ứng
			self.kill()  # Xóa đối tượng khỏi game


class Tree(Generic):  # Lớp Tree kế thừa từ lớp Generic, đại diện cho cây trong game
	def __init__(self, pos, surf, groups, name, player_add):
		super().__init__(pos, surf, groups)  # Gọi hàm khởi tạo của lớp cha `Generic` để thiết lập vị trí, bề mặt và nhóm

		# Thuộc tính cây
		self.health = 5  # Sức khỏe của cây (tạo ra 5 đơn vị sức khỏe cho cây)
		self.alive = True  # Cây còn sống hay không, mặc định là sống
		stump_path = f'c:/Desktop/KHMT/s3 - import/s3 - import/graphics/stumps/{"small" if name == "Small" else "large"}.png'  
		# Đường dẫn đến hình ảnh gốc cây, chọn theo kích thước của cây (nhỏ hoặc lớn)
		self.stump_surf = pygame.image.load(stump_path).convert_alpha()  # Tải hình ảnh gốc cây và chuyển đổi sang định dạng hỗ trợ alpha (trong suốt)

		# Quả táo
		self.apple_surf = pygame.image.load('c:/Desktop/KHMT/s3 - import/s3 - import/graphics/fruit/apple.png')  
		# Tải hình ảnh quả táo
		self.apple_pos = APPLE_POS[name]  # Lấy vị trí của các quả táo dựa vào tên cây (Small hoặc Large)
		self.apple_sprites = pygame.sprite.Group()  # Nhóm chứa các quả táo sẽ được tạo ra
		self.create_fruit()  # Gọi hàm để tạo ra các quả táo

		self.player_add = player_add  # Hàm để thêm tài nguyên cho người chơi (gỗ hoặc táo)

		# Âm thanh
		self.axe_sound = pygame.mixer.Sound('c:/Desktop/KHMT/s3 - import/s3 - import/audio/axe.mp3')  
		# Tải âm thanh khi chặt cây

	def damage(self):  # Hàm xử lý khi cây bị chặt
		self.health -= 1  # Giảm sức khỏe của cây mỗi khi bị chặt
		self.axe_sound.play()  # Phát âm thanh khi chặt cây

		# Loại bỏ một quả táo
		if len(self.apple_sprites.sprites()) > 0:  # Kiểm tra nếu có quả táo nào trên cây
			random_apple = choice(self.apple_sprites.sprites())  # Chọn ngẫu nhiên một quả táo
			Particle(  # Tạo một hạt hiệu ứng tại vị trí của quả táo
				pos = random_apple.rect.topleft,  # Vị trí của quả táo
				surf = random_apple.image,  # Hình ảnh của quả táo
				groups = self.groups()[0],  # Nhóm sprite để quản lý
				z = LAYERS['fruit'])  # Lớp đồ họa cho quả táo
			self.player_add('apple')  # Thêm táo vào tài nguyên của người chơi
			random_apple.kill()  # Xóa quả táo khỏi nhóm và khỏi game

	def check_death(self):  # Kiểm tra xem cây có chết không (sức khỏe <= 0)
		if self.health <= 0:
			# Tạo một hạt hiệu ứng khi cây chết
			Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS['fruit'], 300)
			self.image = self.stump_surf  # Đổi hình ảnh của cây thành gốc cây
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)  # Cập nhật lại vị trí của gốc cây
			self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)  # Tạo hitbox mới cho gốc cây
			self.alive = False  # Đánh dấu cây đã chết
			self.player_add('wood')  # Thêm gỗ vào tài nguyên của người chơi

	def update(self,dt):  # Hàm cập nhật trạng thái của cây
		if self.alive:  # Nếu cây còn sống
			self.check_death()  # Kiểm tra xem cây có chết không

	def create_fruit(self):  # Hàm tạo quả táo
		for pos in self.apple_pos:  # Lặp qua tất cả các vị trí có thể có quả táo
			if randint(0,10) < 2:  # Với xác suất 20%, tạo quả táo
				x = pos[0] + self.rect.left  # Tính toán vị trí x của quả táo
				y = pos[1] + self.rect.top  # Tính toán vị trí y của quả táo
				Generic(  # Tạo một đối tượng Generic (quả táo)
					pos = (x,y),  # Vị trí của quả táo
					surf = self.apple_surf,  # Hình ảnh quả táo
					groups = [self.apple_sprites,self.groups()[0]],  # Nhóm chứa quả táo
					z = LAYERS['fruit'])  # Lớp đồ họa cho quả táo
