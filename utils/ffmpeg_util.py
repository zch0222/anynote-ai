import ffmpeg


def extract_sound(input_file_path: str, out_file_path: str):
    (
        ffmpeg
        .input(input_file_path)
        .output(out_file_path, acodec='libmp3lame')  # 使用 MP3 编码器
        .run()
    )
