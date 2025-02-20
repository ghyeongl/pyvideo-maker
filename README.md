# pyvideo-maker

이 저장소는 이미지 시퀀스를 동영상으로 만들거나, 여러 영상을 합치거나, 영상 속도를 조절하는 등의 작업을 간단히 수행할 수 있는 스크립트를 제공합니다.

## 주요 기능

1. **image_to_video**  
   - 일반 컬러 이미지(8비트)를 하나의 영상으로 생성
   
2. **image_to_video_gray16**  
   - 16비트 흑백 이미지를 0~65535 범위를 0~255로 정규화하여 영상 생성
   
3. **image_to_video_color**  
   - 16비트(혹은 8비트) 흑백 이미지를 정규화하고, (옵션) 컬러맵을 적용하여 영상 생성
   
4. **video_composition2**  
   - 두 영상을 좌우로 붙여 하나의 영상으로 만듦
   
5. **video_composition4**  
   - 네 영상을 2×2 격자로 합침
   
6. **video_slowmo**  
   - 기존 영상을 슬로우 모션(더 느리게) 또는 빠른 재생(더 빠르게)으로 변환

---

## 설치 및 환경 설정

1. **conda 환경 파일**을 사용하거나, `pip`로 직접 의존성(moviepy, pillow, numpy, opencv-python 등)을 설치합니다.
2. (예) conda-forge 채널 이용:
   ```bash
   conda install -c conda-forge ffmpeg moviepy opencv pillow numpy
   ```
   - `ffmpeg`가 최신 버전이어야 동영상 인코딩 관련 오류가 발생하지 않습니다.

3. **python main.py** 명령으로 스크립트를 실행할 수 있습니다.

---

## 사용법

아래 예시들은 `python main.py <기능> [추가 옵션들]` 형식으로 작성합니다.

### 1) image_to_video

- **설명**: 일반 8비트(RGB) 이미지들을 순차적으로 이어 붙여 한 편의 영상을 만듭니다.
- **옵션**:
  - `--image_dir <폴더 경로>`: 이미지들이 있는 폴더
  - `--output <결과 영상 파일 이름>` (기본값: `output.mp4`)
  - `--fps <초당 프레임>` (기본값: 24)

#### 예시
```bash
python main.py image_to_video \
    --image_dir ./images \
    --output sample_video.mp4 \
    --fps 30
```

### 2) image_to_video_gray16

- **설명**: 16비트 흑백 이미지(Depth 등)를 0~255 범위로 정규화하여 영상 생성.
- **옵션**:
  - `--image_dir <폴더 경로>`
  - `--output <결과 영상 파일 이름>`
  - `--fps <초당 프레임>`

#### 예시
```bash
python main.py image_to_video_gray16 \
    --image_dir ./depth_images \
    --output depth_video.mp4 \
    --fps 24
```
- 이 경우, 폴더 안에 있는 TIFF나 PNG 등(16비트 그레이스케일)을 자동 정규화해 하나의 영상으로 만듭니다.

### 3) image_to_video_color

- **설명**: 16비트(또는 8비트) 흑백 이미지를 정규화한 후, **컬러맵**(기본 `COLORMAP_JET`)을 적용하여 영상 생성할 수 있습니다.
- **옵션**:
  - `--image_dir <폴더 경로>`
  - `--output <결과 영상 파일 이름>`
  - `--fps <초당 프레임>`
  - `--use_colormap`: 해당 옵션을 추가하면 OpenCV 컬러맵을 적용하여 다양한 색상으로 시각화

#### 예시
```bash
# 컬러맵 적용하지 않음 (흑백)
python main.py image_to_video_color \
    --image_dir ./depth_images \
    --output grayscale_depth.mp4

# 컬러맵 적용 (JET)
python main.py image_to_video_color \
    --image_dir ./depth_images \
    --output color_depth.mp4 \
    --use_colormap
```

### 4) video_composition2

- **설명**: 두 영상을 좌우로 나란히 붙여 하나의 영상으로 만듭니다.
- **옵션**:
  - `--video1 <영상1 경로>`
  - `--video2 <영상2 경로>`
  - `--output <결과 영상 파일 이름>`

#### 예시
```bash
python main.py video_composition2 \
    --video1 first.mp4 \
    --video2 second.mp4 \
    --output side_by_side.mp4
```

### 5) video_composition4

- **설명**: 네 영상을 2×2 형태로 배치한 하나의 영상을 생성합니다.
- **옵션**:
  - `--video1 <영상1 경로>`
  - `--video2 <영상2 경로>`
  - `--video3 <영상3 경로>`
  - `--video4 <영상4 경로>`
  - `--output <결과 영상 파일 이름>`

#### 예시
```bash
python main.py video_composition4 \
    --video1 a.mp4 \
    --video2 b.mp4 \
    --video3 c.mp4 \
    --video4 d.mp4 \
    --output four_grid.mp4
```

### 6) video_slowmo

- **설명**: 기존 영상을 슬로우 모션(더 느리게) 또는 빠른 재생(더 빠르게)으로 변환.
- **옵션**:
  - `--input_video <원본 영상 경로>`
  - `--output <결과 영상 파일 이름>`
  - `--speed_factor <재생 속도 배율>`:  
    - `< 1`: 슬로우 모션(예: 0.5 -> 2배 느려짐)  
    - `> 1`: 빠른 재생(예: 2.0 -> 2배 빠름)

#### 예시
```bash
# 0.5 -> 절반 속도 (2배 길어짐)
python main.py video_slowmo \
    --input_video original.mp4 \
    --output slow.mp4 \
    --speed_factor 0.5

# 2.0 -> 2배속
python main.py video_slowmo \
    --input_video original.mp4 \
    --output fast.mp4 \
    --speed_factor 2.0
```

---

## 주의 사항

- **FFmpeg 버전**  
  - MoviePy로 영상 인코딩 시 구버전 ffmpeg(특히 4.0 이전)에서는 `-preset` 등 일부 옵션을 인식하지 못할 수 있습니다.  
  - 가급적 `conda-forge` 등에서 **최신 ffmpeg**를 설치하세요.

- **이미지 해상도**  
  - MoviePy의 `ImageSequenceClip`은 모든 이미지가 동일 해상도가 아니면 오류가 발생할 수 있습니다.  
  - 본 스크립트는 내부적으로 `resize(newsize=target_size)` 등을 이용해 첫 번째 이미지 해상도에 맞춰 다른 이미지를 강제 리사이즈합니다.

- **16비트 Depth**  
  - 단순 변환(`convert("RGB")`) 시 매우 어두워지거나 하얗게만 보일 수 있습니다.  
  - `image_to_video_gray16` 또는 `image_to_video_color`처럼 **정규화** 과정을 거치면, 차이를 눈으로 확인하기 쉬운 형태로 시각화할 수 있습니다.

---

## 라이선스
- 본 코드의 의존 라이브러리는 각각 자체 라이선스를 따릅니다.  
- 예시 코드 자체는 자유롭게 수정/활용 가능합니다.