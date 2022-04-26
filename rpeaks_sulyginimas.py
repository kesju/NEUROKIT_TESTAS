# %%
# Skriptas rpeaks sekų, gautų iš .json failo ir EKG įrašo, panaudojant NEUROKIT2, sulyginimui 

import pandas as pd
import numpy as np
import json, sys
import neurokit2 as nk

def zive_read_file_1ch(filename):
    f = open(filename, "r")
    a = np.fromfile(f, dtype=np.dtype('>i4'))
    ADCmax=0x800000
    Vref=2.5
    b = (a - ADCmax/2)*2*Vref/ADCmax/3.5*1000
    ecg_signal = b - np.mean(b)
    return ecg_signal

def AnalyseHeartrate(ecg_signal_df):
    _, rpeaks = nk.ecg_peaks(ecg_signal_df['orig'], sampling_rate=200, correct_artifacts=False)
    ret = {'rpeaks':rpeaks['ECG_R_Peaks'].tolist()}
    return ret 

sys.stdout.reconfigure(encoding='utf-8')

pd.set_option("display.max_rows", 6000, "display.max_columns",200)
pd.set_option('display.width', 1000)

print("Skriptas rpeaks sulyginimui. Lyginamas rpeaks masyvas, suformuotas iš json failo,")
print("nuskaityto iš Zive frontendo ir rpeaks masyvas, gautas iš EKG signalo naudojant")
print("Neurokit2 funkciją ecg_peaks. EKG signalas (įrašas) irgi gautas iš Zive frontendo.")
print("Abu rpeaks masyvai įrašomi į json vizualiniam sulyginimui su http://www.jsondiff.com/")
print("rpeaks iš json failo varde pridėta '-js', rpeaks iš signalo - pridėta '-sg'")


file_names = ['1625402.027', '1625400.796', '1630757.924','1644283.039', '1644398.788',
'1645154.772','1644283.039', '1644398.788', '1645154.772']
# file_names = ['1625402.027']
# file_name = ['mano_1638705.736']

for file_name in file_names:    
    print(f"\nZive įrašas:  {file_name:>2}")

    # I-a dalis: nuskaitome rpeaks iš json failo
    filename = file_name + '.json'
    with open(filename,'r', encoding='UTF-8', errors = 'ignore') as f:
        data = json.loads(f.read())
    rpeaks_dict = data['rpeaks']
    rpeaks_from_json = np.array([dict['sampleIndex'] for dict in rpeaks_dict])
    # rpeaks_from_json = np.array([3,5,7,10,11,12,13,15,17,19,20,22,23,24])
    # print(rpeaks_from_json)

    print(f"rpeaks iš json failo: {len(rpeaks_from_json)}")
    # print(rpeaks_json) 

    # Suformuojame supaprastintą json failą sulyginimui, prie vardo pridėta 'js'
    # Sulyginimui naudoju http://www.jsondiff.com/
    data = [{"sampleIndex":int(c), "annotationValue":"N"} for c in rpeaks_from_json]
    filename = file_name + '-js' + '.json'
    with open(filename, 'w', encoding='UTF-8') as outfile:
        json.dump(data, outfile)
    # print(data)    


    # II-a dalis: suformuojame rpeaks su Neurokitu,
    # pakartojant Zive skriptą iš analysis.py ir heartrate_analysis.py
    ecg_signal_df = pd.DataFrame(zive_read_file_1ch(file_name), columns=['orig'])
    analysis_results = AnalyseHeartrate(ecg_signal_df)
    rpeaks_from_signal = analysis_results['rpeaks']
    print(f"rpeaks iš signal: {len(rpeaks_from_signal)}")

    # print(rpeaks_from_signal)
    
  # Suformuojame supaprastintą json failą sulyginimui, prie vardo pridėta 'sg'
    data = [{"sampleIndex":int(c), "annotationValue":"N"} for c in rpeaks_from_signal]
    filename = file_name + '-sg' + '.json'
    with open(filename, 'w', encoding='UTF-8') as outfile:
        json.dump(data, outfile)
    # print(data)    

    print("\nReikšmės faile rpeaks_from_json kurių nėra faile rpeaks_from_signal")
    ab = np.setdiff1d(rpeaks_from_json, rpeaks_from_signal)
    # https://numpy.org/doc/stable/reference/generated/numpy.setdiff1d.html
    # print(ab)   # Return the unique values in a that are not in b

    flag = np.size(ab)
    if flag:
        sorter = np.argsort(rpeaks_from_json)
        idxs = sorter[np.searchsorted(rpeaks_from_json, ab, sorter=sorter)]
        print(f"i     index   rpeak")
        for i in range(len(idxs)):
            print(f"{i} {idxs[i]:>9} {ab[i]:>7}")
        # print(idxs)
    else:
        print('Tokių reikšmių nėra')

    print("Reikšmės faile rpeaks_from_signal kurių nėra faile rpeaks_from_json")
    ba = np.setdiff1d(rpeaks_from_signal,rpeaks_from_json)
    # print(ba)   # Return the unique values in b that are not in a

    flag = np.size(ba)
    if flag:
        sorter = np.argsort(rpeaks_from_signal)
        idxs = sorter[np.searchsorted(rpeaks_from_signal, ba, sorter=sorter)]
        print(f"i     index   rpeak")
        for i in range(len(idxs)):
            print(f"{i} {idxs[i]:>9} {ba[i]:>7}")
        # print(idxs)
    else:
        print('Tokių reikšmių nėra')






