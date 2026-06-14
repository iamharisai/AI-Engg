

## 3_rag_v1.py
This file execution took some minutes because of loading and chinking and embedding , but In Langsmith it shows this trace took only 5.48s, which is actually the the time of retriver and answering question. It is not tracing chunking and embedding, so Langsmith is not tracking everything. And every time we need to load the pdf freshly. Let's solve these two problems:
