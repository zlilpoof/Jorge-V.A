import json
from users import user
import os

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()

    
    def load_config(self):
        with open(self.config_file, 'r') as f:
            self._config = json.load(f)
        for key, value in self._config.items():
            setattr(self, key, value)
            

    def save_config(self):
        for key, value in self._config.items():
            self._config[key] = getattr(self, key)
        with open(self.config_file, 'w') as f:
            json.dump(self._config, f, indent=4)
        

    def change_mic(self):
        self.mic_muted = not self.mic_muted
        self.save_config()
        return self.mic_muted
    
    
    def change_sound(self):
        self.sound_muted = not self.sound_muted
        self.save_config()
        return self.sound_muted
    
    
    def save(self, *args, **kwargs):
        questions = kwargs.get("questions")
        answers = kwargs.get("answers")
        if questions and answers:
            user.save(questions=questions, answers=answers)
        self.save_config()


config_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json'))
settings = Config(config_file)
