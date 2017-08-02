% Intrinsic and Extrinsic Camera Parameters
%
% This script file can be directly executed under Matlab to recover the camera intrinsic and extrinsic parameters.
% IMPORTANT: This file contains neither the structure of the calibration objects nor the image coordinates of the calibration points.
%            All those complementary variables are saved in the complete matlab data file Calib_Results.mat.
% For more information regarding the calibration model visit http://www.vision.caltech.edu/bouguetj/calib_doc/


%-- Focal length:
fc = [ 289.750770874899729 ; 290.513062342272178 ];

%-- Principal point:
cc = [ 166.911629750701223 ; 113.111424888606422 ];

%-- Skew coefficient:
alpha_c = 0.000000000000000;

%-- Distortion coefficients:
kc = [ 0.047188150634811 ; -0.083029788357708 ; 0.000271957215313 ; 0.000352382186641 ; 0.000000000000000 ];

%-- Focal length uncertainty:
fc_error = [ 2.659410521893145 ; 2.399928426983010 ];

%-- Principal point uncertainty:
cc_error = [ 3.531090509791818 ; 3.297088442450774 ];

%-- Skew coefficient uncertainty:
alpha_c_error = 0.000000000000000;

%-- Distortion coefficients uncertainty:
kc_error = [ 0.029145449909784 ; 0.081914062606881 ; 0.003811873002642 ; 0.004269393482472 ; 0.000000000000000 ];

%-- Image size:
nx = 320;
ny = 240;


%-- Various other variables (may be ignored if you do not use the Matlab Calibration Toolbox):
%-- Those variables are used to control which intrinsic parameters should be optimized

n_ima = 15;						% Number of calibration images
est_fc = [ 1 ; 1 ];					% Estimation indicator of the two focal variables
est_aspect_ratio = 1;				% Estimation indicator of the aspect ratio fc(2)/fc(1)
center_optim = 1;					% Estimation indicator of the principal point
est_alpha = 0;						% Estimation indicator of the skew coefficient
est_dist = [ 1 ; 1 ; 1 ; 1 ; 0 ];	% Estimation indicator of the distortion coefficients


%-- Extrinsic parameters:
%-- The rotation (omc_kk) and the translation (Tc_kk) vectors for every calibration image and their uncertainties

%-- Image #1:
omc_1 = [ 2.118339e+00 ; 2.105560e+00 ; -3.299425e-01 ];
Tc_1  = [ -9.003880e+01 ; -6.777250e+01 ; 4.575591e+02 ];
omc_error_1 = [ 1.151738e-02 ; 1.078729e-02 ; 2.349250e-02 ];
Tc_error_1  = [ 5.564842e+00 ; 5.145620e+00 ; 4.805461e+00 ];

%-- Image #2:
omc_2 = [ 1.755423e+00 ; 1.736335e+00 ; -1.214994e-02 ];
Tc_2  = [ -1.843232e+02 ; -7.088046e+01 ; 4.171617e+02 ];
omc_error_2 = [ 9.479472e-03 ; 1.071022e-02 ; 1.603619e-02 ];
Tc_error_2  = [ 5.209692e+00 ; 4.891305e+00 ; 4.977213e+00 ];

%-- Image #3:
omc_3 = [ 2.135484e+00 ; 2.138907e+00 ; -7.392179e-02 ];
Tc_3  = [ -1.816502e+02 ; -1.018295e+02 ; 4.321134e+02 ];
omc_error_3 = [ 1.079425e-02 ; 1.260048e-02 ; 2.446089e-02 ];
Tc_error_3  = [ 5.339888e+00 ; 5.039520e+00 ; 5.342507e+00 ];

%-- Image #4:
omc_4 = [ -1.845584e+00 ; -1.886873e+00 ; 9.208429e-01 ];
Tc_4  = [ -6.779200e+01 ; -9.741328e+01 ; 5.621991e+02 ];
omc_error_4 = [ 1.188942e-02 ; 9.146177e-03 ; 1.831086e-02 ];
Tc_error_4  = [ 6.888687e+00 ; 6.346094e+00 ; 4.753280e+00 ];

%-- Image #5:
omc_5 = [ 1.783270e+00 ; 1.987083e+00 ; -4.773335e-01 ];
Tc_5  = [ -1.081667e+02 ; -6.278091e+01 ; 5.497799e+02 ];
omc_error_5 = [ 9.758173e-03 ; 1.197481e-02 ; 1.981857e-02 ];
Tc_error_5  = [ 6.650141e+00 ; 6.227816e+00 ; 5.559539e+00 ];

