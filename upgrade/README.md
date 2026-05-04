# Adaptive Franchise Training System
### A Behaviorally Grounded Reinforcement Learning Prototype for QSR Training

**University of Louisville | Yum! Center for Global Franchise Excellence**
**ABM Conference 2026 | Palma de Mallorca, Spain**

---

## Overview

This repository contains a research prototype simulating an adaptive training system for quick-service restaurant (QSR) franchise environments. The system tracks behavioral learning signals in real time and dynamically adjusts training difficulty, pacing, and feedback — rather than delivering the same standardized content to every trainee.

The core idea: instead of one-size-fits-all training, the system continuously adapts based on how each individual is actually learning.

---

## Research Context

Most franchise training systems are standardized by design. While this supports consistency, it assumes all trainees learn at the same pace and in the same way. In reality, trainees differ significantly in attention, response patterns, learning speed, and cognitive load tolerance.

This prototype models an adaptive training loop grounded in:
- **Cognitive Load Theory** (Sweller, 1988)
- **Reinforcement Learning principles** (Sutton & Barto, 2018)
- **Attention and response control measurement** (Bundesen, 1990; Logan, 1994)

---

## System Architecture

```
adaptive-franchise-training-rl/
│
├── main.py                        # Entry point
├── constants.py                   # All research parameters
├── data_models.py                 # LearnerInteraction + LearnerProfile
│
├── metrics/                       # Behavioral signal computation
│   ├── attention.py               # Attention consistency
│   ├── response_control.py        # Speed-accuracy tradeoff
│   ├── learning_efficiency.py     # Improvement over time
│   ├── cognitive_load.py          # Load proxy
│   ├── error_pattern.py           # Repeated vs random errors
│   └── __init__.py                # compute_all_metrics()
│
├── simulator/                     # Adaptive policy engine
│   └── adaptive_policy.py         # 5-rule policy + mastery + decay
│
├── experiments/                   # Simulation runner
│   └── run_simulation.py          # Control vs treatment experiment
│
├── analysis/                      # Results and visualization
│   ├── metrics_over_time.py       # Learning curve tracking
│   ├── learning_profiles.py       # Learner type classification
│   ├── results_summary.py         # Multi-trial aggregation
│   └── plots.py                   # Matplotlib visualizations
│
└── cognition/                     # Cognitive modeling
    └── reward_function.py         # RL reward signal definition
```

---

## Behavioral Signals Tracked

| Signal | What it measures |
|--------|-----------------|
| Attention consistency | Response time variability across trials |
| Response control | Speed-accuracy tradeoff |
| Learning efficiency | Accuracy improvement over time |
| Cognitive load | Behavioral proxy (time + errors) |
| Error pattern | Repeated vs random error distribution |

---

## Adaptive Policy Rules

The system applies these rules in order (first match wins):

1. **Impulsive** — fast + inaccurate → slow down, increase feedback
2. **Overload** — slow + inaccurate → simplify content
3. **Stuck** — 3+ wrong in a row → repeat content
4. **Ready to advance** — improving + low load → increase difficulty
5. **Default** — on track → maintain settings

---

## Learner Profiles

The system classifies each learner into one of five types:

| Profile | Description |
|---------|-------------|
| Efficient | Fast, accurate, low load |
| Deep Learner | Slower but steady, improving |
| Impulsive | Fast but inaccurate |
| Attention Variable | Inconsistent response patterns |
| Struggling | High load, low accuracy, not improving |

---

## How to Run

```bash
# Install dependencies
pip install numpy matplotlib

# Run single simulation
python main.py

# Results saved to results/ folder
```

---

## Key Parameters (constants.py)

| Parameter | Value |
|-----------|-------|
| Mastery threshold | 80% accuracy |
| Min attempts for mastery | 5 |
| Spaced repetition intervals | 1, 3, 7, 14 rounds |
| Knowledge decay rate | 10% per round |
| Difficulty levels | Easy, Medium, Hard |
| Learners per simulation | 50 |
| Training rounds | 20 |

---

## Experimental Design

This prototype supports a randomized controlled comparison:

- **Control group** — standard training (fixed easy difficulty, no adaptation)
- **Treatment group** — adaptive training (policy-based dynamic adjustment)

Outcomes compared:
- Learning performance
- Cognitive load
- Learning efficiency trajectory
- Learner profile distribution

---

## Research Contribution

This system is designed as a **cognitive-state-aware adaptive learning framework** — not just a content recommendation engine. It models how people learn under cognitive constraints, which is an underexplored area in both franchise training research and adaptive learning systems literature.

The combination of RL-inspired policy, behavioral signal tracking, cognitive load modeling, and experimental validation in a real-world franchise context represents a novel contribution to organizational training effectiveness research.

---

## Citation

If referencing this work:

> [Author]. (2026). *Adaptive Reinforcement Learning for Franchise Training: Cognitive Load, Attention, and Performance in Quick-Service Restaurant Systems.* Advances in Business Management Conference, Palma de Mallorca, Spain.

---

## Contact

University of Louisville | Yum! Center for Global Franchise Excellence
