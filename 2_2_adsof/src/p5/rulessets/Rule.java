/**
 * 
 */
package p5.rulessets;

import java.util.function.Consumer;
import java.util.function.Predicate;

/**
 * Class to represent a rule. Rules have a condition and an execution (which will be executed if the condition is met)
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class Rule<T> {
	private String name;
	private String description;
	private Predicate<? super T> condition;
	private Consumer<? super T> execution;
	
	private Rule(String name, String description) {
		this.name = name;
		this.description = description;
	}
	
	/**
	 * Static creation of a rule of a given type
	 * @param <N> - generic type of the object the rule can be applied on
	 * @param name - name of the rule
	 * @param description - description of the rule
	 * @return Rule<N> - the rule 
	 */
	public static <N> Rule<N> rule(String name, String description){
		return new Rule<N>(name, description);
	}
	
	/**
	 * Sets the condition the rule should check
	 * @param condition - condition to check
	 * @return the updated rule
	 */
	public Rule<T> when(Predicate<? super T> condition){
		this.condition = condition;
		return this;
	}
	
	/**
	 * Sets the action that should be taken if the condition is met
	 * @param execution - execution to do
	 * @return the updated rule
	 */
	public Rule<T> exec(Consumer<? super T> execution){
		this.execution = execution;
		return this;
	}
	
	/**
	 * Checks the condition on a given object and executes the rule if it is satisfied
	 * @param obj 
	 */
	public void process(T obj) {
		if (this.condition.test(obj)) this.execution.accept(obj);
	}
	
	public String toString() {
		return this.name + ": " + this.description;
	}

	/**
	 * @return the condition
	 */
	public Predicate<? super T> getCondition() {
		return condition;
	}

	/**
	 * @return the execution
	 */
	public Consumer<? super T> getExecution() {
		return execution;
	}
}
