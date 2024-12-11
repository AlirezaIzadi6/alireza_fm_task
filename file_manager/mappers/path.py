class Resource:
    def __init__(self, complete_path):
        if complete_path == '':
            self.name = 'index'
            self.path = ''
        else:
            path_splitted = complete_path.split('/')
            if len(path_splitted) == 1:
                self.name = complete_path
                self.path = ''
            else:
                self.name = path_splitted[-1]
                self.path = '/'.join(path_splitted[:-1])