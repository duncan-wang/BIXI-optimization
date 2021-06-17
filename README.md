# BIXI-optimization

### Route optimization for bike rebalancing within the BIXI bike-sharing system

Published in Towards Data Science: https://towardsdatascience.com/a-mixed-integer-optimization-approach-to-rebalancing-a-bike-sharing-system-48d5ad0898bd

 
Project Contributors: Tiancheng Zhang, Becky Zhou, Hanna Swail, & Duncan Wang 

BIXI is a non-for-profit, Montreal-based public bike sharing system with a network of over 7000 bikes dispersed across 600+ stations on the island. Since BIXI's cost scheme is designed for short-term trips, the dynamic nature of the system presents the operational risk of costs incurred due to bike shortages in locations with high demand, and bike surpluses in locations with low demand. In order to reduce potential imbalances within the bike share system, operators of BIXI known as "drivers" are required to redistribute bicycles from one station to another using trucks, in order to rebalance the system when necessary. As such, there is a significant value in examining how BIXI can meet the fluctuating demands of customers through rebalancing bikes to alleviate shortages and surpluses. Doing so can ensure that BIXI can continue to attract more riders, while minimizing inefficiencies due to imbalances in the system.

For this project, we aimed to use mixed-integer optimization to generate a bike rebalancing strategy which meets the fluctuating demands of BIXI customers, while minimizing estimated costs incurred from running the distribution system. We used Gurobi Solver. 

We created three models; the first model aims to rebalance bikes in a way which minimizes cost of rebalancing, the second model minimizes time, and the third model uses a priority constraint to ensure preferential rebalancing of stations near hospital first. 

The files contain the codes for data preprocessing, visualization and three optimization models we covered in the report. Raw datasets were obtained from BIXI Open Data. All datasets necessary for the demo problem in the report are stored in their respective folder. Note that we refer to our base model as Problem 1, operation time minimization extension as Problem 2 and prioritized routing as Problem 3.
