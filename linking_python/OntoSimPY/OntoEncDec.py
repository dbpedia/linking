from OntoSimImports import *
import OntoSimConstants as cnst


class OntoEncDec():
    act_func = 'softmax'
    lr_rate = 0.001

    def EncDec_net_256(self, conf, encoded_entity):

        X = Input(shape=(encoded_entity.shape[1],), name='enc_dec_ip')  # batch size unknown

        encoded_h1 = Dense(256, activation=self.act_func, name='1_enc_dense')(X)

        Y = Dense(300, activation=self.act_func, name='1_dec_dense')(encoded_h1)

        autoencoder = Model(X, Y)
        encoder = Model(X, encoded_h1)

        opt = Adam(lr=self.lr_rate)

        l_val = 'mean_squared_error'
        autoencoder.compile(loss=l_val, optimizer=opt)

        return autoencoder, encoder

    def EncDec_net_224(self, conf, encoded_entity):

        X = Input(shape=(encoded_entity.shape[1],), name='enc_dec_ip')  # batch size unknown

        encoded_h1 = Dense(256, activation=self.act_func, name='1_enc_dense')(X)
        encoded_h2 = Dense(224, activation=self.act_func, name='2_enc_dense')(encoded_h1)

        decoder_h1 = Dense(256, activation=self.act_func, name='1_dec_dense')(encoded_h2)
        Y = Dense(300, activation=self.act_func, name='2_dec_dense')(decoder_h1)

        autoencoder = Model(X, Y)
        encoder = Model(X, encoded_h2)

        opt = Adam(lr=self.lr_rate)

        l_val = 'mean_squared_error'
        autoencoder.compile(loss=l_val, optimizer=opt)

        return autoencoder, encoder

    def EncDec_net_192(self, conf, encoded_entity):

        X = Input(shape=(encoded_entity.shape[1],), name='enc_dec_ip')  # batch size unknown

        encoded_h1 = Dense(256, activation=self.act_func, name='1_enc_dense')(X)
        encoded_h2 = Dense(224, activation=self.act_func, name='2_enc_dense')(encoded_h1)
        encoded_h3 = Dense(192, activation=self.act_func, name='3_enc_dense')(encoded_h2)

        decoder_h1 = Dense(224, activation=self.act_func, name='1_dec_dense')(encoded_h3)
        decoder_h2 = Dense(256, activation=self.act_func, name='2_dec_dense')(decoder_h1)
        Y = Dense(300, activation=self.act_func, name='3_dec_dense')(decoder_h2)

        autoencoder = Model(X, Y)
        encoder = Model(X, encoded_h3)

        opt = Adam(lr=self.lr_rate)

        l_val = 'mean_squared_error'
        autoencoder.compile(loss=l_val, optimizer=opt)

        return autoencoder, encoder

    def EncDec_net_160(self, conf, encoded_entity):

        X = Input(shape=(encoded_entity.shape[1],), name='enc_dec_ip')  # batch size unknown

        encoded_h1 = Dense(256, activation=self.act_func, name='1_enc_dense')(X)
        encoded_h2 = Dense(224, activation=self.act_func, name='2_enc_dense')(encoded_h1)
        encoded_h3 = Dense(192, activation=self.act_func, name='3_enc_dense')(encoded_h2)
        encoded_h4 = Dense(160, activation=self.act_func, name='4_enc_dense')(encoded_h3)

        decoder_h1 = Dense(192, activation=self.act_func, name='1_dec_dense')(encoded_h4)
        decoder_h2 = Dense(224, activation=self.act_func, name='2_dec_dense')(decoder_h1)
        decoder_h3 = Dense(256, activation=self.act_func, name='3_dec_dense')(decoder_h2)
        Y = Dense(300, activation=self.act_func, name='4_dec_dense')(decoder_h3)

        autoencoder = Model(X, Y)
        encoder = Model(X, encoded_h4)

        opt = Adam(lr=self.lr_rate)

        l_val = 'mean_squared_error'
        autoencoder.compile(loss=l_val, optimizer=opt)

        return autoencoder, encoder

    def EncDec_net_128(self, conf, encoded_entity):

        X = Input(shape=(encoded_entity.shape[1],), name='enc_dec_ip')  # batch size unknown

        encoded_h1 = Dense(256, activation=self.act_func, name='1_enc_dense')(X)
        encoded_h2 = Dense(224, activation=self.act_func, name='2_enc_dense')(encoded_h1)
        encoded_h3 = Dense(192, activation=self.act_func, name='3_enc_dense')(encoded_h2)
        encoded_h4 = Dense(160, activation=self.act_func, name='4_enc_dense')(encoded_h3)
        encoded_h5 = Dense(128, activation=self.act_func, name='5_enc_dense')(encoded_h4)

        decoder_h1 = Dense(160, activation=self.act_func, name='1_dec_dense')(encoded_h5)
        decoder_h2 = Dense(192, activation=self.act_func, name='2_dec_dense')(decoder_h1)
        decoder_h3 = Dense(224, activation=self.act_func, name='3_dec_dense')(decoder_h2)
        decoder_h4 = Dense(256, activation=self.act_func, name='4_dec_dense')(decoder_h3)
        Y = Dense(300, activation=self.act_func, name='5_dec_dense')(decoder_h4)

        autoencoder = Model(X, Y)
        encoder = Model(X, encoded_h5)

        opt = Adam(lr=self.lr_rate)

        l_val = 'mean_squared_error'
        autoencoder.compile(loss=l_val, optimizer=opt)

        return autoencoder, encoder

    def EncDec_net_96(self, conf, encoded_entity):

        X = Input(shape=(encoded_entity.shape[1],), name='enc_dec_ip')  # batch size unknown

        encoded_h1 = Dense(256, activation=self.act_func, name='1_enc_dense')(X)
        encoded_h2 = Dense(224, activation=self.act_func, name='2_enc_dense')(encoded_h1)
        encoded_h3 = Dense(192, activation=self.act_func, name='3_enc_dense')(encoded_h2)
        encoded_h4 = Dense(160, activation=self.act_func, name='4_enc_dense')(encoded_h3)
        encoded_h5 = Dense(128, activation=self.act_func, name='5_enc_dense')(encoded_h4)
        encoded_h6 = Dense(96, activation=self.act_func, name='6_enc_dense')(encoded_h5)

        decoder_h1 = Dense(128, activation=self.act_func, name='1_dec_dense')(encoded_h6)
        decoder_h2 = Dense(160, activation=self.act_func, name='2_dec_dense')(decoder_h1)
        decoder_h3 = Dense(192, activation=self.act_func, name='3_dec_dense')(decoder_h2)
        decoder_h4 = Dense(224, activation=self.act_func, name='4_dec_dense')(decoder_h3)
        decoder_h5 = Dense(256, activation=self.act_func, name='5_dec_dense')(decoder_h4)
        Y = Dense(300, activation=self.act_func, name='6_dec_dense')(decoder_h5)

        autoencoder = Model(X, Y)
        encoder = Model(X, encoded_h6)

        opt = Adam(lr=self.lr_rate)

        l_val = 'mean_squared_error'
        autoencoder.compile(loss=l_val, optimizer=opt)

        return autoencoder, encoder

    def EncDec_net_64(self, conf, encoded_entity):

        X = Input(shape=(encoded_entity.shape[1],), name='enc_dec_ip')  # batch size unknown

        encoded_h1 = Dense(256, activation=self.act_func, name='1_enc_dense')(X)
        encoded_h2 = Dense(224, activation=self.act_func, name='2_enc_dense')(encoded_h1)
        encoded_h3 = Dense(192, activation=self.act_func, name='3_enc_dense')(encoded_h2)
        encoded_h4 = Dense(160, activation=self.act_func, name='4_enc_dense')(encoded_h3)
        encoded_h5 = Dense(128, activation=self.act_func, name='5_enc_dense')(encoded_h4)
        encoded_h6 = Dense(96, activation=self.act_func, name='6_enc_dense')(encoded_h5)
        encoded_h7 = Dense(64, activation=self.act_func, name='7_enc_dense')(encoded_h6)

        decoder_h1 = Dense(96, activation=self.act_func, name='1_dec_dense')(encoded_h7)
        decoder_h2 = Dense(128, activation=self.act_func, name='2_dec_dense')(decoder_h1)
        decoder_h3 = Dense(160, activation=self.act_func, name='3_dec_dense')(decoder_h2)
        decoder_h4 = Dense(192, activation=self.act_func, name='4_dec_dense')(decoder_h3)
        decoder_h5 = Dense(224, activation=self.act_func, name='5_dec_dense')(decoder_h4)
        decoder_h6 = Dense(256, activation=self.act_func, name='6_dec_dense')(decoder_h5)
        Y = Dense(300, activation=self.act_func, name='7_dec_dense')(decoder_h6)

        autoencoder = Model(X, Y)
        encoder = Model(X, encoded_h7)

        opt = Adam(lr=self.lr_rate)

        l_val = 'mean_squared_error'
        autoencoder.compile(loss=l_val, optimizer=opt)

        return autoencoder, encoder

    def EncDec_net_32(self, conf, encoded_entity):

        X = Input(shape=(encoded_entity.shape[1],), name='enc_dec_ip')  # batch size unknown

        encoded_h1 = Dense(256, activation=self.act_func, name='1_enc_dense')(X)
        encoded_h2 = Dense(224, activation=self.act_func, name='2_enc_dense')(encoded_h1)
        encoded_h3 = Dense(192, activation=self.act_func, name='3_enc_dense')(encoded_h2)
        encoded_h4 = Dense(160, activation=self.act_func, name='4_enc_dense')(encoded_h3)
        encoded_h5 = Dense(128, activation=self.act_func, name='5_enc_dense')(encoded_h4)
        encoded_h6 = Dense(96, activation=self.act_func, name='6_enc_dense')(encoded_h5)
        encoded_h7 = Dense(64, activation=self.act_func, name='7_enc_dense')(encoded_h6)
        encoded_h8 = Dense(32, activation=self.act_func, name='8_enc_dense')(encoded_h7)

        decoder_h1 = Dense(64, activation=self.act_func, name='1_dec_dense')(encoded_h8)
        decoder_h2 = Dense(96, activation=self.act_func, name='2_dec_dense')(decoder_h1)
        decoder_h3 = Dense(128, activation=self.act_func, name='3_dec_dense')(decoder_h2)
        decoder_h4 = Dense(160, activation=self.act_func, name='4_dec_dense')(decoder_h3)
        decoder_h5 = Dense(192, activation=self.act_func, name='5_dec_dense')(decoder_h4)
        decoder_h6 = Dense(224, activation=self.act_func, name='6_dec_dense')(decoder_h5)
        decoder_h7 = Dense(256, activation=self.act_func, name='7_dec_dense')(decoder_h6)
        Y = Dense(300, activation=self.act_func, name='8_dec_dense')(decoder_h7)

        autoencoder = Model(X, Y)
        encoder = Model(X, encoded_h8)

        opt = Adam(lr=self.lr_rate)

        l_val = 'mean_squared_error'
        autoencoder.compile(loss=l_val, optimizer=opt)

        return autoencoder, encoder

    def main(self, conf, encoded_entity):

        vec_len = conf["vec_len"]

        if (vec_len == 256):
            print("256-d encoding start ===========")
            autoencoder, encoder = self.EncDec_net_256(conf, encoded_entity)
            print("256-d encoding end =============")
        if (vec_len == 224):
            print("224-d encoding start ===========")
            autoencoder, encoder = self.EncDec_net_224(conf, encoded_entity)
            print("224-d encoding end =============")
        if (vec_len == 192):
            print("192-d encoding start ===========")
            autoencoder, encoder = self.EncDec_net_192(conf, encoded_entity)
            print("192-d encoding end =============")
        if (vec_len == 160):
            print("160-d encoding start ===========")
            autoencoder, encoder = self.EncDec_net_160(conf, encoded_entity)
            print("160-d encoding end =============")
        if (vec_len == 128):
            print("128-d encoding start ===========")
            autoencoder, encoder = self.EncDec_net_128(conf, encoded_entity)
            print("128-d encoding end =============")
        if (vec_len == 96):
            print("96-d encoding start ===========")
            autoencoder, encoder = self.EncDec_net_96(conf, encoded_entity)
            print("96-d encoding end =============")
        if (vec_len == 64):
            print("64-d encoding start ===========")
            autoencoder, encoder = self.EncDec_net_64(conf, encoded_entity)
            print("64-d encoding end =============")
        if (vec_len == 32):
            print("32-d encoding start ===========")
            autoencoder, encoder = self.EncDec_net_32(conf, encoded_entity)
            print("32-d encoding end =============")

        return autoencoder, encoder

    def __init__(self):
        print('OntoEncDec is initialized')