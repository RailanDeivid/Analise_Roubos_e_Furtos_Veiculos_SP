<p align="center">
<img loading="lazy" src="http://img.shields.io/static/v1?label=STATUS&message=FINALIZADO&color=GREEN&style=for-the-badge"/>
</p>

# Análise de Dados Públicos de Furtos e Roubos no municipio de Guarulhos-SP

## Descrição

Este projeto faz parte de uma atividade extensiva dedicada à análise e disseminação de dados públicos sobre furtos e roubos em Guarulhos-SP. A iniciativa visa não apenas compreender as tendências de crimes na região, mas também proporcionar insights valiosos para a comunidade. Através da aplicação de técnicas avançadas de ciência de dados

## Informações dos Dados:
Os dados usados para o desenvolvimento desse projeto são dados abertos da [Secretaria de Segurança Publica de São paulo (SSP)](https://www.ssp.sp.gov.br/estatistica/consultas)
São Paulo é pioneiro na divulgação mensal dos dados estatísticos por Estado, área, município e unidade policial. Os índices também são divulgados trimestralmente. Conteúdo ajuda a monitorar a evolução das tendências criminais e o planejamento do Estado e das polícias.
<br>
As estatísticas criminais são utilizadas para retratar a situação da segurança pública e permitir o planejamento de ações policiais e de investimentos no setor. Em São Paulo, a compilação dos dados é feita pela Secretaria da Segurança Pública, por intermédio da Coordenadoria de Análise e Planejamento (CAP) - responsável pela análise dos dados de interesse policial e pela realização de estudos para prevenir e reprimir a criminalidade.
<br>
* No site das SSP, você pode encontrar:
  * Dados criminais
  * Dados de Produtividade
  * Morte Decorrente de Intervenção Policial
  * Celulares subtraídos
  * Veículos subtraídos
  * Objetos subtraídos

Etapas do projeto:

- [x] Tratamento e armazenamento em um arquivo parquet
- [x] Deploy Dashboard no Streamlit

## Principais Tecnologias Utilizadas

- ``Python 3.12.1``
- ``Streamlit``
- ``Pandas``
- ``Numpy``
- ``Matplotlib``
- ``Seaborn``
- ``plotly``
- ``Folium``

## 📁 Acesso aos do  arquivos projeto
Você pode acessar os arquivos do projeto:

Dados Brutos: [raw](https://github.com/RailanDeivid/Analise_roubos_e_furtos_veiculos_SP/tree/main/data/raw)

Transformações dos dados: [data_preprocessing.ipynb](https://github.com/RailanDeivid/Analise_roubos_e_furtos_veiculos_SP/blob/main/src/preprocessed/data_preprocessing.ipynb)

Dados Tratados: [VeiculosSubtraidos.parquet](https://github.com/RailanDeivid/Analise_roubos_e_furtos_veiculos_SP/tree/main/data/processed)

Codigo App Streamlit: [App](https://github.com/RailanDeivid/Analise_roubos_e_furtos_veiculos_SP/tree/main/app)


## Deploy Streamlit

Link app: [Roubos e Furtos em Guarulhos](https://roubos-e-furtos-em-guarulhos.streamlit.app/)

![image](https://github.com/RailanDeivid/Analise_roubos_e_furtos_veiculos_SP/assets/78448568/598683f0-c0bd-4ba7-b55f-be322cbc7466)


