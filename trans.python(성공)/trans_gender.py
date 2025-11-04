import json
import os
from pathlib import Path

# JSON 파일 경로
json_path = "/home/dohyeong/Desktop/COCO/annotations/instances_all.json"
out_dir = Path("/home/dohyeong/Desktop/COCO/annotations/")

# 출력 디렉토리 생성
out_dir.mkdir(parents=True, exist_ok=True)

# JSON 파일 로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 성별 데이터 추출 (각 어노테이션의 gender_presentation_masc, gender_presentation_fem 값 가져오기)
annotations = data["annotations"]

# 남성과 여성 그룹 생성
men_annotations = []
women_annotations = []
men_image_ids = set()
women_image_ids = set()

# 각 어노테이션에서 성별 정보를 추출
for ann in annotations:
    gender_masc = ann["attributes"].get("gender_presentation_masc", 0)
    gender_fem = ann["attributes"].get("gender_presentation_fem", 0)
    
    # 남성인 경우 (gender_presentation_masc >= 1)
    if gender_masc >= 1:
        men_annotations.append(ann)
        men_image_ids.add(ann["image_id"])
    
    # 여성인 경우 (gender_presentation_fem >= 1)
    if gender_fem >= 1:
        women_annotations.append(ann)
        women_image_ids.add(ann["image_id"])

# 남성 그룹 JSON 생성
men_images = [img for img in data["images"] if img["id"] in men_image_ids]
coco_men = {
    "info": {"description": "FACET Gender Group - Men"},
    "licenses": [],
    "images": men_images,
    "annotations": men_annotations,
    "categories": [{"id": 1, "name": "person", "supercategory": "person"}],
}

# 남성 그룹 JSON 파일 저장
men_path = out_dir / "gender_men.json"
with open(men_path, "w", encoding="utf-8") as f:
    json.dump(coco_men, f, ensure_ascii=False)

print(f"Men Group → {men_path} (images={len(men_images)}, anns={len(men_annotations)})")

# 여성 그룹 JSON 생성
women_images = [img for img in data["images"] if img["id"] in women_image_ids]
coco_women = {
    "info": {"description": "FACET Gender Group - Women"},
    "licenses": [],
    "images": women_images,
    "annotations": women_annotations,
    "categories": [{"id": 1, "name": "person", "supercategory": "person"}],
}

# 여성 그룹 JSON 파일 저장
women_path = out_dir / "gender_women.json"
with open(women_path, "w", encoding="utf-8") as f:
    json.dump(coco_women, f, ensure_ascii=False)

print(f"Women Group → {women_path} (images={len(women_images)}, anns={len(women_annotations)})")
