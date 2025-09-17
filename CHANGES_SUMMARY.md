# 数据结构修改总结

## 📋 主要修改内容

### 1. 场景重命名
- `cityflow` → `outdoor`
- `mtmmc` → `indoor`

### 2. 任务类型重命名
- `MotionReasoning` → `MotionState`
- `TemporalReasoning` → `ArrivalTimeInterval`
- `SpatialReasoning` → `GeoLocation`
- `TimelineInference` → `CasualReordering`
- `NextCameraForecasting` → `NextSpotForecasting`

### 3. 文件结构变更
- **视频文件**: 文件名前缀从 `cityflow_*`/`mtmmc_*` 改为 `outdoor_*`/`indoor_*`
- **地图文件**: 
  - 目录从 `./media/` 改为 `./map/`
  - 文件名前缀更新为新的任务名称（如 `timeline_map_*` → `CasualReordering_map_*`）
- **JSON文件**: 只保留 `cases` 字段，删除其他所有字段

### 4. 字段更新
- `task_id`: 更新为新的任务名称
- `map_image_path`: 路径和文件名都更新
- `video_path` 和 `crop_video_path`: 文件名前缀更新

## 🔧 app.py 修改内容

### 1. 场景选择更新
```python
# 原来
scene = st.selectbox("选择场景", ["cityflow", "mtmmc"], index=0)

# 现在
scene = st.selectbox("选择场景", ["outdoor", "indoor"], index=0)
```

### 2. 任务类型映射更新
```python
# 原来
task_types = {
    "cityflow": ["MotionReasoning", "SpatialReasoning", ...],
    "mtmmc": ["MotionReasoning", "SpatialReasoning", ...]
}

# 现在
task_types = {
    "outdoor": ["MotionState", "GeoLocation", ...],
    "indoor": ["MotionState", "GeoLocation", ...]
}
```

### 3. 任务描述更新
```python
# 原来
"MotionReasoning": "运动推理 - 选择题"
"TimelineInference": "时间线推理 - 选择题"

# 现在
"MotionState": "运动状态推理 - 选择题"
"CasualReordering": "因果重排序推理 - 选择题"
```

### 4. 特殊处理：CasualReordering任务
对于 `CasualReordering` 任务（原 `TimelineInference`），不显示摄像头的时间范围信息：

```python
# 对于CasualReordering任务，不显示时间范围
if task_type == "CasualReordering":
    expander_title = f"📹 摄像头 {camera_id}"
else:
    # 显示时间范围
    start_time_str = seconds_to_time_format(camera['start_timestamp'])
    end_time_str = seconds_to_time_format(camera['end_timestamp'])
    expander_title = f"📹 摄像头 {camera_id} (时间: {start_time_str} - {end_time_str})"
```

### 5. 路径处理更新
- 默认场景从 `mtmmc` 改为 `indoor`
- 替代路径查找也相应更新

## ✅ 验证要点

1. **场景选择**: 确保可以选择 `outdoor` 和 `indoor`
2. **任务类型**: 确保所有新的任务类型都能正确加载
3. **地图显示**: 确保地图文件路径正确，能正常显示
4. **视频显示**: 确保视频文件路径正确，能正常播放
5. **CasualReordering**: 确保不显示时间范围信息
6. **答题界面**: 确保不同任务类型的答题界面正确显示

## 📁 文件结构
```
data/
├── outdoor/
│   ├── outdoor_MotionState_30.json
│   ├── outdoor_GeoLocation_30.json
│   ├── outdoor_ArrivalTimeInterval_30.json
│   ├── outdoor_CasualReordering_30.json
│   ├── outdoor_NextSpotForecasting_30.json
│   ├── outdoor_TrajectoryForecasting_30.json
│   ├── outdoor_MultiTrajectoryForecasting_30.json
│   ├── raw_video/ (outdoor_* 文件)
│   ├── crop_video/ (outdoor_* 文件)
│   └── map/ (新任务名称前缀的PNG文件)
└── indoor/
    ├── indoor_MotionState_30.json
    ├── indoor_GeoLocation_30.json
    ├── indoor_ArrivalTimeInterval_30.json
    ├── indoor_CasualReordering_30.json
    ├── indoor_NextSpotForecasting_30.json
    ├── indoor_TrajectoryForecasting_30.json
    ├── indoor_MultiTrajectoryForecasting_30.json
    ├── raw_video/ (indoor_* 文件)
    ├── crop_video/ (indoor_* 文件)
    └── map/ (新任务名称前缀的PNG文件)
```
