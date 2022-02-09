/**
 * 
 */
package p5.graph;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.Predicate;

/**
 * Class to implement graphs where properties are applicable
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 * @param <N> - type of the node
 * @param <E> - type of the edge
 *
 */
public class ConstrainedGraph<N, E> extends Graph<N, E> {
	Optional<Node<N>> witness = Optional.empty();
	
	public ConstrainedGraph() {
		super();
	}
	
	/**
	 * Checks if all the nodes in the graph fulfill the property
	 * @param prop - predicate to check
	 * @return true if all nodes fulfill the property
	 */
	public boolean forAll(Predicate<Node<N>> prop) {
		List<Node<N>> list = this.check(prop);
		if (list.size() == this.nodes.size()) return true;
		return false;
	}
	
	/**
	 * Checks if only exactly one node satisfies the property
	 * @param prop - predicate to check
	 * @return true if only one node fulfills the property
	 */
	public boolean one(Predicate<Node<N>> prop) {
		List<Node<N>> list = this.check(prop);
		if (list.size() == 1) return true;
		return false;
	}
	
	/**
	 * Checks if at least one node satisfies the property
	 * @param prop - predicate to check
	 * @return true if at least one node fulfills the property
	 */
	public boolean exists(Predicate<Node<N>> prop) {
		List<Node<N>> list = this.check(prop);
		if (list.size() > 0) return true;
		return false;
	}
	
	/**
	 * Returns all the nodes that satisfy the property
	 * @param prop - predicate to check
	 * @return list of all nodes fulfilling the property
	 */
	private List<Node<N>> check(Predicate<Node<N>> prop){
		List<Node<N>> list = new ArrayList<>();
		for (Node<N> n : this.nodes) {
			if (prop.test(n)) {
				list.add(n);
				this.witness = Optional.of(n);
			}
		}
		if (list.size() == 0) this.witness = Optional.empty();
		return list;
	}
	
	/**
	 * gets the witness
	 * @return the witness
	 */
	public Optional<Node<N>> getWitness(){
		return this.witness;
	}
}
