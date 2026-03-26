from nextlib.tools.json_tool import JsonTool


class ResultData:
    def __init__(self):
        self.data = JsonTool()

        self.width = 0
        self.height = 0
        self.grid_size = []
        self.map_name = ''
        self.density = []
        self.velocity = []
        self.event = ''

    def get(self, filename):
        self.data.read(filename)

        self.width = self.data.get('width')
        self.height = self.data.get('height')
        self.grid_size = self.data.get('gridsize')

        self.map_name = self.data.get('map_name')

        self.density = self.data.get('density')
        self.velocity = self.data.get('velocity')

        self.event = self.data.get('event')


class ResultOutput:
    def __init__(self, path=''):
        self.path = path
        self.file = ''
        self.result = ResultData()

    def read_last_data(self):
        last_file = f'{self.path}/000001.log'
        self.file = last_file

        self.result.get(self.file)

        print(self.result.width, self.result.height)
        print(self.result.grid_size, self.result.map_name)
        print(self.result.density)
        print(self.result.velocity)
        print(self.result.event)
