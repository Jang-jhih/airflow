#!/bin/bash

# 定義要搜尋的資料夾列表
folders=("airflow" "superset" "volumn" "hadoop-spark")

# 遍歷資料夾並啟動每個資料夾中的 docker-compose
for folder in "${folders[@]}"; do
  if [ -d "$folder" ] && [ -f "$folder/docker-compose.yml" ]; then
    echo "啟動 $folder 中的 docker-compose"
    (cd "$folder" && docker-compose up -d)
  else
    echo "警告：$folder 資料夾不存在或 docker-compose.yml 文件缺失"
  fi
done

