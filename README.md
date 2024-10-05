# Integration of KGs and PSNs for biomedical application

## Abstract
Over the past year, there has been significant progress in automating the collection, integration, and analysis of biomedical data through knowledge graphs (KGs), which represent entities (e.g., proteins, drugs) and their relationships. KGs have been used in areas like RNA-targeted therapies [[1]](#fn1). Graph representation learning techniques [[2]](#fn1), such as graph neural networks, help extract insights from KGs by predicting new relationships between entities. However, a gap persists between case-specific predictions and generalized knowledge from KGs.

The goal is to develop an approach that integrates specific sample data with broad knowledge from knowledge graphs (KGs), while also deriving new relationships within a KG based on information from specific sample data. This involves linking nodes representing individual patients or samples to broader concepts like genes or RNA molecules. To implement the integration of the two knowledge sources we intend to take inspiration from [[3]](#fn1). Secondly, given the vast number of nodes in a KG compared to the often limited number of cases in medical studies, new techniques should be developed to process a KG in a way that biases its representation to retain information from less represented nodes.

## References
<a name="fn1">1</a> Cavalleri, ..., Casiraghi, Valentini, Mesiti. RNA-KG: An ontology-based knowledge graph for representing interactions involving RNA molecules. To appear in Scientific Data. 

<a name="fn1">2</a> Hamilton, W. L. (2020). Graph representation learning. Synthesis Lectures on Artifical Intelligence and Machine Learning, 14(3), 1-159.

<a name="fn1">3</a> Chandak, P., Huang, K. & Zitnik, M. Building a knowledge graph to enable precision medicine. Sci Data 10, 67 (2023).

## Contents
At the moment the repository is populated by:
* `code` directory, containing the following:
    * `PrimeKG_Analysis/PrimeKGAnalysis.ipynb`, notebook used to understand PrimeKG's characteristics, including the degree distributions per node type and clusterability

## Dependencies
To install the dependencies required to run the code, use `pip`:

```pip install -r requirements.txt```
