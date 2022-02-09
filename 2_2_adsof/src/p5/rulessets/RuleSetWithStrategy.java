/**
 * 
 */
package p5.rulessets;

import p5.rulessets.strategies.IStrategy;

/**
 * Rule set in which the rules are applied to the context with a given strategy
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class RuleSetWithStrategy<T> extends RuleSet<T> {
	private IStrategy<T> strategy;
	
	public RuleSetWithStrategy(IStrategy<T> strategy) {
		super();
		this.strategy = strategy;
	}
	
	@Override
	public void process() {
		strategy.applyStrategy(this.rules, this.context);
	}

	/**
	 * @return the strategy
	 */
	public IStrategy<T> getStrategy() {
		return strategy;
	}

	/**
	 * @param strategy the strategy to set
	 */
	public void setStrategy(IStrategy<T> strategy) {
		this.strategy = strategy;
	}
	
}
