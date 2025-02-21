#!/usr/bin/env python
import os
import argparse
import cv2
from PIL import Image
import numpy as np

from moviepy.editor import (
    VideoFileClip, 
    ImageSequenceClip, 
    ImageClip,
    concatenate_videoclips,
    vfx, 
    clips_array
)

def image_to_video(image_dir, output_name, fps=24):

    valid_ext = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    image_files = sorted(
        f for f in os.listdir(image_dir)
        if os.path.splitext(f)[1].lower() in valid_ext
    )
    image_paths = [os.path.join(image_dir, f) for f in image_files]

    if not image_paths:
        raise ValueError("No images found in the specified directory.")

    # 첫 번째 이미지를 열어 target_size를 정함
    with Image.open(image_paths[0]) as first_img:
        target_size = first_img.size  # 예: (width, height)

    # 모든 이미지를 ImageClip으로 만들고, target_size로 resize
    clips = []
    for path in image_paths:
        with Image.open(path) as img:
            img_rgb = img.convert("RGB")
            frame = np.asarray(img_rgb)       # numpy 배열로 변환
    
        # ImageClip 객체 생성 + 크기 조정
        clip = ImageClip(frame).resize(newsize=target_size)
        # 각 이미지가 정해진 duration(프레임 당 1/FPS 초) 만큼 재생된다고 가정
        # 여기서는 이미지 당 1프레임만큼 재생시키기 위해 duration=1.0/fps
        clip = clip.set_duration(1.0 / fps)
        clips.append(clip)

    # 모든 클립을 순차적으로 이어붙이기
    final_clip = concatenate_videoclips(clips, method="compose")

    # fps로 설정하면, 총 프레임 수 = len(images), 총 길이 = len(images)*(1/fps)
    final_clip.write_videofile(output_name, fps=fps, codec="h264_nvenc")


def image_to_video_gray16(image_dir, output_name, fps=24):
    """
    16비트(혹은 일반 8비트) 흑백 이미지를 0~255 범위로 정규화 후 동영상화.
    """
    valid_ext = {".png", ".jpg", ".jpeg", ".tiff"}
    image_files = sorted(
        f for f in os.listdir(image_dir)
        if os.path.splitext(f)[1].lower() in valid_ext
    )
    image_paths = [os.path.join(image_dir, f) for f in image_files]
    
    if not image_paths:
        raise ValueError("No images found in the specified directory.")

    clips = []
    for path in image_paths:
        # 16비트 그레이스케일 이미지 로드
        with Image.open(path) as img:
            arr_16 = np.array(img)  # np.uint16, shape=(H, W)
        
        # 최소 ~ 최대 값을 0~255로 정규화
        min_val, max_val = arr_16.min(), arr_16.max()
        if max_val == min_val:
            arr_8 = np.zeros_like(arr_16, dtype=np.uint8)
        else:
            arr_8 = ((arr_16 - min_val) / (max_val - min_val) * 255).astype(np.uint8)
        
        # 흑백 -> RGB(3채널) 변환
        # 일단 PIL Image로 다시 만들고 convert("RGB") -> numpy 변환
        pil_gray_8 = Image.fromarray(arr_8, mode="L")   # 'L' 8비트 흑백
        pil_rgb_8  = pil_gray_8.convert("RGB")
        arr_rgb_8  = np.array(pil_rgb_8)

        # MoviePy ImageClip 생성 (numpy 배열)
        clip = ImageClip(arr_rgb_8).set_duration(1.0 / fps)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_name, fps=fps, codec="h264_nvenc")


def image_to_video_color(image_dir, output_name, fps=24, use_colormap=True):
    """
    16비트(혹은 일반 8비트) 흑백 이미지를 컬러맵 적용 후 동영상화.
    """
    valid_ext = {".png", ".jpg", ".jpeg", ".tiff"}
    image_files = sorted(
        f for f in os.listdir(image_dir)
        if os.path.splitext(f)[1].lower() in valid_ext
    )
    image_paths = [os.path.join(image_dir, f) for f in image_files]
    
    if not image_paths:
        raise ValueError("No images found in the specified directory.")

    clips = []
    for path in image_paths:
        with Image.open(path) as img:
            arr_16 = np.array(img)
        
        # 정규화
        min_val, max_val = arr_16.min(), arr_16.max()
        if max_val == min_val:
            arr_8 = np.zeros_like(arr_16, dtype=np.uint8)
        else:
            arr_8 = ((arr_16 - min_val) / (max_val - min_val) * 255).astype(np.uint8)
        
        if use_colormap:
            # 컬러맵 적용 (JET)
            arr_color = cv2.applyColorMap(arr_8, cv2.COLORMAP_JET)
            arr_color = cv2.cvtColor(arr_color, cv2.COLOR_BGR2RGB)
        else:
            # 흑백 -> RGB
            pil_gray_8 = Image.fromarray(arr_8, mode="L")
            pil_rgb_8 = pil_gray_8.convert("RGB")
            arr_color = np.array(pil_rgb_8)

        clip = ImageClip(arr_color).set_duration(1.0 / fps)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_name, fps=fps, codec="h264_nvenc")


