import numpy as np
import bisect

def get_keys_with_second_key(od_data, target_key):
    """
    Returns all first keys in od_data that have target_key as their second key.
    """
    return [i for i in od_data if target_key in od_data[i]]

def filter_data(od_data, dist_data):
    """
    Cleans the od_data by removing all origins and destinations that do not exist in dist_data.

    Parameters:
    od_data (dict): Origin-Destination data dictionary
    dist_data (dict): Distance data dictionary

    Returns:
    tuple: Cleaned od_data
    """
    common_nodes = list(dist_data.keys())

    for key in list(od_data.keys()):
        if key not in common_nodes:
            del od_data[key]
        else:
            for sub_key in list(od_data[key].keys()):
                if sub_key not in common_nodes:
                    del od_data[key][sub_key]
    return od_data

def create_q_bin(od_data, dist_data, each_num=500):
    """
    Sorts distance values and divides them into bins of specified size.
    """
    sts, eds, dis = [], [], []
    left_list, right_list = [], []

    # Collecting data for sorting
    for i in od_data.keys():
        for j in od_data[i].keys():
            sts.append(i)
            eds.append(j)
            dis.append(dist_data[i][j])

    # Sorting distances
    arglist = np.argsort(dis)
    num_elements = len(arglist)
    binnum = num_elements // each_num

    bin_mid, st_list, ed_list = [], [], []
    st_list = [sts[arg] for arg in arglist]
    ed_list = [eds[arg] for arg in arglist]
    st_ed = {i: {} for i in dist_data.keys()}

    # Creating bins
    for i in range(binnum):
        mid_sum, mid_num = 0, 0
        start_idx = i * each_num
        end_idx = num_elements if (i == binnum - 1 and num_elements % each_num != 0) else (i + 1) * each_num

        for j in range(start_idx, end_idx):
            now_idx = j
            mid_sum += dis[arglist[now_idx]]
            mid_num += 1
            st_idx, ed_idx = st_list[now_idx], ed_list[now_idx]
            st_ed[st_idx][ed_idx] = i

        if mid_num:
            bin_mid.append(mid_sum / mid_num)
        left_list.append(dis[arglist[start_idx]])
        right_list.append(dis[arglist[end_idx - 1]])

    data_dic = {"bin_mid": bin_mid, "call_dic": st_ed, "bin_left": left_list, "bin_right": right_list}
    return data_dic

def cal_bindex(now_dist, q_bin):
    """
    Calculates the bin index for a given distance using binary search.
    """
    left_list = q_bin['bin_left']
    index = bisect.bisect_left(left_list, now_dist)
    return max(0, index - 1)

def cal_real_infer_sum(od_data, m_in, m_out, Q_hist, Q_call):
    """
    Calculates the real and inferred totals based on the given data and parameters.
    """
    real_tot = 0
    infer_tot = 0
    for i in od_data.keys():
        for j in od_data[i].keys():
            real_tot += od_data[i][j]
            infer_tot += m_out[i] * m_in[j] * Q_hist[Q_call[i][j]]
    return real_tot, infer_tot

def calculate_mass(od_data, q_bin, iter_step=10):
    """
    Calculates the mass values for the given data over a specified number of iterations.
    """
    bin_mid = q_bin["bin_mid"]
    Q_call = q_bin["call_dic"]
    binnum = len(bin_mid)
    Q_hist = [1 for _ in range(binnum)]

    sum_out = {i: sum(od_data[i].values()) for i in od_data}
    second_keys = {j for i in od_data for j in od_data[i]}
    sum_in = {j: sum(od_data[i][j] for i in od_data if j in od_data[i]) for j in second_keys}

    M_out = {i: 1 for i in od_data}
    M_in = {i: 1 for i in second_keys}

    for t in range(iter_step):
        tem_M_out, tem_M_in = {}, {}
        for i in od_data.keys():
            tem_sum = sum(M_in[j] * Q_hist[Q_call[i][j]] for j in od_data[i] if i != j)
            tem_M_out[i] = (sum_out[i] / float(tem_sum)) if tem_sum != 0 else 0
        for i in second_keys:
            st_list = get_keys_with_second_key(od_data, i)
            tem_sum = sum(M_out[j] * Q_hist[Q_call[j][i]] for j in st_list if i != j)
            tem_M_in[i] = (sum_in[i] / float(tem_sum)) if tem_sum != 0 else 0
        M_in, M_out = tem_M_in.copy(), tem_M_out.copy()

        new_Q, Q_num, new_Q_std = [0] * binnum, [0] * binnum, [0] * binnum
        for i in od_data:
            for j in od_data[i]:
                if i != j and M_out[i] != 0 and M_in[j] != 0:
                    bindex = Q_call[i][j]
                    Q_num[bindex] += 1
                    new_Q[bindex] += od_data[i][j] / (M_out[i] * M_in[j])
                    new_Q_std[bindex] += (od_data[i][j] / (M_out[i] * M_in[j])) ** 2
        Q_hist = [new_Q[i] / Q_num[i] if Q_num[i] != 0 else 0 for i in range(binnum)]
        Q_std = [(((new_Q_std[i] / Q_num[i] - (Q_hist[i] ** 2)) / Q_num[i]) ** 0.5) if Q_num[i] != 0 else 0 for i in
                 range(binnum)]

        real_tot, infer_tot = cal_real_infer_sum(od_data, M_in, M_out, Q_hist, Q_call)

        for i in range(len(Q_hist)):
            Q_hist[i] *= real_tot / infer_tot
            Q_std[i] *= real_tot / infer_tot

    real_tot, infer_tot = cal_real_infer_sum(od_data, M_in, M_out, Q_hist, Q_call)
    Avg_Min = sum(M_in.values()) / float(len(M_in.keys()))
    Avg_Mout = sum(M_out.values()) / float(len(M_out.keys()))
    Max_Q = max(Q_hist)

    for i in range(len(Q_hist)):
        Q_hist[i] /= Max_Q
        Q_std[i] /= Max_Q

    norm = (Avg_Min * Avg_Mout * Max_Q * real_tot / infer_tot) ** (0.5)

    for i in M_in.keys():
        M_in[i] *= norm / float(Avg_Min)
    for i in M_out.keys():
        M_out[i] *= norm / float(Avg_Mout)

    return M_in, M_out, Q_hist, Q_std

