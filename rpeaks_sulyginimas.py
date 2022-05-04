# %%
# Skriptas rpeaks sekų, gautų iš .json failo ir EKG įrašo, panaudojant NEUROKIT2, sulyginimui

import pandas as pd
import numpy as np
import json
import yaml
import neurokit2 as nk
from pathlib import Path


def zive_read_file_1ch(filename):
    f = open(filename, "r")
    a = np.fromfile(f, dtype=np.dtype('>i4'))
    ADCmax = 0x800000
    Vref = 2.5
    b = (a - ADCmax/2)*2*Vref/ADCmax/3.5*1000
    ecg_signal = b - np.mean(b)
    return ecg_signal


def AnalyseHeartrate(ecg_signal_df):
<<<<<<< HEAD
    _, rpeaks = nk.ecg_peaks(
        ecg_signal_df['orig'], sampling_rate=200, method="neurokit", correct_artifacts=False)
    ret = {'rpeaks': rpeaks['ECG_R_Peaks'].tolist()}
    return ret
=======
    _, rpeaks = nk.ecg_peaks(ecg_signal_df['orig'], method="neurokit", sampling_rate=200, correct_artifacts=False)
    ret = {'rpeaks':rpeaks['ECG_R_Peaks'].tolist()}
    return ret 
>>>>>>> db6faaafc95328d5235184c019113e5d6bd15478


pd.set_option("display.max_rows", 6000, "display.max_columns", 200)
pd.set_option('display.width', 1000)

print("Skriptas rpeaks sulyginimui. Lyginamas rpeaks masyvas, suformuotas iš json failo,")
print("nuskaityto iš Zive frontendo ir rpeaks masyvas, gautas iš EKG signalo naudojant")
print("Neurokit2 funkciją ecg_peaks. EKG signalas (įrašas) irgi gautas iš Zive frontendo.")
print("Abu rpeaks masyvai įrašomi į json vizualiniam sulyginimui su http://www.jsondiff.com/")
print("rpeaks iš json failo varde pridėta '-js', rpeaks iš signalo - pridėta '-sg'")

rec_dir = Path("data")

filepath = Path(rec_dir, "name_list.yaml")
with open(filepath, "r") as f:
    dictionary = yaml.load(f, Loader=yaml.FullLoader)
list = dictionary['file_names']
for file_name in list:
    print(str(file_name))

for file_name in list:
    file_name = str(file_name)
    print(f"\nZive įrašas:  {file_name:>2}")

    # I-a dalis: nuskaitome rpeaks iš json failo

    filepath = Path(rec_dir, file_name + '.json')
    with open(filepath, 'r', encoding='UTF-8', errors='ignore') as f:
        data = json.loads(f.read())
    rpeaks_dict = data['rpeaks']
    rpeaks_from_json = np.array([dict['sampleIndex'] for dict in rpeaks_dict])
    # rpeaks_from_json = np.array([3,5,7,10,11,12,13,15,17,19,20,22,23,24])
    # print(rpeaks_from_json)

    print(f"rpeaks iš json failo: {len(rpeaks_from_json)}")
    # print(rpeaks_json)

    # Suformuojame supaprastintą json failą sulyginimui, prie vardo pridėta 'js'
    # Sulyginimui naudoju http://www.jsondiff.com/
    # data = [{"sampleIndex":int(c), "annotationValue":"N"} for c in rpeaks_from_json]
    # filename = file_name + '-js' + '.json'
    # with open(filename, 'w', encoding='UTF-8') as outfile:
    #     json.dump(data, outfile)
    # print(data)

    # II-a dalis: suformuojame rpeaks su Neurokitu,
    # pakartojant Zive skriptą iš analysis.py ir heartrate_analysis.py
    filepath = Path(rec_dir, file_name)
    signal_raw = zive_read_file_1ch(filepath)
    # signal = nk.signal_filter(signal=signal_raw, sampling_rate=200, lowcut=0.5, method="butterworth", order=5)
    signal = signal_raw
    ecg_signal_df = pd.DataFrame(signal, columns=['orig'])

    analysis_results = AnalyseHeartrate(ecg_signal_df)
    rpeaks_from_signal = analysis_results['rpeaks']
    print(f"rpeaks iš signal: {len(rpeaks_from_signal)}")

    # print(rpeaks_from_signal)
<<<<<<< HEAD

  # Suformuojame supaprastintą json failą sulyginimui, prie vardo pridėta 'sg'
=======
    
  # Suformuojame spython3 upaprastintą json failą sulyginimui, prie vardo pridėta 'sg'
>>>>>>> db6faaafc95328d5235184c019113e5d6bd15478
    # data = [{"sampleIndex":int(c), "annotationValue":"N"} for c in rpeaks_from_signal]
    # filename = file_name + '-sg' + '.json'
    # with open(filename, 'w', encoding='UTF-8') as outfile:
    #     json.dump(data, outfile)
    # print(data)

    # Sulyginimas

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
    ba = np.setdiff1d(rpeaks_from_signal, rpeaks_from_json)
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
