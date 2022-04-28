# https://pythonspeed.com/articles/activate-conda-dockerfile/

FROM continuumio/miniconda3

RUN mkdir /source
WORKDIR /source

# Create the environment:
COPY ecg_lnx_38.yml ./

RUN conda env create -f ecg_lnx_38.yml
RUN echo "created conda environment ecg_lnx"

ADD heartrate_analysis.py mq_listener.py analyse.py zive_cnn_fda_vu_v1.py quality_analysis.py atrial_fibrillation.py ./
ADD model_cnn_fda_vu_v1 model_cnn_fda_vu_v1

# Make RUN commands use the new environment:
# SHELL ["conda", "run", "-n", "ecg_lnx", "/bin/bash", "-c"]


# The code to run when container is started:
ENTRYPOINT ["conda", "run", "-n", "ecg_lnx", "/bin/bash", "-c"]

# Sitas eilutes naudoju tik Zive aplinkoje
ADD index.js ./
# node_modules are preinstalled in a previous CI step (node_modules step)
# lokalioje aplinkoje reikia susikurti tuscia folderi node_modules
ADD node_modules node_modules
CMD ["node ./index.js"]
RUN apt-get update && apt-get install jq -y

ADD test.sh ./
ADD test ./test