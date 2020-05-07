import pandas as pd
import numpy as np
import numpy.linalg as lin
import glob
import matplotlib.pyplot as plt


def GetInput(filename):
    output = []
    df = pd.read_csv(filename, header=0, delimiter=";")
    azi = [-80, -35, 0, 45, 65]
    ele = [-22.5, 39.375, -16.875, 0, 73.125]

    for i in range(len(df)):
        print(i)
        head_pos = df.iloc[i]['Head Position'].replace("(", "")
        head_pos = head_pos.replace(")", "")
        head_pos = head_pos.replace(",", "")
        head_pos = head_pos.split(" ")

        point_pos = df.iloc[i]['Point Location'].replace("(", "")
        point_pos = point_pos.replace(")", "")
        point_pos = point_pos.replace(",", "")
        point_pos = point_pos.split(" ")

        head_rot = df.iloc[i]['Head Rotation'].replace("(", "")
        head_rot = head_rot.replace(")", "")
        head_rot = head_rot.split(",")

        qr = float(head_rot[3])
        qi = float(head_rot[0])
        qj = float(head_rot[1])
        qk = float(head_rot[2])

        s = lin.norm(np.array([qr, qi, qj, qk]))

        R_head = np.array([[1 - 2 * s * (qj ** 2 + qk ** 2), 2 * s * (qi * qj - qk * qr), 2 * s * (qi * qk + qj * qr)],
                           [2 * s * (qi * qj + qk * qr), 1 - 2 * s * (qi ** 2 + qk ** 2), 2 * s * (qj * qk - qi * qr)],
                           [2 * s * (qi * qk - qj * qr), 2 * s * (qj * qk + qi * qr), 1 - 2 * s * (qi ** 2 + qj ** 2)]])

        H_hinw = np.array([[R_head[0][0], R_head[0][1], R_head[0][2], float(head_pos[0])],
                           [R_head[1][0], R_head[1][1], R_head[1][2], float(head_pos[1])],
                           [R_head[2][0], R_head[2][1], R_head[2][2], float(head_pos[2])],
                           [0., 0., 0., 1.]])

        T_binw = np.array([[float(point_pos[0])],
                           [float(point_pos[1])],
                           [float(point_pos[2])],
                           [1.]])

        H_binh = np.matmul(lin.inv(H_hinw), T_binw)
        x_1 = float(H_binh[0])
        x_3 = float(H_binh[1])
        x_2 = float(H_binh[2])

        r = np.sqrt((x_1 ** 2 + x_2 ** 2 + x_3 ** 2))
        # x_1 = float(point_pos[0]) - float(head_pos[0])
        # x_3 = float(point_pos[1]) - float(head_pos[1])
        # x_2 = float(point_pos[2]) - float(head_pos[2])
        theta = np.arcsin(x_1 / r)
        phi = np.arcsin(x_3 / r / np.cos(theta))

        # (azi, test_azi, ele, test_ele, sub, set, audio)
        row_array = np.array(
            (float(azi[df.iloc[i]["Stimuli Location"]-1]), float(theta * 360 / 2 / np.pi),
             float(ele[df.iloc[i]["Stimuli Location"]-1]), float(phi * 360 / 2 / np.pi),
             filename.split("_")[1], filename.split("_")[2], filename.split("_")[3]))
        output.append(row_array)
    return output


result = pd.DataFrame(columns=["azi", "test_azi", "ele", "test_ele", "subject_id", "hrtf", "audio"])
for file in glob.glob("Allsub/*.txt"):
    print(file)
    array = GetInput(file)
    df_temp = pd.DataFrame(array, columns=["azi", "test_azi", "ele", "test_ele", "subject_id", "hrtf", "audio"])
    result = pd.concat([result, df_temp], axis=0)


result[["azi", "test_azi", "ele", "test_ele"]] = result[["azi", "test_azi", "ele", "test_ele"]].apply(pd.to_numeric)
result['azi_error'] = np.abs(result['azi'] - result['test_azi'])
result['ele_error'] = np.abs(result['ele'] - result['test_ele'])


azi = [-80, -35, 0, 45, 65]
ele = [-22.5, 39.375, -16.875, 0, 73.125]


def getdata(**identifier):
    df = result
    for key, value in identifier.items():
        df = df.loc[df[key] == value]
    zeros1 = np.zeros([4, 5])
    zeros2 = np.zeros([4, 5])
    data = pd.DataFrame(zeros1, index=["est_azi", "est_ele", "generic_azi", "generic_ele"])
    error = pd.DataFrame(zeros2, index=["est_azi", "est_ele", "generic_azi", "generic_ele"])

    hrtf = np.array(["est", "generic"])

    for hrtf_id in hrtf:
        print(hrtf_id)
        for pp, item in enumerate(zip(azi, ele)):
            df_hrtf = df.loc[df["hrtf"] == hrtf_id]
            df_hrtf_ang = df_hrtf[(df_hrtf['azi'] == item[0]) & (df_hrtf['ele'] == item[1])]

            data.loc[hrtf_id+"_azi", pp] = np.average(df_hrtf_ang["azi_error"])
            error.loc[hrtf_id+"_azi", pp] = np.std(df_hrtf_ang["azi_error"])/len(df_hrtf_ang["azi_error"])
            data.loc[hrtf_id+"_ele", pp] = np.average(df_hrtf_ang["ele_error"])
            error.loc[hrtf_id+"_ele", pp] = np.std(df_hrtf_ang["ele_error"])/len(df_hrtf_ang["ele_error"])
    return df, data, error


df_temp, d, e = getdata(subject_id="1")
plt.figure()
plt.errorbar(azi, d.loc["est_azi"], yerr=e.loc["est_azi"], fmt='o')
plt.errorbar(azi, d.loc["generic_azi"], yerr=e.loc["generic_azi"], fmt='o')
plt.legend(['est', 'generic'])



for pp, item in enumerate(zip(azi, ele)):
    print(pp)
    result_2_est_item = result_2_est[(result_2_est['azi'] == item[0]) & (result_2_est['ele'] == item[1])]
    data[pp] = np.average(result_2_est_item['azi_error'])
    error[pp] = np.std((result_2_est_item['azi_error']))/16

plt.figure()
plt.errorbar(azi, data, yerr=error, fmt='o')








result.to_csv("subject1_2.csv", index=False)



