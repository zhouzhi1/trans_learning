import keras


def build_model(input_shape, nb_classes, pre_model_path=None, freezen=False, freezen_layers=None):
    input_layer = keras.layers.Input(input_shape)

    conv1 = keras.layers.Conv2D(filters=128, kernel_size=8, padding='same')(input_layer)
    conv1 = keras.layers.normalization.BatchNormalization()(conv1)
    conv1 = keras.layers.Activation(activation='relu')(conv1)

    conv2 = keras.layers.Conv2D(filters=256, kernel_size=5, padding='same')(conv1)
    conv2 = keras.layers.normalization.BatchNormalization()(conv2)
    conv2 = keras.layers.Activation('relu')(conv2)

    conv3 = keras.layers.Conv2D(128, kernel_size=3, padding='same')(conv2)
    conv3 = keras.layers.normalization.BatchNormalization()(conv3)
    conv3 = keras.layers.Activation('relu')(conv3)

    gap_layer = keras.layers.pooling.GlobalAveragePooling2D()(conv3)

    output_layer = keras.layers.Dense(nb_classes, activation='softmax')(gap_layer)

    model = keras.models.Model(inputs=input_layer, outputs=output_layer)

    if pre_model_path is not None:
        print('pre_model_path:', pre_model_path)
        print('loading model...')
        pre_model = keras.models.load_model(pre_model_path)
        print('loaded model !!!')
        for i in range(len(model.layers) - 1):
            model.layers[i].set_weights(pre_model.layers[i].get_weights())
        if freezen is True and freezen_layers is not None:
            for i in freezen_layers:
                model.layers[i].trainable = False

    model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy'])
    return model
