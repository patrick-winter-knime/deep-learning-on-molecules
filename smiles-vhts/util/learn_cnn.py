import h5py
from data_structures import reference_data_set
from models import cnn_shared


def train(data_file, identifier, batch_size, epochs):
    prefix = data_file[:data_file.rfind('.')]
    classes_hdf5 = h5py.File(data_file, 'r')
    smiles_path = prefix + '-smiles_matrices.h5'
    smiles_hdf5 = h5py.File(smiles_path, 'r')
    train_path = prefix + '-' + identifier + '-train.h5'
    train_hdf5 = h5py.File(train_path, 'r')
    feature_model_path = prefix + '-' + identifier + '-cnn.h5'
    smiles_matrix = reference_data_set.ReferenceDataSet(train_hdf5['ref'], smiles_hdf5['smiles_matrix'])
    classes = reference_data_set.ReferenceDataSet(train_hdf5['ref'], classes_hdf5[identifier + '-classes'])
    model = cnn_shared.SharedFeaturesModel(smiles_matrix.shape[1:], classes.shape[1])
    model.predictions_model.fit(smiles_matrix, classes, epochs=epochs, shuffle='batch', batch_size=batch_size)
    model.save_features_model(feature_model_path)
    classes_hdf5.close()
    smiles_hdf5.close()
    train_hdf5.close()
