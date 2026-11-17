"""check every model files which named stl or STL
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

    # <compiler meshdir="../../meshes/ned2/stl"> 
    meshdir = (MJCF_DIR / root.find("compiler").get("meshdir")).resolve()
    real_names = set(os.listdir(meshdir))

    # find out all <mesh file="..."/>
    missing = [
        mesh.get("file")
        for mesh in root.iter("mesh")
        if mesh.get("file") not in real_names
    ]
    assert missing == [], f"{model_file} 引用了不存在的网格文件（注意大小写）：{missing}"