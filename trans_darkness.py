import cv2
import numpy as np
import os
import argparse

def adjust_brightness_pixel_multiply(image_path, output_path, darkness_factor):
    """
    (논문 방식) 이미지를 읽어와 모든 픽셀 값(BGR)에 
    darkness_factor를 직접 곱하여 밝기를 조절합니다.
    
    :param image_path: 원본 이미지 경로
    :param output_path: 저장할 이미지 경로
    :param darkness_factor: 명도 조절 계수
                           - 0.1 = 매우 어두움 (픽셀 값의 10%만 사용)
                           - 0.5 = 중간 정도 어두움 (픽셀 값의 50%만 사용)
                           - 0.9 = 약간 어두움 (픽셀 값의 90%만 사용)
                           - 1.0 = 원본 (변화 없음)
                           값이 클수록 밝고, 작을수록 어둡습니다.
    """
    try:
        # 1. 이미지를 BGR 순서로 읽어옵니다.
        image = cv2.imread(image_path)
        if image is None:
            print(f"경고: 이미지를 읽을 수 없습니다: {image_path}")
            return

        # 2. (중요!) 픽셀 곱셈 연산을 위해 이미지 타입을 float32로 변환합니다.
        #    (원본 uint8은 0~255 정수라서 0.5 같은 실수를 곱하면 0이 됩니다.)
        image_float = image.astype(np.float32)

        # 3. (핵심) 논문에 명시된 대로, BGR 모든 픽셀 값에 
        #    darkness_factor를 직접 곱합니다.
        #    예: factor=0.1이면 매우 어두워지고, factor=0.9이면 약간만 어두워집니다.
        image_darkened_float = image_float * darkness_factor
        
        # 4. 값이 0~255 범위를 벗어나지 않도록 클리핑(clipping)합니다.
        image_darkened_float = np.clip(image_darkened_float, 0, 255)

        # 5. 이미지를 저장하기 위해 다시 8비트 정수(uint8)로 변환합니다.
        final_bgr = image_darkened_float.astype(np.uint8)

        # 6. 결과 이미지를 지정된 경로에 저장합니다.
        cv2.imwrite(output_path, final_bgr)

    except Exception as e:
        print(f"오류 발생 ({image_path}): {e}")

# --- 스크립트 실행 부분 ---
if __name__ == "__main__":
    
    # 명령줄 인자 파서 설정
    parser = argparse.ArgumentParser(description='이미지의 밝기를 조절합니다.')
    parser.add_argument('--level', type=float, default=None,
                        help='적용할 어둠 수준 (0.1 ~ 1.0). 값이 작을수록 어둡고, 1.0은 원본. 지정하지 않으면 모든 수준 적용')
    args = parser.parse_args()
    
    # 1. 원본 FACET 이미지들이 있는 폴더 경로
    source_dir = "/home/dohyeong/Desktop/COCO/val2017(origin)" 
    
    # 2. 어둡게 변경된 이미지들을 저장할 상위 폴더 경로
    output_base_dir = "/home/dohyeong/Desktop/COCO/FACET_darkness_test"
    
    # 3. 적용할 어둠 수준 결정
    if args.level is not None:
        # --level 인자가 제공된 경우, 해당 수준만 사용
        darkness_levels = [args.level]
        print(f"지정된 수준 {args.level:.1f}로만 처리합니다.")
    else:
        # --level 인자가 없는 경우, 모든 수준 사용
        darkness_levels = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        print("모든 어둠 수준에 대해 처리합니다.")

    # 모든 어둠 수준에 대해 반복
    for level in darkness_levels:
        
        # 각 수준별로 하위 폴더 생성 (예: "./FACET_darkness_test/darkness_0.5")
        current_output_dir = os.path.join(output_base_dir, f"darkness_{level:.1f}")
        os.makedirs(current_output_dir, exist_ok=True)
        
        print(f"--- {level:.1f} 수준 (논문 방식)으로 밝기 조절 시작 ---")

        # 원본 이미지 폴더의 모든 파일을 순회
        for filename in os.listdir(source_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                
                # 원본 파일 경로
                original_file_path = os.path.join(source_dir, filename)
                
                # 저장할 파일 경로
                output_file_path = os.path.join(current_output_dir, filename)
                
                # 밝기 조절 함수(논문 방식) 실행
                adjust_brightness_pixel_multiply(original_file_path, output_file_path, level)
    
    print("--- 모든 작업 완료 ---")