def calculate_sums(od_data, q_bin):
    """
    Calculates the sums for input and output along with Q_hist and Q_std values.
    """
    bin_mid = q_bin["bin_mid"]
    Q_call = q_bin["call_dic"]
    binnum = len(bin_mid)

    sum_out = {i: sum(od_data[i].values()) for i in od_data}
    second_keys = {j for i in od_data for j in od_data[i]}
    sum_in = {j: sum(od_data[i][j] for i in od_data if j in od_data[i]) for j in second_keys}

    new_Q, Q_num, new_Q_std = [0] * binnum, [0] * binnum, [0] * binnum
    for i in od_data:
        for j in od_data[i]:
            if i != j and sum_out[i] != 0 and sum_in[j] != 0:
                bindex = Q_call[i][j]
                Q_num[bindex] += 1
                new_Q[bindex] += od_data[i][j] / (sum_out[i] * sum_in[j])
                new_Q_std[bindex] += (od_data[i][j] / (sum_out[i] * sum_in[j])) ** 2

    Q_hist = [new_Q[i] / Q_num[i] if Q_num[i] != 0 else 0 for i in range(binnum)]
    Q_std = [(((new_Q_std[i] / Q_num[i] - (Q_hist[i] ** 2)) / Q_num[i]) ** 0.5) if Q_num[i] != 0 else 0 for i in
             range(binnum)]

    real_tot, infer_tot = cal_real_infer_sum(od_data, sum_in, sum_out, Q_hist, Q_call)

    for i in range(len(Q_hist)):
        Q_hist[i] *= real_tot/infer_tot
        Q_std[i] *= real_tot/infer_tot

    return sum_in, sum_out, Q_hist, Q_std

def calculate_GDPs(od_data, GDP_dic, q_bin):
    """
    Calculates Q_hist and Q_std values based on GDP data.
    """
    bin_mid = q_bin["bin_mid"]
    Q_call = q_bin["call_dic"]
    binnum = len(bin_mid)

    new_Q, Q_num, new_Q_std = [0] * binnum, [0] * binnum, [0] * binnum
    for i in od_data:
        for j in od_data[i]:
            if i != j and GDP_dic[i] != 0 and GDP_dic[j] != 0:
                bindex = Q_call[i][j]
                Q_num[bindex] += 1
                new_Q[bindex] += od_data[i][j] / (GDP_dic[i] * GDP_dic[j])
                new_Q_std[bindex] += (od_data[i][j] / (GDP_dic[i] * GDP_dic[j])) ** 2

    Q_hist = [new_Q[i] / Q_num[i] if Q_num[i] != 0 else 0 for i in range(binnum)]
    Q_std = [(((new_Q_std[i] / Q_num[i] - (Q_hist[i] ** 2)) / Q_num[i]) ** 0.5) if Q_num[i] != 0 else 0 for i in
             range(binnum)]

    real_tot, infer_tot = cal_real_infer_sum(od_data, GDP_dic, GDP_dic, Q_hist, Q_call)

    for i in range(len(Q_hist)):
        Q_hist[i] *= real_tot / infer_tot
        Q_std[i] *= real_tot / infer_tot

    return Q_hist, Q_std