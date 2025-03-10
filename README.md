# Integration of KGs and PSNs for biomedical application

## Abstract
Over the past year, there has been significant progress in automating the collection, integration, and analysis of biomedical data through knowledge graphs (KGs), which represent entities (e.g., proteins, drugs) and their relationships. KGs have been used in areas like RNA-targeted therapies [[1]](#fn1). Graph representation learning techniques [[2]](#fn2), such as graph neural networks, help extract insights from KGs by predicting new relationships between entities. However, a gap persists between case-specific predictions and generalized knowledge from KGs.

The goal is to develop an approach that integrates specific sample data with broad knowledge from knowledge graphs (KGs), while also deriving new relationships within a KG based on information from specific sample data. This involves linking nodes representing individual patients or samples to broader concepts like genes or RNA molecules. Secondly, given the vast number of nodes in a KG compared to the often limited number of cases in medical studies, new techniques should be developed to process a KG in a way that biases its representation to retain information from less represented nodes.

For experimentation purposes we have used various knowledge base created using PheKnowLator[[3]][#fn3], described in the report, and patient data contained in the 0.1.21 v. cohort of GA4GH Phenopackets[[4]][#fn4] that represent individuals with Mendelian diseases.

## References
<a name="fn1">1</a> Cavalleri, ..., Casiraghi, Valentini, Mesiti. RNA-KG: An ontology-based knowledge graph for representing interactions involving RNA molecules.

<a name="fn2">2</a> Hamilton, W. L. (2020). Graph representation learning. Synthesis Lectures on Artifical Intelligence and Machine Learning, 14(3), 1-159.

<a name="fn3">3</a> Callahan, Tiffany J. et al. An Open-Source Knowledge Graph Ecosystem for the Life Sciences. ArXiv abs/2307.05727 (2023)

<a name="fn4">4</a> Peter Robinson, Daniel Danis, Lex Dingemans, adamklocperk, Peter Hansen, & tudorgroza. (2024). monarch-initiative/phenopacket-store: 0.1.21 (0.1.21). Zenodo.

## Contents
At the moment the main features of the repository are the following:
 * `utils/prepareData.py`, the script to build the KG we have worked on, mainly by incorporating the KG with the patient information
 * `KG_analysis/KG_analysis.ipynb`, a notebook that describes the characteristics of the used KG
