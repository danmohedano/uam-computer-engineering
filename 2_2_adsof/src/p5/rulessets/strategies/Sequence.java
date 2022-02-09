/**
 * 
 */
package p5.rulessets.strategies;

import java.util.Collection;

import p5.rulessets.Rule;

/**
 * Class to implement the sequence strategy (apply all rules once to every object)
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class Sequence<T> implements IStrategy<T> {
	public Sequence() {}
	@Override
	public void applyStrategy(Collection<Rule<? super T>> rules, Collection<T> objs) {
		for (Rule<? super T> rule : rules) {
			for (T obj : objs) {
				rule.process(obj);
			}
		}
	}

}
