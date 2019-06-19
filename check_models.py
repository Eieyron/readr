import pickle

from tensorflow import keras

# models' first layer is lambda layer that requires the input dataset's mean and standard deviation
# these are therefore pickled for faster loading of models
mean_px, std_px = pickle.load(open('./dev.pkl', 'rb'))

# a bit too slow
# loop to load and check out the stats of the models
for i in range(10):
	model = keras.models.load_model('./models/w_m'+str(i)+'_eF.h5')
	print("Model "+str(i))
	model.summary()