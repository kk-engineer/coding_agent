class StepLogger:

    def __init__(self):
        self.steps = []

    def add(self, step_type, content):

        self.steps.append({
            "type": step_type,
            "content": content
        })

    def get_steps(self):

        return self.steps