import joblib
import os
import sys


def RF_CART(data):
    for i in range(0, len(data)):
        data[i][0] -= 1.25508300e+04
        data[i][1] -= 6.07853117e+05
        data[i][2] -= 1.48725399e+03
        data[i][3] -= 2.34303238e+04
        data[i][4] -= 2.12043206e+03
        data[i][5] -= 4.71846941e+04
        data[i][6] -= 6.03510074e+01
        data[i][7] -= 1.24105098e+02
        data[i][8] -= 8.59590391e+03
        data[i][9] -= 3.73007631e+04
        data[i][10] -= 6.52365604e+00
        data[i][11] -= 2.24559050e-02
        data[i][12] -= 6.65396164e+00
        data[i][13] -= 7.25696055e+01
        data[i][0] /= 3.58904371e+03
        data[i][1] /= 1.69657991e+06
        data[i][2] /= 7.27800803e+02
        data[i][3] /= 4.79646185e+04
        data[i][4] /= 9.64293219e+02
        data[i][5] /= 9.42520411e+04
        data[i][6] /= 2.12948549e+01
        data[i][7] /= 3.75990000e+03
        data[i][8] /= 9.65909155e+02
        data[i][9] /= 1.87228692e+05
        data[i][10] /= 7.38228426e-01
        data[i][11] /= 1.09441712e-01
        data[i][12] /= 6.29295121e-01
        data[i][13] /= 1.25659864e+01
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    clf_f = joblib.load(path + '/model/model_f.pkl')
    clf_t = joblib.load(path + '/model/model_t.pkl')
    result_t = clf_t.predict(data)
    result_f = clf_f.predict(data)
    return [result_t, result_f]
