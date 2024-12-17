from pygame.math import Vector2  # Nhập module Vector2 từ pygame để sử dụng cho các tọa độ (vector)
# screen
SCREEN_WIDTH = 1280  # Độ rộng màn hình (pixel)
SCREEN_HEIGHT = 720  # Độ cao màn hình (pixel)
TILE_SIZE = 64  # Kích thước của một ô vuông trên màn hình (pixel)

# overlay positions 
OVERLAY_POSITIONS = {
    'tool' : (40, SCREEN_HEIGHT - 15),  # Vị trí của công cụ (tool) trên màn hình
    'seed': (70, SCREEN_HEIGHT - 5)  # Vị trí của hạt giống (seed) trên màn hình
}

# PLAYER_TOOL_OFFSET: Sự dịch chuyển của công cụ khi người chơi sử dụng
PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50,40),  # Dịch chuyển công cụ khi hướng sang trái
    'right': Vector2(50,40),  # Dịch chuyển công cụ khi hướng sang phải
    'up': Vector2(0,-10),  # Dịch chuyển công cụ khi hướng lên
    'down': Vector2(0,50)  # Dịch chuyển công cụ khi hướng xuống
}

# LAYERS: Các lớp đồ họa (layers) trong game, mỗi lớp có độ ưu tiên riêng (giá trị càng cao càng ở trên)
LAYERS = {
    'water': 0,  # Lớp nước, độ ưu tiên thấp nhất
    'ground': 1,  # Lớp đất, thấp hơn đất trồng
    'soil': 2,  # Lớp đất trồng
    'soil water': 3,  # Lớp đất có nước
    'rain floor': 4,  # Lớp sàn mưa
    'house bottom': 5,  # Lớp dưới của ngôi nhà
    'ground plant': 6,  # Lớp cây trồng trên mặt đất
    'main': 7,  # Lớp chính
    'house top': 8,  # Lớp trên của ngôi nhà
    'fruit': 9,  # Lớp trái cây
    'rain drops': 10  # Lớp giọt mưa
}

# Apple positions: Vị trí các quả táo (Small và Large) trong game
APPLE_POS = {
    'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],  # Vị trí các quả táo nhỏ
    'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]  # Vị trí các quả táo lớn
}

# GROW_SPEED: Tốc độ phát triển của các loại cây trồng
GROW_SPEED = {
    'corn': 1,  # Tốc độ phát triển của cây ngô (1 là tốc độ mặc định)
    'tomato': 0.7  # Tốc độ phát triển của cây cà chua (0.7 là tốc độ chậm hơn ngô)
}

# SALE_PRICES: Giá bán các mặt hàng trong game
SALE_PRICES = {
    'wood': 4,  # Giá bán gỗ
    'apple': 2,  # Giá bán táo
    'corn': 10,  # Giá bán ngô
    'tomato': 20  # Giá bán cà chua
}

# PURCHASE_PRICES: Giá mua các mặt hàng trong game
PURCHASE_PRICES = {
    'corn': 4,  # Giá mua ngô
    'tomato': 5  # Giá mua cà chua
}
