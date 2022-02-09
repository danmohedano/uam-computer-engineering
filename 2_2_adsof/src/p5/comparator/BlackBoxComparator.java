/**
 * 
 */
package p5.comparator;

import java.lang.reflect.InvocationTargetException;
import java.util.*;
import java.util.function.Predicate;

import p5.graph.ConstrainedGraph;
import p5.graph.Node;

/**
 * Class to implement a comparator between Constrained Graphs using predicates and criteria
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class BlackBoxComparator<N, E> implements Comparator<ConstrainedGraph<N,E>> {
	private Map<Predicate<Node<N>>, Criteria> properties = new HashMap<>();
	
	public BlackBoxComparator() {	}
	
	/**
	 * Compare two constrained graphs using the properties stored in the comparator
	 * @return natural order
	 */
	@Override
	public int compare(ConstrainedGraph<N, E> o1, ConstrainedGraph<N, E> o2) {
		return this.execute(o1) - this.execute(o2);
	}

	/**
	 * Adds a new property to the comparator
	 * @param c - criteria
	 * @param prop - property
	 * @return the updated comparator
	 */
	public BlackBoxComparator<N,E> addCriteria(Criteria c, Predicate<Node<N>> prop) {
		this.properties.put(prop, c);
		return this;
	}
	
	/**
	 * Executes all properties in a given Constrained graph
	 * @param o - the graph
	 * @return amount of properties passed
	 */
	private int execute(ConstrainedGraph<N, E> o) {
		int n = 0;		
		for (Map.Entry<Predicate<Node<N>>, Criteria> p: this.properties.entrySet()) {
			try {
				if ((boolean)p.getValue().getFunction().invoke(o, p.getKey())) n++;
			} catch (IllegalAccessException | IllegalArgumentException | InvocationTargetException e) {
				e.printStackTrace();
			}	
		}
		return n;
	}
}