def video_composition2(video1_path, video2_path, output_name="composition2.mp4"):
    """
    2개의 영상을 좌우로 나란히 붙여서 output_name으로 저장.
    """
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)

    # clips_array([[clip1, clip2]]) -> 1행 2열(가로로 붙임)
    final_clip = clips_array([[clip1, clip2]])
    final_clip.write_videofile(output_name, codec="h264_nvenc")

def video_composition4(video1_path, video2_path, video3_path, video4_path, output_name="composition4.mp4"):
    """
    4개의 영상을 2x2 격자로 붙여서 output_name으로 저장.
    """
    c1 = VideoFileClip(video1_path)
    c2 = VideoFileClip(video2_path)
    c3 = VideoFileClip(video3_path)
    c4 = VideoFileClip(video4_path)

    # 2행 2열 구조: [[c1, c2],
    #               [c3, c4]]
    final_clip = clips_array([[c1, c2],
                              [c3, c4]])
    final_clip.write_videofile(output_name, codec="h264_nvenc")

def video_slowmo(input_video, output_video, speed_factor):
    """
    영상 재생 속도를 speed_factor로 조절하여 output_video로 저장.
    speed_factor > 1 -> 더 빠르게(영상 길이 짧아짐)
    speed_factor < 1 -> 더 느리게(슬로우모션, 길이 길어짐)
    """
    clip = VideoFileClip(input_video)
    # moviepy의 speedx( factor ) :
    #   factor가 2.0 이면 2배 빠른 재생 -> 영상 길이는 절반
    #   factor가 0.5 이면 0.5배 빠른 재생 -> 실제로는 2배 느려짐
    modified_clip = clip.fx(vfx.speedx, speed_factor)
    modified_clip.write_videofile(output_video, codec="h264_nvenc")

def main():
    parser = argparse.ArgumentParser(description="Video Processing Tools")

    # 실행할 기능
    parser.add_argument(
        "function",
        type=str,
        choices=["image_to_video", "image_to_video_gray16", "image_to_video_color", 
                "video_composition2", "video_composition4", "video_slowmo"],
        help="Choose which function to run."
    )

    # 공통 매개변수
    parser.add_argument("--output", type=str, default="output.mp4", help="Output video file name.")

    # image_to_video 관련
    parser.add_argument("--image_dir", type=str, help="Directory containing images.")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second for image_to_video.")

    # video_composition2 관련
    parser.add_argument("--video1", type=str, help="Path to the first video.")
    parser.add_argument("--video2", type=str, help="Path to the second video.")

    # video_composition4 관련
    parser.add_argument("--video3", type=str, help="Path to the third video.")
    parser.add_argument("--video4", type=str, help="Path to the fourth video.")

    # video_slowmo 관련
    parser.add_argument("--speed_factor", type=float, default=1.0,
                        help="Speed factor for slowmo (0.5 -> half speed, 2.0 -> double speed).")
    parser.add_argument("--input_video", type=str, help="Input video path for slowmo.")

    # 컬러맵 관련
    parser.add_argument("--use_colormap", action="store_true",
                       help="Apply colormap to grayscale images")

    args = parser.parse_args()

    if args.function == "image_to_video":
        # image_dir 체크
        if not args.image_dir:
            parser.error("image_to_video requires --image_dir <folder path>")
        image_to_video(
            image_dir=args.image_dir,
            output_name=f"outputs/{args.output}",
            fps=args.fps
        )

    elif args.function == "image_to_video_gray16":
        if not args.image_dir:
            parser.error("image_to_video_gray16 requires --image_dir <folder path>")
        image_to_video_gray16(
            image_dir=args.image_dir,
            output_name=f"outputs/{args.output}",
            fps=args.fps
        )

    elif args.function == "image_to_video_color":
        if not args.image_dir:
            parser.error("image_to_video_color requires --image_dir")
        image_to_video_color(
            image_dir=args.image_dir,
            output_name=args.output,
            fps=args.fps,
            use_colormap=args.use_colormap
        )

    elif args.function == "video_composition2":
        if not (args.video1 and args.video2):
            parser.error("video_composition2 requires --video1 and --video2")
        video_composition2(args.video1, args.video2, args.output)

    elif args.function == "video_composition4":
        # 4개 영상 모두 필요
        if not (args.video1 and args.video2 and args.video3 and args.video4):
            parser.error("video_composition4 requires --video1, --video2, --video3, and --video4")
        video_composition4(args.video1, args.video2, args.video3, args.video4, args.output)

    elif args.function == "video_slowmo":
        if not args.input_video:
            parser.error("video_slowmo requires --input_video")
        video_slowmo(args.input_video, args.output, args.speed_factor)

if __name__ == "__main__":
    main()
