# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from typing import Dict, List

from composabl_core import SkillController

import numpy as np
from pdm.sensors import sensors

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
            
class PDMStrategy(SkillController):
    def __init__(self, *args, **kwargs):
        self.counter = 0

    async def compute_action(self, obs, action):
        #sensors_name = [s.name for s in sensors]
        #obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.counter += 1

        PDMS = [int(obs["section_0_induct_flow"]), int(obs["section_1_induct_flow"]), int(obs["section_2_induct_flow"]), int(obs["section_3_induct_flow"]), int(obs["section_4_induct_flow"])]
        action_ = PDMS.index(min(PDMS))
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
    



