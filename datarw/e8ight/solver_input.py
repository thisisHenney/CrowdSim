from nextlib.tools.json_tool import JsonTool


class SolverData:
    def __init__(self, filename=''):
        self.data = JsonTool()
        self.file = filename

    def create(self, filename='', version=202405, method='SPH2D', title=''):
        if filename != '':
            self.file = filename

        self.data.create(self.file)
        self.data.add("meta", {
            "version": version,
            "method": method,
            "title": title
        })
        self.data.add("config", {"comment": "This is a comment"})
        self.data.add("config", {"solver_common": {
            "solver_type": "CROWD",
            "simulation_start_time": 0.0,
            "simulation_end_time": 20.0,
            "time_step": 0.02,
            "pathfield_iteration": 2,

            "radius": 0.25,
            "H": 1,
            "s_pref": 1.4,
            "s_max": 1.8,
            "a_max": 9999999999.9,

            "K_obs": 200.0,
            "K_ag": 50.0,
            "K_goal": 1.0,

            "tau": 0.5,
            "V_0": 2.1,
            "sigma": 0.3,
            "T": 2.0,
            "U_0": 2.1,
            "R": 0.1,

            "w": 1.0,
            "k": 200.0,
            "T_p": 0.1,

            "blending": {
                "collision_avoidance": "SF",
                "is_blending": True,
                "collision_density": 2.0,
                "sph_density": 4.0
              },

            "initial_velocity": [0, 0],
            "devices": [0]
        }})

        self.data.add("config", {'grid': []})
        self.data.add("config", {'materials': []})
        self.data.add("config", {'particle_generation': []})
        self.data.add("config", {'inlet': []})
        self.data.add("config", {'outlet': []})
        self.data.add("config", {'result_report': {}})

    def add_grid(self, name='dummy'):
        self.data.add('config.grid', {
            "name": name,
            "domain": {
                "min": [-11, -11, 1],
                "max": [11, 11, 1]
            },
            "width": -1,
            "max_particle": 10000,
            "comment": "max_particle는 초기화시 allocate할 입자 수. 너무 크게 잡으면 메모리가 부족할 수 있음. 이후 동적으로 늘어남"
        })

    def add_material(self, name='solid', is_main=False):
        self.data.add('config.materials', {
            "name": name,
            "is_main_material": is_main,
            "rho_min": 0,
            "rho_max": 5,
            "mu": 0.0,
            "outlet_id": -1
        })

    def add_particle_generation(self, grid=0):
        self.data.add('config.particle_generation', {
            "two_dimensional": True,
            "domain_general": True,
            "path_field": False,
            "is_manhattan": False,
            "pwb": False,
            "base_dx": 0.4,
            "base_region": {
                "min": [
                    -12,
                    -12,
                    0
                ],
                "max": [
                    12,
                    12,
                    1
                ]
            },
            "regional_segment": [],
            "grid": grid
        })

    def add_particle_generation_regional_segment(self, index, name='', path='', invert=False, material='', region_type=''):
        self.data.add(f'config.particle_generation[{index}].regional_segment',
            {
                    "name": name,
                    "mesh_path": path,
                    "invert_normal": invert,
                    "material": material,
                    "region_type": region_type
                }
            )

    def add_particle_generation_binary(self, path="binary_data_test", material="fluid", grid=0):
        self.data.add('config.particle_generation', {
            "binary_path": path,
            "material": material,
            "grid": grid
        })

    def add_inlet(self, _type='CROWD'):
        if _type == 'CROWD':
            self.data.add('config.inlet', {
                "name": "",
                "type": _type,
                "exclude_outlets": [],
                "p1": [0, 0],
                "p2": [0, 0],
                "velocity": [1.4, 0],
                "dx": 1,
                "interval": 100,
                "start_time": 0,
                "end_time": 0,
                "material_index": 1,
                "grid": 1,
                "outlet_index": -1
            })

    def add_outlet(self, is_point=True, num=0):
        if is_point:
            self.data.add('config.outlet', {
                "name": "outlet",
                "num": num,
                "type": 'point',
                "is_erase": False,
                "p1": [0, -11],
                "grid": 1
            })
        else:
            self.data.add('config.outlet', {
                "name": "outlet",
                "num": num,
                "type": 'line',
                "is_erase": False,
                "p1": [0, -11],
                "p2": [0, -11],
                "grid": 1
            })

    def add_result_report(self):
        self.data.add('config.result_report', {
            "export_path": "",
            "export_format": [
                "BINARY_VTK",
                "NFILE"
            ],
            "save_start_time": 0.0,
            "save_end_time": 100,
            "save_time_interval": 0.1,
            "items": {
                "density": True,
                "pressure": True,
                "restDensity": True,  # "rest_density": True,
                "position": True,
                "velocity": True,
                "goal_position": True,
                "adjoint": True,
                "prt_idx": True,
                "forward_vector": True,
                "line_id": True,
                "acceleration_collision": True
            },
            "flags": {
                "path_goal_point": False,
                "path_solid": False
            }
        })

    def save(self):
        self.data.save()

    def load(self, filename):
        self.file = filename
        self.data = JsonTool()
        self.data.read(filename)



if __name__ == "__main__":
    # solver = SolverData()
    # solver.create('./test.json')
    # solver.add_grid('dummy')
    # solver.add_grid('fluid')
    # solver.add_material('solid')
    # solver.add_material('fluid', True)
    # solver.add_particle_generation('solid', "room_evacuation_basic.stl", "solid", 0)
    # solver.add_particle_generation('fluid', "room_evacuation_basic_agent.stl", "fluid", 1)
    # # solver.add_inlet("CROWD")
    # solver.add_outlet("point")
    # solver.save()

    # solver = SolverData()
    # solver.create('/home/test/Desktop/Test1/test1.json')
    # solver.add_grid('dummy')
    # solver.add_grid('fluid')
    # solver.add_material('solid')
    # solver.add_material('fluid', True)
    # solver.add_particle_generation('solid')
    # solver.add_particle_generation('fluid')
    # solver.add_particle_generation_regional_segment("test1.stl", "solid", 0)
    # solver.add_particle_generation_regional_segment("test1_agent_small_2.stl", "fluid", 1)
    # solver.add_result_report(0.02)

    # # solver.add_inlet("CROWD")
    # solver.add_outlet("point")
    # solver.save()
    ...
