from composabl import Sensor

obs_constraints = {
            # trailers vars
            "trailer_1_load_composition": {"low": -1 , "high": 100},
            "trailer_1_heat_vol_total": {"low": 0 , "high": 1000000},
            "trailer_1_percent_irregular": {"low": 0 , "high": 1000},
            "trailer_1_percent_small": {"low": 0 , "high": 1000},
            "trailer_1_percent_loose": {"low": 0 , "high": 1000},
            "trailer_1_percent_large_primary": {"low": 0 , "high": 1000},
            "trailer_1_percent_small_primary": {"low": 0 , "high": 1000},
            #"trailer_1_large_primary": {"low": 0 , "high": 10000},
            #"trailer_1_small_primary": {"low": 0 , "high": 10000},
            #"trailer_1_small": {"low": 0 , "high": 10000},
            #"trailer_1_irregular": {"low": 0 , "high": 10000},

            "trailer_1_origin_name": {"low": -1 , "high": 1000},
            "trailer_1_destination_name": {"low": -1 , "high": 1000},
            "trailer_1_load_origin": {"low": -1 , "high": 1000},
            # environment vars
            "hub_occupied_doors": {"low": 0 , "high": 1000},
            "hour_of_day": {"low": 0 , "high": 1000},
            #"last_action": {"low": 0 , "high": 1000},
            "irregular_available": {"low": 0 , "high": 100},

            "day_of_week": {"low": 0 , "high": 1000},
            "day_twilight": {"low": 0 , "high": 1000},
            "hub_outbound_std_sum": {"low": 0 , "high": 1000000},
            "trailers_in_yard": {"low": 0 , "high": 1000}
        }

#create sensors from obs_constraints
sensors = []

sensors.append(Sensor("trailer_1_load_composition", "", lambda obs: obs[0]))
sensors.append(Sensor("trailer_1_heat_vol_total", "", lambda obs: obs[1]))
sensors.append(Sensor("trailer_1_percent_irregular", "", lambda obs: obs[2]))
sensors.append(Sensor("trailer_1_percent_small", "", lambda obs: obs[3]))
sensors.append(Sensor("trailer_1_percent_loose", "", lambda obs: obs[4]))
sensors.append(Sensor("trailer_1_percent_large_primary", "", lambda obs: obs[5]))
sensors.append(Sensor("trailer_1_percent_small_primary", "", lambda obs: obs[6]))
sensors.append(Sensor("trailer_1_origin_name", "", lambda obs: obs[7]))
sensors.append(Sensor("trailer_1_type", "", lambda obs: obs[8]))
sensors.append(Sensor("trailer_1_load_origin", "", lambda obs: obs[9]))
sensors.append(Sensor("hub_occupied_doors", "", lambda obs: obs[10]))
sensors.append(Sensor("hour_of_day", "", lambda obs: obs[11]))
sensors.append(Sensor("irregular_available", "", lambda obs: obs[12]))

sensors.append(Sensor("day_of_week", "", lambda obs: obs[13]))
sensors.append(Sensor("day_twilight", "", lambda obs: obs[14]))
sensors.append(Sensor("hub_outbound_std_sum", "", lambda obs: obs[15]))
sensors.append(Sensor("trailers_in_yard", "", lambda obs: obs[16]))

sensors.append(Sensor("section_0_induct_flow", "", lambda obs: obs[17]))
sensors.append(Sensor("section_0_occupied_doors_pct", "", lambda obs: obs[18]))
sensors.append(Sensor("section_1_induct_flow", "", lambda obs: obs[19]))
sensors.append(Sensor("section_1_occupied_doors_pct", "", lambda obs: obs[20]))
sensors.append(Sensor("section_2_induct_flow", "", lambda obs: obs[21]))
sensors.append(Sensor("section_2_occupied_doors_pct", "", lambda obs: obs[22]))
sensors.append(Sensor("section_3_induct_flow", "", lambda obs: obs[23]))
sensors.append(Sensor("section_3_occupied_doors_pct", "", lambda obs: obs[24]))
sensors.append(Sensor("section_4_induct_flow", "", lambda obs: obs[25]))
sensors.append(Sensor("section_4_occupied_doors_pct", "", lambda obs: obs[26]))
sensors.append(Sensor("section_5_induct_flow", "", lambda obs: obs[27]))
sensors.append(Sensor("section_5_occupied_doors_pct", "", lambda obs: obs[28]))


