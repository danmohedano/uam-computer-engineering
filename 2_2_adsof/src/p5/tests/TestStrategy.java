/**
 * 
 */
package p5.tests;

import java.util.ArrayList;
import java.util.Arrays;

import p5.rulessets.*;
import p5.rulessets.strategies.*;
import p5.graph.*;
/**
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class TestStrategy {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		final int INIT_CONSTANT = 1000;
		System.out.println("TESTING ASLONGASPOSSIBLE STRATEGY");
		ConstrainedGraph<Integer, Integer> g = new ConstrainedGraph<Integer, Integer>();
		Node<Integer> n0 = new Node<Integer>(0); // The value of the node is the path length. N0 is the initial node
		Node<Integer> n1 = new Node<Integer>(INIT_CONSTANT); // we initialise the rest to a high value, that will be reduced…
		Node<Integer> n2 = new Node<Integer>(INIT_CONSTANT); // progresively
		Node<Integer> n3 = new Node<Integer>(INIT_CONSTANT);
		g.addAll(Arrays.asList(n0, n1, n2, n3));
		g.connect(n0, 1, n1);
		g.connect(n0, 7, n2);
		g.connect(n1, 2, n2);
		g.connect(n1, 10, n3);
		g.connect(n2, 3, n3);
		System.out.println("Initial graph: \n"+g);
		// Execution strategy “as long as possible”
		RuleSetWithStrategy<Node<Integer>> rs = new RuleSetWithStrategy<Node<Integer>>(new AsLongAsPossible<>());
		rs.add( Rule.<Node<Integer>>rule("r1", "reduces the value of the node"). // This rule implements Dijkstra’s algorithm!
		 when(z -> g.exists( x -> x.isConnectedTo(z) &&
		 x.getValue() + (Integer)x.getEdgeValues(z).get(0) < z.getValue() ) ).
		 exec(z -> z.setValue(g.getWitness().get().getValue()+
		(Integer) g.getWitness().get().getEdgeValues(z).get(0))));
		rs.setExecContext( g );
		rs.process();
		System.out.println("Nodes of the initial graph: \n"+new ArrayList<>(g));
		System.out.println("(Some) correctness tests: ");
		System.out.println("No unreachable nodes: "+g.forAll( n -> n.getValue() < INIT_CONSTANT));
		System.out.println("Only one initial node: "+g.one( n -> n.getValue().equals(0)));
		
		
		System.out.println("\nTESTING SEQUENCE STRATEGY");
		
		ConstrainedGraph<Integer, Integer> g1 = new ConstrainedGraph<Integer, Integer>();
		Node<Integer> n10 = new Node<Integer>(0); // The value of the node is the path length. N0 is the initial node
		Node<Integer> n11 = new Node<Integer>(INIT_CONSTANT); // we initialise the rest to a high value, that will be reduced…
		Node<Integer> n12 = new Node<Integer>(INIT_CONSTANT); // progresively
		Node<Integer> n13 = new Node<Integer>(INIT_CONSTANT);
		g1.addAll(Arrays.asList(n10, n11, n12, n13));
		g1.connect(n10, 1, n11);
		g1.connect(n10, 7, n12);
		g1.connect(n11, 2, n12);
		g1.connect(n11, 10, n13);
		g1.connect(n12, 3, n13);
		System.out.println("Initial graph: \n"+g1);
		// Execution strategy “as long as possible”
		RuleSetWithStrategy<Node<Integer>> rs1 = new RuleSetWithStrategy<Node<Integer>>(new Sequence<>());
		rs1.add( Rule.<Node<Integer>>rule("r1", "reduces the value of the node"). // This rule implements Dijkstra’s algorithm!
		 when(z -> g.exists( x -> x.isConnectedTo(z) &&
		 x.getValue() + (Integer)x.getEdgeValues(z).get(0) < z.getValue() ) ).
		 exec(z -> z.setValue(g.getWitness().get().getValue()+
		(Integer) g.getWitness().get().getEdgeValues(z).get(0))));
		rs1.setExecContext( g1 );
		rs1.process();
		System.out.println("Nodes of the initial graph: \n"+new ArrayList<>(g1));
		System.out.println("(Some) correctness tests: ");
		System.out.println("No unreachable nodes: "+g1.forAll( n -> n.getValue() < INIT_CONSTANT));
		System.out.println("Only one initial node: "+g1.one( n -> n.getValue().equals(0)));
	}

}
