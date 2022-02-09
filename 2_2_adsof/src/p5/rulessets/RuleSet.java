/**
 * 
 */
package p5.rulessets;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

/**
 * Class to represent a collection of rules and a collection of objects to which the rules should be applied
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class RuleSet<T> {
	protected List<Rule<? super T>> rules = new ArrayList<>();
	protected List<T> context = new ArrayList<>();
	
	public RuleSet() {	}
	
	/**
	 * Adds a new rule to the given rule set
	 * @param rule - rule to add
	 * @return the updated rule set
	 */
	public RuleSet<T> add(Rule<? super T> rule){
		this.rules.add(rule);
		return this;
	}
	
	/**
	 * Adds new objects to the context of the rule set
	 * @param c - collection of objects
	 */
	public void setExecContext(Collection<? extends T> c) {
		this.context.addAll(c);
	}
	
	/**
	 * Processes the context with the rules in the rule set
	 */
	public void process() {
		for (Rule<? super T> rule : this.rules) {
			for (T obj : this.context) {
				rule.process(obj);
			}
		}
	}
}