%-- Image #6:
omc_6 = [ -1.638820e+00 ; -1.949155e+00 ; 1.062470e+00 ];
Tc_6  = [ -4.516206e+01 ; -1.121030e+02 ; 5.114655e+02 ];
omc_error_6 = [ 1.168585e-02 ; 9.101303e-03 ; 1.644657e-02 ];
Tc_error_6  = [ 6.275176e+00 ; 5.775934e+00 ; 4.121501e+00 ];

%-- Image #7:
omc_7 = [ 2.020091e+00 ; 1.999561e+00 ; 2.651474e-01 ];
Tc_7  = [ -1.389269e+02 ; -1.003593e+02 ; 3.040375e+02 ];
omc_error_7 = [ 9.737636e-03 ; 8.910734e-03 ; 1.718129e-02 ];
Tc_error_7  = [ 3.913402e+00 ; 3.601707e+00 ; 3.853077e+00 ];

%-- Image #8:
omc_8 = [ 1.896074e+00 ; 1.905468e+00 ; -9.003822e-02 ];
Tc_8  = [ -1.205284e+02 ; -1.156360e+02 ; 3.294366e+02 ];
omc_error_8 = [ 8.785061e-03 ; 9.545946e-03 ; 1.575997e-02 ];
Tc_error_8  = [ 4.087190e+00 ; 3.745322e+00 ; 3.862054e+00 ];

%-- Image #9:
omc_9 = [ 2.179586e+00 ; 2.153935e+00 ; -1.975461e-01 ];
Tc_9  = [ -1.192495e+02 ; -6.614363e+01 ; 4.972110e+02 ];
omc_error_9 = [ 1.425130e-02 ; 1.330279e-02 ; 2.908012e-02 ];
Tc_error_9  = [ 6.062933e+00 ; 5.662170e+00 ; 5.565148e+00 ];

%-- Image #10:
omc_10 = [ -1.630067e+00 ; -1.750938e+00 ; 1.144919e+00 ];
Tc_10  = [ -2.459557e+01 ; -8.657534e+01 ; 5.212507e+02 ];
omc_error_10 = [ 1.175814e-02 ; 9.040693e-03 ; 1.537251e-02 ];
Tc_error_10  = [ 6.374634e+00 ; 5.863274e+00 ; 3.809069e+00 ];

%-- Image #11:
omc_11 = [ -1.823947e+00 ; -1.994014e+00 ; 2.345867e-01 ];
Tc_11  = [ -4.974762e+01 ; -1.656086e+02 ; 5.051214e+02 ];
omc_error_11 = [ 1.128308e-02 ; 1.270190e-02 ; 2.269691e-02 ];
Tc_error_11  = [ 6.292864e+00 ; 5.700286e+00 ; 5.694152e+00 ];

%-- Image #12:
omc_12 = [ 2.069326e+00 ; 2.003010e+00 ; 8.161966e-02 ];
Tc_12  = [ -1.631893e+02 ; -9.673175e+01 ; 3.768388e+02 ];
omc_error_12 = [ 1.015370e-02 ; 1.066840e-02 ; 2.016514e-02 ];
Tc_error_12  = [ 4.754656e+00 ; 4.408005e+00 ; 4.628453e+00 ];

%-- Image #13:
omc_13 = [ 2.051922e+00 ; 1.923687e+00 ; 3.894933e-01 ];
Tc_13  = [ -1.682650e+02 ; -7.374818e+01 ; 3.909546e+02 ];
omc_error_13 = [ 1.187756e-02 ; 1.036204e-02 ; 2.113359e-02 ];
Tc_error_13  = [ 5.031527e+00 ; 4.635861e+00 ; 5.049442e+00 ];

%-- Image #14:
omc_14 = [ 1.668707e+00 ; 1.865220e+00 ; -9.850171e-01 ];
Tc_14  = [ -1.161353e+02 ; -1.252917e+01 ; 5.440948e+02 ];
omc_error_14 = [ 7.838889e-03 ; 1.159815e-02 ; 1.671997e-02 ];
Tc_error_14  = [ 6.563895e+00 ; 6.221298e+00 ; 4.760346e+00 ];

%-- Image #15:
omc_15 = [ -1.883748e+00 ; -2.096609e+00 ; 9.566131e-01 ];
Tc_15  = [ -1.365586e+02 ; -9.298172e+01 ; 4.607830e+02 ];
omc_error_15 = [ 1.185600e-02 ; 8.658461e-03 ; 1.788036e-02 ];
Tc_error_15  = [ 5.624648e+00 ; 5.297795e+00 ; 4.262636e+00 ];

