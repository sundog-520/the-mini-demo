1.Data Format: JSON
The tree structure is ideal for describing BOMs (Bill of Materials) and is easy to transmit via REST API, simulating the interaction of modern ERP systems.
Libraries: Zero-Dependency Architecture
By avoiding heavy external dependencies like Pandas or NumPy, the script maintains a minimal footprint. This ensures high performance in serverless environments (e.g., AWS Lambda) and eliminates the risk of "dependency hell" during long-term maintenance.
2.Constraint-based Greedy Heuristic
Since the components are not interdependent (e.g., the supplier of component A does not affect the procurement of component B), the local optimum of this problem is the global optimum.
3.How you would incorporate uncertainty in lead times or supplier failure？
  Hard Constraint Filtering
The first step in the code is: `if s['lead_time'] <= data['ddl']`.
Solution: This establishes a "safety margin." All suppliers whose delivery times exceed the deadline (DDL) are directly removed from the shortlist.
Uncertainty Optimization: In practice, human schedulers typically set a safety buffer for the DDL. For example, even if the part is only needed on production line 25, the DDL entered into the code might be set to 20 to offset uncertainties such as logistical delays.
  Waterfall Backfilling
The `remaining_demand` logic in the code allows orders to be assigned to multiple suppliers.
Solution: If the first (cheapest) supplier cannot fully cover your needs due to capacity limitations or minimum order quantity logic, the code automatically switches to the second or third cheapest supplier.
Uncertainty Optimization: This "multi-source sourcing" model naturally reduces reliance on a single supplier. If a supplier suddenly defaults (e.g., goes bankrupt or runs out of stock), this plan has already identified a "backup" option with the second-highest unit price.
  Minimum Order Quantity (MOQ) Risk Hedging: The code uses `max(remainingdemand, sup['moq'])`.
Response: Although this may lead to buying more than demand (inventory overflow), in periods of high uncertainty, "buying more" itself is a risk mitigation measure (safety stock).
Uncertainty Optimization: When a supplier may default, purchasing overstock according to MOQ ensures that even if the next batch of purchases fluctuates, there will still be surplus stock in the warehouse to support production.
