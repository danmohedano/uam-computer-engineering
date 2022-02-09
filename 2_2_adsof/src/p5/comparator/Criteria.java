/**
 * 
 */
package p5.comparator;

import java.lang.reflect.Method;
import java.util.function.Predicate;

import p5.graph.ConstrainedGraph;

/**
 * Criteria class to relate the criteria with the method to use in the constrained graph
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public enum Criteria {
	EXISTENTIAL("exists"),
	UNITARY("one"),
	UNIVERSAL("forAll");
	
	private Criteria(String function) {
		this.function = function;
	}
	private String function;
	/**
	 * Get the method of constrained graph associated with this criteria
	 * @return the method
	 */
	public Method getFunction(){
		ConstrainedGraph<Object,Object> g = new ConstrainedGraph<Object, Object>();
		try {
			return g.getClass().getDeclaredMethod(function, Predicate.class);
		} catch (NoSuchMethodException | SecurityException e) {
			e.printStackTrace();
			return null;
		}
	}
}
