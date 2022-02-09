/**
 * 
 */
package p5.graph;

/**
 * Class to implement generic edges
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 * @param E - type of the information stored in the edge
 * @param N - type of the node
 */
public class Edge<E, N> {
	private Node<N> to;
	private Node<N> from;
	private E info;
	
	public Edge(Node<N> from, E info, Node<N> to) {
		this.to = to;
		this.from = from;
		this.info = info;
	}

	public String toString() {
		return "( " + from.getId() + " --" + this.info + "--> " + to.getId() + " )";
	}
	/**
	 * @return the to
	 */
	public Node<N> getTo() {
		return to;
	}

	/**
	 * @param to the to to set
	 */
	public void setTo(Node<N> to) {
		this.to = to;
	}

	/**
	 * @return the from
	 */
	public Node<N> getFrom() {
		return from;
	}

	/**
	 * @param from the from to set
	 */
	public void setFrom(Node<N> from) {
		this.from = from;
	}

	/**
	 * @return the info
	 */
	public E getInfo() {
		return info;
	}

	/**
	 * @param info the info to set
	 */
	public void setInfo(E info) {
		this.info = info;
	}
	
}
