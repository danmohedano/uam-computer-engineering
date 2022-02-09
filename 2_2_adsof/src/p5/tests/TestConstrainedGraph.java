/**
 * 
 */
package p5.tests;

import java.util.*;

import p5.graph.*;

/**
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class TestConstrainedGraph {
	
	public static void main(String[] args) {
		ConstrainedGraph<Integer, Integer> g = new ConstrainedGraph<Integer, Integer>();
		Node<Integer> n1 = new Node<Integer>(1);
		Node<Integer> n2 = new Node<Integer>(2);
		Node<Integer> n3 = new Node<Integer>(3);
		g.addAll(Arrays.asList(n1, n2, n3));
		g.connect(n1, 1, n2);
		g.connect(n1, 7, n3);
		g.connect(n2, 1, n3);
		System.out.println("All nodes of g connected with n3? "+g.forAll(n -> n.equals(n3) || n.isConnectedTo(n3))); // true
		System.out.println("Is there exactly one node connected to n2? "+g.one( n -> n.isConnectedTo(n2))); // true
		System.out.println("Is there at least one node of g connected to n2? "+g.exists( n -> n.isConnectedTo(n2))); // (*) true
		g.exists( n -> n.getValue().equals(89)); // Not satisfied: Optional is null
		g.getWitness().ifPresent( w -> System.out.println("Witness 1 = "+g.getWitness().get()));
		g.exists( n -> n.isConnectedTo(n2)); // Satisfied: Optional has value
		g.getWitness().ifPresent( w -> System.out.println("Witness 2 = "+g.getWitness().get()));
	}

}