/**
 * 
 */
package p5.rulessets.strategies;

import java.util.Collection;

import p5.rulessets.Rule;

/**
 * Interface to represent a given strategy. It can apply a collection of rules to a collection of objects following a specific strategy
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public interface IStrategy<T> {
	void applyStrategy(Collection<Rule<? super T>> rules, Collection<T> objs);
}
