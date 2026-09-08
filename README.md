\# RulebookAI



RulebookAI is a rule-grounded university policy question-answering system.



Instead of behaving like a generic chatbot, the system retrieves relevant rules from a university rulebook corpus and uses those rules to construct an answer.



\## Key Features



\- Question answering over university regulations

\- Rule-based retrieval from the rulebook corpus

\- Source citation for retrieved rules

\- Relevance/similarity scores

\- Displays the rules used to generate an answer

\- Detects potential contradictions and exceptions

\- Handles unknown questions without blindly inventing rules

\- FastAPI backend

\- Simple HTML frontend



\## Architecture



```text

User Question

&#x20;     |

&#x20;     v

Frontend

&#x20;     |

&#x20;     v

FastAPI /ask endpoint

&#x20;     |

&#x20;     v

Rule Retrieval

&#x20;     |

&#x20;     v

Relevant Rules

&#x20;     |

&#x20;     +------> Answer Generation

&#x20;     |

&#x20;     +------> Source Information

&#x20;     |

&#x20;     +------> Rules Used

&#x20;     |

&#x20;     +------> Contradiction Detection

&#x20;     |

&#x20;     v

Frontend Response

