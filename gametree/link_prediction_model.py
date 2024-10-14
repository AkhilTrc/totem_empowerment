import tensorflow as tf
import tensorflow_docs as tfdocs
import tensorflow_docs.modeling
from gametree.visualization import Visualization
from tensorflow import keras
from tensorflow.keras import layers


class LinkPredictionModel():
    """Model that predicts links between elements.
    """
    def __init__(self, time, step, epochs=1, batch_size=32, steps_per_epoch=None, class_weight=None, output_bias=None, game_version='totem'):
        """Initializes a link prediction model.

        Args:
            time (str): Time that will be used as folder name for saving pictures.
            step (int): Iteration round.
            epochs (int, optional): Number of epochs to train the model. Defaults to 1.
            batch_size (int, optional): Number of samples per gradient update. Defaults to 32.
            steps_per_epoch (int, optional): Total number of steps (batches of samples) before declaring one epoch finished
                        and starting the next epoch. Defaults to None.
            class_weight (dictionary, optional): Maps class indices (integers) to a weight (float) value,
                        used for weighting the loss function (during training only).
                        This can be useful to tell the model to "pay more attention" to samples from an under-represented class.
                        Defaults to None.
            output_bias (float, optional): Initial bias to get better initial convergence. Defaults to None.
            game_version (str, optional): 'totem'.
                        States what element and combination set is going to be used.
        """
        # print info for user
        print('\nInitialize link prediction model.')

        # set attributes
        self.game_version = game_version
        self.time = time
        self.step = step
        self.epochs = epochs
        self.batch_size = batch_size
        self.steps_per_epoch = steps_per_epoch
        self.output_bias = output_bias
        self.class_weight = class_weight

    def evaluate_model(self, X, y, validation_split=None):  
        """Get, train and evaluate model for predicting links between two elements.

        Args:
            X (tuple): Tuple containing inputs for training (1), testing (2) and validation (3, optional).
                        Each is an ndarray(dtype=float, ndim=2)).
            y (tuple): Tuple containing outputs for training (1), testing (2) and validation (3, optional).
                        Each is an ndarray(dtype=int, ndim=1)).
            validation_split (float, optional): Fraction of the training data to be used as validation data.
                        Defaults to None which means validation set is given manually with X and y.

        Returns:
            tuple:
                - test_predictions (ndarray(dtype=float, ndim=1)): Prediction on test data.
                - test_metrics (dictionary): Metric info on test data (model).
        """
        # extract train and test data
        X_train, y_train = X[0], y[0]
        X_test, y_test = X[1], y[1]

        # get input size
        n_inputs = X_train.shape[1]

        # build model
        model = self.build_model(n_inputs)
        model.summary()

        # apply early stopping
        # early_stop = keras.callbacks.EarlyStopping(monitor='val_auc',
        #                                           verbose=1, mode='max',
        #                                           patience=15, restore_best_weights=True)

        # print info for user
        print('\nFit link prediction model.')

        if validation_split is not None:
            # train model
            history = model.fit(X_train, y_train,
                                steps_per_epoch=self.steps_per_epoch,
                                epochs=self.epochs,
                                batch_size=self.batch_size,
                                validation_split=validation_split,
                                verbose=0,
                                callbacks=[tfdocs.modeling.EpochDots()],
                                #          tf.keras.callbacks.TensorBoard(log_dir='./logs')],
                                class_weight=self.class_weight)
        else:
            X_val, y_val = X[2], y[2]

            # train model
            history = model.fit(X_train, y_train,
                                steps_per_epoch=self.steps_per_epoch,
                                epochs=self.epochs,
                                batch_size=self.batch_size,
                                validation_data = (X_val, y_val),
                                verbose=0,
                                callbacks=[tfdocs.modeling.EpochDots()],
                                #          tf.keras.callbacks.TensorBoard(log_dir='./logs')],
                                class_weight=self.class_weight)

        # visualization of training progress
        visualization = Visualization(self.time, '{}LinkPred'.format(self.game_version), self.step)
        visualization.plot_progress(history, ['loss', 'auc', 'precision', 'recall'])

        # make predictions and plot confusion matrix and ROC
        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)
        visualization.plot_confusion_matrix((y_train, y_test), (train_predictions, test_predictions), p=0.5)
        # visualization.plot_roc((y_train, y_test), (train_predictions, test_predictions))

        # check generalization on test data
        test_metrics = model.evaluate(X_test, y_test, verbose=0, return_dict=True)

        # print info for user
        print('\nReturn results from link prediction model.')

        # return test predictions and test metrics
        return test_predictions, test_metrics


    def build_model(self, n_inputs):
        """Creates and returns model for predicting links between two elements.

        Args:
            n_inputs (int): Input size.

        Returns:
            Sequential: Model.
        """
        # print info for user
        print('\nBuild link prediction model.')

        # set output bias
        if self.output_bias is not None:
            output_bias = tf.keras.initializers.Constant(self.output_bias)
        else:
            output_bias = None

        # define architecture
        model = keras.Sequential([
            layers.Dense(16, activation='relu', input_shape=[n_inputs]),
            layers.Dense(1, activation='sigmoid', bias_initializer=output_bias)
        ])

        # define learning rate
        lr = 1e-3

        # define optimizer
        optimizer = tf.keras.optimizers.Adam(lr)

        # define metrics
        metrics = [
            keras.metrics.TruePositives(name='tp'),
            keras.metrics.FalsePositives(name='fp'),
            keras.metrics.TrueNegatives(name='tn'),
            keras.metrics.FalseNegatives(name='fn'),
            keras.metrics.BinaryAccuracy(name='accuracy'),
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall'),
            keras.metrics.AUC(name='auc'),
        ]

        # compile model
        model.compile(loss= keras.losses.BinaryCrossentropy(),
                      optimizer=optimizer,
                      metrics=metrics)

        return model
