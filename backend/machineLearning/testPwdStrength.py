from mL import *

def test_input():
    user_inp = input()
    user_inp_f = np.array(extract_features(user_inp)).reshape(1, -1)
    #print(user_inp_f)
    df_inp = pd.DataFrame(user_inp_f, columns=['password', 'length', 'upper', 'lower', 'digit', 'spe', 'strength'])
    inp_x = df_inp[['length', 'upper', 'lower', 'digit', 'spe']].values
    inp_y = df_inp['strength']
    inp_pred = scaler.transform(inp_x)

    #print(df_inp)

    strength = knn.predict(scaler.transform(inp_x))

    return strength