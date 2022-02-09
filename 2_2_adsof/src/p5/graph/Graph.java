/**
 * 
 */
package p5.graph;

import java.util.*;

/**
 * Class to implement a generic graph. Can be used as a collection of nodes
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 * @param N - type of the node
 * @param E - type of the edge
 */
public class Graph<N, E> implements Collection<Node<N>>{
	protected List<Node<N>> nodes = new ArrayList<>();
	protected List<Edge<E, N>> edges = new ArrayList<>();
	
	public Graph(){
		
	}
	
	/**
	 * Connects to nodes with an edge with the given information
	 * @param from - from node in the edge
	 * @param info - info stored in the edge
	 * @param to - to node in the edge
	 */
	public void connect(Node<N> from, E info, Node<N> to) {
		if (nodes.contains(from) && nodes.contains(to)) {
			Edge<E, N> newEdge = new Edge<E, N>(from, info, to);
			this.edges.add(newEdge);
		}
	}
	
	/**
	 * Checks if two nodes in the graph are connected
	 * @param from - from node
	 * @param to - to node
	 * @return true if they are connected
	 */
	public boolean areConnected(Node<N> from, Node<N> to) {
		return !(this.getEdgeValues(from, to).isEmpty());
	}
	
	/**
	 * Checks if a node is connected to another node with a given value
	 * @param from - from node
	 * @param to - value of the to node
	 * @return true if they are connected
	 */
	public boolean areConnected(Node<N> from, N to) {
		for (Edge<E,N> x: this.edges) {
			if (x.getFrom() == from && x.getTo().getValue() == to) return true;
		}
		return false;
	}
	
	/**
	 * Returns all the edge values of the edges between two nodes
	 * @param from - from node
	 * @param to - to node
	 * @return list of values
	 */
	public List<E> getEdgeValues(Node<N> from, Node<N> to){
		List<E> list = new ArrayList<>();
		for (Edge<E,N> x: this.edges) {
			if (x.getFrom() == from && x.getTo() == to) {
				if (!(list.contains(x.getInfo()))) list.add(x.getInfo());
			}
		}
		return list;
	}
	
	/**
	 * Returns the set of nodes to which the given node is connected
	 * @param n - node
	 * @return set of nodes
	 */
	public Set<Node<N>> neighbours(Node<N> n){
		Set<Node<N>> set = new HashSet<>();
		for (Edge<E,N> x: this.edges) {
			if (x.getFrom() == n) set.add(x.getTo());
		}
		return set;
	}
	
	public String toString() {
		String s = "Nodes: \n";
		for (Node<N> x: nodes) {
			s += x + "\n";
		}
		s += "Edges: \n";
		for (Edge<E,N> e: edges) {
			s += e + "\n";
		}
		return s;
	}
	
	@Override
	public int size() {
		return nodes.size();
	}

	@Override
	public boolean isEmpty() {
		return nodes.isEmpty();
	}

	@Override
	public boolean contains(Object o) {
		return nodes.contains(o);
	}

	@Override
	public Iterator<Node<N>> iterator() {
		return nodes.iterator();
	}

	@Override
	public Object[] toArray() {
		return nodes.toArray();
	}

	@Override
	public <T> T[] toArray(T[] a) {
		return nodes.toArray(a);
	}

	@Override
	public boolean add(Node<N> e) {
		if (e.getGraph() == null && !(this.nodes.contains(e))) {
			e.setGraph(this);
			return nodes.add(e);
		}
		else
			return false;
	}

	@Override
	public boolean remove(Object o) {
		if (!(o instanceof Node<?>)) return false;
		Node<N> r = (Node<N>)o;
		r.setGraph(null);
		for (Edge<E,N> x : edges) {
			if (x.getTo() == r || x.getFrom() == r) {
				edges.remove(x);
			}
		}
		return nodes.remove(o);
	}

	@Override
	public boolean containsAll(Collection<?> c) {
		return nodes.containsAll(c);
	}

	@Override
	public boolean addAll(Collection<? extends Node<N>> c) {
		boolean check = true;
		for (Node<N> x: c) {
			if (this.add(x) == false) check = false;
		}
		return check;
	}

	@Override
	public boolean removeAll(Collection<?> c) {
		boolean check = true;
		for (Object x : c) {
			if(this.remove(x) == false) check = false;
		}
		return check;
	}

	@Override
	public boolean retainAll(Collection<?> c) {
		boolean check = true;
		for (Object x : this) {
			if (!c.contains(x)) {
				if (this.remove(x) == false) check = false;
			}
		}
		return check;
	}

	@Override
	public void clear() {
		for (Node<N> x: nodes) {
			x.setGraph(null);
		}
		nodes.clear();
		edges.clear();
	}

	

}
