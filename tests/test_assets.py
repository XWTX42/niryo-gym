"""检查 MJCF 模型文件里引用的每个网格文件，都以完全相同的大小写存在。

为什么不直接用 os.path.exists？
macOS 默认文件系统不区分大小写：问 "a.stl 存在吗"，有 a.STL 也会回答"存在"。
所以在 Mac 上 exists() 永远发现不了这个 bug。
os.listdir() 返回的是磁盘上真实的文件名，拿它逐字比较，在任何系统上都能发现问题。
"""
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

MJCF_DIR = Path(__file__).resolve().parents[1] / "niryo_gym" / "niryo_robot" / "mjcf" / "ned2"
MODEL_FILES = ["ned2.xml", "ned2mocap.xml", "ned2free.xml"]


@pytest.mark.parametrize("model_file", MODEL_FILES)
def test_mesh_files_exist_with_exact_case(model_file):
    root = ET.parse(MJCF_DIR / model_file).getroot()

    # <compiler meshdir="../../meshes/ned2/stl"> 规定了网格文件放在哪；它是相对于 XML 文件所在目录的
    meshdir = (MJCF_DIR / root.find("compiler").get("meshdir")).resolve()
    real_names = set(os.listdir(meshdir))

    # 找出所有 <mesh file="..."/>，收集磁盘上不存在（按精确大小写）的那些
    missing = [
        mesh.get("file")
        for mesh in root.iter("mesh")
        if mesh.get("file") not in real_names
    ]
    assert missing == [], f"{model_file} 引用了不存在的网格文件（注意大小写）：{missing}"