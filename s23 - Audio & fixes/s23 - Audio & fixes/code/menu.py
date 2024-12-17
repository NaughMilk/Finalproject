import pygame
from settings import *
from timer import Timer

class Menu:
    def __init__(self, player, toggle_menu):
        # general setup
        self.player = player  # Lưu đối tượng người chơi để truy cập thông tin kho đồ và tiền
        self.toggle_menu = toggle_menu  # Hàm để mở/tắt menu
        self.display_surface = pygame.display.get_surface()  # Lấy bề mặt hiển thị (màn hình) của pygame
        self.font = pygame.font.Font('c:/Desktop/KHMT/s3 - import/s3 - import/font/LycheeSoda.ttf', 30)  # Chọn font cho menu

        # options
        self.width = 400  # Chiều rộng của menu
        self.space = 10  # Khoảng cách giữa các mục trong menu
        self.padding = 8  # Khoảng cách giữa văn bản và viền của từng mục

        # entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())  # Liệt kê tất cả vật phẩm và hạt giống của người chơi
        self.sell_border = len(self.player.item_inventory) - 1  # Xác định mốc để phân biệt vật phẩm bán và hạt giống mua
        self.setup()  # Gọi hàm setup để tạo các mục menu

        # movement
        self.index = 0  # Chỉ số mục hiện tại mà người chơi đang chọn
        self.timer = Timer(200)  # Khởi tạo một bộ đếm thời gian để tránh việc nhấn phím quá nhanh

    def display_money(self):
        """Hiển thị số tiền của người chơi"""
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')  # Tạo văn bản hiển thị số tiền
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))  # Đặt vị trí hiển thị ở giữa dưới màn hình

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10, 10), 0, 4)  # Vẽ nền trắng cho số tiền
        self.display_surface.blit(text_surf, text_rect)  # Vẽ số tiền lên màn hình

    def setup(self):
        """Thiết lập các mục trong menu"""
        self.text_surfs = []  # Danh sách các đối tượng văn bản của từng mục trong menu
        self.total_height = 0  # Tổng chiều cao của menu

        # Tạo văn bản cho mỗi mục và tính toán tổng chiều cao của menu
        for item in self.options:
            text_surf = self.font.render(item, False, 'Black')  # Render mỗi mục bằng font đã chọn
            self.text_surfs.append(text_surf)  # Thêm vào danh sách
            self.total_height += text_surf.get_height() + (self.padding * 2)  # Cộng thêm chiều cao của mục hiện tại

        self.total_height += (len(self.text_surfs) - 1) * self.space  # Cộng khoảng cách giữa các mục
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2  # Vị trí bắt đầu của menu ở giữa màn hình
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)  # Tạo hình chữ nhật bao quanh menu

        # buy / sell text surface
        self.buy_text = self.font.render('buy', False, 'Black')  # Tạo văn bản cho mục mua
        self.sell_text = self.font.render('sell', False, 'Black')  # Tạo văn bản cho mục bán

    def input(self):
        """Xử lý đầu vào của người chơi"""
        keys = pygame.key.get_pressed()  # Lấy trạng thái các phím
        self.timer.update()  # Cập nhật thời gian của bộ đếm

        if keys[pygame.K_ESCAPE]:  # Nếu nhấn ESC, đóng menu
            self.toggle_menu()

        if not self.timer.active:  # Nếu bộ đếm không hoạt động (tránh nhấn phím quá nhanh)
            if keys[pygame.K_UP]:  # Nếu nhấn phím mũi tên lên, chọn mục trước
                self.index -= 1
                self.timer.activate()  # Kích hoạt bộ đếm thời gian

            if keys[pygame.K_DOWN]:  # Nếu nhấn phím mũi tên xuống, chọn mục sau
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:  # Nếu nhấn phím Space, xác nhận chọn mục
                self.timer.activate()  # Kích hoạt bộ đếm thời gian

                current_item = self.options[self.index]  # Lấy mục người chơi chọn

                # Nếu mục là vật phẩm và người chơi có vật phẩm trong kho
                if self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1  # Giảm số lượng vật phẩm trong kho
                        self.player.money += SALE_PRICES[current_item]  # Tăng tiền cho người chơi

                # Nếu mục là hạt giống và người chơi có đủ tiền
                else:
                    seed_price = PURCHASE_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1  # Mua thêm hạt giống
                        self.player.money -= PURCHASE_PRICES[current_item]  # Giảm tiền của người chơi

        # Kiểm tra các giá trị hợp lệ cho mục hiện tại
        if self.index < 0:
            self.index = len(self.options) - 1  # Quay lại cuối danh sách nếu di chuyển lên quá đầu
        if self.index > len(self.options) - 1:
            self.index = 0  # Quay lại đầu danh sách nếu di chuyển xuống quá cuối

    def show_entry(self, text_surf, amount, top, selected):
        """Hiển thị từng mục trong menu"""
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))  # Vẽ nền cho mục
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)  # Vẽ nền trắng cho mục

        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))  # Vị trí văn bản
        self.display_surface.blit(text_surf, text_rect)  # Vẽ văn bản lên màn hình

        # Hiển thị số lượng sản phẩm (ví dụ: số lượng gỗ, quả táo)
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))  # Vị trí số lượng
        self.display_surface.blit(amount_surf, amount_rect)

        # Nếu mục đang được chọn, vẽ viền xung quanh
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            if self.index <= self.sell_border:  # Mục bán
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:  # Mục mua
                pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        """Cập nhật menu và hiển thị các mục trong menu"""
        self.input()  # Xử lý đầu vào của người chơi
        self.display_money()  # Hiển thị số tiền của người chơi

        # Hiển thị từng mục trong menu
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())  # Lấy danh sách các vật phẩm và hạt giống
            amount = amount_list[text_index]  # Số lượng của mỗi mục
            self.show_entry(text_surf, amount, top, self.index == text_index)  # Hiển thị mục và số lượng
