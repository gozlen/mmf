import numpy as np

from pythia.core.registry import Registry


class MultiTask:
    def __init__(self, dataset_type, config):
        self.config = config
        self.dataset_type = dataset_type

        self.task_names = map(lambda x: x.strip(),
                              self.config['tasks'].split(","))

        self.tasks = []
        self.tasks_lens = []

        for task_name in self.task_names:
            task_class = Registry.get_task_class(task_name)
            if task_class is None:
                print("[Error] %s not present in our mapping"
                      % task_name)
                return

            if task_name not in self.config['task_attributes']:
                print("[Error] No attributes present for task %s in config."
                      " Skipping" % task_name)

            task_attributes = self.config['task_attributes'][task_name]
            task_attributes['dataset_type'] = self.dataset_type

            task = task_class(**task_attributes)
            task.load()

            self.tasks.append(task)
            self.tasks_lens.append(len(task))

        self.task_probabilities = self.tasks_lens

        self.num_tasks = len(self.tasks)

        training_parameters = self.config['training_parameters']
        if training_parameters['task_size_proportional_sampling']:
            self.task_probabilities /= sum(self.tasks_lens)

        self.change_task()

    def change_task(self):
        self.selected_task = np.random.choice(self.num_tasks, 1,
                                              p=self.task_probabilities)
        self.chosen_task = self.tasks[self.selected_tasks]
        self.chosen_task.change_dataset()

    def calculate_loss(self, output, expected_output):
        loss = self.chosen_task.calculate_loss(output, expected_output)
        Registry.register('metrics.%s.loss' % self.dataset_type, loss)
        return loss

    def __len__(self):
        return sum(self.tasks_len)

    def __getitem__(self, idx):
        idx = idx % self.tasks_lens[self.selected_task]
        item = self.chosen_task[idx]

        return item

    def report_metrics(self, loss, extra_info=None, should_print=True):
        self.chosen_task.report_metrics(loss, extra_info, should_print)

    def update_config_for_model(self, config):
        for task in self.tasks:
            task.update_config_for_model(config)

    def prepare_batch(self, batch):
        return self.chosen_task.prepare_batch(batch)

    def init_args(self, parser):
        for task in self.tasks:
            task.init_args(parser)

    def clean_config(self, config):
        for task in self.tasks:
            task.clean_config(config)

        return config