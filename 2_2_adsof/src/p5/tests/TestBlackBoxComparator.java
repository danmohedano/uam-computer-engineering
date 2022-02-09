/**
 * 
 */
package p5.tests;

import java.util.*;

import p5.graph.*;
import p5.comparator.*;

/**
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class TestBlackBoxComparator {
	
	public static void main(String[] args) {
		ConstrainedGraph<Integer, Integer> g = new ConstrainedGraph<Integer, Integer>();
		Node<Integer> n1 = new Node<Integer>(1);
		Node<Integer> n2 = new Node<Integer>(2);
		Node<Integer> n3 = new Node<Integer>(3);
		g.addAll(Arrays.asList(n1, n2, n3));
		g.connect(n1, 1, n2);
		g.connect(n1, 7, n3);
		g.connect(n2, 1, n3);
		
		ConstrainedGraph<Integer, Integer> g1 = new ConstrainedGraph<Integer, Integer>();
		g1.addAll(Arrays.asList(new Node<Integer>(4)));
		BlackBoxComparator<Integer, Integer> bbc = new BlackBoxComparator<Integer, Integer>();
		bbc.addCriteria( Criteria.EXISTENTIAL, n -> n.isConnectedTo(1)). 
		 addCriteria( Criteria.UNITARY, n -> n.neighbours().isEmpty()).
		 addCriteria( Criteria.UNIVERSAL, n -> n.getValue().equals(4));
		
		List<ConstrainedGraph<Integer, Integer>> cgs = Arrays.asList(g, g1);
		Collections.sort(cgs, bbc); // We use the comparator to order a list with two graphs
		System.out.println(cgs); // prints g (satisfies the 2nd property) and then g1 (satisfies the 2nd and 3rd) (corrected)
	}

}
