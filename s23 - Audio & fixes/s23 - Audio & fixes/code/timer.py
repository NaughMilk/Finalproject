import pygame  # Nhập thư viện pygame để sử dụng các chức năng đồ họa và thời gian

class Timer:
    def __init__(self, duration, func = None):  # Khởi tạo hàm Timer với thời gian chạy (duration) và hàm callback (func) mặc định là None
        self.duration = duration  # Thời gian chạy của bộ đếm (tính bằng ms)
        self.func = func  # Hàm callback sẽ được gọi khi hết thời gian
        self.start_time = 0  # Thời gian bắt đầu (mặc định là 0)
        self.active = False  # Trạng thái của bộ đếm, mặc định là không hoạt động

    def activate(self):  # Kích hoạt bộ đếm
        self.active = True  # Đặt trạng thái bộ đếm thành 'hoạt động'
        self.start_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại (tính bằng mili giây kể từ khi pygame bắt đầu)

    def deactivate(self):  # Tắt bộ đếm
        self.active = False  # Đặt trạng thái bộ đếm thành 'không hoạt động'
        self.start_time = 0  # Đặt thời gian bắt đầu về 0

    def update(self):  # Cập nhật bộ đếm và kiểm tra xem đã hết thời gian chưa
        current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại
        if current_time - self.start_time >= self.duration:  # Kiểm tra xem đã hết thời gian chưa
            if self.func and self.start_time != 0:  # Nếu có hàm callback và thời gian bắt đầu khác 0
                self.func()  # Gọi hàm callback
            self.deactivate()  # Tắt bộ đếm
