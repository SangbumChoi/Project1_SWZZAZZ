import sys
import cv2
from moviepy.editor import AudioFileClip, VideoFileClip
from PyQt5.QtWidgets import QProgressBar, QMainWindow, QApplication, QVBoxLayout, QWidget, QFileDialog


class VideoSave(QMainWindow):

    def __init__(self, name):
        super().__init__()

        self.progress = QProgressBar(self)
        self.name = name

        self.resize(350, 60)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.progress)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def saveVideo(self):
        cap = cv2.VideoCapture(self.name)
        count = 0
        four_cc = cv2.VideoWriter_fourcc(*'DIVX')
        name = QFileDialog.getSaveFileName(self, "Save File", "output.avi", "Videos(*.avi)")
        # if user doesn't select file directory
        if not name[0]:
            return

        out = cv2.VideoWriter(name[0], four_cc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(3)), int(cap.get(4))))

        self.progress.setMaximum(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                count += 1
                out.write(frame)
                self.progress.setValue(count)
            else:
                break

        cap.release()
        out.release()

        audio = AudioFileClip(self.name)
        video = VideoFileClip(name[0])
        result = video.set_audio(audio)
        result.write_videofile(name[0].replace(".avi", ".mp4"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    videoSave = VideoSave(r'C:\Users\kimda\Desktop\github\Team_Island\VideoSave\input.mp4')
    videoSave.saveVideo()
    sys.exit(app.exec_())
