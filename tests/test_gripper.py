"""Under the mode of mocap, the command should be settled on grippers"""
import gymnasium as gym
import numpy as np
import pytest

import niryo_gym  # noqa: F401


@pytest.mark.parametrize("gripper_cmd", [1.0, -1.0])
def test_mocap_gripper_command_reaches_actuators(gripper_cmd):

    env = gym.make("NiryoLift-v1", control_type="mocap")
    env.reset(seed=0)

    # check grippers' commands
    action = np.array([0.0, 0.0, 0.0, gripper_cmd])
    env.step(action)

    # check whether it is settled on grippers
    ctrl = env.unwrapped.data.ctrl
    np.testing.assert_allclose(ctrl, [gripper_cmd, gripper_cmd])

    env.close()