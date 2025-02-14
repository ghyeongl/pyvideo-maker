#!/usr/bin/env python
import os
import argparse

from moviepy.editor import (
    VideoFileClip, 
    ImageSequenceClip, 
    vfx, 
    clips_array
)

def image_to_video(images, output_name, directory=".", fps=24):
    """
    images에 지정된 이미지 파일 목록을 하나의 동영상으로 변환하여 output_name으로 저장.
    - images: 이미지 파일 이름 리스트 (예: ["img1.jpg", "img2.jpg", ...])
    - directory: 이미지들이 있는 디렉토리 경로
    - fps: 초당 프레임 수
    """
    # 디렉토리 + 파일명 합쳐서 전체 경로 구성
    image_paths = [os.path.join(directory, img) for img in images]

    # ImageSequenceClip 생성
    clip = ImageSequenceClip(image_paths, fps=fps)

    # 동영상 저장
    clip.write_videofile(output_name, codec="libx264")

def video_composition2(video1_path, video2_path, output_name="composition2.mp4"):
    """
    2개의 영상을 좌우로 나란히 붙여서 output_name으로 저장.
    """
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)

    # clips_array([[clip1, clip2]]) -> 1행 2열(가로로 붙임)
    final_clip = clips_array([[clip1, clip2]])
    final_clip.write_videofile(output_name, codec="libx264")

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
    final_clip.write_videofile(output_name, codec="libx264")

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
    modified_clip.write_videofile(output_video, codec="libx264")

def main():
    parser = argparse.ArgumentParser(description="Video Processing Tools")

    # 실행할 기능
    parser.add_argument(
        "function",
        type=str,
        choices=["image_to_video", "video_composition2", "video_composition4", "video_slowmo"],
        help="Choose which function to run."
    )

    # 공통 매개변수
    parser.add_argument("--output", type=str, default="output.mp4", help="Output video file name.")

    # image_to_video 관련
    parser.add_argument("--images", nargs="+", help="List of image file names.")
    parser.add_argument("--directory", type=str, default=".", help="Directory containing images.")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second for image_to_video.")

    # video_composition2 관련
    parser.add_argument("--video1", type=str, help="Path to the first video.")
    parser.add_argument("--video2", type=str, help="Path to the second video.")

    # video_composition4 관련
    parser.add_argument("--video3", type=str, help="Path to the third video.")
    parser.add_argument("--video4", type=str, help="Path to the fourth video.")

    # video_slowmo 관련
    parser.add_argument("--speed_factor", type=float, default=1.0, help="Speed factor for slowmo (0.5 -> half speed, 2.0 -> double speed).")
    parser.add_argument("--input_video", type=str, help="Input video path for slowmo.")

    args = parser.parse_args()

    if args.function == "image_to_video":
        if not args.images:
            parser.error("image_to_video requires --images <list of image filenames>")
        image_to_video(
            images=args.images,
            output_name=args.output,
            directory=args.directory,
            fps=args.fps
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
