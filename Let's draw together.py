import tkinter as tk
import random
import pygame

class SplitCanvas:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.regions = [] 
        self.update_canvas_size()
        self.emoji_questions = {}
        self.canvas.bind("<Button-1>", self.split_region)
        root.bind("<Configure>", self.on_resize)

        pygame.mixer.init() 


        self.click_sound = pygame.mixer.Sound("448081__breviceps__tic-toc-click.wav")


        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        root.geometry(f"{screen_width}x{screen_height}")

        self.canvas.create_text(screen_width // 2, screen_height // 2, text="Click Now!", fill="#D3D3D3", font=("Arial", 40))

    def update_canvas_size(self):
      
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width > 1 and height > 1:
            self.regions = [(0, 0, width, height)]

    def on_resize(self, event):
       
        if event.widget == self.canvas:
            self.update_canvas_size()
            self.canvas.delete("all") 
            self.redraw_regions()
            self.reposition_emojis()
            
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            self.canvas.create_text(width // 2, height // 2, text="Click Now!", fill="#D3D3D3", font=("Arial", 40))

    def redraw_regions(self):
        
        for region in self.regions:
            x1, y1, x2, y2 = region
            if y1 == y2: 
                self.canvas.create_line(x1, y, x2, y, fill="black", width=4)
            elif x1 == x2: 
                self.canvas.create_line(x, y1, x, y2, fill="black", width=4)

    def reposition_emojis(self):
        
        for region_center, (region, emoji, bg_color) in self.emoji_questions.items():
            x1, y1, x2, y2 = region
            new_x = (x1 + x2) // 2
            new_y = (y1 + y2) // 2
            self.create_dynamic_emoji(new_x, new_y, emoji, region, bg_color)

    def generate_random_emoji(self):
   
        emoji_list = ["😀", "😂", "😎", "❤️", "🔥", "💡", "🍀", "🎉", "🚀", "🐱"]
        return random.choice(emoji_list)

    def generate_random_color(self):
       
        return f"#{random.randint(0, 0xFFFFFF):06x}"

    def split_region(self, event):
       
        x, y = event.x, event.y

        for region in self.regions:
            x1, y1, x2, y2 = region
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.regions.remove(region)

                if random.choice(["horizontal", "vertical"]) == "horizontal":
                   
                    self.regions.append((x1, y1, x2, y))
                    self.regions.append((x1, y, x2, y2))
                    self.canvas.create_line(x1, y, x2, y, fill="black", width=4)
                else:
                    
                    self.regions.append((x1, y1, x, y2))
                    self.regions.append((x, y1, x2, y2))
                    self.canvas.create_line(x, y1, x, y2, fill="black", width=4)

                
                self.click_sound.play()

                self.canvas.delete("emoji") 
                self.add_or_update_emojis()
                break

    def add_or_update_emojis(self):
      
        updated_emojis = {}

        for region in self.regions:
            x1, y1, x2, y2 = region
            region_center = ((x1 + x2) // 2, (y1 + y2) // 2)

            emoji = self.generate_random_emoji()
            color = self.generate_random_color() 
            updated_emojis[region_center] = (region, emoji, color)
            self.create_dynamic_emoji(region_center[0], region_center[1], emoji, region, color)

        self.emoji_questions = updated_emojis

    def create_dynamic_emoji(self, x, y, emoji, region, bg_color):
        
        x1, y1, x2, y2 = region
        
        width = x2 - x1
        height = y2 - y1

        
        font_size = min(width, height) // 5  
        font_size = max(font_size, 12) 


        self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="", tags="emoji")  # 添加背景矩形
        self.canvas.create_text(x, y, text=emoji, fill="black", font=("Arial", font_size), tags="emoji")


root = tk.Tk()
root.title("Let's Draw Together!")

split_canvas = SplitCanvas(root)


root.mainloop()

