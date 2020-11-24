#!/user/bin/env python
# encoding = utf-8
"""
@author  : Qinjian Zheng
@contact : qinjian.zheng@student.unsw.edu.au
@file    : compute_candidate_key.py
@ide     : PyCharm
@time    : 2020-10-16 14:23:20
"""

from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def compute_closure(X, F):
    X_plus = X
    change = True
    while change:
        change = False
        for w,z in F:
            if type(w) == tuple:
                w_set = set(w)
            else:
                w_set = {w}
            if type(z) == tuple:
                z_set = set(z)
            else:
                z_set = {z}            
            if w_set.issubset(X_plus) \
                and not z_set.issubset(X_plus):
                X_plus = X_plus.union(z_set)
                change = True
    return X_plus

def compute_candidate_key(X, R, F):
    # X is a superkey
    T = set()
    remove = True
    while remove:
        for i in X:
            X_inter = compute_closure(X.difference({i}), F)
            if X_inter == R:
                X = X.difference({i})
            else:
                remove = False
    T = T.union(X)
    return T

def compute_all_candidate_keys(R, F):
    candidate_keys = []
    F_LHS = set()
    F_RHS = set()
    for w, z in F:
        if type(w) == tuple:
            w_set = set(w)
        else:
            w_set = {w}
        if type(z) == tuple:
            z_set = set(z)
        else:
            z_set = {z}
        F_LHS = F_LHS.union(w_set)
        F_RHS = F_RHS.union(z_set)
    powerset_X = list([set(x) for x in powerset(F_LHS)])
    for s in powerset_X:
        # whether set s is a superkey
        if compute_closure(s,F) == R:
            X_superkey = s
            # closure = R and not in candidate key ---> a potential candidate key
            if compute_closure(X_superkey, F) == R \
                and X_superkey not in candidate_keys:
               candidate_keys.append(
                   compute_candidate_key(X_superkey, R, F))
    candidate_keys = set([frozenset(x) 
                          for x in candidate_keys 
                          if x != set()])
    return candidate_keys

if __name__ == '__main__':
    # X = {'A'}
    # F = {('A','B'),(('B', 'C'),'D'),('A','C')}
    # R = {'A', 'B', 'C', 'D'}
    
    # R_2 = {'A', 'B', 'C', 'D', 'E'}
    # F_2 = {('A','B'),(('B','C'),'A'),('D','E')}
    # candidate_keys = compute_all_candidate_keys(R_2, F_2)
    # F_3 = {('Prof', 'Fac_Dept'), ('Course', 'Crs_Dept')}
    # R_3 = {'Prof', 'Fac_Dept', 'Course', 'Crs_Dept'}
    # candidate_keys = compute_all_candidate_keys(R_3, F_3)
    R_4 = {'Course', 'Prof', 'Room', 'Room_Cap', 'Enrol_I_mt'}
    F_4 = {('Course',('Prof', 'Room', 'Room_Cap', 'Enrol_Lmt')), ('Room', ('Room_Cap', 'Enrol_Lmt'))}
    R_5 = {'Property_Id', 'City', 'Lot_No', 'Area', 'Price', 'Tax_Rate'}
    F_5 = {('Property_Id', ('City', 'Lot_No', 'Area', 'Price', 'Tax_Rate')), 
            (('City', 'Lot_No'), ('Property_Id', 'Area', 'Price', 'Tax_Rate')),
            ('Area', 'Price'),
            ('City', 'Tax_Rate')}
    print(compute_all_candidate_keys(R_5, F_5))
