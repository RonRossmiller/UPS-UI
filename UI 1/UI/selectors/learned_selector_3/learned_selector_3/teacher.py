import math

import numpy as np
from composabl import Teacher, SkillTeacher
from learned_selector_3.sensors import sensors

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
        ##print(transformed_obs)
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

        if sim_reward == 0:
            reward = 0

        # deal with delayed reward
        # PDM = Package Density per Minute
        PDM_trailer = 16 * (0.103 * float(transformed_obs['trailer_1_percent_large_primary']) + 0.25 * float(transformed_obs['trailer_1_percent_small_primary'])  + 1 * float(transformed_obs['trailer_1_percent_small']))
        PDMS = [int(transformed_obs["section_0_induct_flow"]), int(transformed_obs["section_1_induct_flow"]), int(transformed_obs["section_2_induct_flow"]), int(transformed_obs["section_3_induct_flow"]), int(transformed_obs["section_4_induct_flow"])]
        PDMS[action] = PDMS[action] + PDM_trailer

        #reward = math.exp(-0.1 * np.std(PDMS))
        #reward = math.exp(-0.1 * np.median(PDMS))
        reward = math.exp(-0.1 * np.sum(self.total_yard)) 
        reward = math.exp(-0.001 * np.sum(self.total_induct_std)) + math.exp(-0.1 * np.sum(self.total_yard)) + math.exp(-1 * abs(section_usage_reward))


        self.reward_history.append(reward)
        
        self.count += 1
        self.last_action = action

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        if self.count >= 300:
            return True
        else:
            return False
