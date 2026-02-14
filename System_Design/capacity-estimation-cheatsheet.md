# 🚀 The Ultimate System Design Capacity Estimation Manual

This guide serves as a permanent reference for performing "Back-of-the-Envelope" calculations. Use the **Twitter (300M DAU)** example to ground the concepts.

---

## 1. Core Conversion Table (The Foundation)
Keep these conversions in your head to avoid "math paralysis" during an interview.

| Unit | Power of 10 | Real-World Equivalent |
| :--- | :--- | :--- |
| **Thousand** | $10^3$ | 1 KB |
| **Million** | $10^6$ | 1 MB |
| **Billion** | $10^9$ | 1 GB |
| **Trillion** | $10^{12}$ | 1 TB |
| **Quadrillion** | $10^{15}$ | 1 PB |

* **Time Shortcut:** $1 \text{ Day} \approx 100,000 \text{ Seconds}$ (Actually 86,400). Using 100k makes division instant.
* **Data Shortcut:** $1 \text{ Million requests/day} \approx 12 \text{ requests/second (RPS)}$.

---

## 2. Step-by-Step Estimation Framework

### Step A: Traffic (Throughput)
**Goal:** Determine how many servers/load balancers you need.

1.  **Identify DAU:** (Daily Active Users). Example: **300 Million**.
2.  **Determine Write Rate:** How many times does a user create content? (e.g., 1 tweet/day).
    * $300M / 100,000s = \mathbf{3,000 \text{ QPS (Writes)}}$.
3.  **Determine Read Rate:** How many times do they consume? (e.g., 10 views/day).
    * $3,000 \times 10 = \mathbf{30,000 \text{ QPS (Reads)}}$.
4.  **Peak Factor:** Systems aren't flat. Multiply by **2x to 5x** for peak traffic (events, holidays).

### Step B: Storage (Persistence)
**Goal:** Determine database sharding and hardware costs for 5 years.

1.  **Size the Object:** * `Tweet_ID` (8 bytes) + `User_ID` (8 bytes) + `Text` (280 bytes) + `Metadata` (100 bytes) $\approx$ **400 Bytes**.
2.  **Daily Total:** $300M \times 400B = \mathbf{120 \text{ GB/day}}$.
3.  **Media Multiplier:** If 10% are images (200 KB each):
    * $30M \times 200KB = \mathbf{6 \text{ TB/day}}$.
4.  **Long-term Growth:** $6.12 \text{ TB/day} \times 365 \text{ days} \times 5 \text{ years} \approx \mathbf{11 \text{ PB}}$.

### Step C: Bandwidth (Network)
**Goal:** Determine if you need a CDN or dedicated direct-connect lines.

* **Ingress (In):** What your servers swallow. (6.12 TB / 100k sec) = **~60 MB/s**.
* **Egress (Out):** What you serve to users. Since Reads are 10x Writes: $60MB/s \times 10 = \mathbf{600 \text{ MB/s}}$.

---

## 3. High-Context Design Decisions
*Why do these numbers change the architecture?*

### 1. The Cache Rule (80/20)
Don't cache everything. Cache the **"Hot Data"**.
* **Calculation:** 20% of daily traffic volume. 
* **Context:** For Twitter, 20% of 120GB text = **24 GB**. This fits in one high-memory Redis node. Images are too big to cache in RAM entirely; use a **CDN** (Edge Caching) for those.

### 2. Database Selection
* **If Storage > 1 TB:** A single SQL instance will struggle. You **must** discuss **Sharding** (partitioning data across multiple DBs).
* **If Read QPS > 2k-5k:** A single DB disk cannot keep up. You **must** add **Read Replicas**.

### 3. The "Object Store" Secret
Never store images/videos (BLOBs) in a relational database.
* **Context:** Storing 11 PB in MySQL is a nightmare. 
* **Strategy:** Store the image in **S3/Object Store**. Store only the **URL string** (100 bytes) in the Database. This keeps your DB indexes fast and lean.

---

## 4. Latency "Gut Check"
*If your design requires these steps, keep these times in mind:*

* **Reading from RAM:** 100 ns (Lightning fast)
* **Reading from SSD:** 1 ms (Standard)
* **Packet from NY to London:** 150 ms (Human-perceivable delay)
* **Database Seek:** 10 ms (Slow if done too often)

---

## 5. Summary Checklist for Interviews
1.  [ ] **Clarify:** "Are we talking about 300M total users or active users?"
2.  [ ] **Estimate Traffic:** Calculate QPS (Read vs Write).
3.  [ ] **Estimate Storage:** Calculate 5-year data footprint.
4.  [ ] **Estimate Bandwidth:** Calculate Ingress/Egress per second.
5.  [ ] **Apply Constraints:** "Since we have 11 PB, I will use S3 for media and Sharded NoSQL for metadata."