
import tensorflow

class Tracker(tensorflow.keras.callbacks.Callback):
    def __init__(self, return_at: callable):
        super(Tracker, self).__init__()
        self.return_data = return_at
        self.stats = {
            'Training Loss'      : [],
            'Validation Loss'    : [],
            'Training Accuracy'  : [],
            'Validation Accuracy': []
        }

    def on_epoch_begin(self, epoch, logs=None):
        self.return_data(epoch=epoch)

    def on_train_batch_end(self, batch, logs=None):
        self.return_data(
            training_batch=batch,
            training_accuracy=logs['accuracy'],
            training_loss=logs['loss']
        )

    def on_test_begin(self, logs=None):
        self.return_data(val_eval=True)

    def on_test_batch_end(self, batch, logs=None):
        self.return_data(
            val_eval_batch=batch,
            val_eval_accuracy=logs['accuracy'],
            val_eval_loss=logs['loss'],
        )

    def on_epoch_end(self, epoch, logs=None):
        self.return_data(epoch=epoch)
        self.stats['Training Accuracy'].append(logs['accuracy'])
        self.stats['Training Loss'].append(logs['loss'])
        self.stats['Validation Accuracy'].append(logs['val_accuracy'])
        self.stats['Validation Loss'].append(logs['val_loss'])

    def on_train_end(self, logs=None):
        self.return_data(stats=self.stats)
