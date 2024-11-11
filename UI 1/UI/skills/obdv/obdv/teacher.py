import math

import numpy as np
from composabl import Teacher, SkillTeacher
from obdv.sensors import sensors

class UPSTeacher(Teacher):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.count = 0
        self.sim_reward_history = []
        self.metrics = 'none' # standard, fast, none
        self.outbound_list = []
        self.total_yard = []
        self.total_induct = []
        self.total_induct_std = []
        self.total_sim_pct = []
        self.last_action = None

    async def transform_sensors(self, obs, action):
        return obs

    async def transform_action(self, transformed_obs, action):
        return action

    async def filtered_sensor_space(self):
        return [sensor.name for sensor in sensors]

    async def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        self.sim_reward_history.append(sim_reward)

        sim_pcts = [float(transformed_obs["section_0_occupied_doors_pct"]), float(transformed_obs["section_1_occupied_doors_pct"]), float(transformed_obs["section_2_occupied_doors_pct"]), float(transformed_obs["section_3_occupied_doors_pct"]), float(transformed_obs["section_4_occupied_doors_pct"])]
        section_usage_reward = max(sim_pcts) - min(sim_pcts)
        self.outbound_list.append(float(transformed_obs['hub_outbound_std_sum']))
        self.total_yard.append(float(transformed_obs['trailers_in_yard']))
        self.total_induct_std.append(sim_reward)
        self.total_sim_pct.append(min([float(transformed_obs["section_0_occupied_doors_pct"]), float(transformed_obs["section_1_occupied_doors_pct"]), float(transformed_obs["section_2_occupied_doors_pct"]), float(transformed_obs["section_4_occupied_doors_pct"])]))

        reward = math.exp(-1e-6 * np.sum(self.outbound_list))


        self.reward_history.append(reward)
    
        self.count += 1
        self.last_action = action

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        if type(transformed_obs) == list or type(transformed_obs) == np.ndarray:
            # last mask is for AF-3
            pcts = [int(transformed_obs[-12]), int(transformed_obs[-10]), int(transformed_obs[-8]), int(transformed_obs[-6]), int(transformed_obs[-4]), 1]
        else:
            pcts = [int(transformed_obs["section_0_occupied_doors_pct"]), int(transformed_obs["section_1_occupied_doors_pct"]), int(transformed_obs["section_2_occupied_doors_pct"]), int(transformed_obs["section_3_occupied_doors_pct"]), int(transformed_obs["section_4_occupied_doors_pct"]), 1]
        
        #print(pcts)
        mask = np.array([0 if x >=1 else 1 for x in pcts])
        return mask

    async def compute_success_criteria(self, transformed_obs, action):
        if self.obs_history is None:
            success = False
        else:
            success = False
            if self.metrics == 'standard':
                try:
                    self.plot_obs()
                    self.plot_metrics()
                except Exception as e:
                    print('Error: ', e)

        return success

    async def compute_termination(self, transformed_obs, action):
        if self.count >= 200:
            return True
        else:
            return False
