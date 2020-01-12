
class CrossBrowserModel():

    def __init__(self, base, targets):
        self.base = {'browser': base, 'file': ''}
        self.targets = []
        self.differences_folder = ''
        for target in targets:
            self.targets.append({'browser': target, 'file': ''})

    def set_base_file(self, file_path):
        self.base['file'] = file_path

    def set_target_file(self, key, file_path):
        for target in self.targets:
            if target['browser'] == key:
                    target['file']= file_path

    def set_differences_folder(self, folder):
        self.differences_folder = folder
            