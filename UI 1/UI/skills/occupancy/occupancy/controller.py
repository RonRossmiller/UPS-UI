# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from typing import Dict, List

from composabl_core import SkillController

import numpy as np
from usage.sensors import sensors

def constraint_action(obs, action):
    # GAYLORD
    if int(obs['trailer_1_load_composition']) == 4:
        return 3
    # SMALLS
    elif int(obs['trailer_1_load_composition']) == 5:
        return 3 # 'PS-1'
    # ULD
    elif int(obs['trailer_1_load_composition']) == 7:
        return 5 
    # IRREG
    elif int(obs['trailer_1_load_composition']) == 1 or int(obs['trailer_1_load_composition']) == 0:
        if int(obs['irregular_available']) > 0:
            return 4 # 'PS-5'
        else:
            return action
    
    else:
        # NOT ULD - Hard Constraint
        if int(obs['trailer_1_load_composition']) != 7 and action == 5:
            return np.random.choice([0,1,2,3,4])
        else:
            return action
            
class UsageStrategy(SkillController):
    def __init__(self, *args, **kwargs):
        self.counter = 0

    async def compute_action(self, obs, action):
        pcts = [float(obs["section_0_occupied_doors_pct"]), float(obs["section_1_occupied_doors_pct"]), float(obs["section_2_occupied_doors_pct"]), float(obs["section_3_occupied_doors_pct"]), float(obs["section_4_occupied_doors_pct"]), 1]
        action_ = pcts.index(min(pcts))
        action2 = constraint_action(obs, action_)

        return action2
    
    async def transform_sensors(self, obs):
        return obs

    async def filtered_sensor_space(self):
        return [s.name for s in sensors]

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False
    



