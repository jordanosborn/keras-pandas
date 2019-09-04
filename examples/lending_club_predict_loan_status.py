import logging
import os
import pickle

from tensorflow.keras import Model
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

from keras_pandas import lib
from keras_pandas.Automater import Automater


def main():
    # List out which components are supplied by Automater
    # In this example, we're utilizing X and y generated by the Automater, auto.input_nub, auto.input_layers,
    # auto.output_nub, and auto.suggest_loss

    save_results = True

    # Load data
    observations = lib.load_lending_club()
    print('Observation columns: {}'.format(list(observations.columns)))
    print('Class balance:\n {}'.format(observations['loan_status'].value_counts()))

    # Train /test split
    train_observations, test_observations = train_test_split(observations)
    train_observations = train_observations.copy()
    test_observations = test_observations.copy()

    # List out variable types
    data_type_dict = {'numerical': ['loan_amnt', 'annual_inc', 'open_acc', 'dti', 'delinq_2yrs',
                                    'inq_last_6mths', 'mths_since_last_delinq', 'pub_rec', 'revol_bal',
                                    'revol_util',
                                    'total_acc', 'pub_rec_bankruptcies'],
                      'categorical': ['term', 'grade', 'emp_length', 'home_ownership', 'loan_status', 'addr_state',
                                      'application_type', 'disbursement_method'],
                      'text': ['desc', 'purpose', 'title']}
    output_var = 'loan_status'

    # Create and fit Automater
    auto = Automater(data_type_dict=data_type_dict, output_var=output_var)
    auto.fit(train_observations)

    # Transform data
    train_X, train_y = auto.fit_transform(train_observations)
    test_X, test_y = auto.transform(test_observations)

    # Create and fit keras (deep learning) model.

    x = auto.input_nub
    x = Dense(32)(x)
    x = Dense(32)(x)
    x = auto.output_nub(x)

    model = Model(inputs=auto.input_layers, outputs=x)
    model.compile(optimizer='adam', loss=auto.suggest_loss())

    model.fit(train_X, train_y)

    # Make model predictions and inverse transform model predictions, to get usable results
    pred_test_y = model.predict(test_X)
    auto.inverse_transform_output(pred_test_y)

    # Save all results
    if save_results:
        temp_dir = lib.get_temp_dir()
        model.save(os.path.join(temp_dir, 'model.h5py'))
        pickle.dump(train_X, open(os.path.join(temp_dir, 'train_X.pkl'), 'wb'))
        pickle.dump(train_y, open(os.path.join(temp_dir, 'train_y.pkl'), 'wb'))
        pickle.dump(test_X, open(os.path.join(temp_dir, 'test_X.pkl'), 'wb'))
        pickle.dump(test_y, open(os.path.join(temp_dir, 'test_y.pkl'), 'wb'))
        pickle.dump(pred_test_y, open(os.path.join(temp_dir, 'pred_test_y.pkl'), 'wb'))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
