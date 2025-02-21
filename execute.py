# execute.py
from main import image_to_video, video_slowmo, image_to_video_gray16
import os

def main():
    # (예시) 여러 작업을 한번에 수행하기 위해 파이썬 함수 직접 호출
    # 1) 첫 번째 작업: 이미지 폴더 -> 영상 만들기
    # gt
    image_to_video_gray16(
        image_dir="inputs/gs3lam/office0-gt/depth",
        output_name="outputs/gs3lam/office0-gt-depth.mp4",
        fps=30
    )
    
    image_to_video(
        image_dir="inputs/gs3lam/office0-gt/frame",
        output_name="outputs/gs3lam/office0-gt-frame.mp4",
        fps=30
    )
    
    image_to_video(
        image_dir="inputs/gs3lam/office0-gt/semantic_class",
        output_name="outputs/gs3lam/office0-gt-semantic.mp4",
        fps=30
    )

    # 2) 두 번째 작업: 또 다른 이미지 폴더 -> 영상
    # render
    image_to_video(
        image_dir="inputs/gs3lam/office0-render/eval/rendered_depth",
        output_name="outputs/office0-rd-depth.mp4",
        fps=30
    )
    
    image_to_video(
        image_dir="inputs/gs3lam/office0-render/eval/objects_feature16",
        output_name="outputs/office0-rd-obfeature.mp4",
        fps=30
    )
    
    image_to_video(
        image_dir="inputs/gs3lam/office0-render/eval/rendered_object",
        output_name="outputs/office0-rd-seclass.mp4",
        fps=30
    )
    
    image_to_video(
        image_dir="inputs/gs3lam/office0-render/eval/rendered_rgb",
        output_name="outputs/office0-rd-rgb.mp4",
        fps=30
    )

    print("[INFO] All tasks completed!")

if __name__ == "__main__":
    main()
