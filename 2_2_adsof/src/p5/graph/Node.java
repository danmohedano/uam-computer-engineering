/**
 * 
 */
package p5.graph;

import java.util.*;
/**
 * Class to handle nodes of a generic type
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 * @param T - type of the information stored in the node
 */
public class Node<T> {
	private static int totalNodes = 0;
	private T value;
	private int id;
	private Graph<T,?> graph = null;
	
	public Node(T value) {
		this.value = value;
		this.id = Node.totalNodes;
		Node.totalNodes++;
	}
	
	
	/**
	 * Returns the values of the edges without repetition linking one given node to another
	 * @param n - node to which the node is connected to
	 * @return the values
	 */
	public List<?> getEdgeValues(Node<T> n){
		return this.graph.getEdgeValues(this, n);
	}
	
	/**
	 * Checks if the node is connected to a certain node given its value
	 * @param value - value of the node we wish to check
	 * @return true if connected
	 */
	public boolean isConnectedTo(T value) {
		return this.graph.areConnected(this, value);
	}
	
	/**
	 * Checks if the node is connected to a certain node
	 * @param n - node to check
	 * @return true if connected
	 */
	public boolean isConnectedTo(Node<T> n) {
		return this.graph.areConnected(this, n);
	}
	
	/**
	 * Returns the collection of nodes to which the node is directly connected
	 * @return the collection of nodes
	 */
	public Set<Node<T>> neighbours(){
		return this.graph.neighbours(this);
	}
	
	/**
	 * @return the graph containing this node
	 */
	public Graph<T, ?> getGraph(){
		return this.graph;
	}
	
	/**
	 * @param graph - the graph containing this node
	 */
	public void setGraph(Graph<T, ?> graph) {
		this.graph = graph;
	}

	public String toString() {
		return this.id + " [" + this.value + "]";
	}
	
	/**
	 * @return the info
	 */
	public T getValue() {
		return value;
	}

	/**
	 * @param info the info to set
	 */
	public void setValue(T value) {
		this.value = value;
	}

	/**
	 * @return the id
	 */
	public int getId() {
		return id;
	}

	/**
	 * @param id the id to set
	 */
	public void setId(int id) {
		this.id = id;
	}
	
	
}
