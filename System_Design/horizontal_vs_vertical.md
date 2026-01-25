# 🌐 System Design Fundamentals: Scaling & Architecture

This guide covers the transition from local code to a scalable cloud service, focusing on the trade-offs between **Vertical** and **Horizontal** scaling.

---

### 🚀 1. The Journey: Code ➔ Service ➔ Cloud

* **Standalone Code:** An algorithm running locally on a single machine.
* **The API (Interface):** To share code, we wrap it in an **API**. Users send a **Request** (input) and receive a **Response** (output).
* **The Cloud:** Moving from a local desktop to remote infrastructure (e.g., AWS, GCP). The cloud provides managed reliability and globally accessible hardware.

---

### ⚖️ 2. Scaling Strategies: Vertical vs. Horizontal

Scaling is the ability of your system to handle increasing load. There are two primary ways to achieve this:



| Feature | Vertical Scaling (Scaling Up) | Horizontal Scaling (Scaling Out) |
| :--- | :--- | :--- |
| **Method** | Upgrade the CPU/RAM of a single machine. | Add more machines to the pool. |
| **Complexity** | **Low:** No architectural changes needed. | **High:** Requires a Load Balancer & Service Discovery. |
| **Fault Tolerance** | **Low:** Single Point of Failure (SPOF). | **High:** If one machine fails, others stay up. |
| **Communication** | **Fast:** Uses Interprocess Communication (IPC). | **Slower:** Uses Network/RPC calls. |
| **Data Consistency**| **Easy:** Data lives on one disk/memory. | **Hard:** Data must be synced across many nodes. |
| **Hardware Limit** | **Hard Ceiling:** Machines have a max size. | **Infinite:** Theoretically scale forever. |
| **Cost** | Expensive at the "high-end" (specialized hardware). | Efficient (uses many "commodity" machines). |

---

### 🚦 3. Critical Infrastructure Components

* **Load Balancer:** Essential for Horizontal Scaling. It acts as a traffic cop, distributing incoming requests so no single server is overwhelmed.
    

[Image of load balancer architecture]

* **RPC (Remote Procedure Call):** How different machines talk to each other over a network.
* **SPOF (Single Point of Failure):** A component that, if it breaks, takes down the whole system. Vertical scaling is inherently prone to this.

---

### 🛠️ 4. The Real-World "Hybrid Model"

Modern systems rarely choose just one. The industry standard is a **Hybrid Approach**:
1.  **Scale Vertically** until it is no longer cost-effective or hardware limits are reached.
2.  **Scale Horizontally** by clustering those powerful machines together.

> **Key Trade-off:** System design is the art of balancing **Scalability** (growth), **Resilience** (uptime), and **Consistency** (data accuracy). You usually have to sacrifice a bit of one to get the others.

---

### 📖 Summary Table: Important Terms

| Term | Definition |
| :--- | :--- |
| **API** | A protocol that allows different software to communicate. |
| **Latency** | The time it takes for a single request to be processed. |
| **Throughput** | The total number of requests a system can handle per second. |
| **Consistency** | Ensuring all users see the same data at the same time. |
| **Redundancy** | Having "spare" parts (servers/databases) to prevent downtime. |

---