import os

class User:
    def __init__(self, questions_file, answers_file):
        self.questions_file = questions_file
        self.answers_file = answers_file
        self.load_questions()
        self.load_answers()
    
    
    def load_questions(self):
        with open(self.questions_file, 'r') as f:
            lines = f.readlines()
        return [line.strip() for line in lines]


    def save_questions(self, data):
        with open(self.questions_file, 'w') as f:
            f.write('\n'.join(data))
            
            
    def load_answers(self):
        with open(self.answers_file, 'r') as f:
            lines = f.readlines()
        return [line.strip() for line in lines]


    def save_answers(self, data):
        with open(self.answers_file, 'w') as f:
            f.write('\n'.join(data))
            
            
    def reload(self):
        self.load_answers()
        self.load_questions()
            
            
    def save(self, questions, answers):
        try:
            self.save_questions(questions)
        except RuntimeError:
            print("UNABLE TO SAVE QUESTIONS")
        try:
            self.save_answers(answers)
        except RuntimeError:
            print("UNABLE TO SAVE ANSWERS")
        self.reload()
        
        
questions = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'questions.txt'))
answers = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'answers.txt'))
user = User(questions_file=questions, answers_file=answers)
