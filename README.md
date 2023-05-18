# Aprendizado Profundo para a Predição de Ataques de Negação de Serviço Distribuído

Este é o repositório oficial do nosso [artigo](https://sol.sbc.org.br/index.php/sbrc/article/view/21191) publicado no XL Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC).

### Como este repositório está organizado?
O repositório contém duas pastas principais (experiment_1 e experiment_2) cada uma contendo os artefatos utilizados para os dois experimentos descritos no artigo. Dentro de cada pasta, você irá encontrar:
- **model_*.ipynb:** Arquivo de notebook contendo todo o código necessário para treinar o modelo do experimento descrito em nosso artigo e exibir as métricas de avaliação.
- **full_capture20110818_preprocessed_*.csv:** arquivo CSV contendo os dados pré-processados usados como entrada de rede para treinar o modelo.
- **lstm_autoencoder_ctu13_cap51_*.h:** O arquivo de modelo salvo que foi obtido no final de nosso experimento. Ele pode ser usado para reproduzir o experimento sem ter que treinar o modelo do zero.
- **preprocessing:** Uma pasta contendo os scripts usados na etapa de pré-processamento de dados. Primeiro, o script `data_preprocessing.py` deve ser usado para extrair os recursos selecionados de cada pacote de tráfego de rede e, em seguida, o script `data_transformation.py` deve ser usado para aplicar as medidas estatísticas e obter o formato de dados final usado para treinamento o modelo. Os dados brutos podem ser obtidos no conjunto de dados oficial [website](https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-51/).
