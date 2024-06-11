# LegalAI-RAG-ContractAdvisor
ContractAdvisorRAG: Development of a Q&A system with RAG using Langchain. This repository contains the code and documentation for building an AI-based legal assistance system for contracts. It includes retrieval and generation components, backend and frontend integration, as well as tools for evaluating and optimizing the RAG system using RAGAS.

**Motivation:**

- Efficiently answer questions about specific clauses and terms within contracts.
- Improve accessibility and understanding of legal documents for non-legal professionals.
- Explore the potential of RAG systems in legal applications.

**Objectives:**

* **Research:** Identify best practices and challenges in building and evaluating RAG systems.
* **Implementation:** Build a basic Q&A pipeline with Langchain and evaluate its performance.
* **Optimization:** Enhance the system with targeted improvements for legal document interaction.
* **Evaluation:** Measure the impact of optimizations and document the findings.


**Key Findings:**

![Optimization Techniques Comparison](screenshots/comparison_improvement_approches.png)

* Simple vector database backed RAG pipeline implemented and evaluated with RAGAS.
* Major improvement areas found out at retrieval component.
* The retrieval component optimized with tools like query optimization, context compression, and context reranking.
* The final RAG pipeline for Q&A works fine by combining query optimization with CoHERE reranking from Langchain.

**Project demo video:**

[![ContractAdvisorRAG Video](https://img.youtube.com/vi/KjBWNNN3thA/maxresdefault.jpg)](https://www.youtube.com/watch?v=KjBWNNN3thA)

The video showcases the basic functionality of the ContractAdvisorRAG system.

**Future Work:**

* Continue refining the system with additional legal data and domain-specific training.
* Explore integrating external knowledge sources and legal reasoning capabilities.
* Analyze the system's fairness and potential biases in the context of legal applications.

**Contributing:**

We encourage contributions to this project. Feel free to fork the repository, propose improvements, and share your feedback.

**License:**

This project is licensed under the MIT License.

## Contributors

- [Elias Assamnew](https://github.com/gelifatsy) 

We hope this project contributes to the advancement of AI-powered legal solutions. Please do not hesitate to reach out with any questions or suggestions.