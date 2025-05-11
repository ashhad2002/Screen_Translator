import easyocr
from PIL import ImageGrab
import keyboard
from transformers import MarianMTModel, MarianTokenizer
import tkinter as tk
import os
import uuid
import ctypes
from korean_romanizer.romanizer import Romanizer
import pyperclip

ctypes.windll.user32.SetProcessDPIAware() # Needed so ss isn't messed up by weird dpi issues

reader = easyocr.Reader(['ko', 'en'], gpu=False)

model_name = 'Helsinki-NLP/opus-mt-ko-en' # From my testing, this translation is not as good as the Google Translate one. I'd recommend supplementing these translations with Google Translate.
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

bbox_cache = None # Screen selection variable

def translate_korean_to_english(text):
    if not text.strip():
        return "(No text to translate)"
    inputs = tokenizer(text, return_tensors='pt', truncation=True)
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def extract_text_easyocr_from_image_file(image_path):
    result = reader.readtext(image_path, detail=0)
    return ' '.join(result)

def screen_selection():
    coords = {}

    def on_mouse_down(event):
        coords['x1'], coords['y1'] = event.x, event.y
        coords['rect'] = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red', width=2)

    def on_mouse_drag(event):
        canvas.coords(coords['rect'], coords['x1'], coords['y1'], event.x, event.y)

    def on_mouse_up(event):
        coords['x2'], coords['y2'] = event.x, event.y
        root.quit()

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    root.configure(bg='black')
    canvas = tk.Canvas(root, cursor='cross', bg='black')
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.bind('<Button-1>', on_mouse_down)
    canvas.bind('<B1-Motion>', on_mouse_drag)
    canvas.bind('<ButtonRelease-1>', on_mouse_up)
    root.mainloop()
    root.destroy()

    return (min(coords['x1'], coords['x2']), min(coords['y1'], coords['y2']),
            max(coords['x1'], coords['x2']), max(coords['y1'], coords['y2']))

def capture_and_translate():
    global bbox_cache
    try:
        if bbox_cache is None:
            print("\n📸 Draw a rectangle to capture...")
            bbox_cache = screen_selection()

        image = ImageGrab.grab(bbox_cache)

        save_dir = 'C:/Users/pokel/OneDrive/Pictures/Screenshots'
        tmp_filename = os.path.join(save_dir, f"temp_{uuid.uuid4().hex}.png")
        image.save(tmp_filename)

        print("Running EasyOCR...")
        korean_text = extract_text_easyocr_from_image_file(tmp_filename).strip()
        os.remove(tmp_filename)

        print("\nKorean Text:\n", korean_text if korean_text else "(None detected)")

        if korean_text:
            pyperclip.copy(korean_text)
            print("Copied Korean text to clipboard.")

            try:
                romanized = Romanizer(korean_text).romanize()
                print("\nRomanized:\n", romanized)
            except Exception:
                print("\nCould not romanize text.")

        english = translate_korean_to_english(korean_text)
        print("\nEnglish Translation:\n", english)

    except Exception as e:
        print(f"Error: {e}")

def reset_selection():
    global bbox_cache
    print("\nReselecting screen region...")
    bbox_cache = None
    capture_and_translate()

def main():
    print("Press T to capture and translate. If no region is selected, it will prompt you to select one.")
    print("Press R to select the region and translate.")
    print("Press Esc to exit.")

    keyboard.add_hotkey('t', capture_and_translate)
    keyboard.add_hotkey('r', reset_selection)
    keyboard.wait('esc')

if __name__ == '__main__':
    main()
