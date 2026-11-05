import os, shutil

try:
    import tkinter as tk
    from tkinter import filedialog, simpledialog
    from pygame import mixer
except Exception:
    st=None

try:
    import streamlit as st
except Exception:
    st=None

BG, CARD, TEXT= "#1E1B2E","#282640", "#F3E8FF"
PINK , BLUE, PURPLE = "#FF8FD6", "#8FD9FF","#C9A0FF"

def get_playlist():
    return sorted([f for f in os.listdir() if f.endswith(".mp3")])

def clean(file_name):
    return file_name.replace(".mp3","").replace("_"," ").title()
# ________________
def run_tkinter_app():
    try: mixer.init()
    except Exception: pass

    window= tk.Tk()
    window.title("Vibe Music Player🫠")
    window.geometry("360x450")
    window.configure(bg=BG)

    tk.Label(window, text="my vibe playlist🥰", bg=BG, fg=PURPLE, font=("Arial",15,"bold")).pack(pady=10)
    box = tk.Listbox(window, bg=CARD, fg=TEXT, font=("Arial",12), selectbackground=BLUE, width=28, height=8, bd=0)
    box.pack(pady=8)
    status=tk.Label(window, text="select a song",bg=BG, fg=TEXT, font=("Arial",10))
    status.pack(pady=5)

    def refresh():
        box.delete(0,tk.END)
        for s in get_playlist():
            box.insert(tk.END,clean(s))

    def play():
        if not box.curselection():
            return status.config(text="choose your first song", fg=BLUE)
        song = get_playlist()[box.curselection()[0]]
        try:
            mixer.music.load(song)
            mixer.music.play()
            status.config(text="playing:"+ clean(song), fg =BLUE)
        except Exception:
            status.config(text="file is missing", fg=PINK)

    def pause():
        if mixer.get_init():mixer.pause()

    def resume():
        if mixer.get_init():mixer.music.unpause()
    def stop():
        if mixer.get_init():mixer.music.stop()
    def add_song():
        path = filedialog.askopenfile(title="select MP3", filetypes=[("MP3 files", "*.mp3")])
        name = simpledialog.askstring("Song Name","Enter name:") if path else None
        if path and name :
            new_file = name.strip().replace(" ","_").lower()+".mp3"
            shutil.copy(path, new_file)
            refresh()
            status.config (text="Added:"+  clean(new_file),fg=PINK)

    refresh()
    row=tk.Frame(window,bg=BG)
    row.pack(pady=8)
    tk.Button(row, text="play",command=play, bg=BLUE, width=6).grid(row=0, column=0, padx=3)
    tk.Button(row, text="pause",command=pause, bg=PINK, width=6).grid(row=0, column=1, padx=3)
    tk.Button(row, text="resume", command=resume, bg=BLUE, width=6).grid(row=0, column=2, padx=3)
    tk.Button(row, text="stop", command=stop, bg=PURPLE, width=6).grid(row=0, column=3, padx=3)
    tk.Button(window, text="add song", command=add_song, bg=PURPLE, width=20).pack(pady=8)
    window.mainloop()
                             
def run_streamlit_app():       
    st.set_page_config(page_title="Calm Vibes Music🥰😍")
    st.markdown(f"<style>.stApp{{background-color:{BG};color:{TEXT};}} h1,h2,h3,p,label{{color:{PURPLE}!important;}}</style>", unsafe_allow_html=True)
    st.title("Clam Vibes Music Player🥰😍")

    playlist = get_playlist()
    if playlist:                                                                              
        song = st.selectbox("Select a song to play", playlist, format_func=clean)
        st.success("Now playing:" + clean(song))
        with open(song, "rb")as f:
            st.audio(f.read(), format="audio/mp3")
    else:
        st.warning("No songs yet!")

    st.subheader("upload songs")
    up_file = st.file_uploader("upload MP3", type=["mp3"])
    up_name = st.text_input("song name ")
    if st.button("Save") and up_file and  up_name.strip():
        new_file = up_name.strip().replace(" ","_").lower() +".mp3"
        with open(new_file,"wb") as f:
            f.write(up_file.getbuffer())
        st.success("saved:" + clean(new_file))
        st.rerun()

# if __name__ == "__main__":
#     run_tkinter_app()
if st and st.runtime.exists():
    run_streamlit_app()
else:
    run_tkinter_app
