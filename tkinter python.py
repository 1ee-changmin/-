import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw


# Helper function to create circular images
def create_circle_image(image_path, size):
    try:
        img = Image.open(image_path).resize((size, size), Image.Resampling.LANCZOS)
        circle = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, size, size), fill=255)
        img.putalpha(circle)
        return ImageTk.PhotoImage(img)
    except:
        placeholder = Image.new("RGB", (size, size), color="gray")
        return ImageTk.PhotoImage(placeholder)


# Data
notifications = [
    {"club": "그림 동아리", "text": "그림 과제 제출 완료", "image": "art club.jpg", "read": False},
    {"club": "영화 동아리", "text": "이번주 7/23일 모임 공지", "image": "movie club.jpg", "read": False},
    {"club": "코딩 동아리", "text": "새 자료가 등록되었습니다", "image": "coding club.jpg", "read": False},
    {"club": "영어 회화 동아리", "text": "모임 장소 변경 안내", "image": "english club.jpg", "read": False},
    {"club": "발표 동아리", "text": "코멘트가 등록되었습니다\n한글 파일 첨부 hwp", "image": "presentation club.jpg", "read": False},
    {"club": "베이킹 동아리", "text": "활동 사진이 등록되었습니다", "image": "baking club1.jpg", "read": False},
]

resources = [
    {"type": "사진", "title": "2024-07-01 활동 사진", "icon": "photo.jpg"},
    {"type": "동영상", "title": "토론발표 영상\n업로드 | 3일 전", "icon": "video.jpg"},
    {"type": "파일", "title": "2기 코딩 동아리 지원 양식.pdf", "icon": "file.jpg"},
    {"type": "코드 소스", "title": "code.py", "icon": "code.jpg"},
]

clubs = {
    "지원한 동아리": [{"name": "그림 동아리", "image": "art club.jpg"}, {"name": "영화 동아리", "image": "movie club.jpg"}],
    "현재 활동 중인 동아리": [{"name": "코딩 동아리", "image": "coding club.jpg"}, {"name": "영어 회화 동아리", "image": "english club.jpg"}],
    "찜한 동아리": [{"name": "발표 동아리", "image": "presentation club.jpg"}, {"name": "베이킹 동아리", "image": "baking club1.jpg"}],
}


class ClubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("동아리 앱")
        self.geometry("300x500")

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Active Filter
        self.active_club_filter = "전체"

        # Create Tabs
        self.create_notification_tab()
        self.create_resource_tab()
        self.create_mypage_tab()

    def create_scrollable_canvas(self, parent):
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    # Notification Tab
    def create_notification_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="동아리 알림")

        self.scrollable_frame = self.create_scrollable_canvas(frame)
        self.update_notification_tab()

    def update_notification_tab(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for notification in notifications:
            noti_frame = ttk.Frame(self.scrollable_frame)
            noti_frame.pack(fill="x", padx=10, pady=5)

            # Add circular image
            image = create_circle_image(notification["image"], 50)
            img_label = tk.Label(noti_frame, image=image)
            img_label.image = image
            img_label.pack(side="left", padx=5)

            # Add notification button
            button = ttk.Button(
                noti_frame,
                text=f"{notification['club']}",
                command=lambda n=notification: self.open_notification_detail(n),
            )
            button.pack(side="left", padx=10)

            # Add unread indicator
            if not notification["read"]:
                unread_label = tk.Label(noti_frame, text="🔴", fg="red")
                unread_label.pack(side="right", padx=10)

    def open_notification_detail(self, notification):
        notification["read"] = True
        detail_window = tk.Toplevel(self)
        detail_window.title(notification["club"])
        detail_window.geometry("300x300")

        label = tk.Label(detail_window, text=notification["text"], wraplength=280, justify="left")
        label.pack(pady=10)

        close_button = ttk.Button(detail_window, text="닫기", command=detail_window.destroy)
        close_button.pack(pady=10)

        self.update_notification_tab()

    # Resource Tab
    def create_resource_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="동아리 자료실")

        scrollable_frame = self.create_scrollable_canvas(frame)

        for resource in resources:
            res_frame = ttk.Frame(scrollable_frame)
            res_frame.pack(fill="x", padx=10, pady=5)

            icon = create_circle_image(resource["icon"], 50)
            icon_label = tk.Label(res_frame, image=icon)
            icon_label.image = icon
            icon_label.pack(side="left", padx=5)

            button = ttk.Button(
                res_frame,
                text=f"{resource['type']}",
                command=lambda r=resource: self.open_resource_detail(r),
            )
            button.pack(side="left", padx=5)

    def open_resource_detail(self, resource):
        detail_window = tk.Toplevel(self)
        detail_window.title(resource["type"])
        detail_window.geometry("300x300")

        label = tk.Label(detail_window, text=resource["title"], wraplength=280, justify="left")
        label.pack(pady=10)

        close_button = ttk.Button(detail_window, text="닫기", command=detail_window.destroy)
        close_button.pack(pady=10)

    # MyPage Tab
    def create_mypage_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="마이페이지")

        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill="x", pady=10)

        for filter_name in ["전체", "지원한 동아리", "현재 활동 중인 동아리", "찜한 동아리"]:
            button = ttk.Button(
                filter_frame,
                text=filter_name,
                command=lambda f=filter_name: self.update_mypage_list(f),
            )
            button.pack(side="left", padx=5)

        self.mypage_frame = self.create_scrollable_canvas(frame)
        self.update_mypage_list("전체")

    def update_mypage_list(self, filter_name):
        self.active_club_filter = filter_name

        for widget in self.mypage_frame.winfo_children():
            widget.destroy()

        if filter_name == "전체":
            all_clubs = [club for group in clubs.values() for club in group]
        else:
            all_clubs = clubs.get(filter_name, [])

        for club in all_clubs:
            club_frame = ttk.Frame(self.mypage_frame)
            club_frame.pack(fill="x", padx=10, pady=5)

            image = create_circle_image(club["image"], 50)
            img_label = tk.Label(club_frame, image=image)
            img_label.image = image
            img_label.pack(side="left", padx=5)

            button = ttk.Button(
                club_frame,
                text=club["name"],
                command=lambda c=club: self.open_club_detail(c),
            )
            button.pack(side="left", padx=10)

    def open_club_detail(self, club):
        detail_window = tk.Toplevel(self)
        detail_window.title(club["name"])
        detail_window.geometry("300x300")

        label = tk.Label(detail_window, text=f"{club['name']} 상세 정보")
        label.pack(pady=10)

        close_button = ttk.Button(detail_window, text="닫기", command=detail_window.destroy)
        close_button.pack(pady=10)


if __name__ == "__main__":
    app = ClubApp()
    app.mainloop()
