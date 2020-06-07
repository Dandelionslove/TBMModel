import joblib
import os
import sys

def RF_CART(data):
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    clf_f = joblib.load(path + '/model_f.pkl')
    clf_t = joblib.load(path + '/model_t.pkl')
    result_t = clf_t.predict(data)
    result_f = clf_f.predict(data)
    return [result_t, result_f]
