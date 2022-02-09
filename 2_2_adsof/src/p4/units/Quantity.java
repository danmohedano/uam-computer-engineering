/**
 * 
 */
package p4.units;

/**
 * Enumeration to handle quantities
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public enum Quantity {
	LENGTH("L"), TIME("t");
	
	private final String abbrev;
	private Quantity(String x){ abbrev = x; }
	public String toString()
	{
		return abbrev;
	}
}
