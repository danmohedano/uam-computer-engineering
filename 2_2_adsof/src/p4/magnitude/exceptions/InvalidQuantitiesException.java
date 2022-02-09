/**
 * 
 */
package p4.magnitude.exceptions;

import p4.units.IPhysicalUnit;

/**
 * Exception thrown when the quantities do not match
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
@SuppressWarnings("serial")
public class InvalidQuantitiesException extends QuantityException {
	
	public InvalidQuantitiesException(IPhysicalUnit u1, IPhysicalUnit u2) {
		super(u1, u2);
	}
	
	public String toString() {
		return "Quantities " + this.u1.getQuantity() + " and " + this.u2.getQuantity() + " are not compatible";
	}
}
