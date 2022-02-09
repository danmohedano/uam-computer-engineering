/**
 * 
 */
package p5.rulessets.strategies;

import java.util.Collection;

import p5.rulessets.Rule;

/**
 * Class to implement the As long as possible strategy (keeps applying rules to the same object until it can't)
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class AsLongAsPossible<T> implements IStrategy<T> {

	public AsLongAsPossible() {	}
	
	@Override
	public void applyStrategy(Collection<Rule<? super T>> rules, Collection<T> objs) {
		for (Rule<? super T> rule : rules) {
			for (T obj : objs) {
				while(rule.getCondition().test(obj)) rule.getExecution().accept(obj);
			}
		}
	}

}
