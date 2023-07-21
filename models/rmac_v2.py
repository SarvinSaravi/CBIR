import numpy as np
import tensorflow as tf
import os
from keras.applications import ResNet101
from keras.utils import img_to_array
from keras import Model
from keras.applications.resnet import preprocess_input
from dataloading.dataloading import loading_an_image
import cv2
class RMAC:
    def __init__(self, scales: list(), levels=3, pca=True, device_id=0, verbose=False):
        self.scales=scales
        self.levels=levels
        self.pca=pca
        self.model=self.set_model()
        self.regions=None
        self.device_id=device_id
        self.verbose=verbose


    @staticmethod
    def set_model():
        layer = "conv5_block3_out"
        base_model = ResNet101(include_top=False,
                               input_shape=(None, None, 3),
                               weights='weights/resnet101_weights_tf_dim_ordering_tf_kernels_notop.h5',
                               )
        base_out = base_model.get_layer(layer).output
        model = Model(base_model.input, base_out)
        return model
    
    def make_regions(self, shape):
        # Authored by G. Tolias, 2015.
        overlap = 0.4
        steps = np.asarray([2, 3, 4, 5, 6, 7])
        B, H, W, D = shape
        w = min([W, H])
        b = np.asarray((max(H, W) - w)) / (steps - 1)
        idx = np.argmin(np.abs(((w ** 2 - w * b) / (w ** 2)) - overlap))

        Wd = 0
        Hd = 0
        if H < W:
            Wd = idx + 1
        elif H > W:
            Hd = idx + 1

        self.regions = []
        for l in range(self.levels):

            wl = int(2 * w / (l + 2))
            wl2 = int(wl / 2 - 1)

            b = 0 if not (l + Wd) else ((W - wl) / (l + Wd))
            cenW = np.asarray(np.floor(wl2 + np.asarray(range(l + Wd + 1)) * b), dtype=np.int32) - wl2
            b = 0 if not (l + Hd) else ((H - wl) / (l + Hd))
            cenH = np.asarray(np.floor(wl2 + np.asarray(range(l + Hd + 1)) * b), dtype=np.int32) - wl2

            for i in cenH:
                for j in cenW:
                    if i >= W or j >= H:
                        continue
                    ie = i + wl
                    je = j + wl
                    if ie >= W:
                        ie = W
                    if je >= H:
                        je = H
                    if ie - i < 1 or je - j < 1:
                        continue
                    self.regions.append((i, j, ie, je))

        if self.verbose:
            print('RMAC regions = %s' % self.regions, len(self.regions))
    
    def PCAlearning(self, x):
        print(" > PCA Learning is starting....")
        
        mean = tf.reduce_mean(x, axis=0) 
        x = tf.subtract(x, mean) # (n_region * batch_size, )
        if self.verbose:
            print(" > Centered feature: ", x.shape)
        with tf.device("/GPU:1"):
            C = tf.matmul(x, x, transpose_a=True)/x.shape[0]
        
        eigenvalues, P = tf.linalg.eigh(C)
        D = eigenvalues
        # if self.verbose:
            #  Compute the square root of the inverse of the eigenvalues
            # print(" > Compute the square root of the inverse of the eigenvalues", tf.linalg.diag(tf.linalg.diag(D)), tf.linalg.diag(D))
            
        D_m12 = tf.linalg.diag(1.0 / tf.sqrt(D + 1E-9))
       
        if self.verbose:
            #  Compute the square root of the inverse of the eigenvalues
            print(" > Compute the square root of the inverse of the eigenvalues", D.shape)
        # with tf.device("/GPU:1"):
        #     PD = tf.matmul(P, D) 
        #     PDP_t = tf.matmul(PD, P, transpose_b=True) # (2048, 2048)
        
        if self.verbose:
        #     # compute the whitening mat
        #     print(' > Covariance mat: ', covariance_matrix, PDP_t)
            print(" > Check validation: ", D, tf.linalg.inv(tf.matmul(D_m12,D_m12)))
        
        with tf.device("/GPU:1"):
            whitening_matrix = tf.matmul(D_m12, P, transpose_b=True) # (2048, 2048)

        self.whitening_matrix = whitening_matrix
        self.mean = mean
        return whitening_matrix
    
    def PCAwhitening(self, x):
        # x = tf.subtract(x, self.mean)
        # x_whiten = tf.transpose(tf.matmul(self.whitening_matrix, x, transpose_b=True))
        x_whiten = tf.matmul(x,self.whitening_matrix)

        return x_whiten
    
    def PCAlearning_matlab(self, x):
        print(" > PCA Learning is starting....")
        
        mean = tf.reduce_mean(x, axis=0) 
        x = tf.subtract(x, mean) # (n_region * batch_size, )
        if self.verbose:
            print(" > Centered feature: ", x.shape)
        with tf.device("/GPU:1"):
            C = tf.matmul(x, x, transpose_a=True)/x.shape[0]
        
        eigenvalues, P = tf.linalg.eigh(C)
        D = eigenvalues
        # if self.verbose:
            #  Compute the square root of the inverse of the eigenvalues
            # print(" > Compute the square root of the inverse of the eigenvalues", tf.linalg.diag(tf.linalg.diag(D)), tf.linalg.diag(D))
            
        D_m12 = tf.linalg.diag(1.0 / tf.sqrt(D + 1E-9))
       
        if self.verbose:
            #  Compute the square root of the inverse of the eigenvalues
            print(" > Compute the square root of the inverse of the eigenvalues", D.shape)
        # with tf.device("/GPU:1"):
        #     PD = tf.matmul(P, D) 
        #     PDP_t = tf.matmul(PD, P, transpose_b=True) # (2048, 2048)
        
        if self.verbose:
        #     # compute the whitening mat
        #     print(' > Covariance mat: ', covariance_matrix, PDP_t)
            print(" > Check validation: ", D, tf.linalg.inv(tf.matmul(D_m12,D_m12)))
        
        with tf.device("/GPU:0"):
            whitening_matrix = tf.matmul(D_m12, P, transpose_b=True) # (2048, 2048)

        self.whitening_matrix = whitening_matrix
        self.mean = mean
        return whitening_matrix
    
    def postprocess(self,y):
        # (batch, n_region, 2048)
       
        # y = tf.transpose(y, [1, 0, 2])

        y = tf.math.l2_normalize(y, axis=2)
        
        # sum
        y = tf.reduce_mean(y, axis=1)
        y = tf.math.l2_normalize(y, axis=1)
        return y

    def extract_features(self, dataset_path):
        y = [] 
        self.make_regions((None, 7, 7, 2048))
        all_img_names = os.listdir(dataset_path)
        for img_name in all_img_names:
            image_path = dataset_path + '/' + img_name
            origin = loading_an_image(image_path)
            im_size_hw = np.array(origin.shape[0:2])
            if self.verbose:
                print(" > origin: ", im_size_hw)
            sr_features = []
            for s in self.scales:
                img = origin
                ratio = float(s) / np.max(im_size_hw)
                new_size = tuple(np.round(im_size_hw * ratio).astype(np.int32))
                if self.verbose:
                    print(" > new_size: ", new_size)
                img = cv2.resize(img, new_size)
                img = img_to_array(img)
                img = np.expand_dims(img, axis=0)
                img = preprocess_input(img)
                x = self.model.predict(img, verbose=False)  # (1, 7, 7, 2048)

                for r in self.regions:
                    x_sliced = x[:, r[1]:r[3], r[0]:r[2], :]
                    x_maxed = tf.reduce_max(x_sliced, axis=(1,2))  # (2048, )
                    sr_features.append(x_maxed)  # (n_regions, 2048)
        
            y.append(sr_features)  

        # y = tf.convert_to_tensor(y) 
        y = tf.stack(y)
        y = tf.squeeze(y)
        if self.verbose:
                print("Regioned features: ", y.shape)

        if self.pca:
            a, b, c = y.shape
            y = tf.reshape(y, (a*b, c)) 
            if self.verbose:
                print("Before pca: ", y.shape)

            with tf.device("/GPU:0"):
                self.PCAlearning(y)
        
                y = tf.math.l2_normalize(y, axis=1)
                y = self.PCAwhitening(y)
            print(" > Whitening is Done: ", y.shape) # (batch_size * n_regions, 2048)

            y = tf.reshape(y, (a, b, c))
            if self.verbose:
                print("y_reshaped after pca: ", y.shape)
        
        y = self.postprocess(y)  # input must be (batch, n_regions, 2048)

        print("> The feature vectors shape:", y.shape)
        return all_img_names, y
    