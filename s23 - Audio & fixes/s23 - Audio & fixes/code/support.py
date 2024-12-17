from os import walk  # Nhập hàm walk từ thư viện os để duyệt qua các thư mục và tệp tin
import pygame  # Nhập thư viện pygame để sử dụng các chức năng đồ họa

# Hàm import_folder: Nhập tất cả các tệp ảnh từ thư mục và trả về dưới dạng danh sách
def import_folder(path):
    surface_list = []  # Khởi tạo danh sách để lưu trữ các bề mặt (surface) ảnh

    for _, __, img_files in walk(path):  # Duyệt qua tất cả các tệp tin trong thư mục (path)
        for image in img_files:  # Duyệt qua mỗi tệp ảnh
            full_path = path + '/' + image  # Tạo đường dẫn đầy đủ đến tệp ảnh
            image_surf = pygame.image.load(full_path).convert_alpha()  # Tải ảnh và chuyển đổi ảnh sang dạng surface với alpha channel
            surface_list.append(image_surf)  # Thêm ảnh đã tải vào danh sách

    return surface_list  # Trả về danh sách các bề mặt ảnh

# Hàm import_folder_dict: Nhập tất cả các tệp ảnh từ thư mục và trả về dưới dạng dictionary với tên tệp làm khóa
def import_folder_dict(path):
    surface_dict = {}  # Khởi tạo từ điển để lưu trữ các bề mặt (surface) ảnh với khóa là tên tệp ảnh

    for _, __, img_files in walk(path):  # Duyệt qua tất cả các tệp tin trong thư mục (path)
        for image in img_files:  # Duyệt qua mỗi tệp ảnh
            full_path = path + '/' + image  # Tạo đường dẫn đầy đủ đến tệp ảnh
            image_surf = pygame.image.load(full_path).convert_alpha()  # Tải ảnh và chuyển đổi ảnh sang dạng surface với alpha channel
            surface_dict[image.split('.')[0]] = image_surf  # Lưu ảnh vào từ điển với khóa là tên tệp ảnh (không có phần mở rộng)

    return surface_dict  # Trả về từ điển các bề mặt ảnh
