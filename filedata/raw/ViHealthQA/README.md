---
task_categories:
- question-answering
language:
- vi
tags:
- medical
pretty_name: Vietnamese Healthcare Question Answering Dataset
size_categories:
- 10K<n<100K
---
## Disclaimer:
The dataset may contain personal information crawled along with the contents of various sources. Please make a filter in pre-processing data before starting your research training.

# SPBERTQA: A Two-Stage Question Answering System Based on Sentence Transformers for Medical Texts
This is the official repository for the ViHealthQA dataset from the paper [SPBERTQA: A Two-Stage Question Answering System Based on Sentence Transformers for Medical Texts](https://arxiv.org/pdf/2206.09600.pdf), which was accepted at the [KSEM-2022](https://ksem22.smart-conf.net/index.html).

# Citation Information
The provided dataset is only used for research purposes!

```
@InProceedings{nguyen2022viheathqa,
  author="Nguyen, Nhung Thi-Hong
  and Ha, Phuong Phan-Dieu
  and Nguyen, Luan Thanh
  and Van Nguyen, Kiet
  and Nguyen, Ngan Luu-Thuy",
  title="SPBERTQA: A Two-Stage Question Answering System Based on Sentence Transformers for Medical Texts",
  booktitle="Knowledge Science, Engineering and Management",
  year="2022",
  publisher="Springer International Publishing",
  address="Cham",
  pages="371--382",
  isbn="978-3-031-10986-7"
}

```

# Abstract

Question answering (QA) systems have gained explosive attention in recent years. However, QA tasks in Vietnamese do not have many datasets. Significantly, there is mostly no dataset in the medical domain. Therefore, we built a Vietnamese Healthcare Question Answering dataset (ViHealthQA), including 10,015 question-answer passage pairs for this task, in which questions from health-interested users were asked on prestigious health websites and answers from highly qualified experts. This paper proposes a two-stage QA system based on Sentence-BERT (SBERT) using multiple negatives ranking (MNR) loss combined with BM25. Then, we conduct diverse experiments with many bag-of-words models to assess our system’s performance. With the obtained results, this system achieves better performance than traditional methods.

# Dataset
The ViHealthQA dataset is consist of 10,015 question-answer passage pairs. Note that questions are from health-interested users asked on prestigious health websites and answers are from highly qualified experts.

The dataset is divided into three parts as below:
1. Train set: 7.01K question-answer pairs
2. Valid set: 2.01 question-answer pairs
3. Test set: 993 question-answer pairs

# Contact
Please feel free to contact us by email luannt@uit.edu.vn if you have any further information!