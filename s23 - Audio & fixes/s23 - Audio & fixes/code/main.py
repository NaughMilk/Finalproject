import pygame  # Thư viện Pygame cho việc phát triển game
import sys  # Thư viện hệ thống
from settings import *  # Import các cài đặt từ file settings
from level import Level  # Import lớp Level từ file level

class Game:  # Định nghĩa lớp Game
    def __init__(self):  # Hàm khởi tạo của lớp Game
        pygame.init()  # Khởi tạo Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Tạo cửa sổ game với kích thước SCREEN_WIDTH x SCREEN_HEIGHT
        pygame.display.set_caption('THE WONDERLAND')  # Đặt tiêu đề cửa sổ game
        self.clock = pygame.time.Clock()  # Tạo đối tượng Clock để điều khiển tốc độ khung hình
        self.level = Level()  # Khởi tạo đối tượng Level
        self.scroll_offset = 0  # Biến điều chỉnh độ cuộn màn hình
        self.game_state = "menu"  # Trạng thái game ban đầu là menu
        self.show_story = False  # Biến kiểm tra xem có hiển thị câu chuyện không
        self.main_menu = True  # Biến kiểm tra xem đang ở màn hình menu chính hay không

        # Load các hình ảnh nút bấm
        self.button_images = {
            "Day": pygame.image.load("c:/Desktop/KHMT/s3 - import/s3 - import/bonus/day.png").convert_alpha(),
            "Night": pygame.image.load("c:/Desktop/KHMT/s3 - import/s3 - import/bonus/night.png").convert_alpha(),
            "Rain": pygame.image.load("c:/Desktop/KHMT/s3 - import/s3 - import/bonus/rain.png").convert_alpha(),
            "Story": pygame.image.load("c:/Desktop/KHMT/s3 - import/s3 - import/bonus/story.png").convert_alpha()  # Nút Story
        }

        # Vị trí các nút bấm trên màn hình
        self.button_positions = {
            "Day": self.button_images["Day"].get_rect(topleft=(10, 50)),  # Nút Day
            "Night": self.button_images["Night"].get_rect(topleft=(10, 120)),  # Nút Night
            "Rain": self.button_images["Rain"].get_rect(topleft=(10, 190)),  # Nút Rain
            "Story": self.button_images["Story"].get_rect(topleft=(SCREEN_WIDTH - 110, SCREEN_HEIGHT - 60))  # Nút Story
        }

        # Trạng thái của game
        self.show_help = False  # Màn hình hướng dẫn
        self.show_shop = False  # Màn hình cửa hàng

    def draw_main_menu(self):  # Hàm vẽ màn hình menu chính
        """Display the main menu with a background and 'Play' button."""
        # Hiển thị background của menu chính
        background = pygame.image.load('c:/Desktop/KHMT/s3 - import/s3 - import/bonus/main_menu.png').convert()  # Load hình nền
        background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))  # Điều chỉnh kích thước hình nền
        self.screen.blit(background, (0, 0))  # Vẽ hình nền lên màn hình

        # Hiển thị nút 'Play'
        play_button_width, play_button_height = 200, 60  # Kích thước nút Play
        play_button_x = (self.screen.get_width() - play_button_width) // 2  # Vị trí x của nút Play
        play_button_y = (self.screen.get_height() - play_button_height) // 2  # Vị trí y của nút Play
        play_button = pygame.Rect(play_button_x, play_button_y, play_button_width, play_button_height)  # Tạo hình chữ nhật cho nút Play
        pygame.draw.rect(self.screen, (255, 255, 255), play_button, border_radius=10)  # Vẽ nút Play với nền trắng
        pygame.draw.rect(self.screen, (0, 0, 0), play_button, 3, border_radius=10)  # Vẽ viền đen cho nút Play

        # Hiển thị chữ 'Play' trên nút
        font = pygame.font.Font(None, 50)  # Tạo font chữ với kích thước 50
        text_surface = font.render("Play", True, (0, 0, 0))  # Tạo mặt phẳng chữ 'Play' với màu đen
        text_rect = text_surface.get_rect(center=play_button.center)  # Đặt vị trí của chữ 'Play' ở giữa nút
        self.screen.blit(text_surface, text_rect)  # Vẽ chữ lên màn hình

        return play_button  # Trả về đối tượng nút Play



    def handle_main_menu_events(self, event):
        """Handle events in the main menu."""  # Xử lý sự kiện trong menu chính
        if event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra nếu người dùng nhấn chuột
            mouse_pos = event.pos  # Lấy vị trí chuột
            play_button = self.draw_main_menu()  # Vẽ menu chính và lấy nút Play
            if play_button.collidepoint(mouse_pos):  # Kiểm tra nếu nhấn vào nút Play
                self.game_state = "playing"  # Chuyển sang trạng thái chơi game


    def draw_menu(self):
        """Draw the menu with white backgrounds and images."""  # Vẽ menu với nền trắng và hình ảnh
        for label, rect in self.button_positions.items():  # Lặp qua các nút bấm
            # Draw white background
            background_rect = pygame.Rect(
                rect.left - 5, rect.top - 5, rect.width + 10, rect.height + 10  # Vị trí và kích thước của nền
            )
            pygame.draw.rect(self.screen, (255, 255, 255), background_rect, border_radius=10)  # Vẽ nền trắng
            pygame.draw.rect(self.screen, (0, 0, 0), background_rect, 2)  # Vẽ viền đen cho nền
            # Draw the icon
            self.screen.blit(self.button_images[label], rect)  # Vẽ biểu tượng của nút bấm


    def draw_status(self):
        """Display the current time of day and weather with white text and black outline."""  # Hiển thị thời gian và thời tiết
        font = pygame.font.Font('c:/Desktop/KHMT/s3 - import/s3 - import/font/LycheeSoda.ttf', 30)  # Tạo font chữ
        status_text = f"Time: {self.level.time_of_day} | Weather: {'Rainy' if self.level.is_raining else 'Clear'}"  # Văn bản trạng thái


        # Render the main text (white)
        text_surf_main = font.render(status_text, True, 'White')  # Vẽ văn bản chính (màu trắng)


        # Render the outline text (black)
        text_surf_outline = font.render(status_text, True, 'Black')  # Vẽ văn bản viền (màu đen)
        text_rect = text_surf_main.get_rect(topright=(self.screen.get_width() - 10, 10))  # Đặt vị trí văn bản ở góc trên bên phải


        # Draw the outline by placing black text around the white text
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Đặt viền đen xung quanh văn bản trắng
        for dx, dy in offsets:  # Lặp qua các điểm offset để vẽ viền
            outline_rect = text_rect.move(dx, dy)  # Di chuyển vị trí văn bản viền
            self.screen.blit(text_surf_outline, outline_rect)  # Vẽ viền đen


        # Draw the main text (white) on top
        self.screen.blit(text_surf_main, text_rect)  # Vẽ văn bản chính lên trên viền


    def draw_story(self):
        """Vẽ nội dung câu chuyện lên màn hình."""  # Vẽ nội dung câu chuyện
        self.screen.fill((255, 182, 193))  # Màu nền hồng cho câu chuyện
        font = pygame.font.Font('c:/Desktop/KHMT/s3 - import/s3 - import/font/VNF-Comic Sans.ttf', 20)  # Tạo font chữ
    
    # Nội dung câu chuyện
        story_text = """Trong một khu rừng xanh mướt, bạn đóng vai chú thỏ Naunau, linh vật được giao trọng trách 
        cai quản khu rừng bởi môi trường nơi đây luôn cần sự chăm sóc đến từ các tình nguyện viên.

        Với ý định gắn bó lâu dài với nơi đây, chú thỏ không mong muốn cứ ẩn nấp trong khu rừng như thế bởi cuộc sống 
        sẽ thật nhàm chán nếu ta không hành động. Và thế là, bạn quyết định biến khu rừng thành một thiên đường trái cây, 
        nơi mỗi loại quả đều ẩn chứa hương vị độc đáo và chia sẻ nó với thế giới bên ngoài như một loại lương thực. 

        Nhiệm vụ của bạn là chăm sóc từng vườn trái cây kỳ diệu mọc lên trong rừng, thu hoạch chúng, rồi mang những 
        món quà ngọt ngào ấy đến để trao đổi. Nhưng khu rừng không chỉ là một vùng đất thanh bình. 
        Những bí mật của nó luôn chờ đợi bạn khám phá.

        Ngoài những nguồn tài nguyên sẵn có, chú thỏ còn có thể đi khám phá khu rừng xung quanh với không chỉ là 
        những cây mà còn là các cao  nguyên, hồ nước cùng những khung cảnh tuyệt đẹp. 

        Khám phá The Wonderland cùng chú thỏ Naunau thư giãn
        …
        và đón chờ những điều kỳ diệu
        …"""  # Nội dung câu chuyện
        
        # Hiển thị nội dung câu chuyện
        y = 50  # Tọa độ y bắt đầu
        lines = story_text.split("\n")  # Chia câu chuyện thành từng dòng
        for line in lines:  # Lặp qua từng dòng
            text_surf = font.render(line.strip(), True, 'black')  # Vẽ từng dòng chữ
            text_rect = text_surf.get_rect(topleft=(50, y))  # Đặt vị trí của dòng chữ
            self.screen.blit(text_surf, text_rect)  # Vẽ dòng chữ lên màn hình
            y += 40  # Khoảng cách giữa các dòng



    def handle_events(self, event):  # Xử lý các sự kiện trong game.
        """Xử lý các sự kiện trong game."""  # Hàm này xử lý các sự kiện liên quan đến game
        if event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra nếu sự kiện là nhấp chuột
            mouse_pos = event.pos  # Lấy vị trí chuột
            self.handle_button_click(mouse_pos)  # Xử lý nhấp chuột trên nút bấm


        if event.type == pygame.KEYDOWN:  # Kiểm tra nếu có phím được nhấn
            if event.key == pygame.K_ESCAPE:  # Trở về màn hình chính khi nhấn ESC
                self.show_story = False  # Ẩn câu chuyện, trở về màn hình chính

    def draw_help_screen(self):  # Hiển thị màn hình hướng dẫn với nội dung bằng tiếng Việt và cho phép cuộn chuột.
        """Hiển thị màn hình hướng dẫn với nội dung bằng tiếng Việt và cho phép cuộn chuột."""  # Hàm này vẽ màn hình hướng dẫn.
        self.screen.fill((40, 40, 40))  # Nền tối cho màn hình hướng dẫn


    # Font cho tiêu đề và nội dung hướng dẫn
        title_font = pygame.font.Font('c:/Desktop/KHMT/s3 - import/s3 - import/font/VNF-Comic Sans.ttf', 50)  # Tạo font cho tiêu đề
        text_font = pygame.font.Font('c:/Desktop/KHMT/s3 - import/s3 - import/font/VNF-Comic Sans.ttf', 30)  # Tạo font cho nội dung hướng dẫn


    # Tiêu đề màn hình hướng dẫn
        title_text = "CÁCH CHƠI"  # Nội dung tiêu đề
        title_surf = title_font.render(title_text, True, 'white')  # Vẽ tiêu đề với màu chữ trắng
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 40))  # Đặt tiêu đề ở giữa màn hình
        self.screen.blit(title_surf, title_rect)  # Vẽ tiêu đề lên màn hình


    # Nội dung hướng dẫn
        text_lines = [  # Dữ liệu các dòng hướng dẫn
            ("1. Di chuyển nhân vật:", 'lightblue'),  # Dòng 1: Màu lightblue
            ("Đi lên: Nhấn phím Mũi tên lên (Up Arrow).", 'lightblue'),
            ("Đi xuống: Nhấn phím Mũi tên xuống (Down Arrow).", 'lightblue'),
            ("Đi sang trái: Nhấn phím Mũi tên trái (Left Arrow).", 'lightblue'),
            ("Đi sang phải: Nhấn phím Mũi tên phải (Right Arrow).", 'lightblue'),
            ("2. Sử dụng công cụ:", 'lightgreen'),
            ("Sử dụng công cụ (Cày đất, Chặt cây, Tưới nước):", 'lightgreen'),
            ("Nhấn Phím Space để sử dụng công cụ hiện tại của bạn.", 'lightgreen'),
            ("Công cụ có thể là Cày đất, Chặt cây, hoặc Tưới nước.", 'lightgreen'),
            ("Thay đổi công cụ: Nhấn Phím Q để thay đổi công cụ.", 'lightgreen'),
            ("3. Trồng cây:", 'lightyellow'),
            ("Chọn hạt giống bạn muốn trồng bằng phím E.", 'lightyellow'),
            ("Nhấn Phím Ctrl để trồng cây vào ô đất đã được cày xới.", 'lightyellow'),
            ("4. Thu hoạch cây:", 'lightcoral'),
            ("Khi cây đủ lớn, đứng gần cây để thu hoạch sản phẩm.", 'lightcoral'),
            ("5. Sử dụng cửa hàng:", 'lightgoldenrodyellow'),
            ("Nhấn Phím S để mở cửa hàng và mua bán sản phẩm.", 'lightgoldenrodyellow'),
            ("6. Thay đổi thời gian và thời tiết:", 'lightpink'),
            ("Nhấn nút Day/Night để thay đổi ngày/đêm.", 'lightpink'),
            ("Nhấn nút Rain để kích hoạt mưa giúp cây phát triển nhanh hơn.", 'lightpink'),
            ("7. Ngủ và chuyển ngày:", 'lightskyblue'),
            ("Nhấn Enter khi đứng gần giường để ngủ và chuyển sang ngày mới.", 'lightskyblue'),
            ("8. Cơ chế kinh tế:", 'lightseagreen'),
            ("Kiếm tiền qua việc bán các sản phẩm trong cửa hàng.", 'lightseagreen'),
            ("9. Tương tác trong game:", 'lightpink'),
            ("Tương tác với các đối tượng như Trader (Người bán) và Bed (Giường ngủ).", 'lightpink'),
        ]


    # Vị trí bắt đầu cho văn bản
        y = 100  # Vị trí bắt đầu cho văn bản
        line_height = 50  # Khoảng cách giữa các dòng
        padding = 20  # Padding xung quanh văn bản


    # Thêm phần cuộn chuột
        scroll_offset = self.scroll_offset  # Biến cuộn chuột, sẽ thay đổi khi người chơi cuộn chuột


        for text, color in text_lines:  # Lặp qua từng dòng văn bản hướng dẫn
        # Vẽ nền màu cho từng dòng hướng dẫn
            background_rect = pygame.Rect(padding, y + scroll_offset, self.screen.get_width() - 2 * padding, line_height)  # Vị trí nền cho mỗi dòng
            pygame.draw.rect(self.screen, color, background_rect, border_radius=10)  # Vẽ nền màu cho từng dòng hướng dẫn


        # Render và hiển thị văn bản trên nền
            text_surf = text_font.render(text, True, 'black')  # Vẽ văn bản với màu đen
            text_rect = text_surf.get_rect(center=background_rect.center)  # Đặt vị trí văn bản ở giữa nền
            self.screen.blit(text_surf, text_rect)  # Vẽ văn bản lên màn hình


            y += line_height + 10  # Cập nhật vị trí cho dòng tiếp theo


    # Vẽ nút "Back" để quay lại menu
        back_button_width, back_button_height = 200, 60  # Kích thước nút "Back"
        back_button_x = (self.screen.get_width() - back_button_width) // 2  # Vị trí ngang của nút "Back"
        back_button_y = self.screen.get_height() - back_button_height - 30  # Vị trí dọc của nút "Back"
        back_button = pygame.Rect(back_button_x, back_button_y, back_button_width , back_button_height)  # Vị trí và kích thước nút "Back"
        pygame.draw.rect(self.screen, 'orange', back_button, border_radius=10)  # Vẽ nền nút "Back" với màu cam
        pygame.draw.rect(self.screen, 'black', back_button, 3, border_radius=10)  # Vẽ viền đen cho nút "Back"


        back_text = text_font.render("Back", True, 'black')  # Vẽ chữ "Back"
        back_text_rect = back_text.get_rect(center=back_button.center)  # Đặt vị trí chữ "Back" ở giữa nút
        self.screen.blit(back_text, back_text_rect)  # Vẽ chữ "Back" lên nút



    def handle_help_screen_events(self, event):  # Hàm xử lý sự kiện trên màn hình hướng dẫn
        """Handle events for help screen including scrolling and back button."""  # Chú thích mô tả chức năng của hàm
        if event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra sự kiện click chuột
            mouse_pos = event.pos  # Lấy vị trí chuột

        # Kiểm tra xem có click vào nút "Back" không
            back_button = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() - 90, 200, 60)  # Vị trí và kích thước nút "Back"
            if back_button.collidepoint(mouse_pos):  # Nếu chuột click vào nút "Back"
                self.show_help = False  # Ẩn màn hình hướng dẫn khi nhấn nút "Back"

    # Xử lý cuộn chuột
        if event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra nếu là sự kiện click chuột
            if event.button == 4:  # Cuộn lên
                self.scroll_offset += 30  # Di chuyển lên
            elif event.button == 5:  # Cuộn xuống
                self.scroll_offset -= 30  # Di chuyển xuống

    def handle_button_click(self, pos):  # Hàm xử lý sự kiện click nút
        """Handle button clicks based on position."""  # Chú thích mô tả chức năng của hàm
        if self.button_positions["Day"].collidepoint(pos):  # Kiểm tra nếu click vào nút "Day"
            self.level.set_time_of_day("Day")  # Đặt thời gian trong game là "Day"
        elif self.button_positions["Night"].collidepoint(pos):  # Kiểm tra nếu click vào nút "Night"
            self.level.set_time_of_day("Night")  # Đặt thời gian trong game là "Night"
        elif self.button_positions["Rain"].collidepoint(pos):  # Kiểm tra nếu click vào nút "Rain"
            self.level.toggle_weather()  # Chuyển đổi thời tiết
        elif self.button_positions["Story"].collidepoint(pos):  # Khi nhấn vào nút "Story"
            self.show_story = True  # Hiển thị câu chuyện

    def handle_input(self, event):  # Hàm xử lý sự kiện nhập từ bàn phím
        """Handle keyboard input."""  # Chú thích mô tả chức năng của hàm
        if event.type == pygame.KEYDOWN:  # Nếu có sự kiện nhấn phím
            if self.main_menu:  # Nếu đang ở menu chính
                if event.key == pygame.K_RETURN:  # Bắt đầu game khi nhấn Enter
                    self.main_menu = False  # Ẩn menu chính
            else:
                if event.key == pygame.K_h:  # Toggle help
                    self.show_help = not self.show_help  # Chuyển đổi màn hình giúp đỡ
                elif event.key == pygame.K_s:  # Mở shop
                    self.level.toggle_shop()  # Chuyển sang trạng thái shop

    def run(self):  # Hàm chạy game chính
        while True:  # Vòng lặp chính của game
            # Xử lý sự kiện
            for event in pygame.event.get():  # Duyệt qua các sự kiện
                if event.type == pygame.QUIT:  # Kiểm tra sự kiện thoát
                    pygame.quit()  # Đóng pygame
                    sys.exit()  # Thoát chương trình

            # Kiểm tra trạng thái game (menu chính, trong game hoặc trong menu in-game)
                if self.game_state == "menu":  # Nếu trạng thái game là "menu"
                    self.handle_main_menu_events(event)  # Xử lý sự kiện menu chính
                elif self.game_state == "playing":  # Nếu trạng thái game là "playing"
                    if self.show_help:  # Nếu màn hình hướng dẫn đang mở
                        self.draw_help_screen()  # Vẽ màn hình hướng dẫn
                        self.handle_help_screen_events(event)  # Xử lý sự kiện cuộn chuột và nút "Back"
                    elif self.show_story:  # Nếu màn hình câu chuyện đang mở
                        self.draw_story()  # Vẽ màn hình câu chuyện
                        self.handle_events(event)  # Xử lý sự kiện câu chuyện
                    else:
                        if event.type == pygame.KEYDOWN:  # Kiểm tra nếu có sự kiện phím
                            if event.key == pygame.K_h:  # Mở/tắt màn hình hướng dẫn
                                self.show_help = True
                            elif event.key == pygame.K_s:  # Mở shop
                                self.level.toggle_shop()  # Chuyển sang trạng thái shop
                            elif event.key == pygame.K_RETURN:  # Lệnh Enter khi ngủ
                                if self.level.player.sleep:  # Kiểm tra trạng thái ngủ
                                    self.level.transition.play()  # Chuyển cảnh khi ngủ
                            elif event.key == pygame.K_t:  # Mở câu chuyện khi nhấn T
                                self.show_story = True
                            else:
                                self.handle_input(event)  # Xử lý các phím khác (di chuyển, v.v.)
                        elif event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra nếu có sự kiện click chuột
                            self.handle_button_click(event.pos)  # Xử lý các nút Day/Night/Rain

        # Vẽ màn hình dựa trên trạng thái hiện tại
            if self.game_state == "menu":  # Nếu game đang ở trạng thái "menu"
                self.draw_main_menu()  # Vẽ màn hình menu chính
            elif self.game_state == "playing":  # Nếu game đang ở trạng thái "playing"
                if self.show_help:  # Nếu màn hình hướng dẫn đang mở
                    self.draw_help_screen()  # Vẽ màn hình hướng dẫn
                elif self.show_story:  # Nếu màn hình câu chuyện đang mở
                    self.draw_story()  # Vẽ màn hình câu chuyện
                else:
                    self.screen .fill((255, 255, 255))  # Nền game
                    self.level.run(self.clock.tick() / 1000)  # Chạy logic game
                    self.draw_menu()  # Vẽ các nút Day/Night/Rain
                    self.draw_status()  # Hiển thị thời tiết, thời gian

            pygame.display.update()  # Cập nhật màn hình hiển thị

if __name__ == '__main__':  # Kiểm tra nếu chạy script này
    game = Game()  # Tạo đối tượng game
    game.run()  # Chạy game




