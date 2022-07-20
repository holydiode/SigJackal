import zipfile
from PIL import Image
from math import sqrt
import os
import config
from sys import argv
from io import BytesIO
from progress.bar import IncrementalBar
from pydub import AudioSegment
import moviepy.editor as mpy
import tempfile


class FileHandler:
    def handle_file(self, source, item, target):
        try:
            buffer = self._read_file(source, item.filename)
            buffer = self._jackal(buffer)
            self._save_file(target, buffer, item)
        except Exception as error:
            print("\n Шакалы не справились c фалом" + item.filename)
            print(error)
            if type(self) == FileHandler:
                raise Exception("Файл настолько прогнил, что с ним не справятся даже шакалы")

            FileHandler().handle_file(source, item, target)

    def _read_file(self, source: zipfile.ZipFile, filename):
        return source.open(filename)

    def _jackal(self, file):
        return file

    def _save_file(self, target, buffer, item):
        with target.open(item, 'w') as output:
            while True:
                data = buffer.read(config.buffer_size)
                if data == b'':
                    break
                output.write(data)
        buffer.close()


class ImageHandler(FileHandler):
    def _read_file(self, source, filename):
        buffer = super()._read_file(source, filename)
        img = Image.open(buffer)
        buffer.close()
        return img

    def _jackal(self, file):
        power = config.max_img_pixels
        size = file.size
        if size[0] * size[1] > power:
            jackal_coefficient = sqrt(power / (size[0] * size[1]))
            return file.resize(
                (int(size[0] * jackal_coefficient),
                 int(size[1] * jackal_coefficient)),
                Image.ANTIALIAS)
        return file

    def _save_file(self, target, buffer, item):
        with target.open(item, 'w') as output:
            buffer.save(output, format='PNG')


class AudioHandler(FileHandler):
    def _read_file(self, source, filename):
        buffer = super()._read_file(source, filename)
        buffer = BytesIO(buffer.read())
        return AudioSegment.from_file(buffer)

    def _jackal(self, file: AudioSegment):
        jackal_sound = file
        if config.solo_channal_sound and file.channels > 1:
            jackal_sound = jackal_sound.set_channels(1)
        if jackal_sound.frame_rate > config.max_bit_rate:
            jackal_sound = jackal_sound.set_frame_rate(config.max_bit_rate)
        return jackal_sound

    def _save_file(self, target, buffer: AudioSegment, item):
        buffer_bytes = BytesIO()
        buffer.export(buffer_bytes, format='mp3')
        super()._save_file(target, buffer_bytes, item)


class VideoHandler(FileHandler):
    def _read_file(self, source, filename):
        buffer = super()._read_file(source, filename)
        with tempfile.TemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as file:
            tem_file_name = file.name
            while True:
                data = buffer.read(config.buffer_size)
                if data == b'':
                    break
                file.write(data)

        clip = mpy.VideoFileClip(tem_file_name)
        return clip

    def _jackal(self, file: mpy.VideoFileClip):
        if file.w * file.h > config.max_video_pixels:
            jackal_coefficient = round(config.max_video_pixels / (file.w * file.h), 1)
            file = file.resize(jackal_coefficient)

        return file

    def _save_file(self, target, buffer: mpy.VideoFileClip, item):
        buffer.write_videofile(buffer.filename + '.mp4',
                               codec="libx264",
                               fps=config.video_fps,
                               logger=None)
        buffer.close()

        with open(buffer.filename + '.mp4', 'rb') as file:
            super()._save_file(target, file, item)

        os.remove(buffer.filename)
        os.remove(buffer.filename + '.mp4')


class SIGPackJackaler:
    def __init__(self, work_dir):
        self.work_dir = work_dir
        self.temp_source_path = f"{self.work_dir}\\source"
        self.temp_target_path = f"{self.work_dir}\\target"
        self.handlers_dict = {
            "Images": ImageHandler(),
            "Audio": AudioHandler(),
            "Video": VideoHandler()
        }

    def jackal_pack(self, source_path, target_path):
        with zipfile.ZipFile(source_path, 'r') as source_archive, \
                zipfile.ZipFile(target_path, 'w') as target_archive:
            bar = IncrementalBar('Проект в обработке',
                                 max=len(source_archive.infolist()),
                                 suffix='%(index)d ебучих шакалов из %(max)d')

            for item in source_archive.infolist():
                type_file = os.path.dirname(item.filename)
                handler = self.get_handler(type_file)
                handler.handle_file(source_archive, item, target_archive)
                bar.next()

    def get_handler(self, type_file):
        if type_file in self.handlers_dict:
            return self.handlers_dict[type_file]
        return FileHandler()


if __name__ == '__main__':
    path, source_path, target_path = argv
    jackaler = SIGPackJackaler("temp")
    jackaler.jackal_pack(source_path, target_path)
